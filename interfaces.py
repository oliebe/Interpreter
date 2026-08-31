from abc import ABC, abstractmethod

class Transcriber(ABC):
	@abstractmethod
	def final_text() -> str:
		pass

	#@abstractmethod
	#def displayTime() -> int:
	#	pass

	@staticmethod
	@abstractmethod
	def make_arguments(parser: ArgumentParser) -> None:
		pass


class Translator(ABC):
	@abstractmethod
	def translate(string) -> str:
		pass

	@staticmethod
	@abstractmethod
	def make_arguments(parser: ArgumentParser) -> None:
		pass


class Player(ABC):
	@abstractmethod
	def connect():
		pass

	def send_text(string, timing):
		pass

	def disconnect():
		pass

	@staticmethod
	@abstractmethod
	def make_arguments(parser: ArgumentParser) -> None:
		pass
