from gtts import gTTS
from playsound import playsound
import os, time
text = "123"
lang='en'
tts = gTTS(text, lang=lang)

tts.save('temp.mp3')
playsound('temp.mp3')
time.sleep(2)

os.remove("temp.mp3")