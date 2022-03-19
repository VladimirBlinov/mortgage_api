import unittest
from unittest import TestCase

from mortgage.config import get_api_url


class TestBaseCalendar(TestCase):
    def setUp(self) -> None:
        self.api = get_api_url()

    def test_get_api_url_return_api_link(self):
        self.assertEqual(f'http://127.0.0.1:5005', self.api)


if __name__ == '__main__':
    unittest.main()
