
import streamlit as st
import whisper
from googletrans import Translator
from moviepy.editor import VideoFileClip
import os

# Initialize Whisper model
model = whisper.load_model("medium")

# Translator
translator = Translator()

st.title("🎙️ Urdu Video & Audio AI Agent")
st.markdown("Upload an audio or video file and get Urdu and English text transcripts.")

uploaded_file = st.file_uploader("Upload Audio or Video (.mp3, .wav, .mp4)", type=["mp3", "wav", "mp4"])

if uploaded_file:
    file_name = uploaded_file.name
    with open(file_name, "wb") as f:
        f.write(uploaded_file.read())
    
    # If it's a video, extract audio
    if file_name.endswith(".mp4"):
        st.info("Extracting audio from video...")
        video = VideoFileClip(file_name)
        audio_path = "extracted_audio.wav"
        video.audio.write_audiofile(audio_path)
    else:
        audio_path = file_name

    # Transcribe with Whisper
    st.info("Transcribing Urdu audio...")
    result = model.transcribe(audio_path, language="ur")
    urdu_text = result["text"]

    # Translate Urdu to English
    st.info("Translating to English...")
    translation = translator.translate(urdu_text, src="ur", dest="en")
    english_text = translation.text

    st.subheader("📝 Urdu Transcript")
    st.write(urdu_text)

    st.subheader("🌐 English Translation")
    st.write(english_text)

    # Save transcripts to text files
    with open("urdu_transcript.txt", "w", encoding="utf-8") as urdu_file:
        urdu_file.write(urdu_text)
    with open("english_translation.txt", "w", encoding="utf-8") as eng_file:
        eng_file.write(english_text)

    st.success("Transcripts saved as 'urdu_transcript.txt' and 'english_translation.txt'")

    # Cleanup uploaded and extracted files
    os.remove(file_name)
    if os.path.exists("extracted_audio.wav"):
        os.remove("extracted_audio.wav")
