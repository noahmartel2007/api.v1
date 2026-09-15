from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)
app.json.ensure_ascii = False

db = Database()

@app.route('/v3/etudiants/', methods=['GET'])
def get_etudiants():
    etudiants = db.get_all_etudiants()
    return jsonify(etudiants), 200

@app.route('/v3/etudiants/<int:id>', methods=['GET'])
def get_etudiant(id):
    etudiant = db.get_etudiant_by_id(id)
    if etudiant:
        return jsonify(etudiant), 200
    return jsonify({"erreur": "Étudiant non trouvé"}), 404

# Route /login/ en POST
@app.route('/v3/login/', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({"erreur": "Veuillez fournir un login et un mot de passe"}), 400
        
    login_input = data.get('login')
    password_input = data.get('password')
    
    user = db.verify_user(login_input, password_input)
    
    if user:
        return jsonify({"message": "Connexion réussie", "user": user['login']}), 200
    else:
        return jsonify({"erreur": "Identifiants incorrects"}), 401

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)