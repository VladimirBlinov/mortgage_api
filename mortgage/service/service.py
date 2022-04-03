import json

import pandas as pd
from flask import Request

from mortgage.domain.model import BaseMortgage, ICalculator, Mortgage, Calculator, CalculatorBuilder


def get_calendar(request_data: dict):
    mortgage = Mortgage.from_dict(request_data)
    calculator = Calculator(mortgage)
    cb = CalculatorBuilder(calculator)
    builded_calendar = cb.build_calculator()
    builded_calendar_as_dict = builded_calendar.to_dict('index')
    return builded_calendar_as_dict


def serilalize(dictionary: dict) -> json:
    return json.dumps(dictionary, indent=4)


def get_input_data(request: Request) -> dict:
    input_data = {}
    if len(request.data) > 0:
        input_data = json.loads(request.data)
    elif len(request.args) > 0:
        input_data = request.args.to_dict()
    else:
        raise InvalidInputData('No input data provided')
    return input_data


class InvalidInputData(Exception):
    pass
