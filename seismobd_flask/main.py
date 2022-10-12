from sqlalchemy import true
from flask import Flask,jsonify,make_response,request
from flask_sqlalchemy import SQLAlchemy
import driveService as gs
import services
import data

app = Flask(__name__)
db_name = "seismobd.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name  
db=SQLAlchemy(app)

@app.route("/",methods=["GET"])
def hello_world():
    #g = servicios.auth()
    response = make_response(jsonify({"resultado":"ok"}))
    return response

@app.route("/consultar", methods=["POST"])
def consultarDatos():
    req = request.get_json(silent=True)
    res = gs.consultar_documentos("title='"+req["estacion"]+"'")
    response =make_response(jsonify(res))
    return response

@app.route("/agregarRegistro",methods=["POST"])
def agregarReg():
    req = request.get_json(silent=True)
    res = services.agregarRegistro(req)
    if (res):
        response = make_response(jsonify({"resultado":"ok"}))
    else:
        response = make_response(jsonify({"resultado":"bad request"}))
    return response

@app.route("/agregarSismo",methods=["POST"])
def agregaSis():
    req = request.get_json(silent=True)
    res = services.agregarSismo(req)
    if (res == False):
        response = make_response(jsonify({"resultado":"bad request"}))
        return response
    db.session.add(res)
    print("testo")
    db.session.commit()
    print("loko")
    response = make_response(jsonify({"resultado":"ok"}))
    return response

@app.route("/consultarSismos",methods=["GET"])
def consultaSis():
    response = data.consultaTodoSismo()
    return make_response(jsonify(Sismos=[i.serialize for i in response]))

class Componente(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    componente = db.Column(db.String(10))
    registros = db.relationship('Registro', backref='componente')

class Instituto(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    estaciones = db.relationship('Estacion', backref='instituto')

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")

class Sismo(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    magnitud = db.Column(db.Float)
    fecha = db.Column(db.DateTime)
    id_folder = db.Column(db.String(200))
    registros = db.relationship('Registro', backref='sismo')
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'fecha': dump_datetime(self.fecha),
           'latitud':self.latitud,
           'longitud':self.longitud,
           'magnitud':self.magnitud
       }

class Estacion(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    clave = db.Column(db.String(10))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    instituto_id = db.Column(db.Integer, db.ForeignKey('instituto.id'))
    registros = db.relationship('Registro', backref='estacion')

class Registro(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    estacion_id = db.Column(db.Integer, db.ForeignKey('estacion.id'))
    componente_id = db.Column(db.Integer, db.ForeignKey('componente.id')) 
    sismo_id = db.Column(db.Integer, db.ForeignKey('sismo.id'))
    registro = db.Column(db.String(100))
