import driveService as gs
import data
def agregarRegistro(req):
    ruta = req["archivo"]
    sismo = req["fechaSismo"]

    gs.subir_archivo()

def agregarSismo(req):
    latitud = req["latitud"]
    longitud = req["longitud"]
    magnitud = req["magnitud"]
    fecha = req["fecha"]
    try:
        print("test")
        l= gs.consultar_directorio(fecha)
        print("test!!!!!")
    except:
        print("test2")
        gs.auth()
        l=gs.consultar_directorio(fecha)
    if len(l) == 0:
        id_folder = gs.crear_folder(fecha)
        print(id_folder)
        sismo = data.insertarSismo(latitud, longitud, magnitud, fecha,id_folder)
    else:
        return False
    return sismo

