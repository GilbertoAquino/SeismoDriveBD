import driveService as gs
import data
import os
def agregarRegistro(req):
    ruta = req["archivo"]
    sismo = req["fechaSismo"]
    query = data.consultar_sismos(sismo)
    print(query)
    print("test...")
    return True
    #gs.subir_archivo(ruta=ruta)

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

