from flask import Flask, Response, request
import os
from dotenv import load_dotenv

from mortgage.service import service


load_dotenv()
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def get_calendar():
    try:
        request_data = service.get_input_data(request)
        request_data = service.clean_input_data(request_data)
    except service.InvalidInputData as ex:
        return Response("No input data", status=400, mimetype='text/html')
    calendar = service.get_calendar(request_data)
    calendar_as_json = service.serilalize(calendar)
    return Response(calendar_as_json, status=200, mimetype='application/json')


if __name__ == '__main__':
    host = os.getenv("API")
    port = 5005
    app.run(debug=True, host=host, port=port)
