from enum import unique
from sqlalchemy import true
from flask import Flask,jsonify,make_response,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import driveService as gs
import services
import data
import os

app = Flask(__name__,
            static_url_path='/datos', 
            static_folder='./datos')
db_name = "seismobd.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name  
db=SQLAlchemy(app)
migrate = Migrate(app,db,render_as_batch=True)

@app.route("/",methods=["GET"])
def hello_world():
    #g = servicios.auth()
    db.create_all()
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
    if (res==False):
        response = make_response(jsonify({"resultado":"bad request"}))
    else:
        db.session.add(res)
        db.session.commit()
        response = make_response(jsonify({"resultado":"ok"}))
    return response

@app.route("/agregarSismo",methods=["POST"])
def agregaSis():
    req = request.get_json(silent=True)
    res = services.agregarSismo(req)
    if (res == False):
        response = make_response(jsonify({"resultado":"bad request"}))
        return response
    db.session.add(res)
    db.session.commit()
    response = make_response(jsonify({"resultado":"ok"}))
    return response

@app.route("/consultarSismos",methods=["GET"])
def consultaSis():
    response = data.consultaTodoSismo()
    return make_response(jsonify(Sismos=[i.serialize for i in response]))

@app.route("/agregarInstituto",methods=["POST"])
def agregaInstituto():
    req = request.get_json(silent=True)
    response = services.agregarInstitutos(req)
    print(response)
    db.session.add(response)
    db.session.commit()
    return make_response(jsonify({"resultado":"ok"}))

@app.route("/agregarEstacion",methods=["POST"])
def agregarEstacion():
    req = request.get_json(silent=True)
    response = services.agregarEstaciones(req)
    print(response)
    db.session.add(response)
    db.session.commit()
    return make_response(jsonify({"resultado":"ok"}))

@app.route("/consultarRegistrosPorSismo",methods=["POST"])
def consultaRegistros():
    req = request.get_json(silent=True)
    os.system("rm ./datos/*")
    response = services.consultarRegistrosPS(req)
    return make_response(jsonify({"resultado":"ok"}))

###########################################################################
#MODELS#
###########################################################################

class Componente(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    componente = db.Column(db.String(10))
    registros = db.relationship('Registro', backref='componente')

class Instituto(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    clave = db.Column(db.String(8))
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

    def __str__(self):
        return "id: {}, fecha: {}, magnitud: {}".format(self.id,self.fecha,self.magnitud)
    
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
    id_archivo = db.Column(db.String(100))
