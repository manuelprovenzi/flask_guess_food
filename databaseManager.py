import sqlite3
from user import User

class DatabaseManager:
    def __init__(self,app):
        
        self.app = app
        
        # Connessione al database (creazione se non esiste)
        self.conn = sqlite3.connect('db_food.db',check_same_thread=False)
        # Creazione di un cursore
        self.cursor = self.conn.cursor()
        # Creazione di una tabella
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            email VARCHAR(50),
            punteggio INTEGER DEFAULT 0
        )
        ''')

        # Salva (commit) le modifiche
        self.conn.commit()
    
    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        rows = self.cursor.fetchall()
        return rows
    
    def register_user(self, name, username, password, email):
        query = f'''
        INSERT INTO users (name, username, password, email)
        VALUES ('{name}', '{username}', '{password}', '{email}')
        '''
        self.cursor.execute(query)
        self.conn.commit()
        return self.get_user_id(username, password)
        
    def get_user_id(self, username,password):
        query = f'''
        SELECT id FROM users WHERE username = '{username}' and password = '{password}'
        '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][0]
    
    def get_all_users(self):
        query = f'''
        SELECT * FROM users
        '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        users=[]
        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4], row[5])
            users.append(user)
        return users
    
    def update_user_score(self, id, punteggio):
        query = f'''
        UPDATE users SET punteggio = punteggio+'{punteggio}' WHERE id = {id}
        '''
        self.cursor.execute(query)
        self.conn.commit()