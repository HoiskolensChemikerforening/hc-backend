from django.db import models, transaction
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
import uuid
import datetime
from django.shortcuts import render_to_response, get_object_or_404, render



"""
POTITION_TYPE_CHOICES= (
    ('pHormand/pHorquinde','pHormand/pHorquinde'),
    ('PR-sjaepH','PR-sjaepH'),
    ('Sectreteuse','Sectreteuse'),
    ('Kasserer','Kasserer'),
    ('pHaestsjaepH','pHaestsjaepH'),
    ('IndustrisjaepH','IndustrisjaepH'),
    ('ChemicalsjaepH','ChemicalsjaepH'),
    ('Kjellerstyret','Kjellerstyret'),
    ('Assisterende pHaestsjef','Assisterende pHaestsjef'),
    ('pHaestslave','pHaestslave'),
    ('Redacteur','Redacteur'),
    ('Administrasjonprotogé/sjaepH', 'Administrasjonprotogé/sjaepH'),
    ('Utenrikskomiteen','Utenrikskomiteen'),
    ('Wettrekomiteen','Wettrekomiteen'),
    ('Arrkomiteen','Arrkomiteen'),
    ('Sportskomiteen','Sportskomiteen'),
    ('Arkivar','Arkivar'),
    ('Fadderkomiteen','Fadderkomiteen'),
    ('PTV: (ProgramsTillitsValgt for MTKJ)','PTV: (ProgramsTillitsValgt for MTKJ)'),
    ('Webkomiteen','Webkomiteen')
)"""

"""
---------------READ ME-----------------
- I appen er elections delt inn i to deler, en admin del og en bruker del
- I admindelen vil alt av logikk med stemmetelling og legge til kandidater skjer
- I brukerdelen vil hver bruker kunne stemme på en kandidat når admin gir dem tilgang 
- Valget går ut på at man lager et objekt av Election, det vil si at kun et objekt lages for et medlemsmøte emd valg
- Det legges til unike Position objekter fra lista over som knyttes til election
- Det legges til Candidates objekter knyttet hvert position objekt, disse er hentet fra Django sin User
- For hver position vil det lages nye Candidates-objekter,  
- Dvs: Hvis Joachim stiller til to verv vil User "Joachim" hentes to ganger fra User og danne to Candidates-objekter som er knyttet til hvert sitt position-objekt
- For logikken bak telling av stemmer, se admin_end_voting i views
- Når admin starter valget vil current_position_is_open settes til True og man kan da stemme på en bestemt position
- Når admin slutter valget vil vinnere med flest stemmer lagres i winners og man kan da gå videre til neste valg
---------------------------------------
"""


class Candidates(models.Model):
    candidate_user = models.ForeignKey(User, related_name="candidate")
    votes = models.IntegerField(verbose_name="Antall stemmer", blank=True, default=0)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return self.candidate_user.first_name + " " + self.candidate_user.last_name


class Position(models.Model):
    position_name = models.CharField(max_length=100, verbose_name="Navn på verv")
    spots = models.IntegerField(verbose_name="Antall plasser")
    candidates = models.ManyToManyField(Candidates, blank=True, related_name="positions")
    total_votes = models.IntegerField(default=0)
    voting_done = models.BooleanField(default=False)
    winners = models.ManyToManyField(Candidates, blank=True, related_name="winners", default=None)

    def delete_position(self, *args, **kwargs):
        try:  # prøver å delete candidater under en posisjon
            election = kwargs['election']
            candidates_objects = self.candidates.all()
            self.candidates.remove(candidates_objects)
            candidates_objects.delete()
            self.save()
            election.positions.remove(self)
            self.delete()
            election.save()
        except:  # catcher hvis posisjonen ikke har candidater
            election.positions.remove(self)
            self.delete()
            election.save()

    def __str__(self):
        return self.position_name

    def get_current_position_winners(self):
        all_winners = dict()
        all_results = dict()
        for candidates in self.candidates.all():
            all_results[candidates] = candidates.votes
        for winner_spots in range(self.spots):
            most_votes = 0
            winner = None
            winner_votes = 0
            for result in all_results:
                if all_results[result] >= most_votes:
                    most_votes = all_results[result]
                    winner = result
                    winner_votes = all_results[result]
            all_winners[winner] = winner_votes

            found_winner = False
            for candidate in all_results:
                if all_results[candidate] == winner_votes:
                    all_winners[candidate] = all_results[candidate]
                    if not found_winner:
                        # Når vi finner bestCandidate
                        found_winner = True
                    all_results[candidate] = -1
        self.winners = all_winners



class Election(models.Model):
    is_open = models.BooleanField(verbose_name="Er åpent", default=False) #Generelt for hele valget
    positions = models.ManyToManyField(Position, blank=True, related_name='election')
    current_position = models.ForeignKey(Position, blank=True, null=True, related_name='current_election')
    current_position_is_open = models.BooleanField(verbose_name="Det er åpent for stemming", default=False)  #For delvalget for hver position
    date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.id, self.date)

    def start_current_election(self,*args,**kwargs):
        current_position = get_object_or_404(Position, pk=int(args[0]))  # finner posisjonen vi skal votere om
        candidates = current_position.candidates.all()
        users = User.objects.all()
        for user in users:
            user.profile.voted = False
            user.profile.save()
        if not self.current_position_is_open:  # forhindrer at vi ikke resetter votes ved refresh page
            self.current_position = current_position
            self.current_position.total_votes = 0
            self.current_position_is_open = True
            # Legge til forhndsstemmene i totale stemmer
            for candidate in candidates:
                self.current_position.total_votes += candidate.votes
            self.save()
            self.current_position.save()


    def end_election(self):
        if self.is_open:
            self.is_open = False
            self.date = datetime.date.today()
            self.save()


    def vote(self,*args,**kwargs):
        voted = False
        candidates = self.current_position.candidates.all()
        form = args[1]
        request = args[0]
        vote_blank = request.POST.getlist('Blank')
        if 'Blank' in vote_blank:
            self.current_position.total_votes += 1
            self.current_position.save()
            voted = True
            request.user.profile.voted = voted
            request.user.profile.save()
        else:
            print(form.is_valid())
            if form.is_valid():

                 # Henter ut id nummerene til kandidatene som brukeren stemmer på
                voted_user_list = request.POST.getlist('candidates')
                spots = self.current_position.spots

                if not len(voted_user_list) > spots:  # Checking if user have voted for at least 1 candidate and no more than spots avalible
                    if not request.user.profile.voted:  # check if user has voted
                        # Looper gjennom listen med id-nummerene
                        for number in voted_user_list:
                            candidate_user = candidates.get(id=number)
                            candidate_user.votes += 1

                            self.current_position.total_votes += 1

                            candidate_user.save()
                            self.current_position.save()
                        request.user.profile.voted = True
                        voted = True
                        request.user.profile.save()
        return voted

