from interfaces import Translator
from groq import Groq
import langcodes

class IGroq(Translator):
	#TODO: stream text
	description = "Uses Groq LLM models for translation. Can infer transcription errors and fixes grammar. Needs an API key."
	depends = "groq, langcodes[data]"

	def __init__(self, args):
		self.args = args

	def configure(self):
		self.language_from = langcodes.Language.get(self.args.src).display_name()
		self.language_to = langcodes.Language.get(self.args.tgt).display_name()
		self.messages = [
			  {
				"role": "system",
				"content": "You are a speech interpreter. You will receive unclean strings of text in language \'" + self.language_from + "\' and must fix transcribing errors and grammar, being aware of the given context in previous prompts. After that, you shall translate the text to language \'" + self.language_to + "\' and output only the final translated text."
			  }
			]
		self.client = Groq()

	def translate(self, string):
		self.messages.append({"role": "user", "content": string})

		if len(self.messages) > 6:
			self.messages.pop(1)
			self.messages.pop(1)

		completion = self.client.chat.completions.create(
			model="openai/gpt-oss-120b",
			messages=self.messages,
			temperature=1,
			max_completion_tokens=2048,
			top_p=1,
			reasoning_effort="medium",
			stream=False,
			stop=None
		)

		self.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
		return completion.choices[0].message.content

	@staticmethod
	def make_arguments(parser):
		pass

