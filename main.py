from transcribe import *
import math
from elevenlabs_tts import *
import re

attribute_encode = {'sex' : {'male':1, 'female':0},
                    'accent' : {'british':0, 'american':1, 'irish':2, 'scottish':3, 'indian':4} # Might extend over time
            }

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

# Used as similarity measure for character attributes vs voice attributes
def cosine_similarity(character_att, voice_att): 
    transformed_accent = int(character_att['accent'] == voice_att['accent'])
    character_att['accent'] = transformed_accent
    voice_att['accent'] = transformed_accent

    common_keys = set(character_att.keys()).intersection(set(voice_att.keys()))

    dot_product = sum([character_att[key] * voice_att[key] for key in common_keys])

    mag1 = math.sqrt(sum([val**2 for val in character_att.values()]))
    mag2 = math.sqrt(sum([val**2 for val in voice_att.values()]))

    cosine_sim = dot_product / (mag1 * mag2)

    return cosine_sim

def best_match(character, voices):
    pass

# voices -> (Name, voice_id, sex)
# characters -> (Name, sex)
def assign_voices(voices, characters): # Will extend to assign voices based on multiple attributes like sex, accent, eccentricity, etc.
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

    '''
    # Example usage of similary
    character_att = {'sex':1, 'accent':1, 'eccentricity': 0.9}
    voice_att = {'sex':1, 'accent':1, 'eccentricity': 0.9}

    similarity = cosine_similarity(character_att, voice_att)
    print(similarity)
    '''
