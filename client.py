#! python3

import argparse
import socketio
import json

import asyncio

parser = argparse.ArgumentParser(description="client example")
parser.add_argument('--user_id')

args = parser.parse_args()
user_id = args.user_id

sio = socketio.Client()

print(user_id)
exit()


@sio.on("connect")
def connect():
	pass

@sio.on("validated")
def validated(message):
	sio.emit("listen", key)

@sio.on("message")
def listen_message(message):
	print("[Message] >>", message)

@sio.on("disconnect")
def disconnect():
	pass

sio.connect("ws://localhost:5000")
sio.wait()

