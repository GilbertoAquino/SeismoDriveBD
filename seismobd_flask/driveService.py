from xml.dom import ValidationErr
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import data

credenciales= "credentials_module.json"
id_folder = "1Y_Cf3xBnjqcJPyDvgLyNaW5sbtRy02eF"

def auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return gauth

def subir_archivo(ruta,id_folder):
    response = True
    try:
        gd = login()
        archivo = gd.CreateFile({'parents':[{'kind':"drive#fileLink", "id":id_folder}]})
        archivo['title'] = ruta.split("/")[-1]
        archivo.SetContentFile(ruta)
        archivo.Upload()
    except:
        response = False
    return response

def crear_folder(nombre_carpeta):
    gd=login()
    folder = gd.CreateFile({"title":nombre_carpeta, "mimeType":"application/vnd.google-apps.folder",
                        "parents":[{"kind":"drive#fileLink","id":id_folder}]})
    folder.Upload()
    dir = consultar_directorio(nombre_carpeta)
    response = dir[0]["id"]
    return response

def consultar_documentos(nombre):
    resultado=[]
    gd=login()
    lista_archivos = gd.ListFile({'q': nombre}).GetList()
    for i in lista_archivos:
        dic = {"Estacion": i["title"]}
        resultado.append(dic)
    return lista_archivos

def consultar_directorio(nombre):
    gd=login()
    query = "title='"+nombre+"'"
    lista_archivos = gd.ListFile({'q': query}).GetList()
    if len(lista_archivos) > 1:
        raise ValueError("Se retorno mas de un directorio, revisar nombres.")
    return lista_archivos

def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credenciales)
    if gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    return GoogleDrive(gauth)
    