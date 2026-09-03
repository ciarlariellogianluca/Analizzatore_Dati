"""Unit test per analisi.py."""

import pandas as pd
import pytest

from analisi import (
    conta_eventi_per_categoria,
    conta_eventi_per_fascia_oraria,
    conta_eventi_per_giorno,
    conta_eventi_per_zona,
    genera_riepilogo,
)


@pytest.fixture
def dataframe_analisi():
    """DataFrame sintetico gia' preprocessato, con conteggi non ambigui."""
    return pd.DataFrame(
        {
            "categoria": ["Furto", "Furto", "Furto", "Rapina", "Rapina", "Danneggiamento"],
            "zona": ["Zona_A", "Zona_A", "Zona_A", "Zona_B", "Zona_B", "Zona_C"],
            "giorno_settimana": ["Lunedi", "Lunedi", "Lunedi", "Martedi", "Martedi", "Mercoledi"],
            "fascia_oraria": [
                "20:00-24:00",
                "20:00-24:00",
                "20:00-24:00",
                "08:00-12:00",
                "08:00-12:00",
                "12:00-16:00",
            ],
        }
    )


def test_conta_eventi_per_categoria(dataframe_analisi):
    risultato = conta_eventi_per_categoria(dataframe_analisi)

    assert risultato.to_dict() == {"Furto": 3, "Rapina": 2, "Danneggiamento": 1}


def test_conta_eventi_per_zona(dataframe_analisi):
    risultato = conta_eventi_per_zona(dataframe_analisi)

    assert risultato.to_dict() == {"Zona_A": 3, "Zona_B": 2, "Zona_C": 1}


def test_conta_eventi_per_giorno(dataframe_analisi):
    risultato = conta_eventi_per_giorno(dataframe_analisi)

    assert risultato.to_dict() == {"Lunedi": 3, "Martedi": 2, "Mercoledi": 1}


def test_conta_eventi_per_fascia_oraria(dataframe_analisi):
    risultato = conta_eventi_per_fascia_oraria(dataframe_analisi)

    assert risultato.to_dict() == {"20:00-24:00": 3, "08:00-12:00": 2, "12:00-16:00": 1}


def test_genera_riepilogo_totale_eventi(dataframe_analisi):
    riepilogo = genera_riepilogo(dataframe_analisi)

    assert riepilogo["totale_eventi"] == 6


def test_genera_riepilogo_valori_piu_frequenti(dataframe_analisi):
    riepilogo = genera_riepilogo(dataframe_analisi)

    assert riepilogo["categoria_piu_frequente"] == "Furto"
    assert riepilogo["zona_piu_eventi"] == "Zona_A"
    assert riepilogo["giorno_piu_frequente"] == "Lunedi"
    assert riepilogo["fascia_oraria_piu_frequente"] == "20:00-24:00"


def test_genera_riepilogo_conteggi(dataframe_analisi):
    riepilogo = genera_riepilogo(dataframe_analisi)

    assert riepilogo["eventi_per_categoria"] == {"Furto": 3, "Rapina": 2, "Danneggiamento": 1}
    assert riepilogo["eventi_per_zona"] == {"Zona_A": 3, "Zona_B": 2, "Zona_C": 1}
    assert riepilogo["eventi_per_giorno"] == {"Lunedi": 3, "Martedi": 2, "Mercoledi": 1}
    assert riepilogo["eventi_per_fascia_oraria"] == {
        "20:00-24:00": 3,
        "08:00-12:00": 2,
        "12:00-16:00": 1,
    }
