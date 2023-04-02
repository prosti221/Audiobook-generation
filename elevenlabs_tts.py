import requests
import json
from pydub import AudioSegment
from pydub.playback import play
import io
import gender_guesser.detector as gender

key = open("./elevenlabs_key", "r").read().strip()

attribute_encode = {'sex' : {'male':1, 'female':0},
                    'age' : {'young':1, 'old':0},
                    'accent' : {'british':0, 'american':1, 'irish':2, 'scottish':3, 'indian':4} # Might extend over time
            }

generate_atts = lambda sex, age, accent: {'sex': attribute_encode['sex'][sex], 'age':attribute_encode['age'][age], 'accent':attribute_encode['accent'][accent]}


def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
    "accept": "application/json",
    "xi-api-key": key
    }
    response = requests.get(url, headers=headers)
    #[print(voice['labels']) for voice in response.json()['voices']]
    d = gender.Detector()
    voices = {}
    for voice in response.json()['voices']:
        # If we have no labels, guess sex from name and give default age and accent
        if len(voice['labels']) == 0: 
            pred_sex = d.get_gender(voice['name'])
            pred_sex = 'male' if pred_sex == 'male' or pred_sex == 'mostly_male' or pred_sex == 'unknown' else 'female'
            voices[voice['voice_id']] = generate_atts(pred_sex, 'young', 'american')
        else:
            labels = voice['labels']
            voices[voice['voice_id']] = generate_atts(labels['gender'], labels['age'], labels['accent'])

    return voices

def text_to_speech(voice_id, text):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': key,
        'Content-Type': 'application/json'
    }
    data = {
        "text": text, 
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response.content

def play_from_binary(audio_binary):
    #print(audio_binary)
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary), format='mp3')
    except:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary), format='mp4')

    play(audio_segment)
