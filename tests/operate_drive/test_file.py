from unittest import TestCase
from unittest.mock import MagicMock

from pydrive2.files import GoogleDriveFile

from operate_drive import file as f


class DiyGDriveFileFetchTitleTestCase(TestCase):
    def test_should_fetch(self):
        gdrive_file = MagicMock(spec=GoogleDriveFile)
        a_file = f.DiyGDriveFile(gdrive_file)

        actual = a_file.fetch_title()

        gdrive_file.FetchMetadata.assert_called_once_with("title")
        self.assertEqual(actual, gdrive_file["title"])


class DiyGDriveFileFetchURLTestCase(TestCase):
    """check that a URL to access from a browser can be fetched"""

    def test_should_fetch(self):
        gdrive_file = MagicMock(spec=GoogleDriveFile)
        a_file = f.DiyGDriveFile(gdrive_file)

        actual = a_file.fetch_url()

        gdrive_file.FetchMetadata.assert_called_once_with("alternateLink")
        self.assertEqual(actual, gdrive_file["alternateLink"])
