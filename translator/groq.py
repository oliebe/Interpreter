from interfaces import Translator
from groq import Groq

class IGroq(Translator):
	#TODO: stream text
	description = "Uses Groq models for translation. Fine-tuned for transcription error correction and grammar fixing. Needs an API key."
	depends = "groq"

	def __init__(self, args):
		self.client = Groq()
		self.args = args
		self.language = self.args.tll or "Brazilian Portuguese"
		self.messages = [
			  {
				"role": "system",
				"content": "You are a speech interpreter. You will receive unclean strings of text and must fix transcribing errors and grammar, being aware of the given context in previous prompts. After that, you shall translate the text to " + self.language + " and output only the final translated text."
			  }
			]

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
		parser.add_argument("-tll", help="Groq: Change the translation language. i.e. 'English', 'Spanish', 'Brazilian Portuguese'")

