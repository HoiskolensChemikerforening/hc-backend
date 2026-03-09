

'''
modeller: idemyldring:

scheme: selve organisasjonen
role: hvilken rolle et medlem har
member: en person i systemet
investment: innbetalinger et medlem har gjort
RecruitmentLog (self link i member): hvem rekruterte hvem
ConspiracyType: for flere typer temaer senere'''




'''
BRUKTE FUNKSJONER OG DERES BETYDNING (alfabetisk fra Model field refernces i Django. woohoo)
- BooleanField:                ja/nei, true/false
- CharField:                   kort tekst (navn, tittel, telefonnummer)     
- DateField:                   bare dato
- DateTimeField:               dato og klokkeslett
- DecimalField:                penger eller prosent med desimaler
- EmailField:                  e-postadresse
- ImageField:                  bildeopplastning
- PositiveSmallIntegerField:   små positive verdier (level, rank)
- TextField:                   lang tekst (bio, beskrivelse, notater)

- OneToOneField:               Én-til-én-relasjon. Ett medlem koblet til en bruker. eks: ett Member kan være koblet til én Django User. én User kan bare ha ett Member. OneToOneField kobler dem sammen.
- ForeignKey:                  Mange-til-en-relasjon. Mange medlemmer kan ha samme rolle
- ManyToManyField:             Mange-til-mange-relasjon. mange medlemmer kan være med i mange grupper. 
- ForeignKey("self")           eks medlemmer kan rekruttere andre medlemmer.



annet:
- blank = True                feltet kan stå tomt
- auto_now_add = True         datoen settes automatisk når objektet opprettes for første gang
- unique = True               samme, eks rollenavn, kan ikke finnes to ganger
- null=True, blank=True       kan opprette medlemmet uten å koble til bruker med en gang
- SET_NULL                    dersom noe slettes, blir felet NULL i stedet for at medlemmet slettes. 
- models.CASCADE              slettes forelderen, slettes også barnet. Sletter du scheme-et slettes også medlemmene
'''


'''
# Klassen representerer rollene i systemet. Valgte å ikke hardkode roller med Choises, da å gjøre roller til en klasse gjør det lettere å bygge på denne senere (kilde: reddit)
# Nyttig om jeg senere vil endre roller i admin uten å endre kode. 
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Rollenavn")                                               # gir navn på rollen (eks: taper, rekrutør, leder). 
    rank = models.PositiveSmallIntegerField(default=1, verbose_name="Rang")                                                     # Fant ut max_length ikke kan brukes her. Gir et lite positivt heltall. brukes f.eks. til å si at leder har høyere rang enn rekruttør
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Provisjon i prosent")     # tall med desimaler, nice for penger og prosent.

    def __str__(self):
        return self.name
    

# Scheme skal representere selve pyramiden/organisasjonen. ergo: lager en modell som Django skal gjøre om til en database-tabell.
# Benytter denne da den åpner muligheten for at jeg kan ha flere pyramider på samme nettside.
class Scheme(models.Model):
    title = models.CharField(max_length=100, verbose_name="Navn på pyramiden")       # navn på organisasjonen
    description = models.TextField(blank=True, verbose_name="Beskrivelse")           # valgfritt å legge inn beskrivelse
    start_date = models.DateField(auto_now_add=True, verbose_name="Opprettet dato")  # datoen ved opprettelse av organisasjonen blir automatisk satt
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")              # default er at når organisasjonen er opprettet, så er den aktiv

    def __str__(self):
        return self.title
    

# Beskriver en person i systemet.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Knyttet bruker")                               # kobler sammen User og Member. on_delete: slettes brukeren, slettes også Member-objektet
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="members", verbose_name="Pyramide")                                   # mange medlemmer tilhører ett scheme, men et medlem tilhører én pyramide. related_names="members" er så jeg senere kan gjøre  scheme.members.all() for å hente alle medlemmene
    full_name = models.CharField(max_length=100, verbose_name="Fullt navn")                                                                         # navn på medlem
    nickname = models.CharField(max_length=50, blank=True, verbose_name="Kallenavn")                                                                # kallenavn (valgfritt)
    email = models.EmailField(blank=True, verbose_name="E-post")                                                                                    # Som CharField men Django vet at det skal være en Epost
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefonnummer")                                                        # legger inn telefon nr (valgfritt)
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="Innmeldt")                                                                    # Lagrer dato og klokkeslett når medlemmet ble opprettet
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rolle")                                          # rollekobling. mange medlemmer kan ha samme rolle, men ett medlem har én rolle. SET_NULL; slettes rollen settes feltet til NULL uten å slette medlemmet
    recruiter = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="recruits", verbose_name="Rekruttert av")  # kobling av hvem rekrutterte hvem. "self" betyr at modellen peker til seg selv (et medlem kan ha én recruiter, men et medlem kan ha mange recruits under seg). databasen håndterer relasjonene for meg. yay
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Nivå i pyramiden")                                                            # bare et tall som kan oppdateres basert på hvor mange recruits en person har
    total_invested = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Totalt investert")                            # moneyyyyy
    bio = models.TextField(blank=True, verbose_name="Kort beskrivelse")                                                                             # kan legge til en tekst eller en kommentar
    profile_image =  models.ImageField(upload_to="members/", blank=True, null=True, verbose_name="Profilbilde")                                     # åpner for muligheten til å laste opp bilder. bildene legges i en mappe som heter members/
    is_founder = models.BooleanField(default=False, verbose_name="Er grunnlegger")                                                                  # boolsk felt. de fleste er ikke grunnleggeren, så dette settes automatisk til False
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")                                                                             # de fleste som lager en bruker har intensjon om å være aktiv, så dette er default.

    def __str__(self):
        return self.full_name
    

# Smart modell å ha dersom man vil lage noe mer enn en totalsum. Gjør at man kan lagre flere innbetalinger over tid. 
class Investment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="investments", verbose_name="Medlem")  # Ett medlem kan ha mange investeringer, men hver investering tilhører ett medlem. kan senere bruke member.investments.all()
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Beløp")                              # Moneyyyyy
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Betalt dato")                               # Setter automatisk tidspunkt når investeringen ble registrert
    note = models.CharField(max_length=200, blank=True, verbose_name="Notat")                                        # mulighet for å sette inn en kommentar. eks "startavgift"

    def __str__(self):
        return f"{self.member.full_name} - {self.amount} kr"
    

# En morsom idé jeg fikk. eks tema; romvesener, øglemennesker, flat jord, hemmelige eliter. Nettsiden blir et fiktivt univers hehehe
class ConspiracyTheme(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tema")
    description = models.TextField(blank=True, verbose_name="Beskrivelse")

    def __str__(self):
        return self.name
    

# En koblingstabell mellom Scheme og ConspiracyTheme. Kunne brukt ManyToManyField, men nah, vil lære mer om relasjonene ved å gønne en mellommodell. 
class SchemeTheme(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="scheme_themes")
    theme = models.ForeignKey(ConspiracyTheme, on_delete=models.CASCADE, related_name="theme_schemes")

    # Meta klassen "[...] is a standard pattern in Django to keep configuration separate from the model's actual fields, thus avoiding potential namespace conflicts." fra Stack Overflow
    class Meta:                                    # fant på django greia: "The Meta class, when used, offers numerous ways to customize how a model interacts with the database and the Django admin". Instruksjoner til Django 'framework' på hvordan håndtere ytre klasser
        unique_together = ("scheme", "theme")      # Quote; "Enforces uniqueness across a spesific combination of fields"
        verbose_name = "Pyramide-tema"             # Quote; "A human-readable singular name for the model, used in the admin interface"
        verbose_name_plural = "Pyramide-temaer"    # Quote; "A human-readable plural name for the model, often used in the admin interface"

    def __str__(self):
        return f"{self.scheme.title} - {self.theme.name}"
    
'''

'''
kan gjøres senere for å hente ut diverse

- scheme.members.all()    henter ut alle medlemmene
- members.investments.all()  henter ut alle investeringene til et medlem
- person.recruits.all()
'''



'''
Tenkt struktur

Scheme: en pyramide/organisasjon

schemen har mange;

Members: posisjoner i pyramiden.
    Hvert medlem:
    - tilhører ett Scheme
    - her én Role
    - kan ha én recruiter som også er et Member
    - kan ha mange recruits
    - kan ha mange Investment

Og et Scheme kan ha flere ConspiracyTheme via SchemeTheme
'''



from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from extended_choices import Choices



# Klassen representerer rollene i systemet.
# valgte å gjøre rolle til en egen modell i stedet for å hardkode choices med en gang
# det gjør det lettere å bygge videre senere og endre ting i admin uten å måtte rote i koden hver gang
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Rollenavn")   # navn på rollen. eks: taper, rekruttør, leder
    rank = models.PositiveSmallIntegerField(default=1, verbose_name="Rang")          # lite positivt heltall. kan brukes til å vise hvem som er høyest/lavest i systemet

    def __str__(self):
        return self.name
    

# Scheme skal representere selve pyramiden / organisasjonen
# denne er grei å ha fordi da kan nettsiden i teorien ha flere forskjellige pyramider senere og ikke bare én
class Scheme(models.Model):
    title = models.CharField(max_length=100, verbose_name="Navn")                    # navn på pyramiden / organisasjonen
    description = models.TextField(blank=True, verbose_name="Beskrivelse")           # lengre tekstfelt. kan stå tomt hvis jeg ikke gidder skrive noe
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Opprettet")   # dato + klokkeslett settes automatisk når objektet lages første gang

    def __str__(self):
        return self.title


# Member beskriver en person i systemet. dette er hovedmodellen
# her lagres info om folk i pyramiden og hvordan de henger sammen
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Bruker")   
        # kobler Member til Django sin innebygde User. one-to-one betyr basically én bruker per medlem og omvendt
        # null=True og blank=True gjør at den ikke må kobles til en bruker med en gang
        # CASCADE betyr at hvis user slettes, så slettes dette member-objektet også

    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="members", verbose_name="Scheme")   
        # mange medlemmer kan høre til ett scheme, men ett medlem hører bare til én pyramide
        # related_name="members" gjør at jeg senere kan skrive scheme.members.all() og hente ut alle medlemmene derfra. slay

    full_name = models.CharField(max_length=100, verbose_name="Navn")   # fullt navn på medlemmet
    email = models.EmailField(blank=True, verbose_name="E-post")        
    # som CharField-ish, men Django skjønner at dette skal være e-post og kan validere det litt bedre

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rolle")   
        # kobler medlemmet til en rolle
        # mange medlemmer kan ha samme rolle, men ett medlem har bare én rolle om gangen
        # SET_NULL betyr at hvis rollen slettes, så blir ikke medlemmet slettet. feltet bare settes til null istedenfor

    recruiter = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="recruits", verbose_name="Rekruttert av")
        # "self" betyr at modellen peker til seg selv
        # altså: et medlem kan være rekruttert av et annet medlem
        # én person kan ha én recruiter, men én recruiter kan ha mange recruits under seg
        # related_name="recruits" gjør at jeg senere kan skrive f.eks leder.recruits.all(). yay

    level = models.PositiveSmallIntegerField(default=1, verbose_name="Nivå")  
    # bare et lite positivt tall. kan brukes til å vise hvor langt opp/ned i pyramiden noen er

    join_date = models.DateTimeField(auto_now_add=True, verbose_name="Innmeldt")  
    # lagrer tidspunktet (klokkeslett og dato) medlemmet ble opprettet / meldt inn

    total_invested = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Totalt investert")
        # brukes til penger.
        # max_digits=10 betyr totalt antall sifre
        # decimal_places=2 betyr to tall bak komma. 

    is_founder = models.BooleanField(default=False, verbose_name="Grunnlegger")  
    # true/false-felt. standard er false siden de fleste ikke er grunnleggeren obviously

    is_active = models.BooleanField(default=True, verbose_name="Aktiv")        
    # enda et true/false-felt. default true fordi nye medlemmer som regel er aktive når de først blir lagt inn

    def __str__(self):
        return self.full_name


# denne modellen er smart å ha hvis jeg vil lagre flere betalinger over tid og ikke bare én totalsum
# da kan et medlem ha mange investeringer registrert på seg
class Investment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="investments", verbose_name="Medlem")
        # hver investering tilhører ett medlem
        # ett medlem kan ha mange investeringer
        # related_name="investments" gjør at jeg senere kan skrive member.investments.all() 

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Beløp")  
    # penger moneyyyy

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Registrert")  
    # setter automatisk dato og klokkeslett når investeringen registreres

    note = models.CharField(max_length=200, blank=True, verbose_name="Notat")  
    # lite tekstfelt for kommentar. eks "startavgift" eller "månedlig offergave" lol

    def __str__(self):
        return f"{self.member.full_name} - {self.amount} kr"






