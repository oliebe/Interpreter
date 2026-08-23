from interfaces import Translator

try:
	from deep_translator import GoogleTranslator
except ImportError:
	print("\033[1mError:\033[0m You do not have deep_translator installed")

class IGoogleTranslator(Translator):
	description = "Uses Google Translate API. Not precise and carries transcription errors on."
	def translate(self, string) -> str:
		return GoogleTranslator(source="auto", target="pt").translate(text=string)

