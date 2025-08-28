import streamlit as st
import whisper
import tempfile
import os
import srt
import datetime
import shutil

if shutil.which("ffmpeg") is None:
    st.error("❌ FFMPEG is not found in your system PATH. Please install and add it to PATH.")
    st.stop()

st.image("banner_sr.jpg", use_container_width=True)
st.title("🎙️📄 English Subtitle Generator")

audio_file = st.file_uploader("Upload Audio File (.wav)", type=["wav"])

@st.cache_resource
def load_model():
    return whisper.load_model("medium") 

model = load_model()

if audio_file:
    st.audio(audio_file, format="audio/wav")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

    st.info("🔍 Transcribing audio... Please wait.")
    result = model.transcribe(temp_audio_path, language="en", verbose=False)

    subtitles = []
    for idx, seg in enumerate(result['segments']):
        subtitle = srt.Subtitle(
            index=idx + 1,
            start=datetime.timedelta(seconds=int(seg['start'])),
            end=datetime.timedelta(seconds=int(seg['end'])),
            content=seg['text'].strip()
        )
        subtitles.append(subtitle)

    st.subheader("📜 Transcription Result:")
    for sub in subtitles:
        st.markdown(f"**{sub.index}.** `{sub.start} - {sub.end}` → {sub.content}")

    srt_content = srt.compose(subtitles)
    srt_file_path = os.path.join(tempfile.gettempdir(), "generated_subtitle.srt")
    with open(srt_file_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    with open(srt_file_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Subtitle (.srt)",
            data=f,
            file_name="generated_subtitle.srt",
            mime="text/plain"
        )

    os.remove(temp_audio_path)
