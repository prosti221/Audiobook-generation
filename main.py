from transcribe import *
from elevenlabs_tts import *
import re

def parse(PATH):
    characters = []
    transcription_text = ""
    with open(PATH, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if "%%% Characters %%%" in line:
                for j in range(i+1, len(lines)):
                    character_line = lines[j].strip()
                    if not character_line or "%%%" in character_line:
                        break
                    match = re.match(r"\[(.+?)\]:\s*(male|female)", character_line)
                    if match:
                        name, sex = match.groups()
                        characters.append((name, sex))
            elif "%%% Output %%%" in line:
                for j in range(i+1, len(lines)):
                    output_line = lines[j]
                    if not output_line or "%%%" in output_line:
                        break
                    transcription_text += output_line

    return characters, transcription_text

# voices -> (Name, voice_id, sex)
# characters -> (Name, sex)
def assign_voices(voices, characters):
    voice_map = {}
    used_voice_ids = set()
    for character in characters:
        name, sex = character
        for voice in voices:
            voice_name, voice_id, voice_sex = voice
            if voice_id not in used_voice_ids and sex == voice_sex:
                voice_map[name] = voice_id
                used_voice_ids.add(voice_id)
                break
    return voice_map # {Name: voice_id}

def introduce_characters(voice_map):
    for name, voice_id in voice_map.items():
        play_from_binary(text_to_speech(voice_id, f'Greetings listener! My name is {name}.'))

def read_transcription(voice_map, transcription):
    #pattern = r'\[([\w\s]+)\]:\s*([\w\s,.!?\']+)'
    pattern = r'\[([\w\s]+)\]:\s*([^\[\]]+)'

    for match in re.findall(pattern, transcription):
        character, text = match
        text = text.replace("\n", "")
        print(f"{character}: {text}")
        play_from_binary(text_to_speech(voice_map[character], text))

def transcribe(PATH):
    inp = open('input.txt', 'r').read()
    transcription = transcribe_text(inp)

    print(transcription)
    with open('transcription', 'w') as file:
        file.write(transcription)

if __name__ == '__main__':
    #transcribe('input.txt')
    characters, transcription = parse('transcription')

    # Assign the voices based on attributes (only sex for now)
    voices = get_voices()
    voice_map = assign_voices(voices, characters)

    #introduce_characters(voice_map)

    # Add narrator
    voice_map['Narrator'] = voices[-1][1]
    voices = get_voices()

    # Play generated audiobook
    read_transcription(voice_map, transcription)
