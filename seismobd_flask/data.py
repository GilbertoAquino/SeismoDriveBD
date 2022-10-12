import main
from datetime import datetime as dt

def consultar_sismos(sismo):
    query = main.Sismo.query.filter_by(fecha=sismo)
    return query

def insertarSismo(latitud, longitud, magnitud, fecha,id_folder):
    insert = main.Sismo()
    insert.latitud = latitud
    insert.longitud = longitud
    insert.magnitud = magnitud
    fechadatetime = dt.strptime(fecha,"%Y-%m-%d")
    insert.fecha = fechadatetime
    insert.id_folder = id_folder
    print("holamundo")
    return insert

def consultaTodoSismo():
    query = main.Sismo.query.order_by(main.Sismo.fecha).all()
    print(query)
    return query