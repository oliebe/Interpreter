from interfaces import Player
import socket
import json

class MPVPlayer(Player):
	description = "Send text to mpv screen. Mpv needs to already be running with an open socket."
	depends = "mpv"
	def __init__(self, ipc_path="/tmp/mpvsocket"):
		self.ipc_path = ipc_path
		self.sock = None
	
	def connect(self):
		self.sock = socket.socket(socket.AF_UNIX)
		self.sock.connect(self.ipc_path)

	def send_text(self, string, timing=4000):
		cmd = { "command": ["show_text", string, timing] }
		print(json.dumps(cmd).encode())
		self.sock.sendall(json.dumps(cmd).encode() + b"\n")

	def disconnect(self):
		self.sock.close()
