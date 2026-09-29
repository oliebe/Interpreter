from interfaces import Translator

class IPassthrough(Translator):
	description = "Does not do translation, returns the text unaltered"

	def __init__(self, args):
		pass

	def translate(self, string):
		return string

	@staticmethod
	def make_arguments(parser):
		pass
