import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from chemie.customprofile.models import Profile

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
- For logikken bak telling av stemmer, se admin_end_voting i views
- Når admin starter valget vil current_position_is_open settes til True
  og man kan da stemme på en bestemt position
- Når admin avslutter valget vil vinnere med flest stemmer lagres i winners
  og man kan da gå videre til neste valg
---------------------------------------
"""


class Candidate(models.Model):
    user = models.ForeignKey(
        User,
        related_name="candidate",
        verbose_name="kandidatens bruker",
        on_delete=models.CASCADE,
    )
    votes = models.PositiveIntegerField(
        verbose_name="Antall stemmer", blank=True, default=0
    )

    def __str__(self):
        return self.user.get_full_name()


class Ticket(models.Model):
    candidates = models.ManyToManyField(
        Candidate,
        blank=True,
        related_name="ticket",
        verbose_name="kandidatene som stemmes på",
    )


class Position(models.Model):
    # Name of position
    position_name = models.CharField(
        max_length=100, verbose_name="Navn på verv"
    )

    # Number of spots available
    spots = models.PositiveIntegerField(
        default=1, verbose_name="Antall plasser"
    )
    is_active = models.BooleanField(
        default=False, verbose_name="Er valget åpent"
    )

    # Candidates running for position
    candidates = models.ManyToManyField(
        Candidate,
        blank=True,
        related_name="position",
        verbose_name="Kandidater som stiller",
    )
    tickets = models.ManyToManyField(
        Ticket,
        blank=True,
        related_name="current_position",
        verbose_name="Stemmesedler",
    )

    def add_candidates(self, candidates):
        pass

    def delete_candidates(self, candidates):
        pass
        # if type(candidates) is Candidate:
        #     deletable = candidates
        #     if deletable in self.candidates.all():
        #         deletable.delete()
        #         self.save()
        #         return
        # elif type(candidates) is QuerySet:
        #     deletables = candidates
        # elif type(candidates) is list:
        #     ids = [candidate.id for candidate in candidates]
        #     deletables = Candidate.objects.filter(pk__in=ids)
        # else:
        #     raise AttributeError
        # for candidate in deletables:
        #     if candidate in self.candidates.all():
        #         candidate.delete()
        #     else:
        #         print(
        #             "Candidate {} was not related to position {}".format(
        #                 candidate, self
        #             )
        #         )
        # self.save()

    def get_total_votes(self):
        pass
        # candidate_votes = [cand.votes for cand in self.candidates.all()]
        # total_votes = sum(candidate_votes) + self.blank_votes
        # return total_votes

    def get_blank_votes(self):
        pass

    def get_candidate_votes(self):
        pass

    def __str__(self):
        return self.position_name

    def end_voting_for_position(self):
        pass
        # if self.candidates.all().count() > 0:
        #     if self.spots >= self.candidates.all().count():
        #         winners = self.candidates.all()
        #     else:
        #         winners = []
        #         all_votes = {}
        #         for candidate in self.candidates.all():
        #             all_votes[candidate.id] = candidate.votes
        #         winner_spots = self.spots
        #         while len(winners) < winner_spots:
        #             most_votes = max(all_votes.values())
        #             winner_ids = []
        #             for candidate_id, votes in all_votes.items():
        #                 if votes == most_votes:
        #                     winner_ids.append(candidate_id)
        #                     # Now set the votes of the last found winner to -1,
        #                     # so he is not found again
        #                     all_votes[candidate_id] = -1
        #             winner_candidates = Candidate.objects.filter(
        #                 id__in=winner_ids
        #             )
        #             winners.extend(list(winner_candidates))

        #     # All winners are now stored in a list. Add this to self.winners
        #     self.winners.add(*winners)
        #     """ self.number_of_voters += Profile.objects.filter(voted=True).count() """
        #     self.voting_done = True
        #     self.save()
        # election = Election.objects.latest("id")
        # election.current_position_is_open = False
        # election.current_position = None
        # election.save()


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
        on_delete=models.CASCADE,
        verbose_name="Vervet som skal stemmes på",
    )

    date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.id, self.date)

    @classmethod
    def latest_election_is_open(cls):
        pass

    @classmethod
    def create_new_election(cls):
        pass

    def add_position(self, positions):
        pass
        # if type(positions) is Position:
        #     self.positions.add(positions)
        #     self.save()
        #     return
        # elif type(positions) is QuerySet:
        #     self.positions.add(positions)
        #     self.save()
        #     return
        # elif type(positions) is list:
        #     self.positions.add(*positions)
        #     self.save()
        # else:
        #     raise AttributeError

    def delete_position(self, positions):
        pass
        # if type(positions) is Position:
        #     position = positions
        #     position.delete_candidates(candidates=position.candidates.all())
        #     position.delete()
        #     self.save()
        #     return
        # elif type(positions) is QuerySet:
        #     deletables = positions
        # elif type(positions) is list:
        #     ids = [position.id for position in positions]
        #     deletables = Position.objects.filter(pk__in=ids)
        # else:
        #     raise AttributeError
        # for position in deletables:
        #     if position in self.positions.all():
        #         position.delete_candidates(candidates=position.candidates.all())
        #         position.delete()
        #     else:
        #         raise ValueError
        # self.save()

    def start_current_position_voting(self):
        pass

    def end_current_position_voting(self):
        pass

    def start_current_election(self, current_position):
        pass
        # Find candidates running for current position
        # candidates = current_position.candidates.all()
        # profiles = Profile.objects.filter(voted=True)
        # for profile in profiles:
        #     profile.voted = False
        #     profile.save()
        # if not self.current_position_is_open:
        #     # forhindrer at vi ikke resetter votes ved refresh page
        #     self.current_position = current_position
        #     self.current_position.blank_votes = 0
        #     self.current_position_is_open = True
        #     self.current_position.save()
        #     self.save()

    def end_election(self):
        pass
        # if self.is_open:
        #     self.is_open = False
        #     self.date = datetime.date.today()
        #     self.save()

    def vote(self, profile, candidates=None, blank=False):
        pass
        # if not profile.voted:
        #     if blank:
        #         self.current_position.blank_votes += 1
        #         self.current_position.number_of_voters += 1
        #         self.current_position.save()
        #         profile.voted = True
        #         profile.save()
        #         return True
        #     else:
        #         if type(candidates) is Candidate:
        #             candidate = candidates
        #             candidate.votes += 1
        #             self.current_position.number_of_voters += 1
        #             candidate.save()
        #             self.current_position.save()
        #             return True
        #         elif type(candidates) is QuerySet:
        #             cands = candidates
        #         elif type(candidates) is list:
        #             ids = [candidate.id for candidate in candidates]
        #             cands = Candidate.objects.filter(pk__in=ids)
        #         else:
        #             raise AttributeError
        #         if cands.count() is not 0:
        #             for candidate in cands:
        #                 candidate.votes += 1
        #                 candidate.save()
        #             self.current_position.number_of_voters += 1
        #             self.current_position.save()
        #             profile.voted = True
        #             profile.save()
        #             return True
        # return False
