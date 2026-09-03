"""Property-based test con Hypothesis per caricatore_dati.py e analisi.py."""

import pandas as pd
from hypothesis import given
from hypothesis import strategies as st

from analisi import conta_eventi_per_categoria, conta_eventi_per_zona, genera_riepilogo
from caricatore_dati import ottieni_fascia_oraria

FASCE_ORARIE_VALIDE = [
    "00:00-04:00",
    "04:00-08:00",
    "08:00-12:00",
    "12:00-16:00",
    "16:00-20:00",
    "20:00-24:00",
]

CATEGORIE_SINTETICHE = ["Cat_A", "Cat_B", "Cat_C"]
ZONE_SINTETICHE = ["Zona_X", "Zona_Y", "Zona_Z"]
GIORNI_SINTETICI = ["Lunedi", "Martedi", "Mercoledi"]


# --- Property test 1: fasce orarie ------------------------------------------


@given(ora=st.integers(min_value=0, max_value=23))
def test_ottieni_fascia_oraria_restituisce_sempre_una_fascia_valida(ora):
    """Per qualsiasi ora valida (0-23) il risultato e' una delle sei fasce."""
    assert ottieni_fascia_oraria(ora) in FASCE_ORARIE_VALIDE


# --- Property test 2: coerenza della fascia ---------------------------------


@given(ora=st.integers(min_value=0, max_value=23))
def test_ottieni_fascia_oraria_coerente_con_blocco_di_4_ore(ora):
    """La fascia restituita corrisponde sempre al blocco di 4 ore ora // 4."""
    indice_fascia_attesa = ora // 4
    assert ottieni_fascia_oraria(ora) == FASCE_ORARIE_VALIDE[indice_fascia_attesa]


# --- Property test 3: conteggio per categoria -------------------------------


@given(
    categorie=st.lists(st.sampled_from(CATEGORIE_SINTETICHE), min_size=1, max_size=50)
)
def test_conta_eventi_per_categoria_somma_totale(categorie):
    """La somma dei conteggi per categoria e' sempre pari al numero di righe."""
    dataframe = pd.DataFrame({"categoria": categorie})

    risultato = conta_eventi_per_categoria(dataframe)

    assert risultato.sum() == len(dataframe)


# --- Property test 4: conteggio per zona ------------------------------------


@given(zone=st.lists(st.sampled_from(ZONE_SINTETICHE), min_size=1, max_size=50))
def test_conta_eventi_per_zona_somma_totale(zone):
    """La somma dei conteggi per zona e' sempre pari al numero di righe."""
    dataframe = pd.DataFrame({"zona": zone})

    risultato = conta_eventi_per_zona(dataframe)

    assert risultato.sum() == len(dataframe)


# --- Property test 5: riepilogo ----------------------------------------------


@given(dati=st.data())
def test_genera_riepilogo_proprieta_generali(dati):
    """Il totale eventi e la somma dei conteggi parziali restano coerenti
    qualunque sia la composizione del dataset generato."""
    numero_righe = dati.draw(st.integers(min_value=1, max_value=30))
    colonna_comune = dict(min_size=numero_righe, max_size=numero_righe)

    dataframe = pd.DataFrame(
        {
            "categoria": dati.draw(
                st.lists(st.sampled_from(CATEGORIE_SINTETICHE), **colonna_comune)
            ),
            "zona": dati.draw(st.lists(st.sampled_from(ZONE_SINTETICHE), **colonna_comune)),
            "giorno_settimana": dati.draw(
                st.lists(st.sampled_from(GIORNI_SINTETICI), **colonna_comune)
            ),
            "fascia_oraria": dati.draw(
                st.lists(st.sampled_from(FASCE_ORARIE_VALIDE), **colonna_comune)
            ),
        }
    )

    riepilogo = genera_riepilogo(dataframe)

    assert riepilogo["totale_eventi"] == len(dataframe)
    assert sum(riepilogo["eventi_per_categoria"].values()) == riepilogo["totale_eventi"]
    assert sum(riepilogo["eventi_per_zona"].values()) == riepilogo["totale_eventi"]
