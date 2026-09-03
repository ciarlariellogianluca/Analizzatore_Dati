"""Test di integrazione: eseguono main.py come processo reale (CLI, senza GUI).

Attraversano insieme main.py, caricatore_dati.py e analisi.py cosi' come
li userebbe un utente da riga di comando.
"""

import subprocess
import sys
from pathlib import Path

CARTELLA_PROGETTO = Path(__file__).resolve().parent.parent
TIMEOUT_SECONDI = 30


def _esegui_programma(percorso_csv) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "main.py", str(percorso_csv)],
        capture_output=True,
        text=True,
        cwd=CARTELLA_PROGETTO,
        timeout=TIMEOUT_SECONDI,
    )


# --- Test 1: flusso completo con dataset valido -----------------------------


def test_flusso_completo_con_dataset_valido(tmp_path):
    percorso_csv = tmp_path / "eventi_validi.csv"
    percorso_csv.write_text(
        "data,ora,zona,categoria\n"
        "2026-01-12,22:30,Zona_A,Furto\n"
        "2026-01-13,01:10,Zona_B,Danneggiamento\n"
        "2026-01-14,15:45,Zona_A,Furto\n"
    )

    risultato = _esegui_programma(percorso_csv)

    assert risultato.returncode == 0
    assert "PUBLIC SAFETY DATA ANALYZER" in risultato.stdout
    assert "Totale eventi: 3" in risultato.stdout
    assert "Furto" in risultato.stdout
    assert "Zona_A" in risultato.stdout
    assert "20:00-24:00" in risultato.stdout
    assert "Traceback" not in risultato.stdout
    assert "Traceback" not in risultato.stderr


# --- Test 2: file inesistente -------------------------------------------------


def test_file_inesistente(tmp_path):
    percorso_inesistente = tmp_path / "non_esiste.csv"

    risultato = _esegui_programma(percorso_inesistente)

    assert risultato.returncode != 0
    assert "non trovato" in risultato.stdout.lower()
    assert "Traceback" not in risultato.stdout
    assert "Traceback" not in risultato.stderr


# --- Test 3: colonne mancanti -------------------------------------------------


def test_colonne_mancanti(tmp_path):
    percorso_csv = tmp_path / "colonne_mancanti.csv"
    percorso_csv.write_text("data,zona\n2026-01-12,Zona_A\n")

    risultato = _esegui_programma(percorso_csv)

    assert risultato.returncode != 0
    assert "colonne mancanti" in risultato.stdout
    assert "ora" in risultato.stdout
    assert "categoria" in risultato.stdout
    assert "Traceback" not in risultato.stdout
    assert "Traceback" not in risultato.stderr


# --- Test 4: dati completamente invalidi --------------------------------------


def test_dati_completamente_invalidi(tmp_path):
    percorso_csv = tmp_path / "dati_invalidi.csv"
    percorso_csv.write_text(
        "data,ora,zona,categoria\n"
        "data-non-valida,ora-non-valida,Zona_A,Furto\n"
    )

    risultato = _esegui_programma(percorso_csv)

    assert risultato.returncode != 0
    assert "Nessun record valido" in risultato.stdout
    assert "Traceback" not in risultato.stdout
    assert "Traceback" not in risultato.stderr


# --- Test 5: dataset parzialmente invalido ------------------------------------


def test_dataset_parzialmente_invalido(tmp_path):
    percorso_csv = tmp_path / "dati_parziali.csv"
    percorso_csv.write_text(
        "data,ora,zona,categoria\n"
        "2026-01-12,22:30,Zona_A,Furto\n"
        "data-non-valida,10:00,Zona_B,Rapina\n"
        "2026-01-14,08:15,Zona_A,Furto\n"
    )

    risultato = _esegui_programma(percorso_csv)

    assert risultato.returncode == 0
    assert "Totale eventi: 2" in risultato.stdout
    assert "Traceback" not in risultato.stdout
    assert "Traceback" not in risultato.stderr
