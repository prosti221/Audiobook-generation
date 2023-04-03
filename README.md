# Experimenting with AI generated Audiobooks using GPT4 and ElevenLabs TTS

The input text can be placed in the `input.txt` file. GPT4 is then used to provide a character summary with names and attributes, as well as the text in a manuscript format. The character attributes are then compared with the attributes from a set of ElevenLabs voices, and the most appropriate voice is chosen for each character. The transcribed text is then read line by line using TTS by either the narrator or the character who is speaking.

## Usage

Put the text you want to transcribe in `input.txt`, and run 
```bash
python main.py 
```
You need to have both an OpenAI API key and an ElevenLabs API key.
You will also need to create voices with labels used in the code such that they can be matched with the characters.
The labels used in this project are `{'sex': 'male/female', 'age': 'young/old', 'accent': 'british/american/irish/scottish/indian'}`, but you can change these as you like.

You can set the narrator voice in `main.py` to any voice you like by giving it the `voice_id`.

## Free Alternative to ElevenLabs

I'm experimenting with using Tortoise TTS as a free alternative to ElevenLabs that can be run locally. However, the inference is really slow in comparison.

## TODO

- Add command line argument `--transcribe` if we want to generate transcription, not necessary if transcription is already generated.
- Truncate the transcription for faster TTS generations.
- Run TTS API calls in the background while previous TTS is playing.
