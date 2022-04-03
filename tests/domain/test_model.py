from unittest import TestCase

import pytest
from mortgage.domain.model import Mortgage, MortgageEP, Calculator


def test_mortgage_model_init():
    mortgage = Mortgage(price=20, initial_payment=2,
                        period=30, loan_rate=7.5)
    assert mortgage.price == 20
    assert mortgage.initial_payment == 2
    assert mortgage.period == 30
    assert mortgage.loan_rate == 7.5
    assert mortgage.MONTH_PER_YEAR == 12
    assert mortgage.MLN_MULTIPLIER == 1000000


def test_mortgage_model_with_early_payment_init():
    mortgage = MortgageEP(price=20, initial_payment=2,
                          period=30, loan_rate=7.5, first_month=24,
                          frequency_months=1, early_payment_amount=50000)
    assert mortgage.price == 20
    assert mortgage.initial_payment == 2
    assert mortgage.period == 30
    assert mortgage.loan_rate == 7.5
    assert mortgage.first_month == 24
    assert mortgage.frequency_months == 1
    assert mortgage.early_payment_amount == 50000


def test_mortgage_to_dict():
    data_dict = {'price': 20,
                 'initial_payment': 2,
                 'period': 30,
                 'loan_rate': 7.5,
                 'month_loan_rate': 0,
                 'total_loan_amount': 0,
                 'common_rate': 0,
                 'monthly_payment': 0,
                 'residual_loan': 0,
                 'monthly_percent_part': 0,
                 'monthly_main_part': 0,
                 'overpayment': 0,
                 'avg_percent_part': 0,
                 'avg_monthly_payment': 0,
                 'additional_payments': 0,
                 'total_period': 0,
                 }
    mortgage = Mortgage(price=20, initial_payment=2,
                        period=30, loan_rate=7.5)
    m_dict = mortgage.to_dict()
    assert data_dict == m_dict
    assert data_dict['price'] == m_dict['price']


def test_mortgage_from_dict():
    data_dict = {'price': 18,
                 'initial_payment': 2.5,
                 'period': 30,
                 'loan_rate': 7.6}
    m = Mortgage.from_dict(data_dict)
    assert m.price == 18
    assert m.to_dict()['price'] == data_dict['price']


def test_mortgage_from_dict_less_data():
    data_dict = {'price': '18',
                 'initial_payment': 2.5,
                 'period': 30}
    with pytest.raises(TypeError):
        m = Mortgage.from_dict(data_dict)


def test_mortgage_from_dict_wrong_data():
    data_dict = {'price': '18',
                 'initial_payment': 2.5,
                 'period': 30,
                 'loan_rate': 7.6}
    m = Mortgage.from_dict(data_dict)
    assert m.price == 18


class TestCalculateCalendar(TestCase):
    def setUp(self) -> None:
        self.data_dict = {'price': 18,
                          'initial_payment': 2.5,
                          'period': 30,
                          'loan_rate': 7.6}
        self.mortgage = Mortgage.from_dict(self.data_dict)
        self.calculator = Calculator(self.mortgage)

    def test_base_builder_init(self):
        self.assertIsInstance(self.calculator, Calculator)
        self.assertEqual(self.data_dict['price'], self.calculator.mortgage.price)
        self.assertEqual(self.data_dict['period'], self.calculator.mortgage.to_dict()['period'])
        self.assertEqual(12, self.mortgage.MONTH_PER_YEAR)
        self.assertEqual(1000000, self.mortgage.MLN_MULTIPLIER)

    # todo: change assert to self.assert
    def test_base_builder_prepare_data(self):
        self.calculator.prepare_data()
        assert self.mortgage.price == self.data_dict['price'] * 1000000
        assert self.mortgage.initial_payment == self.data_dict['initial_payment'] * 1000000
        assert self.mortgage.period == self.data_dict['period'] * 12
        assert isinstance(self.calculator.mortgage.period, int)
        assert self.mortgage.month_loan_rate == self.data_dict['loan_rate'] / 12 / 100
        assert self.mortgage.total_loan_amount == self.data_dict['price'] * 1000000 - self.data_dict[
            'initial_payment'] * 1000000

    def test_base_builder_common_rate(self):
        self.calculator.prepare_data()
        self.calculator.common_rate()

        assert isinstance(self.calculator.mortgage.common_rate, float)
        assert self.mortgage.common_rate == (1 + self.data_dict['loan_rate'] / 12 / 100) ** (
                    self.data_dict['period'] * 12)

    def test_monthly_payment(self):
        self.calculator.prepare_data()
        self.calculator.common_rate()
        self.calculator.monthly_payment()
        expected = (self.data_dict['price'] * 1000000 - self.data_dict['initial_payment'] * 1000000) * \
                   (self.data_dict['loan_rate'] / 12 / 100) * ((1 + self.data_dict['loan_rate'] / 12 / 100) ** (
                    self.data_dict['period'] * 12)) / (((1 + self.data_dict['loan_rate'] / 12 / 100) **
                                                        (self.data_dict['period'] * 12)) - 1)
        self.assertEqual(expected, self.mortgage.monthly_payment)

    def test_first_month_calendar(self):
        self.calculator.prepare_data()
        self.calculator.common_rate()
        self.calculator.monthly_payment()
        self.calculator.residual_loan()
        self.calculator.monthly_percent_part()
        self.calculator.monthly_main_part()
        self.calculator.overpayment()
        self.calculator.calculate_first_month()

        self.assertEqual(int(98166.67), int(self.calculator.calendar.iloc[0][0]))
