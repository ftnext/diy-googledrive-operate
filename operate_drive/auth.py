from pydrive2.auth import GoogleAuth


def _authenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return gauth
