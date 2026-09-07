# Interpreter
A modular approach to automatic speech interpreters. Choose what engines will transcribe and translate, and even how the captions will be displayed.

## Dependencies
- Requires `python>=3.14`.
- Vosk requires `vosk` and `sounddevice` packages

Other modules have dependencies highlighted with the option `-l`

## Usage
Run `python main.py` for sane defaults, or choose your transcriber, translator, and displayer manually with `-tc`, `-tl`, and `-d`.

Use `-h` for help (you can see module-specific options by specifying them with `-tc`, `-tl` and `-d`)

## Contributing
Contributions are welcome. If you'd like to contribute with a module, see `interfaces.py` for templates. If you want to improve the app, search for `TODO`s scattered through the project or create an Issue.
