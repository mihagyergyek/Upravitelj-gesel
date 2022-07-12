import bottle, model
from os.path import exists
from datetime import date

with open("skrivnost.txt") as f:
    SKRIVNOST = f.read()

def ime_uporabnikove_datoteke(uporabnisko_ime):
    return f"uporabniki/{uporabnisko_ime}.json"

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST)
    geslo = bottle.request.get_cookie("geslo", secret=SKRIVNOST)
    if uporabnisko_ime == None:
        bottle.redirect("/prijava/")
    else:
        uporabnisko_ime = uporabnisko_ime
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    uporabnik = model.Uporabnik.iz_datoteke(ime_datoteke, geslo)
    return uporabnik

def shrani_trenutnega_uporabnika(uporabnik : model.Uporabnik):
    uporabnisko_ime = uporabnik.uporabnisko_ime
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    uporabnik.v_datoteko(ime_datoteke)

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    vpisano_geslo = bottle.request.forms.getunicode("geslo")
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    uporabnik = exists(ime_datoteke)
    if uporabnik:
        odsifrirano_geslo = model.Uporabnik.iz_datoteke(ime_datoteke, vpisano_geslo).geslo
        if vpisano_geslo == odsifrirano_geslo:
            bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
            bottle.response.set_cookie("geslo", vpisano_geslo, path="/", secret=SKRIVNOST)
            bottle.redirect("/")
    else:
        return bottle.template("prijava.html", napaka="Napačno uporabniško ime ali geslo")

@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    bottle.response.delete_cookie("geslo", path="/")
    bottle.redirect("/")

@bottle.get("/")
def zacetna_stran():
    bottle.redirect("/gesla/")

@bottle.get("/gesla/")
def upravljanje_gesel():
    kategorije = trenutni_uporabnik().shramba.kategorije()
    gesla = trenutni_uporabnik().shramba.gesla
    return bottle.template("gesla.html", kategorije=kategorije, gesla=gesla, napaka=None)

@bottle.post("/gesla/")
def dodaj_geslo():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    if bottle.request.forms.getunicode("ime") == any(geslo.ime for geslo in shramba.gesla):
        ime = None
    else:
        ime = bottle.request.forms.getunicode("ime")
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    try:
        datum = date.fromisoformat(bottle.request.forms["datum"])
    except:
        datum = date.today()
    kategorija = bottle.request.forms.getunicode("kategorija")
    url = bottle.request.forms.getunicode("url")
    if not(ime and uporabnisko_ime and geslo):
        kategorije = trenutni_uporabnik().shramba.kategorije()
        gesla = trenutni_uporabnik().shramba.gesla
        return bottle.template("gesla.html", kategorije=kategorije, gesla=gesla, napaka="Manjkajoči podatki")
    else:
        shramba.dodaj_geslo(ime, uporabnisko_ime, geslo, datum, kategorija, url)
        shrani_trenutnega_uporabnika(uporabnik)
        bottle.redirect("/")

@bottle.post("/odstrani-geslo/")
def odstrani_geslo():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    geslo_za_izbris = bottle.request.forms.getunicode("geslo-za-izbris")
    for objekt in shramba.gesla:
        if geslo_za_izbris == objekt.ime:
            shramba.gesla.remove(objekt)
            print(uporabnik)
            shrani_trenutnega_uporabnika(uporabnik)
            bottle.redirect("/")

@bottle.get("/kartice/")
def upravljanje_kartic():
    kartice = trenutni_uporabnik().shramba.kartice
    return bottle.template("kartice.html", kartice=kartice, napaka=None)

@bottle.post("/kartice/")
def dodaj_kartico():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    stevilka = bottle.request.forms.getunicode("stevilka")
    if not(len(bottle.request.forms.getunicode("cvv")) == 3):
        cvv = None
    else:
        cvv = int(bottle.request.forms.getunicode("cvv"))
    try:
        datum = date.fromisoformat(bottle.request.forms["datum"] + "-01")
    except:
        datum = None
    ime = bottle.request.forms.getunicode("ime")
    if not(stevilka and cvv and datum and ime):
        kartice = trenutni_uporabnik().shramba.kartice
        return bottle.template("kartice.html", kartice=kartice, napaka="Manjkajoči ali nepravilni podatki")
    else:
        shramba.dodaj_kartico(stevilka, cvv, datum, ime)
        shrani_trenutnega_uporabnika(uporabnik)
        bottle.redirect("/kartice/")

@bottle.post("/odstrani-kartico/")
def odstrani_kartico():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    kartica = bottle.request.forms.get("kartica")
    for objekt in shramba.kartice:
        if kartica == objekt.stevilka:
            shramba.kartice.remove(objekt)
            print(uporabnik)
            shrani_trenutnega_uporabnika(uporabnik)
            bottle.redirect("/kartice/")

@bottle.get("/generator/")
def generator():
    return bottle.template("generator.html", generirano_geslo=None)

@bottle.post("/generator/")
def generator_post():
    dolzina = int(bottle.request.forms.get("dolzina"))
    velike_crke = bottle.request.forms.get("velike_crke")
    stevilke = bottle.request.forms.get("stevilke")
    posebni_znaki = bottle.request.forms.get("posebni_znaki")
    generirano_geslo = model.generator_gesel(dolzina, velike_crke, stevilke, posebni_znaki)
    print(generirano_geslo)
    return bottle.template("generator.html", generirano_geslo=generirano_geslo)

@bottle.get("/varnost/")
def varnost():
    shramba = trenutni_uporabnik().shramba
    return bottle.template("varnost.html", shramba=shramba)

bottle.run(reloader=True, debug=True)