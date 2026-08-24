from interfaces import Translator
from groq import Groq

class IGroq(Translator):
	description = "Uses Groq models for translation. Fine-tuned for transcription error correction and grammar fixing. Needs an API key."
	depends = "groq"

	def __init__(self):
		self.client = Groq()
		self.messages = [
			  {
				"role": "system",
				"content": "You are a speech interpreter. You will receive unclean strings of text and must fix transcribing errors and grammar, being aware of the given context in previous prompts. After that, you shall translate the text to Brazilian Portuguese and output the final translated text."
			  }
			]
	def translate(self, string):
		self.messages.append({"role": "user", "content": string})
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
		return completion.choices[0].message.content
	#TODO: stream text
	#TODO: input rotation and backfeeding the ai output
