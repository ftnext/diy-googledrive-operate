from __future__ import annotations

from dataclasses import dataclass

from pydrive2.drive import GoogleDrive

from operate_drive import auth
from operate_drive.file import DiyGDriveFile


@dataclass
class DiyGoogleDrive:
    _drive: GoogleDrive

    def fetch_file_by_id(self, file_id: str) -> DiyGDriveFile:
        metadata = {"id": file_id}
        gdrive_file = self._drive.CreateFile(metadata)
        return DiyGDriveFile(gdrive_file)

    def copy_file(
        self, source_id: str, dest_title: str, parent_dir_id: str | None = None
    ) -> DiyGDriveFile:
        if self._drive.auth.service is None:
            self._drive.GetAbout()  # Workaround to set auth (Issue #6)

        access_to_files = self._drive.auth.service.files()
        metadata = {"title": dest_title}
        request_to_copy = access_to_files.copy(
            fileId=source_id, body=metadata, supportsAllDrives=True
        )
        copied_file_info_dict = request_to_copy.execute()
        return self.fetch_file_by_id(copied_file_info_dict["id"])


def create_diy_gdrive() -> DiyGoogleDrive:
    """Return DiyGDriveFile (wrapper of pydrive2.drive.GoogleDrive)

    Example:

        >>> drive = create_diy_gdrive()

        >>> # return DiyGDriveFile
        >>> file = drive.fetch_file_by_id("file_id")

        >>> # copy a specified file as DiyGDriveFile
        >>> drive.copy_file("source_id", "dest_title")

    DiyGDriveFile is a wrapper of pydrive2.files.GoogleDriveFile

        >>> # fetch specified metadata from Drive API and return
        >>> file.fetch_title()

    supported metadata as `fetch_xxx` are title and alternateLink currently.
    ref: https://developers.google.com/drive/api/v2/reference/files

    """
    gauth = auth._authenticate()
    gdrive = GoogleDrive(gauth)
    return DiyGoogleDrive(gdrive)
