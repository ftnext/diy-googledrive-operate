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

    def fetch_file_by_id(self, file_id: str) -> DiyGDriveFile:
        metadata = {"id": file_id}
        gdrive_file = self._drive.CreateFile(metadata)
        return DiyGDriveFile(gdrive_file)

    def copy_file(self, source_id: str, dest_title: str) -> DiyGDriveFile:
        access_to_files = self._drive.auth.service.files()
        metadata = {"title": dest_title}
        request_to_copy = access_to_files.copy(fileId=source_id, body=metadata)
        copied_file_info_dict = request_to_copy.execute()
        return self.fetch_file_by_id(copied_file_info_dict["id"])
