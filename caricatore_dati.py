"""Caricamento, validazione e preprocessing del dataset CSV."""

import os
from typing import List

import pandas as pd

COLONNE_OBBLIGATORIE: List[str] = ["data", "ora", "zona", "categoria"]

_NOMI_GIORNI_SETTIMANA = {
    0: "Lunedi",
    1: "Martedi",
    2: "Mercoledi",
    3: "Giovedi",
    4: "Venerdi",
    5: "Sabato",
    6: "Domenica",
}


def carica_dati(percorso_file: str) -> pd.DataFrame:
    """Carica il dataset CSV da percorso_file e restituisce un DataFrame."""
    if not os.path.exists(percorso_file):
        raise FileNotFoundError(f"File non trovato: {percorso_file}")

    if not os.path.isfile(percorso_file):
        raise ValueError(f"Il percorso indicato non e' un file: {percorso_file}")

    if not os.access(percorso_file, os.R_OK):
        raise PermissionError(f"Impossibile leggere il file: {percorso_file}")

    try:
        dataframe = pd.read_csv(percorso_file)
    except pd.errors.EmptyDataError as errore:
        raise ValueError(f"Il file CSV e' vuoto: {percorso_file}") from errore
    except pd.errors.ParserError as errore:
        raise ValueError(f"Errore nel formato del file CSV: {errore}") from errore

    return dataframe


def valida_colonne(dataframe: pd.DataFrame) -> None:
    """Verifica che il DataFrame contenga tutte le colonne obbligatorie."""
    if dataframe.empty:
        raise ValueError("il dataset e' vuoto")

    colonne_mancanti = [
        colonna for colonna in COLONNE_OBBLIGATORIE if colonna not in dataframe.columns
    ]

    if colonne_mancanti:
        raise ValueError(f"colonne mancanti: {', '.join(colonne_mancanti)}")


def ottieni_fascia_oraria(ora: int) -> str:
    """Restituisce la fascia oraria (blocco di 4 ore) corrispondente a ora."""
    if not isinstance(ora, int) or ora < 0 or ora > 23:
        raise ValueError(f"Ora non valida: {ora}")

    if 0 <= ora < 4:
        return "00:00-04:00"
    if 4 <= ora < 8:
        return "04:00-08:00"
    if 8 <= ora < 12:
        return "08:00-12:00"
    if 12 <= ora < 16:
        return "12:00-16:00"
    if 16 <= ora < 20:
        return "16:00-20:00"
    return "20:00-24:00"


def preprocessa_dati(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Pulisce e arricchisce il DataFrame con colonne derivate.

    Converte 'data' in datetime, valida 'ora', calcola il giorno della
    settimana e la fascia oraria. Le righe con valori mancanti o non
    validi in una delle colonne obbligatorie vengono scartate.
    """
    df = dataframe.copy()

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    ora_analizzata = pd.to_datetime(df["ora"], format="%H:%M", errors="coerce")

    df["ora"] = ora_analizzata.dt.strftime("%H:%M")
    df["giorno_settimana"] = df["data"].dt.dayofweek.map(_NOMI_GIORNI_SETTIMANA)

    ore = ora_analizzata.dt.hour
    df["fascia_oraria"] = ore.apply(
        lambda ora: ottieni_fascia_oraria(int(ora)) if pd.notna(ora) else pd.NA
    )

    df = df.dropna(
        subset=["data", "ora", "zona", "categoria", "giorno_settimana", "fascia_oraria"]
    )
    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "Nessun record valido dopo il preprocessing: controllare 'data' e 'ora'"
        )

    return df
