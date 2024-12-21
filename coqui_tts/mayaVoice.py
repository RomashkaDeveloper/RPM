import torch
from TTS.api import TTS
import soundfile as sf
import sounddevice as sd

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def getVoice(text):
    tts.tts_to_file(text, speaker_wav="C:/Users/FitmyLook/Downloads/MayaVoice.wav", language="en", file_path="C:/Users/FitmyLook/Desktop/AI/output.wav")
    data, samplerate = sf.read('C:/Users/FitmyLook/Desktop/AI/output.wav')
    sd.play(data, samplerate)
