# Interpreter
A modular approach to real time speech transcription & translation. Plug the engines interchangeably to find what's best for you, be it offline or online, LLM or machine translation, or just plain transcription.

Having a decoupled design in mind, it's possible to easily develop plugins that will seamlessly interface with all other modules through a common interface.

## Available Modules
- **Transcription:** Vosk, Whisper (groq)
- **Translation:** Google & MyMemory (deeptranslate), Argos Translate, LLMs (groq), Just copy (passthrough)
- **Display:** mpv Media Player, Terminal

## Dependencies
- Requires `python>=3.14`.

Basic function dependencies include `sounddevice` and `langcodes`. See dependencies in detail, for each module, with the option `-l`.

## Usage
Run `python main.py` for sane defaults, or choose your transcriber, translator, and displayer manually with `-tc`, `-tl`, and `-ft`.

Use the options `-src` and `-tgt` to specify the language being transcribed and the language to translate, if applicable.

Use `-h` for help (you can see module-specific help by loading the module with `-tc`, `-tl` and `-ft`)

## Contributing
Contributions are welcome, but usage of AI (LLMs) is prohibited (for many reasons). If you'd like to contribute with a module, see `interfaces.py` for templates. If you want to improve the app, search for `TODO`s scattered through the project or create an Issue.
