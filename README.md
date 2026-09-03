# Public Safety Data Analyzer

## Descrizione

Public Safety Data Analyzer è un'applicazione Python per l'analisi
descrittiva di dati storici, aggregati e anonimizzati relativi a eventi
di pubblica sicurezza. A partire da un file CSV, il programma produce
un riepilogo statistico su categoria, zona, giorno della settimana e
fascia oraria degli eventi.

Il programma svolge esclusivamente analisi descrittiva su dati
aggregati: non identifica persone, non gestisce dati personali, non
effettua previsioni né predictive policing e non prende decisioni
operative automatiche.

## Funzionalità attuali

- Selezione del file CSV tramite interfaccia grafica (finestra con
  pulsante "Carica file CSV").
- Caricamento del dataset da file CSV.
- Verifica dell'esistenza e della leggibilità del file.
- Validazione della presenza delle colonne obbligatorie.
- Gestione di dataset vuoti e di valori mancanti o non validi.
- Conversione e validazione di date e orari.
- Calcolo del giorno della settimana per ciascun evento.
- Classificazione di ciascun evento in una fascia oraria di 4 ore.
- Conteggio degli eventi per categoria, zona, giorno della settimana e
  fascia oraria.
- Individuazione della categoria, zona, giorno e fascia oraria più
  frequenti.
- Visualizzazione del riepilogo statistico da terminale.
- Terminazione controllata in caso di errore o di annullamento della
  selezione del file.

## Struttura del dataset

Il file CSV di ingresso deve contenere le seguenti colonne obbligatorie:

| Colonna     | Descrizione                                   |
|-------------|------------------------------------------------|
| `data`      | data in cui si è verificato l'evento            |
| `ora`       | orario in cui si è verificato l'evento          |
| `zona`      | zona geografica aggregata associata all'evento  |
| `categoria` | tipologia dell'evento (es. Furto, Rapina)       |

Esempio:

```csv
data,ora,zona,categoria
2026-01-12,22:30,Zona_A,Furto
2026-01-13,01:10,Zona_B,Danneggiamento
```

Il dataset non deve contenere dati personali riconducibili a persone
fisiche.

## Esecuzione

Avviare il programma con:

```
py main.py
```

Verrà mostrata una finestra grafica: premendo il pulsante "Carica file
CSV" si apre il selettore di file del sistema operativo per scegliere
il dataset da analizzare. Il riepilogo dell'analisi viene mostrato nel
terminale da cui è stato avviato il programma.

## Dipendenze

- Python 3
- [pandas](https://pandas.pydata.org/)
- tkinter (incluso nella libreria standard di Python)

## Struttura del progetto

```
public-safety-data-analyzer/
│
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
│
├── main.py
├── analisi.py
├── caricatore_dati.py
├── dati_esempio.csv
│
├── doc/
│   └── specifica.md
│
└── tests/
```

## Documentazione

La specifica del progetto è disponibile in [doc/specifica.md](doc/specifica.md).

## Stato del progetto

Progetto universitario in sviluppo. La versione attuale implementa il
programma di analisi e la relativa documentazione di specifica; test
automatici, integrazione continua e containerizzazione non sono ancora
stati aggiunti e saranno oggetto di fasi successive.
