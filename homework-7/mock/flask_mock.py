#!/usr/bin/env python3.9

import threading
from wsgiref.simple_server import WSGIRequestHandler
import json
from flask import Flask, jsonify, request
from faker import Faker

import settings

app = Flask(__name__)

CARD_NUMBER = {}


def generate_number():
    fake = Faker()
    return fake.credit_card_number()


@app.route('/number', methods=['POST'])
def create_number():
    card_id = json.loads(request.data)['id']
    if card_id not in CARD_NUMBER:
        CARD_NUMBER[card_id] = generate_number()
        return jsonify(CARD_NUMBER[card_id]), 201
    else:
        return jsonify(f'Card number for {card_id} already exist'), 404


@app.route('/number/<card_id>', methods=['GET'])
def get_number(card_id):
    card_id = int(card_id)
    if CARD_NUMBER.get(card_id):
        return jsonify(CARD_NUMBER[card_id]), 200
    else:
        return jsonify(f'Card number for {card_id} not found'), 404


@app.route('/number/<card_id>', methods=['PUT'])
def update_number(card_id):
    card_id = int(card_id)
    if CARD_NUMBER.get(card_id):
        CARD_NUMBER.update({card_id: generate_number()})
        return jsonify(CARD_NUMBER[card_id]), 200
    else:
        return jsonify(f'Card number for "{card_id}" not found'), 404


@app.route('/number/<card_id>', methods=['DELETE'])
def delete_number(card_id):
    card_id = int(card_id)
    if CARD_NUMBER.get(card_id):
        CARD_NUMBER.pop(card_id)
        return jsonify(f'Card number with id "{card_id}" successfully deleted'), 204
    else:
        return jsonify(f'Card number with id "{card_id}" not found'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    server.start()
    return server