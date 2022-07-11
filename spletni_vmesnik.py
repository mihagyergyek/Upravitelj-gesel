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
    gesla = trenutni_uporabnik().shramba.gesla
    return bottle.template("gesla.html", gesla=gesla, napaka=None)

@bottle.post("/gesla/")
def dodaj_geslo():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    ime = bottle.request.forms.getunicode("ime")
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    datum = date.fromisoformat(bottle.request.forms["datum"])
    kategorija = bottle.request.forms.getunicode("kategorija")
    url = bottle.request.forms.getunicode("url")
    if not(ime and uporabnisko_ime and geslo):
        gesla = trenutni_uporabnik().shramba.gesla
        return bottle.template("gesla.html", gesla=gesla, napaka="Manjkajoči podatki")
    else:
        shramba.dodaj_geslo(ime, uporabnisko_ime, geslo, datum, kategorija, url)
        shrani_trenutnega_uporabnika(uporabnik)
        bottle.redirect("/")

@bottle.get("/kartice/")
def upravljanje_kartic():
    kartice = trenutni_uporabnik().shramba.kartice
    return bottle.template("kartice.html", kartice=kartice)

@bottle.get("/generator/")
def generator():
    return bottle.template("generator.html")


@bottle.post("/kartice/")
def dodaj_kartico():
    uporabnik = trenutni_uporabnik()
    shramba = trenutni_uporabnik().shramba
    stevilka = bottle.request.forms.getunicode("stevilka")
    cvv = bottle.request.forms.getunicode("cvv")
    datum = date.fromisoformat(bottle.request.forms["datum"])
    ime = bottle.request.forms.getunicode("ime")
    shramba.dodaj_kartico(stevilka, cvv, datum, ime)
    shrani_trenutnega_uporabnika(uporabnik)
    bottle.redirect("/kartice/")

@bottle.get("/varnost/")
def varnost():
    return bottle.template("varnost.html")

bottle.run(reloader=True, debug=True)