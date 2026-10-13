from interfaces import Translator
from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator
from langcodes import closest_match

class IDeepTranslator(Translator):
	description = "Uses deep-translator package. Includes options for free online machine translation, but can commit many translation errors."
	depends = "deep-translator, langcodes"

	def __init__(self, args):
		self.args = args

	def configure(self):
		match self.args.tls:
			case "mymemory":
				print("\033[1m Using MyMemory Translator\033[0m")

				langs_dict = MyMemoryTranslator(source="auto", target="en-GB").get_supported_languages(as_dict=True)
				languages = list(langs_dict.values())

				self.language_from = closest_match(self.args.src, languages)[0]
				self.language_to = closest_match(self.args.tgt, languages)[0]
				print("\033[1m Selected source language:\033[0m", self.language_from)
				print("\033[1m Selected target language:\033[0m", self.language_to)
				self.translator = MyMemoryTranslator(source=self.language_from or "auto", target=self.language_to)

			case _: # google
				print("\033[1m Using Google Translator\033[0m")
				langs_dict = GoogleTranslator(source="auto", target="en").get_supported_languages(as_dict=True)
				languages = list(langs_dict.values())

				self.language_from = closest_match(self.args.src, languages)[0]
				self.language_to = closest_match(self.args.tgt, languages)[0]
				print("\033[1m Selected source language:\033[0m", self.language_from)
				print("\033[1m Selected target language:\033[0m", self.language_to)
				self.translator = GoogleTranslator(source=self.language_from or "auto", target=self.language_to)



	def translate(self, string):
		return self.translator.translate(text=string)

	@staticmethod
	def make_arguments(parser):
		parser.add_argument("-tls",
					  help="DeepTranslator: The service to do translation (available options: google, mymemory)")
