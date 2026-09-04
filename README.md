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
  pulsante "Carica file CSV"), oppure modalità CLI/headless.
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

Modalità GUI (apre una finestra per scegliere il file):

```
py main.py
```

Modalità CLI/headless, senza aprire alcuna finestra (usata da test,
CI/CD e Docker):

```
py main.py dati_esempio.csv
```

In entrambi i casi il riepilogo dell'analisi viene stampato nel
terminale.

## Test

Il progetto include una suite di 45 test automatici con `pytest`:

- unit test su `caricatore_dati.py` e `analisi.py`;
- property-based test con Hypothesis, che verificano proprietà generali
  su input generati automaticamente;
- test di integrazione, che eseguono `main.py` come processo reale in
  modalità CLI.

Eseguire l'intera suite:

```
py -m pytest -v
```

Misurare la coverage:

```
py -m coverage run -m pytest
py -m coverage report -m
```

Verificare lo stile del codice:

```
py -m pylint main.py analisi.py caricatore_dati.py
```

## CI/CD

Una pipeline GitHub Actions (`.github/workflows/ci.yml`) viene eseguita
automaticamente ad ogni push e pull request verso `main`:

1. lint del codice con `pylint`;
2. l'intera suite di test sotto coverage;
3. build del pacchetto Python (`python -m build`), pubblicata come
   artifact della run;
4. build dell'immagine Docker.

Solo sui push diretti a `main` — mai sulle pull request — se tutti gli
step precedenti hanno successo, la pipeline pubblica automaticamente
l'immagine Docker aggiornata su Docker Hub.

## Docker

L'applicazione è disponibile come immagine Docker pubblica su Docker
Hub (`kgianni/public-safety-data-analyzer`), pubblicata automaticamente
dalla pipeline CI/CD ad ogni push su `main`.

Scaricare l'ultima immagine pubblicata:

```
docker pull kgianni/public-safety-data-analyzer:latest
```

Eseguire l'analisi su un file CSV locale, montandolo dentro il
container in sola lettura (esempio PowerShell):

```powershell
docker run --rm -v "C:\percorso\del\tuo\file.csv:/dati/file.csv:ro" kgianni/public-safety-data-analyzer:latest /dati/file.csv
```

Il parametro `-v host:container:ro` monta il file CSV della macchina
host dentro il container (qui nel percorso `/dati/file.csv`), in sola
lettura: il file non viene mai copiato nell'immagine né modificato. Il
percorso passato dopo il nome dell'immagine è quello visto dal
container, non quello sulla macchina host. Il CSV deve rispettare lo
stesso formato descritto in [Struttura del dataset](#struttura-del-dataset).

## Dipendenze

- Python 3
- [pandas](https://pandas.pydata.org/)
- tkinter (incluso nella libreria standard di Python, usato solo dalla
  modalità GUI)

## Struttura del progetto

```
public-safety-data-analyzer/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── README.md
├── LICENSE
├── .gitignore
├── .dockerignore
├── Dockerfile
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
    ├── test_caricatore_dati.py
    ├── test_analisi.py
    ├── test_proprieta.py
    └── test_integrazione.py
```

## Documentazione

La specifica del progetto è disponibile in [doc/specifica.md](doc/specifica.md).

## Stato del progetto

Progetto universitario. La versione attuale comprende: il programma di
analisi con modalità GUI e CLI, la specifica del progetto, una suite di
45 test automatici (unit, property-based con Hypothesis, integrazione)
con misurazione della coverage, `pylint` a punteggio massimo, una
pipeline CI/CD su GitHub Actions che esegue lint/test/coverage/build ad
ogni push e pull request, e la pubblicazione automatica dell'immagine
Docker su Docker Hub ad ogni push su `main`.
