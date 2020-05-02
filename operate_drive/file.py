from dataclasses import dataclass

from pydrive2.files import GoogleDriveFile


@dataclass
class DiyGDriveFile:
    _file: GoogleDriveFile
