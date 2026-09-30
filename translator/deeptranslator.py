from interfaces import Translator
from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator

class IDeepTranslator(Translator):
	description = "Uses deep-translator package. Includes options for free online machine translation, but can commit many translation errors."
	depends = "deep-translator"

	def __init__(self, args):
		self.args = args

	def configure(self):
		match self.args.tls:
			case "mymemory":
				print("\033[1m Using MyMemory Translator\033[0m")
				self.translator = MyMemoryTranslator(source=self.args.src or "auto", target=self.args.tgt)
			case _: # google
				print("\033[1m Using Google Translator\033[0m")
				self.translator = GoogleTranslator(source=self.args.src or "auto", target=self.args.tgt)



	def translate(self, string):
		return self.translator.translate(text=string)

	@staticmethod
	def make_arguments(parser):
		parser.add_argument("-tls",
					  help="DeepTranslator: The service to do translation (available options: google, mymemory)")
