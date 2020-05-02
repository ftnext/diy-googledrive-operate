from unittest import TestCase
from unittest.mock import patch

from operate_drive import drive as d


class CreateGdriveTestCase(TestCase):
    @patch("operate_drive.drive.DiyGoogleDrive")
    @patch("operate_drive.drive.GoogleDrive")
    @patch("operate_drive.drive.auth._authenticate")
    def test_should_create(
        self, authenticate, mock_google_drive, diy_google_drive
    ):
        gauth = authenticate.return_value
        gdrive = mock_google_drive.return_value

        actual = d.create_diy_gdrive()

        authenticate.assert_called_once_with()
        mock_google_drive.assert_called_once_with(gauth)
        diy_google_drive.assert_called_once_with(gdrive)
        self.assertEqual(actual, diy_google_drive.return_value)
