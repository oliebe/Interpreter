from interfaces import Player

class TerminalPlayer(Player):
	description = "Send text to the terminal Interpreter was called from."
	def __init__(self, args):
		self.args = args

	def connect():
		return

	def disconnect():
		return

	def send_text(self, string):
		print(string)

	@staticmethod
	def make_arguments(parser):
		return
