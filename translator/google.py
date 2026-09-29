from interfaces import Translator
from deep_translator import GoogleTranslator

class IGoogleTranslator(Translator):
	description = "Uses Google Translate API. Not precise and carries transcription errors on."
	depends = "deep_translator"

	def __init__(self, args):
		pass

	def translate(self, string):
		return GoogleTranslator(source="auto", target="pt").translate(text=string)

	@staticmethod
	def make_arguments(parser):
		pass
