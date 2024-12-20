from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)


DATA_FILE = 'data.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = {}
        save_data(data)
    return data


def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)


data = load_data()


@app.route('/set', methods=['POST'])
@limiter.limit('10/minute')
def set_key():
    key = request.json.get('key')
    value = request.json.get('value')
    if key and value:
        data[key] = value
        save_data(data)
        return jsonify({'message': 'New data zapisana uspesno)'})
    else:
        return jsonify({'error': 'Vyidi i zaidi normalno'}), 400


@app.route('/get/<key>', methods=['GET'])
@limiter.limit('100/day')
def get_value(key):
    value = data.get(key)
    if value:
        return jsonify({'Znachenie': value})
    else:
        return jsonify({'error': 'Takogo klucha net chel'}), 404


@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit('10/minute')
def delete_key(key):
    if key in data:
        del data[key]
        save_data(data)
        return jsonify({'message': 'Kluch udalili('})
    else:
        return jsonify({'error': 'Takogo klucha net chel'}), 404


@app.route('/exists/<key>', methods=['GET'])
@limiter.limit('100/day')
def key_exists(key):
    exists = key in data
    return jsonify({'Sushestvuet?': exists})


if __name__ == '__main__':
    app.run()
