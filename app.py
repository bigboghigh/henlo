from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import time
import json

app = Flask(__name__)
CORS(app)

@app.route('/add/coins.php', methods=['GET', 'POST', 'OPTIONS'])
def handle_request():
    if request.method == 'OPTIONS':  # Handling OPTIONS request
        headers = {
            'Access-Control-Allow-Origin': '*',  # Adjust as needed
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    if request.method == 'POST':
        key = request.json.get('key')
        token = request.json.get('token')
        number = request.json.get('number')

        if key is None or token is None or number is None:
            return jsonify({"error": "Missing parameters"}), 400

        try:
            number = int(number)
        except ValueError:
            return jsonify({"error": "Invalid number parameter"}), 400

        url = 'http://abtalkapi.oneway-tech.com/credits/v3/ad/reward'

        headers = {
            'version': '167465',
            'token': token,
            'deviceid': key,
            'content-type': 'application/json; charset=UTF-8',
        }

        data = {
            "requestTime": 1702555980794,
            "sign": "TKyQ1b8oydBSd8wPxhUqFM4Vcc2IIXHT1PePm55ms1CvU3UvDtMHDS0d2OUHg/QN9u6vLd09qW1sQPiWfc6PjOVNkAyvJGp95S8t8TLDBJeQCgYXadkWJRjk0yPLeQE59hByKlIifzDMwCzcKzifG5m+WPLzIhW5kLYzcm+Y0g96gougnjpC3SSvEkDg9GiyQYeYoqTZ42nKZj2tkVb4fX8xP3Za2qnNU4gyhBQTOnVUlohqm2FZQrdfj7D+D0nndXtnZJ9XUlY0mChpBqzWbWx6ymqjBrjSseuWfzKOgmRwpeL0PzCwevgkWM3qeyJ/R8btUt/FR9XliSFt0FP2hw==",
            "creditAmount": 999,
            "projectId": "DT_2022102902",
        }

        while True:
            try:
                response = requests.post(url, json=data, headers=headers)
                response_json = response.json()
                credit_amount = response_json.get('data', {}).get('creditsAmount')
                if credit_amount is not None and credit_amount >= number:
                    return jsonify({"message": "done"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            time.sleep(15)

    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
