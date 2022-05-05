import json
from flask import Request

from mortgage.domain.model import Mortgage, Calculator, CalculatorBuilder, Chart


def get_calendar(request_data: dict):
    mortgage = Mortgage.from_dict(request_data)
    calculator = Calculator(mortgage)
    cb = CalculatorBuilder(calculator)
    builded_calendar_as_dict = cb.build_calculator()
    chart = Chart(cb.calculator)
    # chart.draw_background()
    builded_calendar_as_dict['chart'] = chart.draw_chart()
    return builded_calendar_as_dict


def serilalize(dictionary: dict) -> json:
    return json.dumps(dictionary, indent=4)


def get_input_data(request: Request) -> dict:
    if len(request.data) > 0:
        input_data = json.loads(request.data)
    elif len(request.args) > 0:
        input_data = request.args.to_dict()
    elif len(request.form) > 0:
        input_data = request.form.to_dict()
    else:
        raise InvalidInputData('No input data provided')
    return input_data


class InvalidInputData(Exception):
    pass
