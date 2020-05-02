from unittest import TestCase
from unittest.mock import patch

from operate_drive import auth as a


class AuthenticateTestCase(TestCase):
    @patch("operate_drive.auth.GoogleAuth")
    def test_should_authenticate(self, mock_google_auth):
        gauth = mock_google_auth.return_value

        actual = a._authenticate()

        mock_google_auth.assert_called_once_with()
        gauth.LocalWebserverAuth.assert_called_once_with()
        self.assertEqual(actual, gauth)
