import json
import unittest
from unittest import TestCase
import requests

from mortgage.config import get_api_url

INPUT_DATA = {'price': 18,
              'initial_payment': 2.5,
              'period': 30,
              'loan_rate': 7.6}

INPUT_PARAMS = '/?price=18&initial_payment=2.5&period=30&loan_rate=7.6'


class TestCalendarWithParamsInURL(TestCase):
    def setUp(self) -> None:
        self.url = get_api_url() + INPUT_PARAMS
        self.session = requests.Session()

    def test_api_request_return_status_code_200(self):
        self.r = self.session.get(self.url)
        self.assertEqual(200, self.r.status_code)


class TestCalendar(TestCase):
    def setUp(self) -> None:
        self.url = get_api_url()
        self.input_data = json.dumps(INPUT_DATA)
        self.session = requests.Session()
        # self.session.headers.update({'Content-Type': 'application/json'})

    def test_get_api_url_return_api_link(self):
        self.assertEqual(f'http://127.0.0.1:5005', self.url)

    def test_api_request_return_status_code_200(self):
        self.r = self.session.post(self.url, data=self.input_data)
        self.assertEqual(200, self.r.status_code)

    def test_api_request_return_data(self):
        self.r = self.session.post(self.url, data=self.input_data)
        self.assertIsInstance(json.loads(self.r.text), (dict,))
        print(self.r.text)

    def test_api_calendar_is_in_returned_data(self):
        self.r = self.session.post(self.url, data=self.input_data)
        response_dict = json.loads(self.r.text)
        self.assertIn('1', response_dict)


if __name__ == '__main__':
    unittest.main()
