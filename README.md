# Upravitelj gesel
Upravitelj gesel je aplikacija, namenjena shranjevanju gesel za spletne strani, bančnih kartic in občutljivih sporočil na enem mestu.

# Prvi zagon
Za zagon je potrebno imeti naložen Python. Na računalnik naložimo Upravitelj-gesel.zip in ga razpakiramo v svojo mapo.
Nato odpremo Notepad ali podoben program in ustvarimo datoteko skrivnost.txt, ki naj bo shranjena v isti mapi kot spletni_vmesnik.py. V datoteki naj bo v eni vrstici poljubno besedilo, ki bo zašifriralo piškotke.

Skrivnosti ne delite z nikomer!

V urejevalniku ali terminalu (ukaz `python spletni_vmesnik.py`) poženemo datoteko spletni_vmesnik.py. Sledimo hiperpovezavi http://127.0.0.1:8080/ in pridemo v aplikacijo.

# Naslednji zagoni
V urejevalniku ali terminalu poženemo datoteko spletni_vmesnik.py in sledimo hiperpovezavi.

# Uporaba aplikacije
Za nov račun kliknemo na gumb "Registracija" in ustvarimo račun. Tam je tudi hiter pregled funkcij Upravitelja. Uporabniki, ki račun že imajo, se prijavijo na prvi strani.
V računu imamo na voljo naslednje strani:
- Gesla
- Kartice
- Beležka
- Generator gesel
- Varnost
- Račun

Na strani "Gesla" imamo shrambo gesel, kjer le-ta dodajamo, spreminjamo in brišemo. Podobno na straneh "Kartice" in "Beležka" dodajamo in brišemo shranjene bančne kartice in sporočila.
Sporočila lahko tudi spreminjamo. Gesla, kartice in beležka so na strežniku zašifrirana.

Generator gesel nam pomaga ustvarjati varna gesla. Izberemo željeno dolžino in vključene znake ter pritisnemo "Generiraj".

"Varnost" je stran, ki analizira varnost naše shrambe. Opozori nas na podvojena, šibka in stara gesla ter na bančne kartice, ki bodo kmalu potekle.
Kot šibka gesla štejejo tudi najpogostejša gesla, ki sicer ustrezajo ostalim pogojem. To lahko preizkusiš npr. z geslom "Mailcreated5240".

"Račun" je namenjen spreminjanju gesla za celoten račun ali brisanju računa.

# Demo račun
Demo račun je namenjen tistim, ki želijo aplikacijo le preizkusiti.
V ta namen se lahko vpišemo z uporabniškim imenom "elon" in geslom "Bezos5". Ta račun ima vnešenih nekaj gesel, kartic in sporočil, s katerimi lahko preizkusimo delovanje Upravitelja.
Če želimo prazen demo račun, se vpišemo z uporabniškim imenom "bezos" in geslom "Musk5". Ta račun je prazen in mu lahko dodajamo gesla, kartice in sporočila.

# Viri
Ikone so bile pridobljene na Font Awesome: https://fontawesome.com/