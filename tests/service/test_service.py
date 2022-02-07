from mortgage.domain.model import BaseMortgage
from mortgage.service.calendar_builder import BaseBuilder

data_dict = {'price': 20,
             'initial_payment': 2,
             'period': 30,
             'loan_rate': 7.5}


def test_base_builder_init():
    mortgage_builder = BaseBuilder(data_dict)

    assert isinstance(mortgage_builder, BaseBuilder)
    assert mortgage_builder.calendar.price == data_dict['price']
    assert mortgage_builder.calendar.to_dict()['period'] == data_dict['period']
    assert mortgage_builder.calendar.MONTH_PER_YEAR == 12
    assert mortgage_builder.calendar.MLN_MULTIPLIER == 1000000


def test_base_builder_prepare_data():
    mb = BaseBuilder(data_dict)
    mb.prepare_data()

    assert mb.calendar.price == data_dict['price'] * 1000000
    assert mb.calendar.initial_payment == data_dict['initial_payment'] * 1000000
    assert mb.calendar.period == data_dict['period'] * 12
    assert isinstance(mb.calendar.period, int)
    assert mb.calendar.month_loan_rate == data_dict['loan_rate'] / 12 / 100
    assert mb.calendar.total_loan_amount == data_dict['price'] * 1000000 - data_dict['initial_payment'] * 1000000


def test_base_builder_common_rate():
    mb = BaseBuilder(data_dict)
    mb.prepare_data()
    mb.common_rate()

    assert isinstance(mb.calendar.common_rate, float)
    assert mb.calendar.common_rate == (1 + data_dict['loan_rate'] / 12 / 100) ** (data_dict['period'] * 12)
