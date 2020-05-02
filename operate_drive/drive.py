from dataclasses import dataclass

from pydrive2.drive import GoogleDrive

from operate_drive import auth
from operate_drive.file import DiyGDriveFile


def create_diy_gdrive():
    gauth = auth._authenticate()
    gdrive = GoogleDrive(gauth)
    return DiyGoogleDrive(gdrive)


@dataclass
class DiyGoogleDrive:
    _drive: GoogleDrive

    def fetch_file_by_id(self, file_id):
        metadata = {"id": file_id}
        gdrive_file = self._drive.CreateFile(metadata)
        return DiyGDriveFile(gdrive_file)
