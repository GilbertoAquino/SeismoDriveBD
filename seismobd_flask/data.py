import main
from datetime import datetime as dt
from time import time as tt

def consultar_sismos_por_fecha(sismo):
    fsismo = dt.strptime(sismo,"%Y-%m-%d").date()
    query = main.Sismo.query.all()
    dummy = []
    for i in query:
        if i.fecha.date() == fsismo:
            dummy.append(i)
    return dummy

def consultar_registros_PS(sismo_id,componente_id):
    if (componente_id == None):
        query = main.Registro.query.filter_by(sismo_id=sismo_id).order_by(main.Registro.registro).all()
    else:
        query = main.Registro.query.filter_by(sismo_id=sismo_id,componente_id=componente_id).all()
    return query

def consultar_registros_PE(estacion_id,componente_id):
    if (componente_id == None):
        query = main.Registro.query.filter_by(estacion_id=estacion_id).order_by(main.Registro.sismo_id).all()
    else:
        query = main.Registro.query.filter_by(sismo_id=estacion_id,componente_id=componente_id).all()
    return query

def consultar_registro_detallado(sismo_id,estacion_id,componente_id):
    query = main.Registro.query.filter_by(sismo_id=sismo_id,componente_id=componente_id,estacion_id=estacion_id).all()
    return query

def consultar_instituto(clave):
    query = main.Instituto.query.filter_by(clave =clave).all()
    return query[0]

def consultar_componente(comp=None):
    if comp == None:
        query = main.Componente.query.all()
    else:
        query = main.Componente.query.filter_by(componente=comp).all()
    return query

def consultar_estacion(comp=None):
    if comp == None:
        query = main.Estacion.query.all()
    else:
        query = main.Estacion.query.filter_by(clave=comp).all()
    return query

def consultar_estacion_porID(id):
    query = main.Estacion.query.filter_by(id=id).all()
    return query[0]

def consultar_componente_porID(id):
    query = main.Componente.query.filter_by(id=id).all()
    return query[0]

def consultar_sismo_porID(id):
    query = main.Sismo.query.filter_by(id=id).all()
    return query[0]

def insertarSismo(latitud, longitud, magnitud, fecha,hora,profundidad,id_folder):
    insert = main.Sismo()
    insert.latitud = latitud
    insert.longitud = longitud
    insert.magnitud = magnitud
    fechadatetime = dt.strptime(fecha,"%Y-%m-%dT%H:%M:%S")
    insert.profundidad = profundidad
    insert.fecha = fechadatetime
    insert.id_folder = id_folder
    return insert

def agregarInsti(nombre,clave):
    insert = main.Instituto()
    insert.nombre = nombre
    insert.clave = clave
    return insert

def agregarEstacion(nombre,clave,lat,lon,objinsti):
    insert = main.Estacion()
    insert.nombre = nombre
    insert.clave = clave
    insert.latitud = lat
    insert.longitud = lon
    insert.instituto_id = objinsti.id
    return insert

def agregarUsuario(user,hashpass):
    try:
        insert = main.User()
        insert.username = user
        insert.hashed_password = hashpass
        insert.roles = "Usuario"
        return insert
    except:
        return False

def insertarRegistro(registro,est_id,comp_id,sismo_id,id_a):
    insert = main.Registro()
    insert.registro = registro
    insert.estacion_id = est_id
    insert.componente_id = comp_id
    insert.sismo_id = sismo_id
    insert.id_archivo = id_a
    return insert

def consultaTodoSismo():
    query = main.Sismo.query.order_by(main.Sismo.fecha).all()
    return query

def consultar_sismos_parametros(m1,m2,p1,p2):
    if (m1 == '' or m2 == ''):
        query = main.Sismo.query.filter(main.Sismo.profundidad>=p1, main.Sismo.profundidad<=p2).order_by(main.Sismo.fecha).all()
    elif (p1 == '' or p2 == ''):
        query = main.Sismo.query.filter(main.Sismo.magnitud>=m1, main.Sismo.magnitud<=m2).order_by(main.Sismo.fecha).all()
    else:
        query = main.Sismo.query.filter(main.Sismo.profundidad>=p1, main.Sismo.profundidad<=p2,main.Sismo.magnitud>=m1, main.Sismo.magnitud<=m2).order_by(main.Sismo.fecha).all()
    return query