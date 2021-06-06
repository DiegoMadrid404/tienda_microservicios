from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedido.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)


class pedidos(db.Model):
    id = db.Column("pedido_id", db.Integer, primary_key=True)
    pedido_cantidad = db.Column(db.Integer)
    pedido_valor_total = db.Column(db.Integer)
    pedido_fecha = db.Column(db.String(100))
    pedido_estado = db.Column(db.String(100))
    pedido_domiciliario = db.Column(db.Integer)
    pedido_cliente = db.Column(db.Integer)
    pedido_producto = db.Column(db.Integer)

    def __init__(self, datos):
        self.pedido_cantidad = datos["cantidad"]
        self.pedido_valor_total = datos["valor_total"]
        self.pedido_fecha = datos["fecha"]
        self.pedido_estado = datos["estado"]
        self.pedido_domiciliario = datos["domiciliario"]
        self.pedido_cliente = datos["cliente"]
        self.pedido_producto = datos["producto"]


@app.route("/")
@cross_origin()
def principal():
    data = pedidos.query.all()
    diccionario_pedidos = {}
    for d in data:
        p = {"id": d.id,
             "cantidad": d.pedido_cantidad,
             "valor_total": d.pedido_valor_total,
             "fecha": d.pedido_fecha,
             "estado": d.pedido_estado,
             "domiciliario": d.pedido_domiciliario,
             "cliente": d.pedido_cliente,
             "producto": d.pedido_producto
             }
        diccionario_pedidos[d.id] = p
    return diccionario_pedidos

@app.route("/agregar/<int:cantidad>/<int:valor_total>/<fecha>/<estado>/<int:domiciliario>/<int:cliente>/<int:producto>")
@cross_origin()
def agregar(cantidad, valor_total, fecha, estado, domiciliario, cliente, producto):
    datos = {"cantidad": cantidad,
             "valor_total": valor_total,
             "fecha": fecha,
             "estado": estado,
             "domiciliario": domiciliario,
             "cliente": cliente,
             "producto": producto
             }
    p = pedidos(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = pedidos.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizar/<int:id>/<int:cantidad>/<int:valor_total>/<fecha>/<estado>/<int:domiciliario>/<int:cliente>/<int:producto>")
@cross_origin()
def actualizar(id, cantidad, valor_total, fecha, estado, domiciliario, cliente, producto):
    p = pedidos.query.filter_by(id=id).first()
    p.pedido_cantidad = cantidad
    p.pedido_valor_total = valor_total
    p.pedido_fecha = fecha
    p.pedido_estado = estado
    p.pedido_domiciliario = domiciliario
    p.pedido_cliente = cliente
    p.pedido_producto = producto
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = pedidos.query.filter_by(id=id).first()
    p = {"id": d.id,
         "valor_total": d.valor_total,
         "fecha": d.fecha,
         "estado": d.estado,
         "domiciliario": d.pedido_domiciliario,
         "cliente": d.pedido_cliente,
         "producto": d.pedido_producto
         }
    return p


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
