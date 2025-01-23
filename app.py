import streamlit as st
import os
from pydub import AudioSegment
import numpy as np
import librosa
from scipy.io.wavfile import write


AudioSegment.converter = r"C:\Users\omara\Downloads\ffmpeg-2025-01-20-git-504df09c34-essentials_build\ffmpeg-2025-01-20-git-504df09c34-essentials_build\bin\ffmpeg.exe"
def isolate_speech(input_file, output_file):
    audio = AudioSegment.from_mp3(input_file)
    wav = "audio.wav"
    audio.export(wav, format="wav")

    y, sr = librosa.load(wav, sr=None)

    intervals = librosa.effects.split(y, top_db=69)

    speech_mask = np.zeros_like(y, dtype=bool)
    for start, end in intervals:
        speech_mask[start:end] = True

    y_speech_only = y * speech_mask

    y_speech_only = librosa.effects.preemphasis(y_speech_only)

    write(output_file, sr, (y_speech_only*32767).astype(np.int16))

    cleaned_audio = AudioSegment.from_wav(output_file)
    cleaned_mp3 = output_file.replace(".wav", ".mp3")
    cleaned_audio.export(cleaned_mp3, format="mp3")

    os.remove(wav)
    os.remove(output_file)

    return cleaned_mp3

st.title("Isolate Speech and Remove Noise")

uploaded_file = st.file_uploader("Upload an MP# file", type=["mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3", start_time=0)
    input_file_path = uploaded_file.name

    with open(input_file_path, "wb") as f:
        f.write(uploaded_file.read())

    output_file_path="output_cleaned.wav"

    if st.button("Start cleaning audio"):
        st.text("Processing...")
        try:
            cleaned_mp3_file = isolate_speech(input_file_path, output_file_path)

            with open(cleaned_mp3_file, "rb") as f:
                st.download_button(
                    label="Download cleaned audio",
                    data=f,
                    file_name="cleaned_audio.mp3",
                    mime="audio/mpeg",
                )
            os.remove(input_file_path)
            os.remove(cleaned_mp3_file)

        except Exception as e:
            st.error(f"An error occurred: {e}")