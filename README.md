# Interpreter
A modular approach to automatic speech interpreters. Choose what engines will transcribe and translate, and even how the captions will be displayed.

Currently in beta stage.

## Usage
Run `python main.py` for sane defaults, or choose your transcriber, translator, and displayer manually with `-tc`, `-tl`, and `-d`.

### Vosk
For Vosk to work you must download a model from https://alphacephei.com/vosk/models , extract it in the project folder, and rename the extracted folder to `model`.

### Translation
Currently Brazilian Portuguese is hardwired in the translation plugins.
