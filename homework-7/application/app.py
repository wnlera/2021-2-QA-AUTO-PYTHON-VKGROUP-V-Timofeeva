#!/usr/bin/env python3.9

import json
import os
from wsgiref.simple_server import WSGIRequestHandler

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

app_data = {}
card_id_seq = 0

number_host = os.environ.get('NUMBER_HOST', "127.0.0.1")
number_port = os.environ.get('NUMBER_PORT', "8082")


@app.route('/card', methods=['POST'])
def create_card():
    global card_id_seq
    card_name = json.loads(request.data)['name']
    card_id_seq += 1
    if card_id_seq not in app_data:
        app_data[card_id_seq] = card_name

        number = None
        try:
            response = requests.post(f'http://{number_host}:{number_port}/number',
                                     json={"id": card_id_seq})
            if response.status_code == 201:
                number = response.json()
            else:
                print(f'Card number for {card_id_seq} already exist')
        except Exception as e:
            print(f'Unable to get number from external system:\n{e}')

        data = {"id": card_id_seq,
                "name": card_name,
                "number": number
                }

        return jsonify(data), 200
    else:
        return jsonify(f'Card with {card_id_seq} already exist'), 404


@app.route('/card/<card_id>', methods=['GET'])
def get_card_name_by_id(card_id):
    print(app_data)
    card_id = int(card_id)
    if card_id in app_data:
        number = None
        try:
            response = requests.get(f'http://{number_host}:{number_port}/number/{card_id}')
            if response.status_code == 200:
                number = response.json()
            else:
                print(f'No number found for card {card_id}')
        except Exception as e:
            print(f'Unable to get number from external system:\n{e}')

        data = {'id': card_id,
                "name": app_data[card_id],
                "number": number
                }

        return jsonify(data), 200
    else:
        return jsonify(f'Card {card_id} not found'), 404


@app.route('/card/<card_id>', methods=['PUT'])
def update_card_by_id(card_id):
    card_id = int(card_id)
    if card_id := app_data.get(card_id):
        name = json.loads(request.data)["name"]
        app_data.update({card_id: name})
        number = None
        try:
            response = requests.put(f'http://{number_host}:{number_port}/number/{card_id}')
            if response.status_code == 200:
                number = response.json()
            else:
                print(f'No numbers found for card {card_id}')
        except Exception as e:
            print(f'Unable to get number from external system:\n{e}')

        data = {'id': card_id,
                "name": app_data[card_id],
                "number": number
                }

        return jsonify(data), 200
    else:
        return jsonify(f'Card {card_id} not found'), 404


@app.route('/card/<card_id>', methods=['DELETE'])
def delete_card_by_id(card_id):
    card_id = int(card_id)
    if app_data.get(card_id):
        number_host = os.environ['NUMBER_HOST']
        number_port = os.environ['NUMBER_PORT']
        try:
            response = requests.delete(f'http://{number_host}:{number_port}/number/{card_id}')
            if response.status_code == 204:
                return jsonify(f'Card with id "{card_id}" successfully deleted'), 200
            else:
                print(f'No surname found for user {card_id}')
        except Exception as e:
            print(f'Unable to get surname from external system 2:\n{e}')

    else:
        return jsonify(f'Card with id {card_id} not found'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '8080')

    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host, port)
