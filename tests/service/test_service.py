from unittest import TestCase

from mortgage.service import service


class TestServiceGetCalendar(TestCase):
    def setUp(self) -> None:
        self.request_data = {'price': 20,
                             'initial_payment': 2,
                             'period': 30,
                             'loan_rate': 7.5}
        self.calendar = service.get_calendar(self.request_data)

    def test_service_get_calendar_return_dict(self):
        self.assertIsInstance(self.calendar, dict)

    def test_service_get_calendar_dict_is_not_empty(self):
        self.assertTrue(bool(self.calendar))
