from abc import ABC, abstractmethod
from mortgage.domain.model import BaseMortgage, ICalculator, Mortgage, Calculator, CalculatorBuilder


def get_calendar(request_data: dict):
    mortgage = Mortgage.from_dict(request_data)
    calculator = Calculator(mortgage)
    cb = CalculatorBuilder(calculator)
    cb.build_calculator()
    return calculator.calendar
