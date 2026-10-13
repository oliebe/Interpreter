from interfaces import Translator
import argostranslate.package as argospkg
import argostranslate.translate as argostrans
import langcodes

class IArgos(Translator):
	description = "Uses Argos Translate offline machine translation (same engine as the online LibreTranslate service)"
	depends = "argostranslate, langcodes"

	def __init__(self, args):
		self.args = args

	def configure(self):
		# Language.get should do most use cases
		self.language_from = langcodes.Language.get(self.args.src).language
		self.language_to = langcodes.Language.get(self.args.tgt).language

		print("\033[1m Selected source language:\033[0m", self.language_from)
		print("\033[1m Selected target language:\033[0m", self.language_to)

		argospkg.update_package_index()
		if argospkg.install_package_for_language_pair(self.language_from, self.language_to) == False:
			print("\033[1;31m *\033[1;39m Error:\033[0m Package installation failed, continuing anyway")

	def translate(self, string):
		return argostrans.translate(string, self.language_from, self.language_to)

	@staticmethod
	def make_arguments(parser):
		pass
