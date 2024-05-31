# Flask Food Guessing Game

## Descrizione

Il progetto "Flask Food Guessing Game" è un'applicazione web sviluppata in Python utilizzando il framework Flask. L'applicazione permette agli utenti di effettuare il login e partecipare a un gioco in cui devono indovinare dei cibi mostrati in modo casuale per ottenere un punteggio. Gli utenti hanno tre vite e un tempo massimo di 5 minuti per completare il gioco. È inoltre possibile visualizzare una classifica con i punteggi di tutti gli utenti.

## Funzionalità

- **Registrazione e Login**: Gli utenti possono registrarsi e accedere all'applicazione.
- **Gioco di Indovinelli**: Gli utenti devono indovinare dei cibi mostrati casualmente.
  - Ogni risposta corretta vale 50 punti.
  - Ogni risposta errata costa 25 punti e una vita.
  - Ogni utente ha a disposizione tre vite.
  - Il gioco ha un limite di tempo di 5 minuti per utente.
- **Classifica**: Gli utenti possono visualizzare una classifica con i punteggi di tutti i giocatori.

## Struttura del Progetto

- `app.py`: Il file principale dell'applicazione Flask.
- `routes.py`: Definisce le route dell'applicazione.
- `templates/`: Contiene i file HTML per le pagine dell'applicazione.
- `static/`: Contiene i file statici come CSS, immagini e JS.
- `__init__.py`: Il file principale dell'applicazione Flask e contiene configurazioni dell'applicazione, incluse le impostazioni del database.

## Requisiti

- Python 3.0
- Flask



## Installazione

1. Clonare il repository:
    ```bash
    git clone https://github.com/tuo-username/flask-food-guessing-game.git
    cd flask-food-guessing-game
    ```

2. Creare un ambiente virtuale:
    ```bash
    python -m venv venv
    source venv/bin/activate # Su Windows usare `venv\Scripts\activate`
    ```

3. Installare le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```

4. Configurare il database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Eseguire l'applicazione:
    ```bash
    flask run
    ```

## Utilizzo

1. Aprire il browser e navigare verso `http://127.0.0.1:5000/`.
2. Registrarsi o effettuare il login.
3. Iniziare a giocare indovinando i cibi mostrati.
4. Visualizzare la classifica per confrontare i propri punteggi con quelli degli altri utenti.

## Contributi

Sono benvenuti contributi di qualsiasi tipo. Per favore, apri una issue o una pull request per discutere i cambiamenti che vorresti apportare.

## Licenza

Questo progetto è sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per maggiori dettagli.

---

Per ulteriori informazioni, contattaci all'indirizzo email: mp@flaskfoodgame.com