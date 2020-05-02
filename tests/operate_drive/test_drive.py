from unittest import TestCase
from unittest.mock import MagicMock, patch

from operate_drive import drive as d


class CreateGdriveTestCase(TestCase):
    @patch("operate_drive.drive.DiyGoogleDrive")
    @patch("operate_drive.drive.GoogleDrive")
    @patch("operate_drive.drive.auth._authenticate")
    def test_should_create(
        self, authenticate, mock_google_drive, mock_diy_google_drive
    ):
        gauth = authenticate.return_value
        gdrive = mock_google_drive.return_value

        actual = d.create_diy_gdrive()

        authenticate.assert_called_once_with()
        mock_google_drive.assert_called_once_with(gauth)
        mock_diy_google_drive.assert_called_once_with(gdrive)
        self.assertEqual(actual, mock_diy_google_drive.return_value)


class DiyGoogleDriveFetchFileByIdTestCase(TestCase):
    @patch("operate_drive.drive.DiyGDriveFile")
    def test_should_fetch(self, mock_diy_gdrive_file):
        from pydrive2.drive import GoogleDrive

        file_id = MagicMock(spec=str)
        gdrive = MagicMock(spec=GoogleDrive)
        my_drive = d.DiyGoogleDrive(gdrive)
        gdrive_file = gdrive.CreateFile.return_value

        actual = my_drive.fetch_file_by_id(file_id)

        gdrive.CreateFile.assert_called_once_with({"id": file_id})
        mock_diy_gdrive_file.assert_called_once_with(gdrive_file)
        self.assertEqual(actual, mock_diy_gdrive_file.return_value)
