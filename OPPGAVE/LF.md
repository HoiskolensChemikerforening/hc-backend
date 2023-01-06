# LF 

###  Query i django

NB! Hvis du allerede har shitbox submissions og brukere vil svarene du får ikke være helt lik LF

#### Bruk python manage.py shell til å finne ...

a) ut når "Etiam pretium iaculis justo." har blitt sladret.

Terminal:

```python manage.py shell ```

```from chemie.shitbox.models import Submission ```

```targetSubmission = Submission.objects.get(content="Etiam pretium iaculis justo.") ```

```print(targetSubmission.date) ```

```exit()```

Svar:
``` 2021-07-05 22:00:00+00:00```

(Stemmer ikke overens med django admin som viser lokal tid ikke UTC)



b) alle brukere som har send inn sladder i 2021. 

``` python manage.py shell ```

``` from chemie.shitbox.models import Submission  ```

```queryset = Submission.objects.filter(date__year=2021) ```

``` users = []```

<code>
for submission in queryset: <br>
&nbsp; &nbsp; users.append(submission.author)
</code>

```print(users) ```

```exit()```

Svar:

```[<User: thansana6>, <User: adallenderg>, <User: wthreshere>, <User: scardenoso2>, <User: adallenderg>, <User: tdelaeglisec>, <User: ppresketth>, <User: ppresketth>] ```



c) alle brukere (username, first and last name) som går anvendt teoretisk.

``` python manage.py shell ```

```from chemie.customprofile.models import Profile ```

```profiles = Profile.objects.filter(specialization=3)```

<code>
for profile in profiles: <br>
&nbsp; &nbsp; print(profile.user.first_name, profile.user.last_name, profile.user.username, end=" ")<br>
&nbsp; &nbsp; print()
</code>

```exit() ```

Svar:

``` Ally Dallender adallenderg``` 

```Reeva Lyles rlylesi```

d) alle brukere (username) som har mer enn 75 HC-coins.

```python manage.py shell ```

```from chemie.customprofile.models import Profile ```

```profiles = Profile.objects.filter(balance__gt=75) ```

```print([profile.user.username for profile in profiles]) ```

```exit() ```

Svar:

``` ['anurcombe0', 'scardenoso2', 'pemmott5', 'thansana6', 'bdurward7', 'cigounetb', 'wthreshere', 'larensonf', 'adallenderg', 'rlylesi', 'mpashenkovj']```


e) alle brukere (username) som går prosess og har mindre enn 75 HC-coins.

```python manage.py shell ```

```from chemie.customprofile.models import Profile ```

```profiles = Profile.objects.filter(balance__lt=75, specialization=7) ```

```print([profile.user.username for profile in profiles]) ```

```exit() ```

Svar:

```['gmeneur1', 'rdeinhard8', 'sstaniona'] ```

#### Bruk python manage.py shell til å endre  ...

f) mengden HC-coins til 75 for alle brukere i e).

```python manage.py shell ```

```from chemie.customprofile.models import Profile ```

```profiles = Profile.objects.filter(balance__lt=75, specialization=7) ```

<code>
for profile in profiles: <br>
&nbsp; &nbsp; profile.balance = 75 <br>
&nbsp; &nbsp; profile.save()
</code>

``` print([profile.balance for profile in profiles]) ```

``` exit()```

Svar:

``` [75, 75, 75]```

#### Bruk python manage.py shell til å legge til  ...

g) ny sladder (bruk brukeren med brukernavnet "sstaniona" som author)

```python manage.py shell ```

```from chemie.shitbox.models import Submission ```

```from django.contrib.auth.models import User```

``` user = User.objects.get(username="sstaniona") ```

```sladder = Submission(content="text ...",author=user) ```

```sladder.save() ```

```exit() ```

Svar:

Sjekk om du klarer å finne teksten du sendte inn gjennom django admin


