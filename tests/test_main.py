from unittest import TestCase
from unittest.mock import call, MagicMock, patch

from operate_drive.drive import DiyGoogleDrive

import main as m


class MainTestCase(TestCase):
    @patch("builtins.print")
    @patch("main.display_information")
    @patch("main.cp_in_drive")
    @patch("main.parse_args")
    def test_should_parse_args(
        self, parse_args, cp_in_drive, display_information, mock_print,
    ):
        args = parse_args.return_value
        dest_file = cp_in_drive.return_value
        info = display_information.return_value

        m.main()

        parse_args.assert_called_once_with()
        cp_in_drive.assert_called_once_with(args.source_id, args.dest_title)
        display_information.assert_called_once_with(dest_file)
        mock_print.assert_called_once_with(info)


class ParseArgsTestCase(TestCase):
    @patch("main.argparse.ArgumentParser")
    def test_should_parse(self, mock_argument_parser):
        parser = mock_argument_parser.return_value

        actual = m.parse_args()

        mock_argument_parser.assert_called_once_with()
        parser.add_argument.assert_has_calls(
            [call("source_id"), call("--dest_title")]
        )
        parser.parse_args.assert_called_once_with()
        self.assertEqual(actual, parser.parse_args.return_value)


class CpInDriveTestCase(TestCase):
    @patch("main.build_dest_title")
    @patch("main.create_diy_gdrive")
    def test_should_copy(self, create_diy_gdrive, build_dest_title):
        source_id = MagicMock(spec=str)
        drive = create_diy_gdrive.return_value
        dest_title = build_dest_title.return_value

        actual = m.cp_in_drive(source_id)

        create_diy_gdrive.assert_called_once_with()
        build_dest_title.assert_called_once_with(drive, source_id)
        drive.copy_file.assert_called_once_with(source_id, dest_title)
        self.assertEqual(actual, drive.copy_file.return_value)


class BuildDestTitleTestCase(TestCase):
    @patch("main.title_of_copy_dest")
    def test_should_return_title(self, title_of_copy_dest):
        drive = MagicMock(spec=DiyGoogleDrive)
        source_id = MagicMock(spec=str)
        source = drive.fetch_file_by_id.return_value
        source_title = source.fetch_title.return_value

        actual = m.build_dest_title(drive, source_id)

        drive.fetch_file_by_id.assert_called_once_with(source_id)
        source.fetch_title.assert_called_once_with()
        title_of_copy_dest.assert_called_once_with(source_title)
        self.assertEqual(actual, title_of_copy_dest.return_value)


class TitleOfCopyDestTestCase(TestCase):
    def test_should_return_title(self):
        source_title = MagicMock(spec=str)

        actual = m.title_of_copy_dest(source_title)

        self.assertEqual(actual, f"copied_{source_title}")


class DisplayInformationTestCase(TestCase):
    def test_should_return_information(self):
        from operate_drive.file import DiyGDriveFile

        gdrive_file = MagicMock(spec=DiyGDriveFile)
        url = gdrive_file.fetch_url.return_value

        actual = m.display_information(gdrive_file)

        gdrive_file.fetch_url.assert_called_once_with()
        self.assertEqual(actual, f"コピーされました: {url}")
