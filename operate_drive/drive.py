from dataclasses import dataclass

from pydrive2.drive import GoogleDrive

from operate_drive import auth


def create_diy_gdrive():
    gauth = auth._authenticate()
    gdrive = GoogleDrive(gauth)
    return DiyGoogleDrive(gdrive)


@dataclass
class DiyGoogleDrive:
    drive: GoogleDrive
