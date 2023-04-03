Experimenting with AI generated audiobooks using GPT4 and ElevenLabs TTS.

The input text can be put in input.txt. GPT4 is then used to give a character summary with names and attributes, as well as the text in a manuscript like format.
The character attributes are compared with the attributes from a set of ElevenLabs voices, and the most appropriate voice is chosen for each character.
The transcribed text is then read line by line using TTS by either the Narrator or which ever character is speaking.

You can set the narrator voice in main.py to which ever one you like by giving it the voice_id.

This requires both an openAI and elevenlabs API key.
You also need to create voices with labels used in the code such that they can be matched with the characters.

The labels used for now are: {'sex' male/female, 'age':young/old, 'accent':british/american/irish/scottish/indian}, change these as you like.

I am experimenting using tortoise TTS as a free alternative to elevenlabs that can be run locally, however inference is REALLY slow in comparison.
