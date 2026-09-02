"""Funzioni di analisi statistica descrittiva sul dataset preprocessato."""

from typing import Any, Dict

import pandas as pd


def conta_eventi_per_categoria(dataframe: pd.DataFrame) -> pd.Series:
    """Conta il numero di eventi per categoria."""
    return dataframe["categoria"].value_counts()


def conta_eventi_per_zona(dataframe: pd.DataFrame) -> pd.Series:
    """Conta il numero di eventi per zona."""
    return dataframe["zona"].value_counts()


def conta_eventi_per_giorno(dataframe: pd.DataFrame) -> pd.Series:
    """Conta il numero di eventi per giorno della settimana."""
    return dataframe["giorno_settimana"].value_counts()


def conta_eventi_per_fascia_oraria(dataframe: pd.DataFrame) -> pd.Series:
    """Conta il numero di eventi per fascia oraria."""
    return dataframe["fascia_oraria"].value_counts()


def genera_riepilogo(dataframe: pd.DataFrame) -> Dict[str, Any]:
    """Costruisce un riepilogo statistico completo del dataset.

    Restituisce un dizionario con conteggi aggregati e i valori
    piu' frequenti per ciascuna dimensione di analisi.
    """
    per_categoria = conta_eventi_per_categoria(dataframe)
    per_zona = conta_eventi_per_zona(dataframe)
    per_giorno = conta_eventi_per_giorno(dataframe)
    per_fascia_oraria = conta_eventi_per_fascia_oraria(dataframe)

    return {
        "totale_eventi": int(len(dataframe)),
        "eventi_per_categoria": per_categoria.to_dict(),
        "eventi_per_zona": per_zona.to_dict(),
        "eventi_per_giorno": per_giorno.to_dict(),
        "eventi_per_fascia_oraria": per_fascia_oraria.to_dict(),
        "categoria_piu_frequente": str(per_categoria.idxmax()),
        "zona_piu_eventi": str(per_zona.idxmax()),
        "giorno_piu_frequente": str(per_giorno.idxmax()),
        "fascia_oraria_piu_frequente": str(per_fascia_oraria.idxmax()),
    }
