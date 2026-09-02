"""Punto di ingresso CLI del Public Safety Data Analyzer."""

import sys
from typing import Any, Dict

import pandas as pd

from analisi import genera_riepilogo
from caricatore_dati import carica_dati, preprocessa_dati, valida_colonne


def mostra_schermata_iniziale() -> str:
    """Mostra una finestra grafica per caricare il file CSV e restituisce il percorso scelto."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        return input(
            "Interfaccia grafica non disponibile.\nInserisci il percorso del file CSV: "
        ).strip()

    percorso_scelto = {"valore": ""}

    def carica_file() -> None:
        percorso = filedialog.askopenfilename(
            title="Seleziona il file CSV",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")],
        )
        if percorso:
            percorso_scelto["valore"] = percorso
            finestra.destroy()

    larghezza, altezza = 480, 320
    colore_sfondo = "#1f2937"
    colore_testo = "#f9fafb"
    colore_testo_secondario = "#9ca3af"

    finestra = tk.Tk()
    finestra.title("Public Safety Data Analyzer")
    finestra.configure(bg=colore_sfondo)
    finestra.resizable(False, False)

    finestra.update_idletasks()
    x = (finestra.winfo_screenwidth() - larghezza) // 2
    y = (finestra.winfo_screenheight() - altezza) // 2
    finestra.geometry(f"{larghezza}x{altezza}+{x}+{y}")

    tk.Label(
        finestra,
        text="Public Safety Data Analyzer",
        font=("Segoe UI", 16, "bold"),
        fg=colore_testo,
        bg=colore_sfondo,
    ).pack(pady=(35, 5))

    tk.Label(
        finestra,
        text="Analisi statistica di eventi di pubblica sicurezza",
        font=("Segoe UI", 10),
        fg=colore_testo_secondario,
        bg=colore_sfondo,
    ).pack(pady=(0, 25))

    tk.Label(
        finestra,
        text="Il file CSV deve contenere le colonne:\ndata, ora, zona, categoria",
        font=("Segoe UI", 9),
        fg="#d1d5db",
        bg=colore_sfondo,
        justify="center",
    ).pack(pady=(0, 25))

    tk.Button(
        finestra,
        text="Carica file CSV",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg="#2563eb",
        activebackground="#1d4ed8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=10,
        command=carica_file,
    ).pack(pady=10)

    tk.Label(
        finestra,
        text="Chiudi la finestra per annullare",
        font=("Segoe UI", 8),
        fg="#6b7280",
        bg=colore_sfondo,
    ).pack(side="bottom", pady=15)

    finestra.mainloop()

    return percorso_scelto["valore"]


def stampa_riepilogo(riepilogo: Dict[str, Any]) -> None:
    """Stampa a video il riepilogo dell'analisi in formato leggibile."""
    print("=" * 40)
    print(" PUBLIC SAFETY DATA ANALYZER")
    print("=" * 40)

    print(f"\nTotale eventi: {riepilogo['totale_eventi']}")

    print("\nEVENTI PER CATEGORIA")
    for categoria, conteggio in riepilogo["eventi_per_categoria"].items():
        print(f"{categoria}: {conteggio}")

    print("\nEVENTI PER ZONA")
    for zona, conteggio in riepilogo["eventi_per_zona"].items():
        print(f"{zona}: {conteggio}")

    print("\nEVENTI PER GIORNO DELLA SETTIMANA")
    for giorno, conteggio in riepilogo["eventi_per_giorno"].items():
        print(f"{giorno}: {conteggio}")

    print("\nEVENTI PER FASCIA ORARIA")
    for fascia, conteggio in riepilogo["eventi_per_fascia_oraria"].items():
        print(f"{fascia}: {conteggio}")

    print(f"\nCategoria piu' frequente: {riepilogo['categoria_piu_frequente']}")
    print(f"Zona con piu' eventi: {riepilogo['zona_piu_eventi']}")
    print(f"Giorno piu' frequente: {riepilogo['giorno_piu_frequente']}")
    print(f"Fascia oraria piu' frequente: {riepilogo['fascia_oraria_piu_frequente']}")


def main() -> None:
    """Coordina scelta del file, caricamento, validazione, analisi e output."""
    percorso_file = mostra_schermata_iniziale()

    if not percorso_file:
        print("Nessun file selezionato. Programma terminato.")
        sys.exit(0)

    try:
        dataframe = carica_dati(percorso_file)
        valida_colonne(dataframe)
        dataframe = preprocessa_dati(dataframe)
        riepilogo = genera_riepilogo(dataframe)
    except (FileNotFoundError, PermissionError, ValueError, pd.errors.ParserError) as errore:
        print(f"Errore: {errore}")
        sys.exit(1)

    stampa_riepilogo(riepilogo)


if __name__ == "__main__":
    main()
