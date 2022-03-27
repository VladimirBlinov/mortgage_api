import json
from flask import Flask, Response, request
import os
from dotenv import load_dotenv

from mortgage.service import service

load_dotenv()
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def get_calendar():
    request_data = request.json
    calendar = service.get_calendar(request_data)
    return Response(json.dumps(calendar), status=200, mimetype='application/json')


if __name__ == '__main__':
    host = os.getenv("API")
    port = 5005
    app.run(debug=True, host=host, port=port)
