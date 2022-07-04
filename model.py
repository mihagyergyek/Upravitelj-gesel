from dataclasses import dataclass
import json
from datetime import date
from typing import List

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
        self.datum = datum.isoformat()
        self.kategorija = kategorija
        self.url = url

@dataclass
class Kartica:
    stevilka : str
    cvv : int
    datum : date
    ime: str

    def __init__(self, stevilka, cvv, datum, ime):
        self.stevilka = stevilka
        self.cvv = cvv
        self.datum = datum.isoformat()
        self.ime = ime

@dataclass
class Shramba:
    gesla : List[Geslo]
    kartice : List[Kartica]

    def dodaj_geslo(self, ime, uporabnisko_ime, geslo, datum=date.today(), kategorija=None, url=None):
        novo_geslo = Geslo(ime, uporabnisko_ime, geslo, datum, kategorija, url)
        self.gesla.append(novo_geslo)

    def dodaj_kartico(self, stevilka, cvv, datum, ime):
        nova_kartica = Kartica(stevilka, cvv, datum, ime)
        self.kartice.append(nova_kartica)

    def v_slovar(self):
        return {
            "gesla": [
                        {"ime": objekt.ime,
                        "uporabnisko_ime": objekt.uporabnisko_ime,
                        "geslo": objekt.geslo,
                        "datum": objekt.datum,
                        "kategorija": objekt.kategorija,
                        "url": objekt.url
                        }
                    for objekt in self.gesla
                ],
            "kartice": [
                {"stevilka": kartica.stevilka,
                "cvv": kartica.cvv,
                "datum": kartica.datum,
                "ime": kartica.ime
                }
                for kartica in self.kartice
            ]
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        gesla = [
            Geslo(g["ime"], g["uporabnisko_ime"], g["geslo"], g["datum"], g["kategorija"], g["url"])
            for g in slovar["gesla"]
        ]
        kartice = [
            Kartica(k["stevilka"], k["cvv"], k["datum"], k["ime"])
            for k in slovar["kartice"]
        ]
        return cls(
            gesla = gesla,
            kartice = kartice
        )

@dataclass
class Uporabnik:
    uporabnisko_ime : str
    geslo : str
    shramba : Shramba

    def __init__(self, uporabnisko_ime, geslo, shramba):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.shramba = shramba

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "geslo": self.geslo,
            "shramba": self.shramba.v_slovar()
        }

    def v_datoteko(self, dat):
        with open(dat, "w") as d:
            json.dump(self.v_slovar(), d, ensure_ascii=False, indent=4)