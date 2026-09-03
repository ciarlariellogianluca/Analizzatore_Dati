# Specifica del progetto

## 1. Nome del progetto

Public Safety Data Analyzer

## 2. Scopo del sistema

Public Safety Data Analyzer è un'applicazione sviluppata in Python per
analizzare dati storici relativi a eventi di pubblica sicurezza.

I dati vengono forniti tramite file CSV e devono essere aggregati e
anonimizzati. Lo scopo del programma è ottenere un riepilogo semplice
dei dati, in modo da capire quali tipi di eventi risultano più frequenti,
in quali zone si verificano maggiormente e come sono distribuiti nei
diversi giorni e nelle diverse fasce orarie.

L'applicazione svolge quindi un'analisi descrittiva dei dati e non ha lo
scopo di effettuare previsioni o prendere decisioni operative.

Inoltre, il dataset utilizzato non deve contenere informazioni personali
o dati che permettano di identificare direttamente una persona.

## 3. Utente del sistema

L'applicazione è pensata per un utente che dispone di un dataset di
eventi di pubblica sicurezza e vuole ottenere alcune statistiche di base
sul suo contenuto.

Ad esempio, l'utente può essere un operatore o un analista interessato
ad avere una visione generale dei dati raccolti.

Nella versione attuale non sono previsti login, account o diversi tipi
di utente.

## 4. Dati di ingresso

Il programma utilizza come input un file CSV.

Il file deve contenere almeno le seguenti colonne:

- **data**: data in cui è stato registrato l'evento;
- **ora**: ora in cui è stato registrato l'evento;
- **zona**: zona geografica associata all'evento;
- **categoria**: tipologia dell'evento, ad esempio Furto, Rapina o
  Danneggiamento.

Un esempio di file valido è:

```csv
data,ora,zona,categoria
2026-01-12,22:30,Zona_A,Furto
2026-01-13,01:10,Zona_B,Danneggiamento
```

Il file non deve contenere dati personali riconducibili a persone
fisiche (nomi, identificativi, indirizzi puntuali o qualsiasi altro dato
che permetta di identificare un individuo).

## 5. Requisiti funzionali

RF01 - Il sistema deve avviarsi mostrando una finestra grafica che
permetta all'utente di avviare la selezione del file CSV da analizzare.

RF02 - Il sistema deve caricare in memoria il contenuto del file CSV
selezionato dall'utente.

RF03 - Il sistema deve verificare che il file CSV caricato contenga le
colonne obbligatorie (data, ora, zona, categoria) e deve segnalare in
modo esplicito quali colonne risultano mancanti, se presenti.

RF04 - Il sistema deve validare e preprocessare i dati caricati,
convertendo la data in un formato elaborabile, verificando la validità
degli orari ed escludendo le righe che presentano valori mancanti o non
validi nelle colonne obbligatorie.

RF05 - Il sistema deve classificare ciascun evento in una fascia oraria
predefinita di 4 ore, sulla base dell'orario registrato.

RF06 - Il sistema deve calcolare il numero di eventi per ciascuna
categoria presente nel dataset.

RF07 - Il sistema deve calcolare il numero di eventi per ciascuna zona
presente nel dataset.

RF08 - Il sistema deve calcolare il numero di eventi per ciascun giorno
della settimana.

RF09 - Il sistema deve calcolare il numero di eventi per ciascuna fascia
oraria.

RF10 - Il sistema deve generare un riepilogo complessivo dell'analisi,
comprendente il numero totale di eventi, i conteggi per categoria, zona,
giorno della settimana e fascia oraria, e i valori più frequenti per
ciascuna di queste dimensioni, mostrandolo all'utente tramite terminale.

RF11 - Il sistema deve gestire in modo controllato le condizioni di
errore (file inesistente, file non leggibile, file CSV vuoto, colonne
mancanti, dati non validi), mostrando un messaggio comprensibile
all'utente e terminando senza generare un errore non gestito.

RF12 - Il sistema deve gestire in modo controllato l'annullamento della
selezione del file, terminando l'esecuzione senza eseguire alcuna
analisi qualora l'utente chiuda la finestra di selezione senza scegliere
un file.

## 6. Requisiti non funzionali

RNF01 - Il sistema deve essere eseguibile tramite Python 3 utilizzando
la libreria pandas per l'elaborazione dei dati.

RNF02 - Il codice deve essere organizzato in moduli distinti, con
separazione tra caricamento/validazione dei dati, analisi statistica e
interfaccia/output verso l'utente.

RNF03 - Il codice deve essere strutturato in funzioni piccole e
leggibili, in modo da risultare comprensibile e facilmente verificabile.

RNF04 - Gli errori riscontrati durante l'esecuzione devono essere
gestiti in modo controllato, restituendo messaggi comprensibili
all'utente finale anziché interrompere il programma con una traccia di
errore tecnica.

RNF05 - Il sistema non deve trattare, memorizzare o mostrare dati
personali riconducibili a persone fisiche.

RNF06 - Il sistema deve essere ragionevolmente portabile su qualsiasi
ambiente dotato di Python 3, pandas e tkinter, senza dipendere da
componenti specifici di un singolo sistema operativo.

## 7. Precondizioni

- È disponibile un interprete Python 3 funzionante.
- Sono disponibili le librerie richieste (pandas e tkinter).
- È disponibile un file di dati in formato CSV da analizzare.
- Il file CSV contiene le quattro colonne obbligatorie (data, ora, zona,
  categoria).

## 8. Postcondizioni

Al termine di un'esecuzione corretta:

- il dataset fornito è stato analizzato;
- le statistiche descrittive richieste sono state calcolate e mostrate
  all'utente;
- il file CSV originale non è stato modificato in alcun modo;
- nessun dato personale è stato trattato o prodotto in output.

## 9. Gestione degli errori

Il sistema deve gestire in modo controllato, senza generare errori non
gestiti visibili all'utente, almeno i seguenti casi:

- **file inesistente**: il percorso indicato non corrisponde a un file
  presente sul sistema;
- **file non leggibile**: il file esiste ma non può essere aperto in
  lettura;
- **CSV vuoto**: il file non contiene alcun dato analizzabile;
- **colonne mancanti**: una o più colonne obbligatorie non sono presenti
  nel file;
- **data non valida**: uno o più valori nella colonna data non sono
  interpretabili come data;
- **ora non valida**: uno o più valori nella colonna ora non sono
  interpretabili come orario;
- **valori mancanti**: una o più righe presentano campi obbligatori
  vuoti;
- **selezione file annullata**: l'utente chiude la finestra di selezione
  senza scegliere alcun file.

In ciascuno di questi casi il sistema deve interrompere l'elaborazione e
comunicare all'utente un messaggio chiaro sulla natura del problema,
senza proseguire con un'analisi su dati incompleti o non validi.

## 10. Casi d'uso

### CU01 - Analizzare un dataset valido

- **Attore**: utente/analista.
- **Precondizioni**: applicazione avviata; è disponibile un file CSV
  valido con le colonne obbligatorie e dati corretti.
- **Flusso principale**:
  1. L'utente avvia l'applicazione.
  2. Il sistema mostra la finestra iniziale.
  3. L'utente seleziona il file CSV tramite l'apposito pulsante.
  4. Il sistema carica, valida e preprocessa i dati.
  5. Il sistema calcola le statistiche richieste.
  6. Il sistema mostra il riepilogo dei risultati.
- **Flussi alternativi / errori**: nessuno; è il caso nominale.
- **Postcondizioni**: il riepilogo statistico è mostrato correttamente;
  il file originale non è modificato.

### CU02 - Selezionare un file non valido

- **Attore**: utente/analista.
- **Precondizioni**: applicazione avviata.
- **Flusso principale**:
  1. L'utente avvia l'applicazione.
  2. L'utente seleziona un file inesistente, non leggibile o non in
     formato CSV valido.
  3. Il sistema tenta il caricamento del file.
- **Flussi alternativi / errori**:
  - se il file non esiste o non è leggibile, il sistema mostra un
    messaggio di errore comprensibile e termina in modo controllato;
  - se il contenuto non è in un formato CSV valido, il sistema segnala
    l'errore di formato e termina in modo controllato.
- **Postcondizioni**: nessuna analisi viene eseguita; l'utente riceve un
  messaggio di errore chiaro.

### CU03 - Caricare un dataset con colonne mancanti

- **Attore**: utente/analista.
- **Precondizioni**: il file CSV selezionato non contiene una o più
  colonne obbligatorie.
- **Flusso principale**:
  1. L'utente seleziona un file CSV.
  2. Il sistema carica il file.
  3. Il sistema verifica la presenza delle colonne obbligatorie.
- **Flussi alternativi / errori**:
  - se una o più colonne obbligatorie risultano mancanti, il sistema
    interrompe l'elaborazione e mostra l'elenco delle colonne mancanti.
- **Postcondizioni**: nessuna analisi viene eseguita; l'utente riceve
  l'elenco delle colonne mancanti.

### CU04 - Annullare la selezione del file

- **Attore**: utente/analista.
- **Precondizioni**: la finestra iniziale dell'applicazione è
  visualizzata.
- **Flusso principale**:
  1. L'utente avvia l'applicazione.
  2. L'utente chiude la finestra senza selezionare alcun file.
- **Flussi alternativi / errori**: nessuno.
- **Postcondizioni**: il programma termina in modo controllato senza
  eseguire alcuna analisi.

## 11. Vincoli del sistema

- Il sistema opera esclusivamente su file in formato CSV.
- Il sistema esegue unicamente analisi statistica descrittiva.
- Il sistema opera solo su dati aggregati e anonimizzati.
- Il sistema non utilizza alcun database.
- Il sistema non utilizza tecniche di machine learning.
- Il sistema non effettua alcun tipo di previsione.
- Il sistema non prevede meccanismi di autenticazione o gestione utenti.
- Il sistema non modifica in alcun modo il file di dati originale.

## 12. Funzionalità escluse dalla versione corrente

Nella versione attuale non fanno parte delle funzionalità applicative:

- machine learning;
- predictive policing;
- utilizzo di un database;
- autenticazione degli utenti;
- analisi di dati personali;
- esposizione di API web.

## 13. Possibili evoluzioni

Come possibili evoluzioni future, coerenti con lo scopo del sistema, si
individuano:

- grafici statistici a supporto del riepilogo testuale;
- filtri temporali sul periodo da analizzare;
- confronto statistico tra periodi diversi;
- esportazione del riepilogo su file.

Queste evoluzioni non sono implementate nella versione attuale e non
costituiscono requisiti del sistema descritto in questo documento.