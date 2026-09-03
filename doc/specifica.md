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