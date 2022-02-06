import pytest
from mortgage.domain.model import Mortgage, MortgageEP


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
    data_dict = {'price': 20,
                 'initial_payment': 2,
                 'period': 30,
                 'loan_rate': 7.5}
    m = Mortgage.from_dict(data_dict)
    assert m.price == 20
    assert m.to_dict()['price'] == data_dict['price']


def test_mortgage_from_dict_less_data():
    data_dict = {'price': '20',
                 'initial_payment': 2,
                 'period': 30}
    with pytest.raises(TypeError):
        m = Mortgage.from_dict(data_dict)


def test_mortgage_from_dict_wrong_data():
    data_dict = {'price': '20',
                 'initial_payment': 2,
                 'period': 30,
                 'loan_rate': 7.5}
    m = Mortgage.from_dict(data_dict)
    assert m.price == 20

