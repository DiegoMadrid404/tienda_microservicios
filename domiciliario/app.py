from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///domiciliario.db'
app.config['SECRET_KEY'] = ".*domiciliari0.*"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class domiciliario(db.Model):
    id  = db.Column("domiciliario_id", db.Integer, primary_key=True)
    domiciliario_nombre = db.Column(db.String(100))
    domiciliario_cedula = db.Column(db.String(20))
    domiciliario_telefono = db.Column(db.String(15))

    def __init__(self, datos):
        self.domiciliario_nombre = datos["nombre"]
        self.domiciliario_cedula = datos["cedula"]
        self.domiciliario_telefono = datos["telefono"]

@app.route("/")
@cross_origin()
def principal():
    data = domiciliario.query.all()
    diccionario_domiciliarios = {}
    for d in data:
        p = {"id": d.id,
             "nombre": d.domiciliario_nombre,
             "cedula": d.domiciliario_cedula,
             "telefono": d.domiciliario_telefono
            }
        diccionario_domiciliarios[d.id] = p
    return diccionario_domiciliarios

@app.route("/agregar/<nombre>/<int:cedula>/<int:telefono>")
@cross_origin()
def agregar(nombre, cedula, telefono):
    datos = {"nombre": nombre,
             "cedula": cedula,
             "telefono": telefono
            }
    p = domiciliario(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = domiciliario.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizar/<int:id>/<nombre>/<int:cedula>/<int:telefono>")
@cross_origin()
def actualizar(id, nombre, cedula, telefono):
    p = domiciliario.query.filter_by(id=id).first()
    p.domiciliario_nombre = nombre
    p.domiciliario_cedula = cedula
    p.domiciliario_telefono = telefono
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = domiciliario.query.filter_by(id=id).first()
    p = {"id": d.id,
         "nombre": d.domiciliario_nombre,
         "cedula": d.domiciliario_cedula,
         "telefono": d.domiciliario_telefono
        }
    return p


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
