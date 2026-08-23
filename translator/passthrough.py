from interfaces import Translator

class IPassthrough(Translator):
	description = "Does not do translation, returns the text unaltered"
	def translate(self, string):
		return string
