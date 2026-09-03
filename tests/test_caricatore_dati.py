"""Unit test per caricatore_dati.py."""

import datetime

import pandas as pd
import pytest

from caricatore_dati import (
    carica_dati,
    ottieni_fascia_oraria,
    preprocessa_dati,
    valida_colonne,
)


# --- carica_dati -----------------------------------------------------------


def test_carica_dati_csv_valido(tmp_path):
    percorso = tmp_path / "valido.csv"
    percorso.write_text(
        "data,ora,zona,categoria\n"
        "2026-01-12,22:30,Zona_A,Furto\n"
        "2026-01-13,01:10,Zona_B,Danneggiamento\n"
    )

    risultato = carica_dati(str(percorso))

    assert list(risultato.columns) == ["data", "ora", "zona", "categoria"]
    assert len(risultato) == 2


def test_carica_dati_file_inesistente(tmp_path):
    percorso = tmp_path / "non_esiste.csv"

    with pytest.raises(FileNotFoundError, match="File non trovato"):
        carica_dati(str(percorso))


def test_carica_dati_csv_vuoto(tmp_path):
    percorso = tmp_path / "vuoto.csv"
    percorso.write_text("")

    with pytest.raises(ValueError, match="vuoto"):
        carica_dati(str(percorso))


def test_carica_dati_csv_malformato(tmp_path):
    percorso = tmp_path / "malformato.csv"
    percorso.write_text(
        "data,ora,zona,categoria\n"
        "2026-01-12,22:30,Zona_A,Furto\n"
        "2026-01-13,01:10,Zona_B,Danneggiamento,valore_in_piu\n"
    )

    with pytest.raises(ValueError, match="formato"):
        carica_dati(str(percorso))


# --- valida_colonne ----------------------------------------------------------


def test_valida_colonne_dataframe_valido():
    dataframe = pd.DataFrame(
        {"data": ["2026-01-12"], "ora": ["22:30"], "zona": ["Zona_A"], "categoria": ["Furto"]}
    )

    risultato = valida_colonne(dataframe)

    assert risultato is None


def test_valida_colonne_manca_una_colonna():
    dataframe = pd.DataFrame({"data": ["2026-01-12"], "ora": ["22:30"], "zona": ["Zona_A"]})

    with pytest.raises(ValueError, match="categoria"):
        valida_colonne(dataframe)


def test_valida_colonne_mancano_piu_colonne():
    dataframe = pd.DataFrame({"data": ["2026-01-12"]})

    with pytest.raises(ValueError) as errore:
        valida_colonne(dataframe)

    messaggio = str(errore.value)
    assert "ora" in messaggio
    assert "zona" in messaggio
    assert "categoria" in messaggio


def test_valida_colonne_dataframe_vuoto():
    dataframe = pd.DataFrame(columns=["data", "ora", "zona", "categoria"])

    with pytest.raises(ValueError, match="vuoto"):
        valida_colonne(dataframe)


# --- ottieni_fascia_oraria ----------------------------------------------------


@pytest.mark.parametrize(
    "ora,fascia_attesa",
    [
        (0, "00:00-04:00"),
        (3, "00:00-04:00"),
        (4, "04:00-08:00"),
        (7, "04:00-08:00"),
        (8, "08:00-12:00"),
        (11, "08:00-12:00"),
        (12, "12:00-16:00"),
        (15, "12:00-16:00"),
        (16, "16:00-20:00"),
        (19, "16:00-20:00"),
        (20, "20:00-24:00"),
        (23, "20:00-24:00"),
    ],
)
def test_ottieni_fascia_oraria_confini(ora, fascia_attesa):
    assert ottieni_fascia_oraria(ora) == fascia_attesa


@pytest.mark.parametrize("ora_non_valida", [-1, 24])
def test_ottieni_fascia_oraria_valori_non_validi(ora_non_valida):
    with pytest.raises(ValueError):
        ottieni_fascia_oraria(ora_non_valida)


# --- preprocessa_dati ----------------------------------------------------------


@pytest.fixture
def riga_valida():
    return pd.DataFrame(
        {"data": ["2026-01-12"], "ora": ["22:30"], "zona": ["Zona_A"], "categoria": ["Furto"]}
    )


def test_preprocessa_dati_conversione_data(riga_valida):
    risultato = preprocessa_dati(riga_valida)

    assert risultato.loc[0, "data"] == pd.Timestamp("2026-01-12")


def test_preprocessa_dati_giorno_settimana(riga_valida):
    risultato = preprocessa_dati(riga_valida)

    giorni = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]
    giorno_atteso = giorni[datetime.date(2026, 1, 12).weekday()]

    assert risultato.loc[0, "giorno_settimana"] == giorno_atteso


def test_preprocessa_dati_fascia_oraria(riga_valida):
    risultato = preprocessa_dati(riga_valida)

    assert risultato.loc[0, "fascia_oraria"] == "20:00-24:00"


def test_preprocessa_dati_scarta_data_non_valida():
    dataframe = pd.DataFrame(
        {
            "data": ["data-non-valida", "2026-01-12"],
            "ora": ["10:00", "22:30"],
            "zona": ["Zona_A", "Zona_B"],
            "categoria": ["Furto", "Rapina"],
        }
    )

    risultato = preprocessa_dati(dataframe)

    assert len(risultato) == 1
    assert risultato.loc[0, "categoria"] == "Rapina"


def test_preprocessa_dati_scarta_ora_non_valida():
    dataframe = pd.DataFrame(
        {
            "data": ["2026-01-12", "2026-01-13"],
            "ora": ["ora-non-valida", "08:15"],
            "zona": ["Zona_A", "Zona_B"],
            "categoria": ["Furto", "Rapina"],
        }
    )

    risultato = preprocessa_dati(dataframe)

    assert len(risultato) == 1
    assert risultato.loc[0, "categoria"] == "Rapina"


def test_preprocessa_dati_nessuna_riga_valida():
    dataframe = pd.DataFrame(
        {
            "data": ["data-non-valida"],
            "ora": ["10:00"],
            "zona": ["Zona_A"],
            "categoria": ["Furto"],
        }
    )

    with pytest.raises(ValueError):
        preprocessa_dati(dataframe)
