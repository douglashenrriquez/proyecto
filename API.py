from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nac = db.Column(db.Date)
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(15))
    cargo = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    salario = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cargo": self.cargo,
            "ciudad": self.ciudad,
            "departamento": self.departamento,
            "direccion": self.direccion,
            "fecha_nac": str(self.fecha_nac) if self.fecha_nac else None,
            "salario": str(self.salario) if self.salario else None,
            "telefono": self.telefono
        }

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(User, user_id)  # Cambiado aquí
    if user:
        return jsonify({
            "id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "cargo": user.cargo,
            "ciudad": user.ciudad,
            "departamento": user.departamento,
            "direccion": user.direccion,
            "fecha_nac": str(user.fecha_nac) if user.fecha_nac else None,
            "salario": str(user.salario) if user.salario else None,
            "telefono": user.telefono
        }), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos de entrada faltantes"}), 400
    if not data.get('nombre'):
        return jsonify({"error": "Nombre es requerido"}), 400
    if not data.get('telefono'):
        return jsonify({"error": "Teléfono es requerido"}), 400

    new_user = User(
        nombre=data['nombre'],
        apellido=data['apellido'],
        fecha_nac=data.get('fecha_nac'),
        ciudad=data.get('ciudad'),
        direccion=data.get('direccion'),
        telefono=data['telefono'],
        cargo=data.get('cargo'),
        departamento=data.get('departamento'),
        salario=data.get('salario')
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "cargo": user.cargo,
            "ciudad": user.ciudad,
            "departamento": user.departamento,
            "direccion": user.direccion,
            "fecha_nac": str(user.fecha_nac) if user.fecha_nac else None,
            "salario": str(user.salario) if user.salario else None,
            "telefono": user.telefono
        })
    return jsonify(result), 200

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.session.get(User, user_id)  # Cambiado aquí
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "Usuario eliminado correctamente"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
