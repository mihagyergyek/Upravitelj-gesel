from dataclasses import dataclass
import json
from datetime import date, timedelta
from typing import List
from itertools import cycle
import urllib.request
import random

VELIKE_CRKE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
MALE_CRKE = [crka.lower() for crka in VELIKE_CRKE]
STEVILKE = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
POSEBNI_ZNAKI = ["!", "@", "#", "$", "%", "^", "&", "*"]

@dataclass
class Geslo:
    ime : str
    uporabnisko_ime : str
    geslo: str
    datum : date
    kategorija : str
    url : str

    def __init__(self, ime, uporabnisko_ime, geslo, datum, kategorija=None, url=None):
        self.ime = ime
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.datum = datum
        self.kategorija = kategorija
        self.url = url

    def prestaro_geslo(self):
        return date.today() - self.datum > timedelta(90)

    def nevarno_geslo(self):
        if len(self.geslo) < 9:
            return True
        elif not any(crka in "0123456789" for crka in self.geslo):
            return True
        elif not any(crka.isupper() for crka in self.geslo):
            return True
        for vrstica in  urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/darkweb2017-top10000.txt"):
            if self.geslo in str(vrstica):
                return True
        return False

@dataclass
class Kartica:
    stevilka : str
    cvv : int
    datum : date
    ime: str

    def __init__(self, stevilka, cvv, datum, ime):
        self.stevilka = stevilka
        self.cvv = cvv
        self.datum = datum
        self.ime = ime

    def blizu_poteka(self):
        return self.datum - date.today() < timedelta(90)

@dataclass
class Shramba:
    gesla : List[Geslo]
    kartice : List[Kartica]

    def dodaj_geslo(self, ime, uporabnisko_ime, geslo, datum=date.today(), kategorija="Ostalo", url=None):
        novo_geslo = Geslo(ime, uporabnisko_ime, geslo, datum, kategorija, url)
        self.gesla.append(novo_geslo)

    def dodaj_kartico(self, stevilka, cvv, datum, ime):
        nova_kartica = Kartica(stevilka, cvv, datum, ime)
        self.kartice.append(nova_kartica)

    def kategorije(self):
        seznam = set()
        for objekt in self.gesla:
            seznam.add(objekt.kategorija)
        return list(seznam)

    def v_slovar(self):
        return {
            "gesla": [
                    {"ime": objekt.ime,
                    "uporabnisko_ime": objekt.uporabnisko_ime,
                    "geslo": objekt.geslo,
                    "datum": objekt.datum.isoformat(),
                    "kategorija": objekt.kategorija,
                    "url": objekt.url
                    }
                for objekt in self.gesla
            ],
            "kartice": [
                    {"stevilka": kartica.stevilka,
                    "cvv": kartica.cvv,
                    "datum": kartica.datum.isoformat(),
                    "ime": kartica.ime
                    }
                for kartica in self.kartice
            ]
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        gesla = [
            Geslo(g["ime"], g["uporabnisko_ime"], g["geslo"], date.fromisoformat(g["datum"]), g["kategorija"], g["url"])
            for g in slovar["gesla"]
        ]
        kartice = [
            Kartica(k["stevilka"], k["cvv"], date.fromisoformat(k["datum"]), k["ime"])
            for k in slovar["kartice"]
        ]
        return cls(
            gesla = gesla,
            kartice = kartice
        )

    def enaka_gesla(self):
        seznam = [objekt.geslo for objekt in shramba.gesla]
        seznam_ponavljajocih = []
        for geslo in seznam:
            if seznam.count(geslo) > 1 and geslo not in seznam_ponavljajocih:
                seznam_ponavljajocih.append(geslo)
        return seznam_ponavljajocih

    def prestara_gesla(self):
        return [objekt for objekt in self.gesla if objekt.prestaro_geslo()]

    def nevarna_gesla(self):
        return [objekt for objekt in self.gesla if objekt.nevarno_geslo()]

    def kartice_blizu_poteka(self):
        return [objekt for objekt in self.kartice if objekt.blizu_poteka()]

@dataclass
class Uporabnik:
    uporabnisko_ime : str
    geslo : str
    shramba : Shramba

    def __init__(self, uporabnisko_ime, geslo, shramba):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.shramba = shramba

    def novo_geslo(self, vnos):
        self.geslo = vnos

    def pravilno_geslo(self, vnos):
        return self.geslo == vnos

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "geslo": self.zasifriraj_geslo(self.geslo),
            "shramba": self.zasifriraj_shrambo().shramba.v_slovar()
        }

    def v_datoteko(self, dat):
        with open(dat, "w", encoding="utf-8") as d:
            json.dump(self.v_slovar(), d, ensure_ascii=False, indent=4)

    @classmethod
    def iz_slovarja(cls, slovar):
        return cls(
            uporabnisko_ime = slovar["uporabnisko_ime"],
            geslo = slovar["geslo"],
            shramba = Shramba.iz_slovarja(slovar["shramba"])
        )

    @classmethod
    def iz_datoteke(cls, dat, vnos):
        with open(dat, encoding="utf-8") as d:
            return cls.iz_slovarja(json.load(d)).odsifriraj_geslo(vnos).odsifriraj_shrambo(vnos)

    @staticmethod
    def zasifriraj_geslo(objekt):
        sifrirano = ''.join(chr((ord(crka) + ord(znak)) % 256) for crka, znak in zip(objekt, objekt))
        return sifrirano

    def odsifriraj_geslo(self, vnos):
        odsifrirano = ''.join(chr((ord(crka) - ord(znak)) % 256) for crka, znak in zip(self.geslo, cycle(vnos)))
        self.geslo = odsifrirano
        return self

    def zasifriraj_shrambo(self):
        slovar = self.shramba.v_slovar()
        for objekt in slovar["gesla"]:
            kljuc = self.geslo
            sifrirano = ''.join(chr(ord(str(crka)) ^ ord(str(znak))) for crka, znak in zip(objekt["geslo"], cycle(kljuc)))
            objekt["geslo"] = sifrirano
        for objekt in slovar["kartice"]:
            kljuc = self.geslo
            sifrirano = ''.join(chr(ord(str(crka)) ^ ord(str(znak))) for crka, znak in zip(objekt["stevilka"], cycle(kljuc)))
            objekt["stevilka"] = sifrirano
            objekt["cvv"] += ord(kljuc[0])
        self.shramba = Shramba.iz_slovarja(slovar)
        return self

    def odsifriraj_shrambo(self, vnos):
        slovar = self.shramba.v_slovar()
        for objekt in slovar["gesla"]:
            kljuc = vnos
            odsifrirano = ''.join(chr(ord(str(crka)) ^ ord(str(znak))) for crka, znak in zip(objekt["geslo"], cycle(kljuc)))
            objekt["geslo"] = odsifrirano
        for objekt in slovar["kartice"]:
            kljuc = vnos
            odsifrirano = ''.join(chr(ord(str(crka)) ^ ord(str(znak))) for crka, znak in zip(objekt["stevilka"], cycle(kljuc)))
            objekt["stevilka"] = odsifrirano
            objekt["cvv"] -= ord(kljuc[0])
        self.shramba = Shramba.iz_slovarja(slovar)
        return self

def generator_gesel(dolzina=14, velike_crke=True, stevilke=True, posebni_znaki=True):
    generirano = ''
    while len(generirano) < dolzina:
        generirano += random.choice(MALE_CRKE)
        if velike_crke:
            generirano += random.choice(VELIKE_CRKE)
        if stevilke:
            generirano += random.choice(STEVILKE)
        if posebni_znaki:
            generirano += random.choice(POSEBNI_ZNAKI)
    random.shuffle(list(generirano))
    return str(generirano)[:dolzina]

gmail = Geslo("gmail", "elonmusk@gmail.com", "qwertyuiop", date(2022, 1, 22))
amazon = Geslo("amazon", "elonmusk", "7uDHy3LhfDAumw", date(2021, 6, 5))
mastercard = Kartica("0000 0000 0000 0000", 123, date(2025, 3, 1), "mastercard")
shramba = Shramba(
    [gmail, amazon],
    [mastercard]
)
elon_musk = Uporabnik("elon", "Bezos5", shramba)