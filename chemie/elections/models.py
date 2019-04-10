from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from chemie.customprofile.models import Profile
from django.shortcuts import redirect

VOTES_REQUIRED_FOR_VALID_ELECTION = 50

"""
---------------READ ME-----------------
- I appen er elections delt inn i to deler, en admin del og en bruker del
- I admindelen vil alt av logikk med stemmetelling
  og legge til kandidater skjer
- I brukerdelen vil hver bruker kunne stemme på en kandidat
  når admin gir dem tilgang
- Valget går ut på at man lager et objekt av Election, det vil si
  at kun et objekt lages for et medlemsmøte emd valg
- Det legges til unike Position objekter knyttes til election
- Det legges til Candidates objekter knyttet hvert position objekt,
  disse er hentet fra Django sin User
- For hver position vil det lages nye Candidates-objekter
- Dvs: Hvis Joachim stiller til to verv vil User "Joachim" hentes to ganger
  fra User og danne to Candidates-objekter som er knyttet til hvert sitt
  position-objekt
- forhåndstemmer og stemmer under valget er avskilt så forhåndstemmer vil bli låst når
  valget på en posisjon starter
- Når brukeren avgir stemmer under valget vil et Ticket objekt bli laget som inneholder
  Kandidatene som brukeren stemmer på
- En ticket som har null kandidater vil bli sett til å bli en blank stemme
---------------------------------------
"""


class Candidate(models.Model):
    user = models.ForeignKey(
        User,
        related_name="candidate",
        verbose_name="kandidatens bruker",
        on_delete=models.CASCADE,
    )

    votes = models.PositiveSmallIntegerField(
        verbose_name="Antall stemmer", default=0
    )

    pre_votes = models.PositiveSmallIntegerField(
        verbose_name="Antall forhåndstemmer", default=0
    )

    def __str__(self):
        return self.user.get_full_name()

    def get_candidate_votes(self):
        return self.votes + self.pre_votes


class Ticket(models.Model):
    candidates = models.ManyToManyField(
        Candidate,
        blank=True,
        related_name="tickets",
        verbose_name="Kandidatene som stemmes på",
    )

    is_blank = models.BooleanField(default=False, verbose_name="Blank stemme")

    position = models.ForeignKey("Position", on_delete=models.CASCADE)

    @classmethod
    def create_ticket(cls, voted_candidates, position):
        new_ticket = cls.objects.create(is_blank=False, position=position)
        new_ticket.candidates.set(voted_candidates)
        new_ticket.save()
        return new_ticket

    @classmethod
    def create_blank_ticket(cls, position):
        new_ticket = cls.objects.create(is_blank=True, position=position)
        return new_ticket


class Position(models.Model):
    position_name = models.CharField(
        max_length=100, verbose_name="Navn på verv"
    )

    spots = models.PositiveSmallIntegerField(
        default=1, verbose_name="Antall plasser"
    )

    number_of_prevote_tickets = models.PositiveSmallIntegerField(
        default=0, verbose_name="Antall personer som har forhåndsstemt"
    )

    is_active = models.BooleanField(  # Brukere kan gå inn og stemme på denne posisjonen
        default=False, verbose_name="Er valget åpent"
    )

    is_done = models.BooleanField(  # valget på denne posisjon er gjennomført
        default=False, verbose_name="Valget er gjennomført"
    )

    candidates = models.ManyToManyField(
        Candidate,
        blank=True,
        related_name="candidate_position",
        verbose_name="Kandidater som stiller",
    )

    tickets = models.ManyToManyField(
        Ticket,
        blank=True,
        related_name="ticket_position",
        verbose_name="Stemmesedler",
    )

    def __str__(self):
        return self.position_name

    def add_candidates(self, user):
        position_candidates = self.candidates.all()
        to_be_added = (
            False if user in [usr.user for usr in position_candidates] else True
        )

        if to_be_added:
            candidate = Candidate.objects.create(user=user)
            self.candidates.add(candidate)
            self.save()

    def delete_candidates(self, candidate_username):
        candidate_user_object = User.objects.get(username=candidate_username)
        all_candidates = self.candidates.all()

        try:
            candidate_object = all_candidates.get(user=candidate_user_object)
            deletable = candidate_object

            if deletable in self.candidates.all():
                deletable.delete()
                self.save()
                return
        except ObjectDoesNotExist:
            return

    def get_number_of_voters(self):
        number_of_tickets = self.tickets.all().count()
        count = number_of_tickets + self.number_of_prevote_tickets
        return count

    def get_non_blank_votes(self):
        non_blank_tickets = self.tickets.filter(is_blank=False)
        return non_blank_tickets.count()

    def get_blank_votes(self):
        blank_tickets = self.tickets.filter(is_blank=True)
        number_of_blank = 0

        for ticket in blank_tickets:
            if ticket.candidates.all().count() == 0:
                number_of_blank += 1

        if (
            blank_tickets.count() != number_of_blank
        ):  # TODO: hvordan vil vi sjekke error
            raise ValueError
        return number_of_blank

    def calculate_candidate_votes(self):  # TODO Validate this fucker with tests
        tickets = self.tickets.exclude(is_blank=True).all()
        candidates = self.candidates.all()

        for candidate in candidates:
            candidate.votes = 0
            candidate.save()

        for candidate in candidates:
            for ticket in tickets:
                if candidate in ticket.candidates.all():
                    candidate.votes += 1
            candidate.save()

    def get_total_votes(self):
        tickets = self.tickets.all()
        total_votes = 0
        candidates = self.candidates.all()

        for candidate in candidates:
            total_votes += candidate.pre_votes

        for ticket in tickets:
            if ticket.is_blank:
                total_votes += 1
            else:
                total_votes += ticket.candidates.all().count()
        return total_votes

    def vote(self, candidates, user):
        ticket = Ticket.create_ticket(
            candidates, self
        )  # Lager stemmeseddelen for brukeren

        self.tickets.add(ticket)
        user.profile.voted = True
        user.profile.save()
        self.save()
        return

    def vote_blank(self, user):
        blank_ticket = Ticket.create_blank_ticket(self)
        self.tickets.add(blank_ticket)
        user.profile.voted = True
        user.profile.save()
        self.save()
        return


class Election(models.Model):
    # For the entire election
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)

    positions = models.ManyToManyField(
        Position, blank=True, related_name="election", verbose_name="Verv"
    )

    current_position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        related_name="current_election",
        on_delete=models.DO_NOTHING,
        verbose_name="Vervet som skal stemmes på",
    )

    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.id, self.date)

    @classmethod
    def current_position_is_active(cls):
        if cls.latest_election_is_open():
            election = cls.get_latest_election()

            if election.current_position is not None:
                if election.current_position.is_active:
                    return True
        return False

    @classmethod
    def latest_election_is_open(cls):
        """Checking if the latest election object is currently open"""

        try:
            election = cls.objects.latest("id")
            if election.is_open:
                return True
        except ObjectDoesNotExist:  # TODO: more exceptions?
            pass

        return False

    @classmethod
    def create_new_election(cls):
        Election.objects.create(is_open=True)
        cls.clear_all_checkins()  # setter alle RFID-checkins til False (ingen har møtt opp enda)

    @classmethod
    def clear_all_checkins(cls):
        # Get all profiles where eligible_for_voting is set to True and set False
        Profile.objects.filter(eligible_for_voting=True).update(
            eligible_for_voting=False
        )

    @classmethod
    def get_latest_election(cls):
        return cls.objects.latest("id")

    @classmethod
    def is_redirected(cls):
        """
        Checks if there is an active voting or the election is open,
        if not return the redirect function to the correct url
        """

        if not cls.latest_election_is_open():
            return True, redirect("elections:admin_start_election")
        else:
            election = cls.get_latest_election()

            if election.current_position_is_active():
                pk = election.current_position.id
                return True, redirect("elections:voting_active", pk=pk)

            return False, None

    def add_position(self, position_name, spots):
        if position_name not in self.positions.all().values_list(
            "position_name", flat=True
        ):
            # hvis vi ikke har lagt til vervet allerede
            position = Position.objects.create(
                position_name=str(position_name), spots=int(spots)
            )

            self.positions.add(position)
            self.save()
        return

    def delete_position(self, position_id):
        position = self.positions.get(id=int(position_id))

        for candidate in position.candidates.all():
            position.delete_candidates(candidate_username=candidate.user.username)

        position.delete()
        self.save()
        return

    def start_current_position_voting(self, position):
        # Find candidates running for current position
        candidates = position.candidates.all()

        if len(candidates) <= 0:
            return False
        else:
            Profile.objects.filter(voted=True).update(voted=False)
            # forhindrer at vi ikke resetter votes ved refresh page

            self.current_position = position
            self.current_position.is_active = True
            self.current_position.save()
            self.save()
            return True

    def end_current_position_voting(self):
        self.current_position.is_active = False
        self.current_position.is_done = True
        self.current_position.save()
        self.save()
        return

    def change_current_position(self, pk):
        new_position = Position.objects.get(pk=pk)
        self.current_position = new_position
        self.save()
        return

    def end_election(self):
        positions = self.positions.all()

        for position in positions:
            position.is_active = False
            position.save()

        self.current_position = None
        self.is_open = False
        self.save()
