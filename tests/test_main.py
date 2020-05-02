from unittest import TestCase
from unittest.mock import patch

import main as m


class MainTestCase(TestCase):
    @patch("main.argparse.ArgumentParser")
    def test_should_parse_args(self, mock_argument_parser):
        parser = mock_argument_parser.return_value

        m.main()

        mock_argument_parser.assert_called_once_with()
        parser.add_argument.assert_called_once_with("source_id")
        parser.parse_args.assert_called_once_with()
