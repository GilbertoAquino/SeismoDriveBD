from datetime import datetime
import driveService as gs
import data
import os
import random
import zipfile
import threading

abecedario="abcdefghijklmnopqrstuvwxyz1234567890"

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

def consultarRegistrosPE(req):
    estacion = req["estacion"]
    componente_id = None
    estacionobj = data.consultar_estacion(estacion.upper())
    query = data.consultar_registros_PE(estacionobj[0].id,componente_id)
    if (query == []):
        return False
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

def consultaSismosPorParametros(req):
    print(req)
    try:
        fecha_inicio = datetime.strptime(req["finicio"],"%Y-%m-%d")
        fecha_fin = datetime.strptime(req["ffinal"],"%Y-%m-%d")
    except:
        fecha_inicio=''
        fecha_fin=''
    m_init = req['minicio']
    m_fin=req['mfinal']
    p_init=req['pinicio']
    p_fin=req['pfinal']
    if ((m_init != '' and m_fin != '') or (p_init != '' and p_fin != '')):
        sismos = data.consultar_sismos_parametros(m_init,m_fin,p_init,p_fin)
    else:
        sismos = data.consultaTodoSismo()
    dummy=[]
    if(fecha_inicio != '' and fecha_fin != ''):
        for i in sismos:
            if(i.fecha>fecha_inicio and i.fecha < fecha_fin ):
                dummy.append(i)
        return dummy
    return sismos

def descargaZip(req):
    os.chdir("SeismoDriveBD/seismobd_flask/datos")
    sismo = req["sismo"]
    componente = req["componente"]
    if componente == "all":
        componente_id = None
    else:
        objcomp = data.consultar_componente(componente)
        componente_id = objcomp[0].id
    sismoobj = data.consultar_sismos_por_fecha(sismo)
    query = data.consultar_registros_PS(sismoobj[0].id,componente_id)
    directorio = random_directory()
    registro=[]
    for i in query:
        gs.descarga_archivo(i.id_archivo,directorio)
        registro.append(directorio+"/"+i.registro)
    file = sismo+"-"+componente+".zip"
    with zipfile.ZipFile(file, mode="w") as archive:
        for filename in registro:
            archive.write(filename)
    os.system("rm -r /home/SisMCS/SeismoDriveBD/seismobd_flask/datos/"+directorio)
    os.chdir("../../../")
    t1 = threading.Thread(target=erraze_zip, args=[file])
    t1.start()
    return file

def descargaZipEst(req):
    os.chdir("SeismoDriveBD/seismobd_flask/datos")
    estacion = req["estacion"]
    componente_id = None
    estacionobj = data.consultar_estacion(estacion.upper())
    query = data.consultar_registros_PE(estacionobj[0].id,componente_id)
    directorio = random_directory()
    registro=[]
    if (query == []):
        return False
    for i in query:
        gs.descarga_archivo(i.id_archivo,directorio)
        registro.append(directorio+"/"+i.registro)
    file = estacion+".zip"
    with zipfile.ZipFile(file, mode="w") as archive:
        for filename in registro:
            archive.write(filename)
    os.system("rm -r /home/SisMCS/SeismoDriveBD/seismobd_flask/datos/"+directorio)
    os.chdir("../../../")
    t1 = threading.Thread(target=erraze_zip, args=[file])
    t1.start()
    return file

def erraze_zip(file):
    import time
    time.sleep(10)
    os.system("rm -r /home/SisMCS/SeismoDriveBD/seismobd_flask/datos/"+file)

def random_directory():
    string=""
    for i in range(0,20):
        string+=random.choice(abecedario)
    os.system("mkdir /home/SisMCS/SeismoDriveBD/seismobd_flask/datos/"+string)
    return string