from interfaces import Translator
from deep_translator import GoogleTranslator

class IGoogleTranslator(Translator):
	description = "Uses Google Translate API. Not precise and carries transcription errors on."
	depends = "deep_translator"

	def __init__(self, args):
		self.args = args
		self.translator = GoogleTranslator(source=self.args.src or "auto", target=self.args.tgt)
		pass

	def translate(self, string):
		return self.translator.translate(text=string)

	@staticmethod
	def make_arguments(parser):
		pass
