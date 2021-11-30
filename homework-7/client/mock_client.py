import socket
import json


import settings


class ApiClient:
    def __init__(self):
        self.target_host = settings.APP_HOST
        self.target_port = int(settings.APP_PORT)
        self.client = None
        self.connect()
        self.url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'

    def connect(self):
        try:
            self.client.close()
        except:
            pass
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(222.5)
        client.connect((self.target_host, self.target_port))
        self.client = client

    def read_data(self):
        total_data = []
        while True:
            # читаем данные из сокета до тех пор пока они там есть
            data = self.client.recv(4096)
            if data:
                print(f'received data: {data}')
                total_data.append(data.decode())
            else:
                break
        print()
        data = ''.join(total_data).splitlines()
        return json.loads(data[-1])

    def sendrecv(self, data):
        res = self.client.send(data.encode())
        response = self.read_data()
        self.connect()
        return response

    def get(self, location):
        data = f"GET {location} HTTP/1.1\r\n" \
               f"Host:{self.target_host}" \
               f"\r\n\r\n"
        return self.sendrecv(data)

    def post(self, location, payload: str, content_type="application/json"):
        data = f'POST {location} HTTP/1.1\r\n' \
               f'Host:{self.target_host}\r\n' \
               f'Content-Type: {content_type}\r\n' \
               f'Content-Length: {len(payload)}\r\n' \
               f'\r\n' \
               f'{payload}' \
               f'\r\n'
        return self.sendrecv(data)

    def put(self, location, payload, content_type="application/json"):
        data = f'PUT {location} HTTP/1.1\r\n' \
               f'Host:{self.target_host}\r\n' \
               f'Content-Type: {content_type}\r\n' \
               f'Content-Length: {len(payload)}\r\n' \
               f'\r\n' \
               f'{payload}' \
               f'\r\n'
        return self.sendrecv(data)

    def delete(self, location):
        data = f"DELETE {location} HTTP/1.1\r\n" \
               f"Host:{self.target_host}" \
               f"\r\n\r\n"
        return self.sendrecv(data)

    def add_card(self, name):
        location = '/card'
        data = json.dumps({"name": name})
        return self.post(location, data)

    def get_card(self, card_id):
        location = f'/card/{card_id}'
        return self.get(location)

    def update_card(self, card_id, name):
        location = f'/card/{card_id}'
        data = json.dumps({"name": name})
        return self.put(location, data)

    def delete_card(self, card_id):
        location = f'/card/{card_id}'
        return self.delete(location)
