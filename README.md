# Interpreter
A modular approach to automatic speech interpreters. Choose what engines will transcribe and translate, and even how the captions will be displayed.

## Dependencies
- Requires `python>=3.14`.

Basic function dependencies include `sounddevice` and `langcodes`. See dependencies in detail, for each module, with the option `-l`.

## Usage
Run `python main.py` for sane defaults, or choose your transcriber, translator, and displayer manually with `-tc`, `-tl`, and `-ft`.

Use `-h` for help (you can see module-specific options by specifying them with `-tc`, `-tl` and `-ft`)

## Contributing
Contributions are welcome. If you'd like to contribute with a module, see `interfaces.py` for templates. If you want to improve the app, search for `TODO`s scattered through the project or create an Issue.
