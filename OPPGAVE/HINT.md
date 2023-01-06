# HINT

a) Koden til sladreboksen ligger under
```chemie/shitbox/models.py```
Import Submission klassen og bruk ```.get()``` på ```Submission.objects```  

b) 
bruk ```.filter()```

c) Ser på Profile klasse i ```chemie/customprofile/models.py```. Husk at brukernavnet tilhører user objektet.

d) bruk ```balance__gt``` (balance greater than) i ```.filter()```.

e) bruk ```balance__lt``` (lesser than) og specialization i ```.filter()```.

f) endre balance variabelen til 75. Husk å bruke ```.save()``` etterpå.

g) bruk klassen fra a) til å lage en ny submission. Husk å bruke ```.save()``` etterpå.



