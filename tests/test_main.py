from unittest import TestCase
from unittest.mock import MagicMock, patch

import main as m


class MainTestCase(TestCase):
    @patch("main.cp_in_drive")
    @patch("main.argparse.ArgumentParser")
    def test_should_parse_args(self, mock_argument_parser, cp_in_drive):
        parser = mock_argument_parser.return_value
        args = parser.parse_args.return_value

        m.main()

        mock_argument_parser.assert_called_once_with()
        parser.add_argument.assert_called_once_with("source_id")
        parser.parse_args.assert_called_once_with()
        cp_in_drive.assert_called_once_with(args.source_id, "copied")


class CpInDriveTestCase(TestCase):
    @patch("main.create_diy_gdrive")
    def test_should_copy(self, create_diy_gdrive):
        source_id = MagicMock(spec=str)
        dest_title_prefix = MagicMock(spec=str)
        drive = create_diy_gdrive.return_value
        source_file = drive.fetch_file_by_id.return_value
        dest_title = (
            f"{dest_title_prefix}_{source_file.fetch_title.return_value}"
        )
        dest_file = drive.copy_file.return_value

        actual = m.cp_in_drive(source_id, dest_title_prefix)

        create_diy_gdrive.assert_called_once_with()
        drive.fetch_file_by_id.assert_called_once_with(source_id)
        source_file.fetch_title.assert_called_once_with()
        drive.copy_file(source_file, dest_title)
        dest_file.fetch_url.assert_called_once_with()
        self.assertEqual(actual, dest_file.fetch_url.return_value)
