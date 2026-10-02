from abc import ABC, abstractmethod

class Transcriber(ABC):
	def __init__(self, args):
		self.args = args

	def configure(self):
		pass

	@abstractmethod
	def final_text() -> str:
		pass

	#@abstractmethod
	#def displayTime() -> int:
	#	pass

	@staticmethod
	def make_arguments(parser: ArgumentParser) -> None:
		pass


class Translator(ABC):
	def __init__(self, args):
		self.args = args

	def configure(self):
		pass

	@abstractmethod
	def translate(string) -> str:
		pass

	@staticmethod
	def make_arguments(parser: ArgumentParser) -> None:
		pass


class Player(ABC):
	def __init__(self, args):
		self.args = args

	def configure(self):
		pass

	def connect(self):
		pass

	@abstractmethod
	def send_text(self, string, timing):
		pass

	def disconnect(self):
		pass

	@staticmethod
	def make_arguments(parser: ArgumentParser) -> None:
		pass
