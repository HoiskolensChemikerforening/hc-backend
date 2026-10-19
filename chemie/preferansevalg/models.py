from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from chemie.customprofile.models import Profile
from django.shortcuts import redirect
from extended_choices import Choices

GENDERS = Choices(
    ("MAN", 1, "Mann"),
    ("WOMAN", 2, "Kvinne"),
    ("IRRELEVANT", 3, "Irrelevant"),
)

class CandidatePref(models.Model): #GOOD
    user = models.ForeignKey(
        User,
        related_name="candidate_preferansevalg",
        verbose_name="kandidatens bruker",
        on_delete=models.CASCADE,
    )

    votes = models.PositiveSmallIntegerField(
        verbose_name="Antall stemmer", default=0
    )

    pre_votes = models.PositiveSmallIntegerField(
        verbose_name="Antall forhåndstemmer", default=0
    )

    image_url = models.CharField(
        max_length=200, default="/static/images/blank_avatar.png"
    )
    """
    gender = models.CharField(
        choices=GENDERS,
        default=GENDERS.IRRELEVANT,
        max_length=50,
    )
    """

    def __str__(self):
        return self.user.get_full_name()

    def get_candidate_votes(self):
        return self.votes + self.pre_votes

    def get_votes_by_rank_for_Candidate(self, position): 
        """
        returnerer en liste, f.eks. [2,4,3] 
        som tilsier at kandidaten var; 
        førsteprioritet på 2 stemmesedler
        andreprioritet på 4 stemmesedler
        tredjeprioritet på 3 stemmesedler

        denne funksjonen ble lagt i ettertid for å håndtere views_admin / admin_results_pref.html lettere
        """
        votes_by_rank = {}

        entries = CandidateRank.objects.filter(
            candidate=self,
            ticket__position=position,
        )

        for entry in entries:
            votes_by_rank[entry.rank] = (
                votes_by_rank.get(entry.rank, 0) + 1
            )

        if not votes_by_rank:
            return []

        return [
            votes_by_rank.get(rank, 0)
            for rank in range(1, max(votes_by_rank) + 1)
        ]



class TicketPref(models.Model): 
    candidates = models.ManyToManyField(
        CandidatePref,
        blank=True,
        related_name="tickets_prefvalg",
        verbose_name="Kandidatene som stemmes på",
        through="CandidateRank"
    )

    #is_blank = models.BooleanField(default=False, verbose_name="Blank stemme")

    position = models.ForeignKey(
        "PositionPref", 
        on_delete=models.CASCADE
    )

    @classmethod
    def create_ticket(cls, voted_candidates, position):
        new_ticket = cls.objects.create(position=position)
        for rank, candidate in enumerate(voted_candidates, start=1):
            CandidateRank.objects.create(
                ticket=new_ticket,
                candidate=candidate,
                rank=rank
            )
        return new_ticket

    @classmethod
    def create_blank_ticket(cls, position):
        new_ticket = cls.objects.create(position=position)

        CandidateRank.objects.create(
            ticket=new_ticket,
            candidate=None,
            rank=1,
        )

        return new_ticket



class CandidateRank(models.Model):
    ticket = models.ForeignKey(TicketPref, on_delete=models.CASCADE)
    candidate = models.ForeignKey(
        CandidatePref, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Kandidat (tom betyr blank stemme)"
    )

    rank = models.PositiveIntegerField(
        verbose_name="Rangering",
        help_text="Lavere tall betyr høyere prioritet (f.eks. 1. plass)"
    )

    class Meta:
        ordering = ['rank']
        constraints = [
            # 1. Sikrer at en kandidat kun dukker opp én gang per billett
            models.UniqueConstraint(
                fields=['ticket', 'candidate'], 
                name='unique_ticket_candidate'
            ),
            # 2. NY: Sikrer at en rangering (f.eks. 1. plass) kun brukes én gang per billett
            models.UniqueConstraint(
                fields=['ticket', 'rank'], 
                name='unique_ticket_rank'
            )
        ]

# TODO: Gi ny logikk, opptelling, stemmeseddel-definisjon... alt:

class PositionPref(models.Model):
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

    by_acclamation = models.BooleanField(
        default=False, verbose_name="Alle kandidater vant med akklamasjon"
    )

    candidates = models.ManyToManyField(
        CandidatePref,
        blank=True,
        related_name="candidate_position",
        verbose_name="Kandidater som stiller",
    )

    tickets = models.ManyToManyField(
        TicketPref,
        blank=True,
        related_name="ticket_position_prefvalg",
        verbose_name="stemmeseddel",
    )

    stemmesedler = models.ManyToManyField(
        CandidateRank,
        blank=True,
        related_name="seddel_position_prefvalg",
        verbose_name="True stemmeseddel"
    )
    """
    gender = models.BooleanField(
        default=False, verbose_name="Is gender important?",
    )

    important_gender = models.PositiveSmallIntegerField(
        choices=GENDERS,
        default=GENDERS.IRRELEVANT,
        verbose_name="The important gender",
    )

    Evt gjøre kjønn valgfritt, noe som dette ish:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].required = False
    """

    def __str__(self):
        return self.position_name

    def add_candidate(self, user):#  gender=None
        # Ikke legg til samme bruker to ganger i samme posisjon.
        if self.candidates.filter(user=user).exists():
            return None

        """
        # Bruk standardverdien dersom kjønn ikke er valgt.
        if gender is None:
            gender = GENDERS.IRRELEVANT
        """
        try:
            image_url = user.profile.image_primary.url
        except (ValueError, ObjectDoesNotExist, AttributeError):
            image_url = "/static/images/blank_avatar.png"

        candidate = CandidatePref.objects.create(
            user=user,
        #    gender=gender,
            image_url=image_url,
        )

        self.candidates.add(candidate)
        return candidate

    def delete_candidate(self, candidate_username):
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
        # Amount of people voting. Counts all tickets and all prevote tickets
        number_of_tickets = self.tickets.all().count()
        count = number_of_tickets + self.number_of_prevote_tickets
        return count

    def get_non_blank_votes(self):
        return self.tickets.filter(
            candidates__isnull=False
        ).distinct().count()

    def get_number_of_tickets(self):
        return self.tickets.count()

    
    """
    En funk for:
    - Sjekke øverste index (første prioritert stemme) og summer hver for seg. ✅
    - Sjekker om noen har over 50% og fjerner den beste✅
    - Gjør om på stemmesedler etter en fjerning. ALLE versjoner av stemmesedler MÅ vises i admin / lagres✅ Må gjøre at admin viser alle outputs av transform_ticket
    - Finner og fjerner den dårligste kandidaten✅
    - Velger om kjønn skal tas i betrakning (skal gjøre i class Position?)
    - def get_outta_here(): ignorer det uønskede kjønnet fra voteringen. Kode kjører vanlig, gir vinner, sjekker kjønn.. feil kjønn? fuck off du vant ikke
    
    TODO:
    - Må gjøre at admin viser alle outputs av transform_ticket
    - prefvalg må hente innsjekka folk fra vanlig valgsiden (henter fra profil?)
    - Fikse HTML-sidene | Troubleshooting av views & forms
    - Sjekke at whas_won transferer til å telle opp fra orignalstemmene med vinner kaset ut
    """
    alle_tickets = TicketPref.objects.all() #TODO bytt ut alle variable som henter fra ticket (CandidateRank) til å hente fra denne variabelen.
    #transform_ticket skal endre denne gjennom stemmeløpet. 

    def get_highest_index(self): #opptelling av stemmer
        first_choices = CandidateRank.objects.filter(rank=1)

        for entry in first_choices:
            if entry.candidate is not None: #not in ('', 0, [], ...)
                entry.candidate.votes += 1 #TODO: Denne endrer stemmene i CandidateRank, ikke ticket - blir ticket oppdatert?
            else:
                blank_votes += 1
        
    def check_has_won(self): #TODO if gender important: do something.
        for candidate in CandidatePref.objects.all():
            if candidate.votes > self.get_total_candidate_votes()/2:
                self.alle_tickets = self.transform_tickets(remove_candidate=candidate, sedler=self.alle_tickets)
                """
                Troubleshooting:
                - Henger koden seg opp i gamle utgave av CandidateRank i kombo med ny Ticket
                - Hvordan følger den opp med 
                """
                print(f"{candidate} har vunnet med {candidate.votes} stemmer")
                print(f"Sjekk om kandidaten er fjernet fra tickets/valg og sånt") #TODO sjekk dette tullballet
                #TODO Sjekk om valget fortsetter uten kandidaten.
                return candidate
            else:
                print(f"Ingen kandidater har over 50% av stemmene. Sjekker etter den med færrest stemmer")
                loser = self.check_who_has_lost()
                print(f"Den med færrest stemmer er: {candidate}")
                
                self.alle_tickets = self.transform_tickets(remove_candidate=loser, sedler=self.alle_tickets)
                print(f"{candidate} er nå (forhåpentligvis) fjernet fra alle tickets. Sjekk")
                return None
            
    def check_who_has_lost(self):
        candidate_with_least_votes = CandidatePref.objects.order_by('votes').first
        bad_candidates = []
        multiple = False
        for candidate in CandidatePref.objects.all():
            if candidate.votes == candidate_with_least_votes.votes:
                bad_candidates.append(candidate)
                multiple = True
        if not multiple:
            return candidate_with_least_votes.candidate
        else: 
            worst = self.check_votes_per_rank(bad_candidates)
            return worst

    def read_orginal_tickets(self): #TODO output vises i admin!
        """
            {
            "Kandidat":[antall stemmer med rank=1, antall stemmer med rank=2, ...],
            "Kandidat 2":...
        }
        """
        candidate_vote_per_rank = {}
        candidates = CandidatePref.objects.all()
        antall_ranks = CandidateRank.objects.values("rank").distinct().count()

        #legge til alle kandidater i dictionary
        for can in candidates:
            candidate_vote_per_rank[f"{can}"] = []

            for r in range(1, antall_ranks + 1):
                opptelling = CandidateRank.objects.filter(
                    rank=r,
                    candidate=can,
                ).count()

                candidate_vote_per_rank[f"{can}"].append(opptelling)

            return candidate_vote_per_rank

    def check_votes_per_rank(self, kandidater_to_check): #sjekker ved stemmerlikhet
        opptelling = self.read_orginal_tickets() #en dictionary
        kandidater = [k for k in kandidater_to_check]
        #laveste_antall = min(opptelling.values())
        rank_check = 1
        worst_not_found = True
        while worst_not_found:
            votes = [opptelling[i][rank_check-1] for i in kandidater] #[#rank1votes_kandidat1, #rank1votes_kandidat2]
            lowest_vote_amount = min(votes)
            amount_of_worst = [i for i in votes if i==lowest_vote_amount] #antall kandidater med færrest antall stemmer
            if len(amount_of_worst) > 1:
                #beholde de verste (fjerne de beste fra kandidater)
                kandidater = [i for i in kandidater if opptelling[i][rank_check-1] == lowest_vote_amount]
                rank_check += 1
            else: #return den verste kandidaten
                the_worst = [i for i in kandidater if opptelling[i][rank_check-1] == lowest_vote_amount]
                return the_worst[0] #TODO sjekk om denne returnerer et Candidate object!
            
    def transform_tickets(self,remove_candidate, sedler):
        nye_tickets = []

        for ticket in sedler:
            rangeringer = (
                CandidateRank.objects
                .filter(ticket=ticket)
                .exclude(candidate=remove_candidate)
                .order_by("rank")
            )

            nye_ticket = TicketPref.objects.create(
                position=ticket.position
            )

            for ny_rank, cr in enumerate(rangeringer, start=1):
                CandidateRank.objects.create(
                    ticket=nye_ticket,
                    candidate=cr.candidate,
                    rank=ny_rank
                )

            nye_tickets.append(nye_ticket)

        return TicketPref.objects.filter(
            id__in=[ticket.id for ticket in nye_tickets]
        )
    


    def get_total_candidate_ticket_votes(self): #Må endres
        # Total votes received on candidates in the form of tickets (not prevotes)
        """
        Sjekker førsteindex i hver stemmeseddel
        """
        return CandidateRank.objects.filter( #Henter kun tickets er hele seddelen er tom
            ticket__in=self.tickets.all(),
            candidate__isnull=False,
            rank=1,
        ).count()

    def get_total_candidate_prevotes(self): #Se over
        # Total votes received on candidates in the form of prevotes (not tickets)
        candidate_prevotes = 0
        for candidate in self.candidates.all():
            candidate_prevotes += candidate.pre_votes
        return candidate_prevotes

    def get_total_candidate_votes(self): #Se over
        # Total votes on candidates in the form of both tickets and prevotes
        return (
            self.get_total_candidate_prevotes()
            + self.get_total_candidate_ticket_votes()
        )

    def get_blank_votes(self):
        return CandidateRank.objects.filter(
            ticket__in=self.tickets.all(),
            candidate__isnull=True,
            rank=1,
        ).count()

    def calculate_candidate_votes(self,): #ÆÆÆÆÆÆ
        # TODO Validate this fucker with tests
        # Go over all tickets and assign votes to each candidate
        #tickets = self.tickets.exclude(is_blank=True).all()
        tickets = self.tickets.all()
        candidates = self.candidates.all()

        for candidate in candidates:
            candidate.votes = 0
            candidate.save()

        for ticket in tickets:
            first_choice = (
                CandidateRank.objects
                .filter(ticket=ticket, rank=1)
                .first()
            )

            if first_choice and first_choice.candidate:
                candidate = first_choice.candidate
                candidate.votes += 1
                candidate.save()

    def get_total_votes(self):
        # Total votes on candidates AND blank votes
        tickets = self.tickets.all()
        total_votes = 0

        candidates = self.candidates.all()

        for candidate in candidates:
            total_votes += candidate.pre_votes

        for ticket in tickets:
            first_choice = CandidateRank.objects.filter(
                ticket=ticket,
                rank=1
            ).first()

            if first_choice is None or first_choice.candidate is None:
                # Blank stemme
                total_votes += 1
            else:
                # Stemme på en kandidat
                total_votes += 1

        return total_votes

    def vote(self, candidates, user): #sjekk om bruker har stemt
        if not user.profile.voted:
            ticket = TicketPref.create_ticket(
                candidates, self
            )  # Lager stemmeseddelen for brukeren

            self.tickets.add(ticket)
            user.profile.voted = True
            user.profile.save()
            self.save()
        return

    def vote_blank(self, user): 
        if not user.profile.voted:
            blank_ticket = TicketPref.create_blank_ticket(self)
            self.tickets.add(blank_ticket)
            user.profile.voted = True
            user.profile.save()
            self.save()
        return


class ElectionPref(models.Model): #GOOD?
    # For the entire election
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)

    positions = models.ManyToManyField(
        PositionPref, blank=True, related_name="election_prefvalg", verbose_name="Verv"
    )

    current_position = models.ForeignKey(
        PositionPref,
        blank=True,
        null=True,
        related_name="current_election_prefvalg",
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
        cls.delete_past_elections()
        ElectionPref.objects.create(is_open=True)
        cls.clear_all_checkins()  # sets all RFID-checkins to False (no one has showed up)

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
    def delete_past_elections(cls):
        """
        Deletes past elections, positions, tickets and candiates
        """
        ElectionPref.objects.all().delete()
        PositionPref.objects.all().delete()
        TicketPref.objects.all().delete()
        CandidatePref.objects.all().delete()
        CandidateRank.objects.all().delete()

    @classmethod
    def is_redirected(cls):
        """
        Checks if there is an active voting or the election is open,
        if not return the redirect function to the correct url
        """

        if not cls.latest_election_is_open():
            return True, redirect("preferansevalg:admin_start_election_pref")
        else:
            election = cls.get_latest_election()

            if election.current_position_is_active():
                pk = election.current_position.id
                return True, redirect("preferansevalg:admin_voting_active_pref", pk=pk)

            return False, None

    def add_position(self, position_name, spots):
        if position_name not in self.positions.all().values_list(
            "position_name", flat=True
        ):
            # hvis vi ikke har lagt til vervet allerede
            position = PositionPref.objects.create(
                position_name=str(position_name), spots=int(spots)
            )

            self.positions.add(position)
            self.save()
        return

    def delete_position(self, position_id):
        position = self.positions.get(id=int(position_id))

        for candidate in position.candidates.all():
            position.delete_candidate(
                candidate_username=candidate.user.username
            )

        position.delete()
        self.save()
        return

    def start_current_position_voting(self, position_id):
        position = PositionPref.objects.get(id=position_id)
        # Find candidates running for current position
        candidates = position.candidates.all()

        if len(candidates) <= 0:
            return
        else:
            Profile.objects.filter(voted=True).update(voted=False)
            # forhindrer at vi ikke resetter votes ved refresh page

            self.current_position = position
            self.current_position.is_active = True
            self.current_position.save()
            self.save()
            return

    def end_current_position_voting(self):
        self.current_position.is_active = False
        self.current_position.is_done = True
        self.current_position.save()
        self.save()
        return

    def end_current_position_voting_by_acclamation(self):
        self.current_position.is_active = False
        self.current_position.is_done = True
        self.current_position.by_acclamation = True
        self.current_position.save()
        self.save()
        return

    def change_current_position(self, pk):
        new_position = PositionPref.objects.get(pk=pk)
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
