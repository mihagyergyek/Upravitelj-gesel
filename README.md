# Upravitelj gesel
Upravitelj gesel je aplikacija, namenjena shranjevanju gesel za spletne strani in bančnih kartic na enem mestu.

# Prvi zagon
Za zagon je potrebno imeti naložen Python. Na računalnik naložimo Upravitelj-gesel.zip in ga razpakiramo v svojo mapo.
Nato odpremo Notepad ali podobnem programu in ustvarimo datoteko skrivnost.txt, ki naj bo shranjena v isti mapi kot spletni_vmesnik.py. V datoteki naj bo v eni vrstici poljubno besedilo, ki bo zašifriralo piškotke.
Skrivnosti ne delite z nikomer!
V VSCode ali drugem urejevalniku poženemo datoteko spletni_vmesnik.py. Sledimo hiperpovezavi http://127.0.0.1:8080/ in pridemo v aplikacijo.

# Naslednji zagoni
V urejevalniku poženemo datoteko spletni_vmesnik.py in sledimo hiperpovezavi.

# Uporaba aplikacije
Za nov račun kliknemo na gumb "Registracija" in ustvarimo račun. Tam je tudi hiter pregled funkcij Upravitelja. Uporabniki, ki račun že imajo, se prijavijo na prvi strani.
V računu imamo na voljo naslednje strani:
- Gesla
- Kartice
- Generator gesel
- Varnost
- Račun

Na strani "Gesla" imamo shrambo gesel, kjer le-ta dodajamo, spreminjamo in brišemo. Podobno na strani "Kartice" dodajamo in brišemo shranjene bančne kartice.
Generator gesel nam pomaga ustvarjati varna gesla. Izberemo željeno dolžino in vključene znake ter pritisnemo "Generiraj".
"Varnost" je stran, ki analizira varnost naše shrambe. Opozori nas na podvojena, šibka in stara gesla ter na bančne kartice, ki bodo kmalu potekle.
"Račun" je namenjen spreminjanju gesla za celoten račun ali brisanju računa.

# Demo račun
Demo račun je namenjen tistim, ki želijo aplikacijo le preizkusiti.
V ta namen se lahko vpišemo z uporabniškim imenom "elon" in geslom "Bezos5". Ta račun ima vnešenih nekaj gesel in kartic, s katerimi lahko preizkusimo delovanje Upravitelja.
Če želimo prazen demo račun, se vpišemo z uporabniškim imenom "bezos" in geslom "Musk5". Ta račun je prazen in mu lahko dodajamo gesla in kartice.
