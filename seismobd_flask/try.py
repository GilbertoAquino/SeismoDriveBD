from pydrive2.auth import GoogleAuth

def auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return gauth

auth()