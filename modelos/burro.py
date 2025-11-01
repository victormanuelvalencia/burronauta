# modelos/burro.py

import json

class Burro:
    def __init__(self, burroenergia_inicial=100, estado_salud="Excelente", pasto=0,
                 number=0, start_age=0, death_age=0, constellations=None):
        self._burroenergia_inicial = burroenergia_inicial
        self._estado_salud = estado_salud
        self._pasto = pasto
        self._number = number
        self._start_age = start_age
        self._death_age = death_age
        self._constellations = constellations or []

    # ----- Getters -----
    def get_burroenergia_inicial(self):
        return self._burroenergia_inicial

    def get_estado_salud(self):
        return self._estado_salud

    def get_pasto(self):
        return self._pasto

    def get_number(self):
        return self._number

    def get_start_age(self):
        return self._start_age

    def get_death_age(self):
        return self._death_age

    def get_constellations(self):
        return self._constellations

    # ----- Setters -----
    def set_burroenergia_inicial(self, value):
        self._burroenergia_inicial = value

    def set_estado_salud(self, value):
        self._estado_salud = value

    def set_pasto(self, value):
        self._pasto = value

    def set_number(self, value):
        self._number = value

    def set_start_age(self, value):
        self._start_age = value

    def set_death_age(self, value):
        self._death_age = value

    def set_constellations(self, value):
        self._constellations = value

    # ----- Conversión desde un diccionario (JSON -> objeto) -----
    @classmethod
    def from_dict(cls, data):
        constellations = data.get("constellations", [])
        return cls(
            burroenergia_inicial=data.get("burroenergiaInicial", 100),
            estado_salud=data.get("estadoSalud", "Desconocido"),
            pasto=data.get("pasto", 0),
            number=data.get("number", 0),
            start_age=data.get("startAge", 0),
            death_age=data.get("deathAge", 0),
            constellations=constellations
        )

    # ----- Conversión a diccionario (objeto -> JSON) -----
    def to_dict(self):
        return {
            "constellations": self._constellations,
            "burroenergiaInicial": self._burroenergia_inicial,
            "estadoSalud": self._estado_salud,
            "pasto": self._pasto,
            "number": self._number,
            "startAge": self._start_age,
            "deathAge": self._death_age
        }

    # ----- Conversión a JSON string -----
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def __str__(self):
        return f"Burro({self._estado_salud}, Energía={self._burroenergia_inicial}, Pasto={self._pasto}, Edad={self._start_age}/{self._death_age})"
