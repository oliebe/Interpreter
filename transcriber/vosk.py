from interfaces import Transcriber
import sounddevice as sd
from vosk import Model, KaldiRecognizer, list_languages
import queue
import json
import sys

class VoskTranscriber(Transcriber):
	description = "Vosk Offline Speech to Text. Supports more than 20 languages and very lightweight."
	depends = "vosk, sounddevice"
	def __init__(self, args):
		self.args = args
		self.sample_rate = 16000
		self.audio_queue = queue.Queue()
		self.device = sd.default.device

		if self.args.tcll:
			print("Available Vosk Languages:")
			list_languages()
			sys.exit()
		#TODO: probably create a configuration spec for these kinds of function
		self.source_choose()
		self.model = Model(lang=self.args.tcl or "en-us")
			
		
	def audio_callback(self, indata, frames, time_info, status):
		self.audio_queue.put(bytes(indata))

	def final_text(self):
		self.stream = sd.RawInputStream(
			samplerate=self.sample_rate,
			blocksize=0,
			dtype='int16',
			channels=1,
			callback=self.audio_callback
			#device=self.device
		)

		with self.stream:
			recognizer = KaldiRecognizer(self.model, self.sample_rate)
			while True:
				try:
					data = self.audio_queue.get()
					if recognizer.AcceptWaveform(data):
						result = json.loads(recognizer.Result())
						return result.get("text")
				except queue.Empty:
					continue

	def source_choose(self):
		print(sd.query_devices())
		dev = int(input("Choose your device: "))
		if dev != -1:
			sd.default.device = dev
			self.sample_rate = sd.query_devices(dev)["default_samplerate"]
			#print(self.sample_rate)
	
	@staticmethod
	def make_arguments(parser: ArgumentParser):
		parser.add_argument("-tcl", 
					  help="Vosk: Change the transcribing language (see -tcll output) (default: en-us)")
		parser.add_argument("-tcll", 
							help="Vosk: List available languages and terminate",
							action="store_true")
