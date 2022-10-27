import driveService as gs
import data
import os

def agregarRegistro(req):
    ruta = req["archivo"]
    sismo = req["fechaSismo"]
    estacion = req["estacion"]
    objest = data.consultar_estacion(estacion)
    if (objest == []):
        return False
    componente = req["componente"]
    objcomp = data.consultar_componente(componente)
    if (objcomp == []):
        return False
    sismo = data.consultar_sismos_por_fecha(sismo)
    reg = data.consultar_registro_detallado(sismo[0].id,objest[0].id,objcomp[0].id)
    if (reg != []):
        print("registro existente",reg)
        return False
    registro = ruta.split("/")[-1]
    if (len(sismo) > 1):
        return False
    try:
        id_archivo = gs.subir_archivo(ruta=ruta, id_folder=sismo[0].id_folder)
        insert = data.insertarRegistro(registro,objest[0].id,objcomp[0].id,sismo[0].id,id_archivo)
    except:
        print("Fallo al insertar o subirc")
        return False
    return insert

def agregarEstaciones(req):
    try:
        nombre = req["nombre"]
    except:
        nombre = req["clave"]
    clave = req["clave"]
    objest = data.consultar_estacion(clave)
    if (objest != []):
        return False
    latitud = req["latitud"]
    longitud = req["longitud"]
    instituto = req["instituto"]
    if (instituto.lower() == "instituto"):
        instituto = "II"
    elif (instituto == "CIRES,"):
        instituto = "CIRES"
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
    hora = req["hora"]
    fecha = fecha +"T"+hora
    profundidad = req["profundidad"]
    try:
        l= gs.consultar_directorio(fecha)
    except:
        os.system("rm credentials_module.json")
        gs.auth()
        l=gs.consultar_directorio(fecha)
    if len(l) == 0:
        id_folder = gs.crear_folder(fecha)
        print(id_folder)
        sismo = data.insertarSismo(latitud, longitud, magnitud, fecha,hora,profundidad,id_folder)
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
    response = []
    for i in query:
        #gs.descarga_archivo(i.id_archivo)
        dummy = {}
        estacion = data.consultar_estacion_porID(i.estacion_id)
        comp = data.consultar_componente_porID(i.componente_id)
        sismo = data.consultar_sismo_porID(i.sismo_id)
        dummy["link"] = "https://drive.google.com/uc?export=download&id="+i.id_archivo
        dummy["estacion"] = estacion.clave
        dummy["componente"] = comp.componente
        dummy["sismo"] = sismo.fecha
        response.append(dummy)
    return response
