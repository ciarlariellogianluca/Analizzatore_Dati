"""Caricamento, validazione e preprocessing del dataset CSV."""

import os
from typing import Any, Dict, List

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


def _converti_data(colonna_data: pd.Series) -> pd.Series:
    """Converte la colonna 'data' in datetime; i valori non validi diventano NaT."""
    return pd.to_datetime(colonna_data, errors="coerce")


def _converti_ora(colonna_ora: pd.Series) -> pd.Series:
    """Converte la colonna 'ora' (formato HH:MM); i valori non validi diventano NaT."""
    return pd.to_datetime(colonna_ora, format="%H:%M", errors="coerce")


def _valore_mancante(valore: Any) -> bool:
    """Indica se un valore di cella e' da considerarsi mancante (vuoto o NaN)."""
    return pd.isna(valore) or str(valore).strip() == ""


def analizza_qualita_dati(dataframe: pd.DataFrame) -> Dict[str, Any]:
    """Analizza la qualita' del dataset grezzo, prima del preprocessing.

    Individua, riga per riga, valori mancanti nelle colonne obbligatorie,
    date/orari non validi e duplicati (stessa data, ora, zona e
    categoria di una riga precedente: si considera duplicata ogni
    occorrenza successiva alla prima). Non modifica il DataFrame e non
    stampa nulla. Assume che l'indice del DataFrame sia quello di
    default (0, 1, 2, ...), coerente con un CSV appena caricato, cosi'
    che il numero di riga mostrato (indice + 2) corrisponda alla riga
    reale nel file CSV (riga 1 = intestazione).
    """
    date_convertite = _converti_data(dataframe["data"])
    ore_convertite = _converti_ora(dataframe["ora"])
    duplicati = dataframe.duplicated(subset=COLONNE_OBBLIGATORIE, keep="first")

    problemi = []
    for indice in dataframe.index:
        riga = dataframe.loc[indice]
        errori = [
            f"{colonna} mancante"
            for colonna in COLONNE_OBBLIGATORIE
            if _valore_mancante(riga[colonna])
        ]

        if not _valore_mancante(riga["data"]) and pd.isna(date_convertite[indice]):
            errori.append(f"data non valida: {riga['data']}")

        if not _valore_mancante(riga["ora"]) and pd.isna(ore_convertite[indice]):
            errori.append(f"ora non valida: {riga['ora']}")

        if duplicati[indice]:
            errori.append("record duplicato")

        if errori:
            problemi.append({"riga": int(indice) + 2, "errori": errori})

    totale_record = int(len(dataframe))
    record_problematici = len(problemi)

    return {
        "totale_record": totale_record,
        "record_validi": totale_record - record_problematici,
        "record_problematici": record_problematici,
        "duplicati": int(duplicati.sum()),
        "problemi": problemi,
    }


def preprocessa_dati(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Pulisce e arricchisce il DataFrame con colonne derivate.

    Converte 'data' in datetime, valida 'ora', calcola il giorno della
    settimana e la fascia oraria. Le righe con valori mancanti o non
    validi in una delle colonne obbligatorie, o duplicate rispetto a una
    riga precedente (stessa data, ora, zona e categoria), vengono
    scartate: questo mantiene il risultato coerente con
    analizza_qualita_dati().
    """
    df = dataframe.copy()

    for colonna in ("zona", "categoria"):
        df[colonna] = df[colonna].apply(lambda v: pd.NA if _valore_mancante(v) else v)

    df["data"] = _converti_data(df["data"])
    ora_analizzata = _converti_ora(df["ora"])

    df["ora"] = ora_analizzata.dt.strftime("%H:%M")
    df["giorno_settimana"] = df["data"].dt.dayofweek.map(_NOMI_GIORNI_SETTIMANA)

    ore = ora_analizzata.dt.hour
    df["fascia_oraria"] = ore.apply(
        lambda ora: ottieni_fascia_oraria(int(ora)) if pd.notna(ora) else pd.NA
    )

    df = df.dropna(
        subset=["data", "ora", "zona", "categoria", "giorno_settimana", "fascia_oraria"]
    )
    df = df.drop_duplicates(subset=COLONNE_OBBLIGATORIE, keep="first")
    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "Nessun record valido dopo il preprocessing: controllare 'data' e 'ora'"
        )

    return df
