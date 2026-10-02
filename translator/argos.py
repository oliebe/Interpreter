from interfaces import Translator
import argostranslate.package as argospkg
import argostranslate.translate as argostrans

class IArgos(Translator):
	description = "Uses Argos Translate offline machine translation (same engine as the online LibreTranslate service)"
	depends = "argostranslate"

	def __init__(self, args):
		self.args = args

	def configure(self):
		self.language_from = self.args.src
		self.language_to = self.args.tgt

		argospkg.update_package_index()
		# Uses ISO 639 language codes, might want to do treatment with langcodes
		argospkg.install_package_for_language_pair(self.language_from, self.language_to)

	def translate(self, string):
		return argostrans.translate(string, self.language_from, self.language_to)

	@staticmethod
	def make_arguments(parser):
		pass
