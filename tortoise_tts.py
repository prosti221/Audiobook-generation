import requests
import json
from pydub import AudioSegment
from pydub.playback import play
import io
import gender_guesser.detector as gender

def get_voices():

    d = gender.Detector()
    
    return None #[(Name, voice_id, sex)] 

def text_to_speech(voice_id, text):
    return None # Returns audio data in binary form

def play_from_binary(audio_binary):
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary), format='mp3')
    except:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary), format='mp4')

    play(audio_segment)

