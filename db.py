import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'user': 'extern_user',
            'password': 'bt5@c13l972',
            'database': 'ciel2027'
        }

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    # Méthodes pour les étudiants
    def get_all_etudiants(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etudiant")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def get_etudiant_by_id(self, id_etudiant):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etudiant WHERE idetudiant = %s", (id_etudiant,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    # Méthode d'authentification pour la v3
    def verify_user(self, login, password):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE login = %s AND password = %s", (login, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user