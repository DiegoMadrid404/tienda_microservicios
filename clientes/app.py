from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class clientes(db.Model):
    id  = db.Column("cliente_id", db.Integer, primary_key=True)
    clientes_nombre = db.Column(db.String(100))
    clientes_cedula = db.Column(db.Integer)
    clientes_direccion = db.Column(db.String(100))

    def __init__(self, datos):
        self.clientes_nombre = datos["nombre"]
        self.clientes_cedula = datos["cedula"]
        self.clientes_direccion = datos["direccion"]

@app.route("/")
@cross_origin()
def principal():
    data = clientes.query.all()
    diccionario_clientes = {}
    for d in data:
        p = {"id": d.id,
             "nombre": d.clientes_nombre,
             "cedula": d.clientes_cedula,
             "direccion": d.clientes_direccion
            }
        diccionario_clientes[d.id] = p
    return diccionario_clientes

@app.route("/agregar/<nombre>/<int:cedula>/<direccion>")
@cross_origin()
def agregar(nombre, cedula, direccion):
    datos = {"nombre": nombre,
             "cedula": cedula,
             "direccion": direccion
            }
    p = clientes(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = clientes.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizar/<int:id>/<nombre>/<int:cedula>/<direccion>")
@cross_origin()
def actualizar(id,nombre, cedula, direccion):
    p = clientes.query.filter_by(id=id).first()
    p.clientes_nombre = nombre
    p.clientes_cedula = cedula
    p.clientes_direccion = direccion
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = clientes.query.filter_by(id=id).first()
    p = {"id": d.id,
         "nombre": d.clientes_nombre,
         "cedula": d.clientes_cedula,
         "direccion": d.clientes_direccion
        }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
