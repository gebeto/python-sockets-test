#! python3

from urllib.request import urlopen, Request
from urllib.parse import urlencode
from pprint import pprint
import socketio
import json

import asyncio


CREDENTIALS_GET_URL = "http://localhost:8080/credentials.json"
CLIENT_MESSAGE_SEND = "http://httpbin.org/post"

KS = "KSKSKSKSKSKSKSKKS"
POSTMAN_TOKEN = "POSTMAN_TOKEN"


def send_request(url, data=None, headers={}):
	request = Request(
		url,
		method="POST",
		data=json.dumps(data).encode() if data else None,
		headers={
			"Content-Type": "application/json",
			"Postman-Token": POSTMAN_TOKEN,
			**headers
		},
	)
	return urlopen(request).read()

def get_connection_credentials():
	response = send_request(
		CREDENTIALS_GET_URL,
		data={
			"apiVersion": "asd",
			"ks": KS,
			"identifier": "asd",
			"type": "system",
		},
		headers={}
	)
	credentials = json.loads(response)
	return credentials["result"]["url"], credentials["result"]["key"]


async def listen_for_announcement(url, key):
	sio = socketio.Client()

	@sio.on("connect")
	def connect():
		pass

	@sio.on("validated")
	def validated(message):
		sio.emit("listen", key)

	@sio.on("message")
	def listen_message(message):
		print(message)
		send_message_to_client(message)

	@sio.on("disconnect")
	def disconnect():
		pass

	sio.connect(url)
	sio.wait()


def send_message_to_client(message):
	response = send_request(
		CLIENT_MESSAGE_SEND,
		data={
			"message": message,
		},
		headers={}
	)
	print(response)


url, key = get_connection_credentials()

asyncio.get_event_loop().run_until_complete(
	listen_for_announcement(url, key)
)
