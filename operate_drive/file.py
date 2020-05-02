from dataclasses import dataclass

from pydrive2.files import GoogleDriveFile


@dataclass
class DiyGDriveFile:
    _file: GoogleDriveFile

    def fetch_title(self):
        self._file.FetchMetadata("title")
        return self._file["title"]

    def fetch_url(self):
        self._file.FetchMetadata("alternateLink")
        return self._file["alternateLink"]
