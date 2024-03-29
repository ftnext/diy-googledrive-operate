from typing import Callable
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pydrive2.drive import GoogleDrive

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
        file_id = MagicMock(spec=str)
        gdrive = MagicMock(spec=GoogleDrive)
        a_drive = d.DiyGoogleDrive(gdrive)
        gdrive_file = gdrive.CreateFile.return_value

        actual = a_drive.fetch_file_by_id(file_id)

        gdrive.CreateFile.assert_called_once_with({"id": file_id})
        mock_diy_gdrive_file.assert_called_once_with(gdrive_file)
        self.assertEqual(actual, mock_diy_gdrive_file.return_value)


@patch("operate_drive.drive.DiyGoogleDrive.fetch_file_by_id")
class DiyGoogleDriveCopyFileTestCase(TestCase):
    def setUp(self):
        self.source_id = MagicMock(spec=str)
        self.dest_title = MagicMock(spec=str)
        # mockにauthプロパティを持たせるためにインスタンス化して渡している
        self.gdrive = MagicMock(spec=GoogleDrive())
        self.a_drive = d.DiyGoogleDrive(self.gdrive)

    def test_should_copy(self, fetch_file_by_id):
        access_to_files = self.gdrive.auth.service.files.return_value
        request_to_copy = access_to_files.copy.return_value
        copied_file_info_dict = request_to_copy.execute.return_value

        actual = self.a_drive.copy_file(self.source_id, self.dest_title)

        self.gdrive.auth.service.files.assert_called_once_with()
        access_to_files.copy.assert_called_once_with(
            fileId=self.source_id,
            body={"title": self.dest_title},
            supportsAllDrives=True,
        )
        request_to_copy.execute.assert_called_once_with()
        fetch_file_by_id.assert_called_once_with(copied_file_info_dict["id"])
        self.assertEqual(actual, fetch_file_by_id.return_value)

    def test_when_auth_service_is_none(self, fetch_file_by_id):
        self.gdrive.auth.service = None
        call_count_get_about = 0

        # Noneだったservice属性をGetAboutメソッドが書き換える副作用をモックで表現した
        def mocked_get_about(files_mock):
            from googleapiclient.discovery import Resource

            def wrapper():
                nonlocal call_count_get_about
                m = MagicMock(spec=Resource)
                m.files = files_mock
                self.gdrive.auth.service = m
                call_count_get_about += 1

            return wrapper

        files_mock = MagicMock(spec=Callable)
        access_to_files = files_mock.return_value
        self.gdrive.GetAbout = mocked_get_about(files_mock)

        request_to_copy = access_to_files.copy.return_value
        copied_file_info_dict = request_to_copy.execute.return_value

        actual = self.a_drive.copy_file(self.source_id, self.dest_title)

        # GetAbout.assert_called_once_with() 相当の検証
        self.assertEqual(call_count_get_about, 1)
        files_mock.assert_called_once_with()
        access_to_files.copy.assert_called_once_with(
            fileId=self.source_id,
            body={"title": self.dest_title},
            supportsAllDrives=True,
        )
        request_to_copy.execute.assert_called_once_with()
        fetch_file_by_id.assert_called_once_with(copied_file_info_dict["id"])
        self.assertEqual(actual, fetch_file_by_id.return_value)

    def test_should_copy_under_specified_dir(self, fetch_file_by_id):
        access_to_files = self.gdrive.auth.service.files.return_value
        request_to_copy = access_to_files.copy.return_value
        copied_file_info_dict = request_to_copy.execute.return_value
        # bool(MagicMock(spec=str)) は False のため、実の文字列を使う
        parent_dir_id = "1K##############################d"
        metadata = {
            "title": self.dest_title,
            "parents": [{"id": parent_dir_id}],
        }

        actual = self.a_drive.copy_file(
            self.source_id, self.dest_title, parent_dir_id
        )

        self.gdrive.auth.service.files.assert_called_once_with()
        access_to_files.copy.assert_called_once_with(
            fileId=self.source_id, body=metadata, supportsAllDrives=True
        )
        request_to_copy.execute.assert_called_once_with()
        fetch_file_by_id.assert_called_once_with(copied_file_info_dict["id"])
        self.assertEqual(actual, fetch_file_by_id.return_value)
