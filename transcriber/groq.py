from interfaces import Transcriber
import sounddevice as sd
import queue
from groq import Groq
import webrtcvad
import wave
import langcodes
import tempfile

class GroqTranscriber(Transcriber):
	description = "Groq online STT Whisper models."
	depends = "groq, webrtcvad-wheels, sounddevice, langcodes"

	def __init__(self, args):
		self.args = args
		self.sample_rate = 16000
		self.audio_queue = queue.Queue()
		self.device = sd.default.device
		self.filename = tempfile.gettempdir() + "/interpreter-chunk.wav"

	def configure(self):
		self.source_choose()
		self.language = langcodes.Language.get(self.args.src).language
		print("\033[1m Selected language:\033[0m", self.language)
		self.client = Groq()
		self.vad = webrtcvad.Vad(self.args.tc_vadlevel)

	def audio_callback(self, indata, frames, time_info, status):
		self.audio_queue.put(bytes(indata))

	def final_text(self):
		self.stream = sd.RawInputStream(
			samplerate=self.sample_rate,
			blocksize=1024,
			dtype='int16',
			channels=1,
			callback=self.audio_callback
		)

		self.write_audio()
		return self.upload_audio()

	def write_audio(self):
		with self.stream, wave.open(self.filename, "wb") as file:
			file.setnchannels(1)
			file.setsampwidth(2)
			file.setframerate(self.sample_rate)

			in_speech = 0
			while True:
				try:
					data = self.audio_queue.get()

					# Taken from webrtcvad-wheel example
					vad_frame = int(self.sample_rate * (10 / 1000) * 2) # 10ms

					if self.vad.is_speech(data[0:vad_frame], int(self.sample_rate)):
						# We are in speech
						# print("IN SPEECH")
						in_speech = 1
						file.writeframes(data)
					elif in_speech:
						# print("NO SPEECH GETTING OUT")
						# Getting out of speech
						in_speech = 0
						break
					else:
						# No voice, just continuing
						continue
						
				except queue.Empty:
					continue

	def upload_audio(self):
		with open(self.filename, "rb") as file:
			transcription = self.client.audio.transcriptions.create(
					file=(self.filename, file.read()),
					model=self.args.tc_model,
					temperature=self.args.tc_temperature,
					language=self.language,
					response_format="verbose_json",
					)
		return transcription.text

	def source_choose(self):
		print(sd.query_devices())
		dev = int(input("Choose your device: "))
		if dev != -1:
			sd.default.device = dev
			self.sample_rate = sd.query_devices(dev)["default_samplerate"]

	@staticmethod
	def make_arguments(parser):
		parser.add_argument("-tc_vadlevel",
					  help="Groq Transcriber: Set the WebRTC Voice Activity Detector agressiveness (0-3)",
					  type=int)
		parser.add_argument("-tc_model",
					  help="Groq Transcriber: Select the model name (default: 'whisper-large-v3-turbo')",
					  default="whisper-large-v3-turbo")
		parser.add_argument("-tc_temperature",
					  help="Groq Transcriber: Change the model temperature (default: 0)",
					  type=int,
					  default=0)
		

