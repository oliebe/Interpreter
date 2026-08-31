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
	parser.add_argument("-tc", "--transcriber", 
						default="vosk", 
						help="Choose the transcribing engine")
	parser.add_argument("-tl", "--translator", 
						default="groq", 
						help="Choose the translation engine")
	parser.add_argument("-d", "--display", 
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
	importlib.import_module("front." + args.display)
	
	# Add arguments from plugins
	Transcriber.__subclasses__()[0].make_arguments(parser)
	Translator.__subclasses__()[0].make_arguments(parser)
	Player.__subclasses__()[0].make_arguments(parser)
	args = parser.parse_known_args()[0]

	if args.help:
		parser.print_help()
		parser.exit()

	#TODO: better Dependency Injection (maybe with the init?)
	print("\033[1mInitializing Transcriber\033[0m")
	ts_model = Transcriber.__subclasses__()[0](args)
	print("\033[1mInitializing Translator\033[0m")
	tl_engine = Translator.__subclasses__()[0](args)
	print("\033[1mInitializing Player\033[0m")
	ft_player = Player.__subclasses__()[0](args)

	while True:
		transcribed = ts_model.final_text()
		if transcribed != "":
			translated = tl_engine.translate(transcribed)
			ft_player.send_text(translated)

	#ftPlayer.disconnect()

main()
