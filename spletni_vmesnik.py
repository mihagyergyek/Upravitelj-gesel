import bottle, model
from os.path import exists
import os
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

@bottle.get("/registracija/")
def registracija():
    return bottle.template("registracija.html", uporabnik=None, napaka=None)

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if exists(ime_uporabnikove_datoteke(uporabnisko_ime)):
        return bottle.template("registracija.html", uporabnik=None, napaka="To uporabniško ime je zasedeno.")
    elif uporabnisko_ime == '' or geslo == '' or ' ' in uporabnisko_ime or ' ' in geslo:
        return bottle.template("registracija.html", uporabnik=None, napaka="Manjkajoči podatki.")
    else:
        uporabnik = model.Uporabnik(uporabnisko_ime, geslo, model.Shramba([], []))
        shrani_trenutnega_uporabnika(uporabnik)
        bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.response.set_cookie("geslo", geslo, path="/", secret=SKRIVNOST)
        bottle.redirect("/")

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", uporabnik=None, napaka=None)

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    vpisano_geslo = bottle.request.forms.getunicode("geslo")
    if vpisano_geslo == '':
        return bottle.template("prijava.html", uporabnik=None, napaka="Manjkajoče geslo")
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    uporabnik = exists(ime_datoteke)
    if uporabnik:
        odsifrirano_geslo = model.Uporabnik.iz_datoteke(ime_datoteke, vpisano_geslo).geslo
        if vpisano_geslo == odsifrirano_geslo:
            bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
            bottle.response.set_cookie("geslo", vpisano_geslo, path="/", secret=SKRIVNOST)
            bottle.redirect("/")
        else:
            return bottle.template("prijava.html", uporabnik=None, napaka="Napačno geslo")
    else:
        return bottle.template("prijava.html", uporabnik=None, napaka="Napačno uporabniško ime ali geslo")

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
    return bottle.template("gesla.html", uporabnik=trenutni_uporabnik(), kategorije=kategorije, gesla=gesla, napaka=None)

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
        return bottle.template("gesla.html", uporabnik=trenutni_uporabnik(), kategorije=kategorije, gesla=gesla, napaka="Manjkajoči podatki")
    else:
        shramba.dodaj_geslo(ime, uporabnisko_ime, geslo, datum, kategorija, url)
        shrani_trenutnega_uporabnika(uporabnik)
        bottle.redirect("/gesla/")

@bottle.post("/odstrani-geslo/")
def odstrani_geslo():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    geslo_za_izbris = bottle.request.forms.getunicode("geslo-za-izbris")
    for objekt in shramba.gesla:
        if geslo_za_izbris == objekt.ime:
            shramba.gesla.remove(objekt)
            shrani_trenutnega_uporabnika(uporabnik)
            bottle.redirect("/gesla/")

@bottle.post("/zamenjaj-geslo/")
def zamenjaj_geslo():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    geslo_za_menjavo = bottle.request.forms.getunicode("geslo-za-menjavo")
    objekt_za_menjavo = bottle.request.forms.getunicode("objekt-za-menjavo")
    for objekt in shramba.gesla:
        if objekt_za_menjavo == objekt.ime:
            objekt.geslo = geslo_za_menjavo
            objekt.datum = date.today()
            shrani_trenutnega_uporabnika(uporabnik)
            bottle.redirect("/gesla/")

@bottle.get("/kartice/")
def upravljanje_kartic():
    kartice = trenutni_uporabnik().shramba.kartice
    return bottle.template("kartice.html", uporabnik=trenutni_uporabnik(), kartice=kartice, napaka=None)

@bottle.post("/kartice/")
def dodaj_kartico():
    uporabnik = trenutni_uporabnik()
    shramba = uporabnik.shramba
    lastnik = bottle.request.forms.getunicode("lastnik")
    if model.prave_oblike(bottle.request.forms.getunicode("stevilka")):
        stevilka = bottle.request.forms.getunicode("stevilka")
    else:
        stevilka = None
    if not(len(bottle.request.forms.getunicode("cvv")) == 3):
        cvv = None
    else:
        cvv = int(bottle.request.forms.getunicode("cvv"))
    try:
        datum = date.fromisoformat(bottle.request.forms["datum"] + "-01")
    except:
        datum = None
    ime = bottle.request.forms.getunicode("ime")
    if not(lastnik and stevilka and cvv and datum and ime):
        kartice = trenutni_uporabnik().shramba.kartice
        return bottle.template("kartice.html", uporabnik=trenutni_uporabnik(), kartice=kartice, napaka="Manjkajoči ali nepravilni podatki")
    else:
        shramba.dodaj_kartico(lastnik, stevilka, cvv, datum, ime)
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
            shrani_trenutnega_uporabnika(uporabnik)
            bottle.redirect("/kartice/")

@bottle.get("/generator/")
def generator():
    uporabnik = trenutni_uporabnik()
    return bottle.template("generator.html", uporabnik=uporabnik, generirano_geslo=None)

@bottle.post("/generator/")
def generator_post():
    dolzina = int(bottle.request.forms.get("dolzina"))
    velike_crke = bottle.request.forms.get("velike_crke")
    stevilke = bottle.request.forms.get("stevilke")
    posebni_znaki = bottle.request.forms.get("posebni_znaki")
    generirano_geslo = model.generator_gesel(dolzina, velike_crke, stevilke, posebni_znaki)
    return bottle.template("generator.html", uporabnik=trenutni_uporabnik(), generirano_geslo=generirano_geslo)

@bottle.get("/varnost/")
def varnost():
    shramba = trenutni_uporabnik().shramba
    return bottle.template("varnost.html", uporabnik=trenutni_uporabnik(), shramba=shramba)

@bottle.get("/racun/")
def racun():
    return bottle.template("racun.html", uporabnik=trenutni_uporabnik(), napaka=None)

@bottle.post("/zamenjaj-uporabnikovo-geslo/")
def zamenjaj_uporabnikovo_geslo():
    uporabnik = trenutni_uporabnik()
    staro_geslo = bottle.request.forms.getunicode("staro-geslo")
    novo_geslo = bottle.request.forms.getunicode("novo-geslo")
    if staro_geslo == uporabnik.geslo:
        uporabnik.geslo = novo_geslo
        bottle.response.set_cookie("geslo", novo_geslo, path="/", secret=SKRIVNOST)
        shrani_trenutnega_uporabnika(uporabnik)
        bottle.redirect("/racun/")
    return bottle.template("racun.html", uporabnik=uporabnik, napaka="Napačno vnešeno staro geslo")

@bottle.post("/izbrisi-racun/")
def izbrisi_racun():
    uporabnik = trenutni_uporabnik()
    geslo = bottle.request.forms.getunicode("geslo")
    ime_racuna = bottle.request.forms.getunicode("ime-racuna")
    if geslo == uporabnik.geslo:
        os.remove(ime_uporabnikove_datoteke(ime_racuna))
        bottle.response.delete_cookie("uporabnisko_ime", path="/")
        bottle.response.delete_cookie("geslo", path="/")
        bottle.redirect("/")
    return bottle.template("racun.html", uporabnik=uporabnik, napaka="Napačno vnešeno geslo")

@bottle.get("/img/<picture>")
def slika(picture):
    return bottle.static_file(picture, root="img")

bottle.run(reloader=True, debug=True)