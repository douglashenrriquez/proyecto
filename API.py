from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "telefono": self.telefono}

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos de entrada faltantes"}), 400

    if not data.get('name'):
        return jsonify({"error": "Nombre es requerido"}), 400
    if not data.get('telefono'):
        return jsonify({"error": "Teléfono es requerido"}), 400

    new_user = User(name=data['name'], telefono=data['telefono'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


#-----------------------------------------------ELIMINAR USUARIOS POR ID-----------------#
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "Usuario eliminado correctamente"}), 200

#------------------------------------------------------------------------------------------#


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
