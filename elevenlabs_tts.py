import requests
import json
from pydub import AudioSegment
from pydub.playback import play
import io
import gender_guesser.detector as gender

key = open("./elevenlabs_key", "r").read().strip()

def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
    "accept": "application/json",
    "xi-api-key": key
    }
    response = requests.get(url, headers=headers)

    d = gender.Detector()
    
    return [(voice['name'], voice['voice_id'], d.get_gender(voice['name'])) for voice in response.json()['voices']]

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
    #print(response.json())

    return response.content

def play_from_binary(audio_binary):
    print(audio_binary)
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary), format='mp3')
    except:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary), format='mp4')

    play(audio_segment)
