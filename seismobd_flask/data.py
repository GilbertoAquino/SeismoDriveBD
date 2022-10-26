import main
from datetime import datetime as dt

def consultar_sismos_por_fecha(sismo):
    fsismo = dt.strptime(sismo,"%Y-%m-%d")
    query = main.Sismo.query.filter_by(fecha=fsismo).all()
    return query

def consultar_registros_PS(sismo_id,componente_id):
    if (componente_id == None):
        query = main.Registro.query.filter_by(sismo_id=sismo_id).all()
    else:
        query = main.Registro.query.filter_by(sismo_id=sismo_id,componente_id=componente_id).all()
    return query

def consultar_instituto(clave):
    query = main.Instituto.query.filter_by(clave =clave).all()
    return query[0]

def consultar_componente(comp=None):
    if comp == None:
        query = main.Componente.query.all()
        for i in query:
            print(i)
    else:
        query = main.Componente.query.filter_by(componente=comp).all()
    return query

def consultar_estacion(comp=None):
    if comp == None:
        query = main.Estacion.query.all()
        for i in query:
            print(i)
    else:
        query = main.Estacion.query.filter_by(clave=comp).all()
    return query

def insertarSismo(latitud, longitud, magnitud, fecha,id_folder):
    insert = main.Sismo()
    insert.latitud = latitud
    insert.longitud = longitud
    insert.magnitud = magnitud
    fechadatetime = dt.strptime(fecha,"%Y-%m-%d")
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
    print(query)
    return query
