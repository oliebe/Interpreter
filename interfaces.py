from abc import ABC, abstractmethod

class Transcriber(ABC):
	@abstractmethod
	def finalText() -> str:
		pass
	#@abstractmethod
	#def displayTime() -> int:
	#	pass

class Translator(ABC):
	@abstractmethod
	def translate(string) -> str:
		pass

class Player(ABC):
	@abstractmethod
	def connect():
		pass
	def send_text(string, timing):
		pass
	def disconnect():
		pass
