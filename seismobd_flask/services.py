import driveService as gs
import data
import os

def agregarRegistro(req):
    ruta = req["archivo"]
    sismo = req["fechaSismo"]
    estacion = req["estacion"]
    objest = data.consultar_estacion(estacion)
    componente = req["componente"]
    objcomp = data.consultar_componente(componente)
    query = data.consultar_sismos_por_fecha(sismo)
    registro = ruta.split("/")[-1]
    if (len(query) > 1):
        return False
    try:
        id_archivo = gs.subir_archivo(ruta=ruta, id_folder=query[0].id_folder)
        insert = data.insertarRegistro(registro,objest[0].id,objcomp[0].id,query[0].id,id_archivo)
    except:
        return False
    return insert

def agregarEstaciones(req):
    try:
        nombre = req["nombre"]
    except:
        nombre = req["clave"]
    clave = req["clave"]
    latitud = req["latitud"]
    longitud = req["longitud"]
    instituto = req["instituto"]
    ObjInsti = data.consultar_instituto(instituto)
    insert = data.agregarEstacion(nombre,clave,latitud,longitud,ObjInsti)
    return insert

def agregarInstitutos(req):
    nombre = req["nombre"]
    clave = req["clave"]
    insert = data.agregarInsti(nombre,clave)
    return insert

def agregarSismo(req):
    latitud = req["latitud"]
    longitud = req["longitud"]
    magnitud = req["magnitud"]
    fecha = req["fecha"]
    try:
        l= gs.consultar_directorio(fecha)
    except:
        os.system("rm credentials_module.json")
        gs.auth()
        l=gs.consultar_directorio(fecha)
    if len(l) == 0:
        id_folder = gs.crear_folder(fecha)
        print(id_folder)
        sismo = data.insertarSismo(latitud, longitud, magnitud, fecha,id_folder)
    else:
        return False
    return sismo

def consultarRegistrosPS(req):
    sismo = req["sismo"]
    componente = req["componente"]
    if componente == "all":
        componente_id = None
    else:
        objcomp = data.consultar_componente(componente)
        componente_id = objcomp[0].id
    sismoobj = data.consultar_sismos_por_fecha(sismo)
    query = data.consultar_registros_PS(sismoobj[0].id,componente_id)
    for i in query:
        gs.descarga_archivo(i.id_archivo)
    return None
