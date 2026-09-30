#!/bin/python
import argparse
import os
import importlib
import ast
import sys
from pathlib import Path
from interfaces import *


# plugin_info: retrieves metadata about a given plugin (description, dependencies)
#	plugin: the plugin name
#	info_type: the name of a variable containing metadata
def plugin_info(plugin, info_type):
	tree = ast.parse(Path(plugin).read_text())
	for node in ast.walk(tree):
		if isinstance(node, ast.ClassDef):
			for statement in node.body:
				if (
					isinstance(statement, ast.Assign) 
					and statement.targets[0].id == info_type
				):
					return statement.value.value


# plugin_list: lists all available plugins in a category, along with their metadata
#	plugin_type: the category to list (transcriber, translator, front)
def plugin_list(plugin_type):
	for plugin in os.listdir(plugin_type):
		if plugin.endswith(".py"):
			path = plugin_type + "/" + plugin
			print(" \033[1mName:\033[0m", plugin)
			print(" \033[1mDescription:\033[0m", plugin_info(path, "description"))
			print(" \033[1mDependencies:\033[0m", plugin_info(path, "depends"))
			print()


def main():
	parser = argparse.ArgumentParser(prog="Interpreter", add_help=False)
	parser.add_argument("-src",
					 help="Language (code) to translate from",
					 default="en")
	parser.add_argument("-tgt",
					 help="Language (code) to translate to",
					 default="pt")
	parser.add_argument("-tc", "--transcriber", 
					 default="vosk", 
					 help="Choose the transcribing engine")
	parser.add_argument("-tl", "--translator", 
					 default="ctranslate2", 
					 help="Choose the translation engine")
	parser.add_argument("-ft", "--frontend", 
					 default="terminal", 
					 help="Choose a different way of displaying text")
	parser.add_argument("-l", "--list", 
					 action="store_true", 
					 help="List all plugins and terminate")
	parser.add_argument("-h", "--help",
					 action="store_true")
	args = parser.parse_known_args()[0]


	if args.list:
		print("\033[1mTranscribers\033[0m")
		plugin_list("transcriber")

		print("\033[1mTranslators\033[0m")
		plugin_list("translator")

		print("\033[1mFrontends\033[0m")
		plugin_list("front")

		sys.exit()

	importlib.import_module("transcriber." + args.transcriber)
	importlib.import_module("translator." + args.translator)
	importlib.import_module("front." + args.frontend)
	
	# Add arguments from plugins
	Transcriber.__subclasses__()[0].make_arguments(parser)
	Translator.__subclasses__()[0].make_arguments(parser)
	Player.__subclasses__()[0].make_arguments(parser)
	args = parser.parse_known_args()[0]

	if args.help:
		parser.print_help()
		parser.exit()

	#TODO: better Dependency Injection (maybe with the init?)

	# Initialization only initializes option-independent things
	# in other words, it does pre-initialization routines
	# (like assigning base variables)
	# Useful for options that print output and terminate
	print("\033[1mInitializing Transcriber\033[0m")
	tc = Transcriber.__subclasses__()[0](args)
	print("\033[1mInitializing Translator\033[0m")
	tl = Translator.__subclasses__()[0](args)
	print("\033[1mInitializing Player\033[0m")
	ft = Player.__subclasses__()[0](args)

	# Configuration sets up user configuration and initializes what is needed
	# to initialize
	# (like options, and thus starting the module)
	print("\033[1mConfiguring Transcriber\033[0m")
	tc.configure()
	print("\033[1mConfiguring Translator\033[0m")
	tl.configure()
	print("\033[1mConfiguring Player\033[0m")
	ft.configure()

	print("\033[1mStarted successfully\033[0m")

	while True:
		transcribed = tc.final_text()
		if transcribed != "":
			translated = tl.translate(transcribed)
			ft.send_text(translated)

	#ftPlayer.disconnect()

main()
