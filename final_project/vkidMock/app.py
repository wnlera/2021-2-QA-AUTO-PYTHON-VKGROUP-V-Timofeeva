import random
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

vk_id ={"testtest": "123456"}

@app.route('/vk_id/<username>', methods=['GET'])
def get_id(username):  # put application's code here
    app.logger.info("="*160)
    app.logger.info(f"This from {request.remote_addr} \/")
    h = "\n".join(map(str, request.headers.items()))
    app.logger.info(f"This headers:\/\n {h} \n\/")

    if vk_id.get(username):
        return {"vk_id": vk_id[username]}, 200
    else:
        return {}, 404

@app.route('/vk_id/create', methods=['POST'])
def create_id():  # put application's code here
    app.logger.info("="*160)
    app.logger.info(f"This from {request.remote_addr} \/")
    h = "\n".join(map(str, request.headers.items()))
    app.logger.info(f"This headers:\/\n {h} \n\/")

    username = json.loads(request.data)['username']
    if username not in vk_id:
        vk_id[username] = random.randint(10**10,10**12)
        return jsonify(vk_id[username]), 201
    else:
        return jsonify(f'Vk id for {username} already exist'), 404


if __name__ == '__main__':
    print("Mock OK2")
    app.run(debug=True, port=5001, host="0.0.0.0")
