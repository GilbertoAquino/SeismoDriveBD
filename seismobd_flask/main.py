from enum import unique
from sqlalchemy import true
from flask import Flask,jsonify,make_response,request,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import driveService as gs
import services
import data
import os
import flask_praetorian

app = Flask(__name__,
            static_url_path='/datos', 
            static_folder='./datos')
db_name = "seismobd.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config["SECRET_KEY"] = "top secret"
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 1}
app.config["JWT_REFRESH_LIFESPAN"] = {"hours": 12}
db=SQLAlchemy(app)
migrate = Migrate(app,db,render_as_batch=True)
guard = flask_praetorian.Praetorian()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Initialize the flask-praetorian instance for the app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active

guard.init_app(app, User)

@app.route("/",methods=["GET"])
@flask_praetorian.auth_required
def hello_world():
    response = make_response(jsonify({"resultado":"ok"}))
    return response

@app.route("/agregarRegistro",methods=["POST"])
@flask_praetorian.auth_required
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
@flask_praetorian.auth_required
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

@app.route("/consultarTodoSismos",methods=["GET"])
@flask_praetorian.auth_required
@cross_origin()
def consultaSis():
    response = data.consultaTodoSismo()
    return make_response(jsonify(Sismos=[i.serialize for i in response]))

@app.route("/agregarInstituto",methods=["POST"])
@flask_praetorian.auth_required
def agregaInstituto():
    req = request.get_json(silent=True)
    response = services.agregarInstitutos(req)
    db.session.add(response)
    db.session.commit()
    return make_response(jsonify({"resultado":"ok"}))

@app.route("/agregarEstacion",methods=["POST"])
@flask_praetorian.auth_required
def agregarEstacion():
    req = request.get_json(silent=True)
    response = services.agregarEstaciones(req)
    if(response == False):
        return make_response(jsonify({"resultado":"bad request"}))
    db.session.add(response)
    db.session.commit()
    return make_response(jsonify({"resultado":"ok"}))

@app.route("/consultarRegistrosPorSismo",methods=["POST"])
@flask_praetorian.auth_required
def consultaRegistros():
    req = request.get_json(silent=True)
    response = services.consultarRegistrosPS(req)
    return make_response(jsonify(response))

@app.route("/consultarRegistrosPorEstacion",methods=["POST"])
@flask_praetorian.auth_required
def consultaRegistrosEstacion():
    req = request.get_json(silent=True)
    response = services.consultarRegistrosPE(req)
    return make_response(jsonify(response))

@app.route("/consultarSismosParametros",methods=["POST"])
@flask_praetorian.auth_required
def consultaSismosPorParametros():
    req = request.get_json(silent=True)
    response = services.consultaSismosPorParametros(req)
    return make_response(jsonify(Sismos=[i.serialize for i in response]))

@app.route("/descargaZip",methods=["POST"])
@flask_praetorian.auth_required
def descargaz():
    req = request.get_json(silent=True)
    response = services.descargaZip(req)
    return make_response(jsonify({"link":"http://localhost:5000/"+response}))

@app.route("/descargaZipEst",methods=["POST"])
@flask_praetorian.auth_required
def descargaze():
    req = request.get_json(silent=True)
    response = services.descargaZipEst(req)
    return make_response(jsonify({"link":"http://localhost:5000/"+response}))
    #return make_response(jsonify(Sismos=[i.serialize for i in response]))

@app.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    username = req.get("username", None)
    password = req.get("password", None)
    user = guard.authenticate(username, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    return (jsonify(ret), 200)

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
    return value.strftime("%Y-%m-%d %H:%M:%S")

class Sismo(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    profundidad = db.Column(db.Float)
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
           'magnitud':self.magnitud,
           'profundidad':self.profundidad
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