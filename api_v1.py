from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
app.json.ensure_ascii = False

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="ciel2027"
    )

@app.route('/v1/etudiants/', methods=['GET'])
def getEtudiants():
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM etudiant")
    result = cursor.fetchall()
    
    etudiants = []
    for row in result:
        etudiants.append({
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        })
    
    cursor.close()
    mydb.close()
    return jsonify(etudiants), 200

@app.route('/v1/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    mydb = get_db_connection()
    cursor = mydb.cursor()
    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    cursor.execute(req)
    row = cursor.fetchone()
    
    cursor.close()
    mydb.close()
    
    if row:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        return jsonify(etudiant), 200
    return jsonify({"erreur": "id invalide"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
