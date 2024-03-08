TeleTracker

Questa repository contiene degli script Python (TeleTesto.py, TeleOttieni.py e TeleVedi.py) progettati per aiutare gli analisti a monitorare e interrompere campagne malware attive che usano Telegram per il controllo e comando (C2).

TeleOttieni.py

È lo script principale per raccogliere informazioni sulle attività delle minacce informatiche e i dati raccolti da dispositivi compromessi. È stato aggiornato con nuove funzionalità e miglioramenti:

✅ Visualizzare i messaggi del canale e scaricare contenuti: Salva il contenuto nella cartella di lavoro corrente all'interno della cartella 'downloads'. Supporta il download di documenti, foto, video, ecc.
✅ Inviare documenti via Telegram: Invia opzionalmente un messaggio. Supporta tutti i tipi di file supportati da Telegram. Rilevamento automatico del tipo MIME.
✅ Selezione dei messaggi: Scegli un numero specifico di messaggi o un ID messaggio da scaricare. Il download avviene SEMPRE dal messaggio più recente a quello più vecchio.
✅ Salvataggio dei log: Creazione di file di testo chiari contenenti informazioni di base (<bot_name>.txt) e salvataggio completo in formato JSON per ogni messaggio (<bot_name>.json).
✅ Recupero informazioni sul bot: Ottiene informazioni sul bot e proprietario, inclusi dettagli sul canale.
✅ Nuova Funzionalità: Possibilità di inviare file
✅ Menu Opzionale:
* MONITOR: Leggi i nuovi messaggi.
* DISRUPT: Cancella i messaggi dai canali utilizzati dalle minacce.
* DISRUPT: Effettua spam ad alta velocità nei canali, con un messaggio scelto dall'utente.

Nota: Questo script è destinato ad analisti o ricercatori nell'ambito della sicurezza informatica che desiderano monitorare, raccogliere dati e rintracciare avversari che usano Telegram per comunicazioni C2.

Installazione

    Installare Python se non è già presente sul sistema.
    Installare la libreria requests: pip install -r requirements
    Clonare il repository: git clone https://github.com/tsale/TeleTracker.git

Utilizzo

TeleTesto.py

    Inviare un messaggio su un canale Telegram: python TeleTexter.py -t TUO_BOT_TOKEN -c ID_CHAT_TARGET -m "Il tuo messaggio"
    Inviare messaggi in loop (spam): python TeleTexter.py -t TUO_BOT_TOKEN -c ID_CHAT_TARGET -m "Il tuo messaggio" --spam

TeleVedi.py

TeleVedi.py è un nuovo strumento che permette di visualizzare e scaricare tutti i messaggi e media da un canale Telegram controllato da una minaccia. Scegli l'opzione 6 dal menù iniziale di TeleGatherer.py per attivarlo. Offre le seguenti possibilità:

    Visualizzare tutti i messaggi sul canale e scaricare tutti i contenuti (foto, video, documenti, ecc.). I contenuti sono scaricati nella cartella 'downloads'.
    Specificare il numero di messaggi da scaricare, dal più nuovo al più vecchio.
    Salvare tutti i testi in due formati: testo leggibile con informazioni di base (.txt) o la lista completa di tutti i messaggi (.json)

Per usare TeleVedi.py, segui questi passaggi:

    Crea un'API Telegram e aggiungi API_hash e API_id nel file .env usando il formato:

    API_ID="XXX"
    API_HASH="XXX"

TeleOttieni.py

    Per raccogliere informazioni da un canale Telegram: python TeleGatherer.py -t TUO_BOT_TOKEN -c ID_CHAT_TARGET

Disclaimer

Utilizza questi strumenti in modo responsabile. Sono destinati esclusivamente a scopi di analisi e ricerca. Assicurati di rispettare tutte le leggi applicabili e i termini di servizio di Telegram.
