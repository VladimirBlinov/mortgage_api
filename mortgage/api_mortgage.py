import json

from flask import Flask, Response, request
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def get_base_calendar():
    request_data = request.json
    response_data = request_data
    return Response(json.dumps(response_data), status=200, mimetype='application/json')


if __name__ == '__main__':
    host = os.getenv("API")
    port = 5005
    app.run(debug=True, host=host, port=port)
