# Trenitalia-YoungChecker

<img width="872" alt="Screenshot 2025-03-03 at 20 12 21" src="https://github.com/user-attachments/assets/75cd94b6-46bd-48cc-bd02-14c803b3d892" />

Dato che trenitalia non offre la possibilità di visualizzare le soluzioni di viaggio in formato calendario, ho deciso di scrivere questo semplice script che permette di verificare in forma di calendario (ASCII art) la presenza o meno di biglietti aventi tariffa YOUNG disponibile, fino a 180 giorni prima e di elencarli in formato JSON. Così da risparmiarsi la fatica di farsi più ricerche per verificare per ogni giorno se la suddetta offerta è disponibile.

Al momento lo script supporta solo le stazioni prinicpali e si riferisce esculsivamente a treni freccia rossa senza cambi. La stazione va digitata come riportato tra le parentesi (case-sensitive) altrimenti verrà richiesto nuovamente l'inserimento finché non viene inserita la città corretta (le stazioni inseribili nel campo partenza sono le stesse inseribili nel campo ritorno e il nome della città si riferisce sempre alla stazione principale della città che si sceglie, ad esempio Milano = Milano Centrale).

# Esempio di funzionamento

<img width="810" alt="Screenshot 2025-03-13 at 20 15 08" src="https://github.com/user-attachments/assets/c34c2cc1-63c7-463b-9f79-614a626f6791" />

- Inserire una delle stazioni proposte

<img width="180" alt="Screenshot 2025-03-03 at 20 28 25" src="https://github.com/user-attachments/assets/e15645a1-9060-4289-9ae7-96e1be77ac98" />

- Inserire nel ritorno una delle stazioni proposte nell'andata (le stazioni proposte sono tra loro interconesse, grafo non orientato)

Il seguente è un esempio di output di ricerca tra Milano e Firenze (perido di osservazione 2 mesi, 60 giorni)
> [!IMPORTANT]  
> Il tempo di risposta varia in base al numero di giorni per cui fissiamo lo scope di osservazione. Più sono i giorni in avanti per cui vogliamo verificare e più il tempo di esecuzione dello script si alzerà.

> [!TIP]
> L'idea migliore è lasciare lo script in background e aggiornarlo ogni tot


1. Per prima cosa ci restituisce tutti i biglietti con tariffa young disponibile fino al giorno desiderato

<img width="595" alt="Screenshot 2025-03-03 at 20 32 55" src="https://github.com/user-attachments/assets/714232ed-1312-489d-b3f2-6c3c082141fe" />

2. Rappresentazione in ASCII art di un calendario delle disponibilità della tariffa young su almeno un biglietto nel giorno indicato (verde = DISPONIBILE, rosso = NON DISPONIBILE)

<img width="409" alt="Screenshot 2025-03-03 at 20 12 43" src="https://github.com/user-attachments/assets/8eab0f0d-d262-4219-8c9d-9348556373c9" />

# NOTE
>[!WARNING]
>Utilizzate il seguente script responsabilmente. Da una rapida lettura dei termini e condizioni sull'utilizzo del sito di trenitalia non viene specificato molto sulla questione e comunque il numero di richieste effettuate non sono esagerate (circa 900 nel caso peggiore) still non rompete trenitalia che già è fragile T-T
- Un enorme rinraziamento va a [simodax.github.io](https://github.com/SimoDax) e al suo [progetto sulle API di trenitalia](https://github.com/SimoDax/Trenitalia-API/wiki/Nuove-API-Trenitalia-lefrecce.it)
- Chiunque voglia destreggiarsi nella creazione di un FE è il benvenuto, l'unico motivo per cui l'ho fatto in ascii art è skill issue

