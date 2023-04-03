from transcribe import *
import math
from elevenlabs_tts import *
import re

# The chosen attributes for voices and characters
attribute_decode = {'sex' : {1:'male', 0:'female'},
                    'age' : {1:'young', 0:'old'},
                    'accent' : {0:'british', 1:'american', 2:'irish', 3:'scottish', 4:'indian'} 
            }

attribute_encode = {'sex' : {'male':1, 'female':0},
                    'age' : {'young':1, 'old':0},
                    'accent' : {'british':0, 'american':1, 'irish':2, 'scottish':3, 'indian':4}
            }

# Extracting characters and the story from the GPT4 transcribed text.
def parse(PATH):
    characters = {} 
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
                    match = re.match(r"\[(.+?)\]:\s*(male|female),\s*(\w+),\s*(\w+)", character_line)
                    if match:
                        name, sex, age, accent = match.groups()
                        characters[name] = {'sex' : attribute_encode['sex'][sex], 'age' : attribute_encode['age'][age], 'accent' : attribute_encode['accent'][accent]}
            elif "%%% Output %%%" in line:
                for j in range(i+1, len(lines)):
                    output_line = lines[j]
                    if not output_line or "%%%" in output_line:
                        break
                    transcription_text += output_line

    return characters, transcription_text

# Might use this similarity measure if I start introducing non-categorical attributes
def cosine_similarity(character_att, voice_att):
    # Define weights for each attribute
    weight_dict = {'sex': 1, 'age': 1, 'accent': 1}

    common_keys = set(character_att.keys()).intersection(set(voice_att.keys()))

    dot_product = sum([character_att[key] * voice_att[key] * weight_dict.get(key, 1) for key in common_keys])

    mag1 = math.sqrt(sum([val**2 * (weight_dict.get(key, 1)**2) for key, val in character_att.items()]))
    mag2 = math.sqrt(sum([val**2 * (weight_dict.get(key, 1)**2) for key, val in voice_att.items()]))

    if mag1 == 0 or mag2 == 0:
        return 0

    cosine_sim = dot_product / (mag1 * mag2)

    return cosine_sim

# A similarity measure between the character attributes and the voice attributes, this is used while we only have categorical attributes.
def jaccard_similarity(character_att, voice_att):
    # Define weights for each attribute
    weight_dict = {'sex': 2, 'age': 1, 'accent': 1.5}

    character_set = set(character_att.items())
    voice_set = set(voice_att.items())

    intersection = character_set.intersection(voice_set)
    union = character_set.union(voice_set)

    weighted_intersection = sum(weight_dict[key] for key, _ in intersection)
    weighted_union = sum(weight_dict[key] for key, _ in union)
    weighted_jaccard_sim = weighted_intersection / weighted_union

    return weighted_jaccard_sim

# Computes the similarity between a character and all voices, returns the voice with highest similarity score
def best_match(character, voices):
    scores = [(voice_id, jaccard_similarity(character, attributes)) for voice_id, attributes in voices.items()]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[0]

# Assigns a voice to each character based on the attributes, returns a voice map {character_name : voice_id}
def assign_voices(voices, characters): 
    voice_map = {} 
    for name, attributes in characters.items():
        match = best_match(attributes, voices)
        voice_map[name] = match[0]
    return voice_map

def introduce_characters(voice_map):
    for name, voice_id in voice_map.items():
        play_from_binary(text_to_speech(voice_id, f'Greetings listener! My name is {name}.'))

# This plays the transcribed text given the assigned voices in voice_map
def read_transcription(voice_map, transcription):
    pattern = r'\[([\w\s]+)\]:\s*([^\[\]]+)'
    for match in re.findall(pattern, transcription):
        character, text = match
        text = text.replace("\n", "")
        print(f"{character}: {text}")
        play_from_binary(text_to_speech(voice_map[character], text))

# Transcribes some text using GPT4 into a manuscript like format and writes it to file
def transcribe(PATH):
    inp = open('input.txt', 'r').read()
    transcription = transcribe_text(inp)

    print(transcription)
    with open('transcription', 'w') as file:
        file.write(transcription)

if __name__ == '__main__':
    #transcribe('input.txt')
    characters, transcription = parse('transcription')

    # Assign the voices based on attributes 
    voices = get_voices()
    voice_map = assign_voices(voices, characters)

    #introduce_characters(voice_map)

    # Add narrator
    voice_map['Narrator'] = 'VzHwQ3PRLGGR95Kdp2Vk' # Add your own narrator by giving it the voice_id

    # Play generated audiobook
    read_transcription(voice_map, transcription)

