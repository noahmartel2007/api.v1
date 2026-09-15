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

# GET - Récupérer tous les étudiants
@app.route('/v2/etudiants/', methods=['GET'])
def get_etudiants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM etudiant")
    etudiants = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(etudiants), 200

# GET - Récupérer un étudiant par son ID
@app.route('/v2/etudiants/<int:id>', methods=['GET'])
def get_etudiant(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM etudiant WHERE idetudiant = %s", (id,))
    etudiant = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if etudiant:
        return jsonify(etudiant), 200
    return jsonify({"erreur": "Étudiant non trouvé"}), 404

# POST - Ajouter un nouvel étudiant
@app.route('/v2/etudiants/', methods=['POST'])
def add_etudiant():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO etudiant (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)"
    values = (data.get('nom'), data.get('prenom'), data.get('email'), data.get('telephone'))
    
    cursor.execute(query, values)
    conn.commit()
    new_id = cursor.lastrowid
    
    cursor.close()
    conn.close()
    return jsonify({"message": "Étudiant créé avec succès", "idetudiant": new_id}), 201

# PUT - Modifier un étudiant existant
@app.route('/v2/etudiants/<int:id>', methods=['PUT'])
def update_etudiant(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE etudiant SET nom = %s, prenom = %s, email = %s, telephone = %s WHERE idetudiant = %s"
    values = (data.get('nom'), data.get('prenom'), data.get('email'), data.get('telephone'), id)
    
    cursor.execute(query, values)
    conn.commit()
    
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    
    if affected > 0:
        return jsonify({"message": "Étudiant mis à jour"}), 200
    return jsonify({"erreur": "Étudiant non trouvé"}), 404

# DELETE - Supprimer un étudiant
@app.route('/v2/etudiants/<int:id>', methods=['DELETE'])
def delete_etudiant(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM etudiant WHERE idetudiant = %s", (id,))
    conn.commit()
    
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    
    if affected > 0:
        return jsonify({"message": "Étudiant supprimé"}), 200
    return jsonify({"erreur": "Étudiant non trouvé"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)