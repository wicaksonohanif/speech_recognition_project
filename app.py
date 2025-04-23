# import library
import streamlit as st
import os
import tempfile
from pydub import AudioSegment, silence
import speech_recognition as sr
import srt
import datetime

# header
st.image("banner_sr.jpg", use_column_width=True) 

# title
st.title("Speech Recognition (Speech to Text) 🎙️📄")

# upload file
audio_file = st.file_uploader("🎧 Upload Audio File (.wav)", type=["wav"])

# paramter settings
st.sidebar.title("⚙️ Settings")
min_silence_len = st.sidebar.slider("Minimum Silence Length (ms)", 100, 3000, 300, step=100)
silence_thresh = st.sidebar.slider("Silence Threshold (dB)", -60, 0, -40, step=1)

if audio_file:
    st.audio(audio_file, format="audio/wav")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

    # audio segmentation
    audio_segment = AudioSegment.from_wav(temp_audio_path)
    voice_segments = silence.detect_nonsilent(audio_segment, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    voice_segments = [(int(start / 1000), int(end / 1000)) for start, end in voice_segments]

    # merge segements
    merged_segments = []
    skip_indices = set()
    for i, (start, end) in enumerate(voice_segments):
        if i in skip_indices:
            continue
        duration = end - start
        if duration < 3 and i + 1 < len(voice_segments):
            next_end = voice_segments[i + 1][1]
            merged_segments.append((start, next_end))
            skip_indices.add(i + 1)
        else:
            merged_segments.append((start, end))

    # speech to text
    recognizer = sr.Recognizer()
    subtitles = []
    st.write("📜 **Result:**")

    with sr.AudioFile(temp_audio_path) as audio_source:
        for idx, (start_sec, end_sec) in enumerate(merged_segments):
            duration = end_sec - start_sec
            try:
                audio_source_offset = start_sec
                audio_source.DURATION = duration
                audio_data = recognizer.record(audio_source, duration=duration)
                recognized_text = recognizer.recognize_google(audio_data, language="id-ID")

                subtitle = srt.Subtitle(
                    index=idx + 1,
                    start=datetime.timedelta(seconds=start_sec),
                    end=datetime.timedelta(seconds=end_sec),
                    content=recognized_text
                )
                subtitles.append(subtitle)
                st.markdown(f"**{idx + 1}.** `{start_sec}s - {end_sec}s` → {recognized_text}")
            except sr.UnknownValueError:
                st.warning(f"{idx + 1}. ...")
            except Exception as e:
                st.error(f"Segement Error {idx + 1}: {e}")

    # export subtitle
    if subtitles:
        srt_content = srt.compose(subtitles)
        srt_file_path = os.path.join(tempfile.gettempdir(), "generated_subtitle.srt")
        with open(srt_file_path, "w", encoding="utf-8") as f:
            f.write(srt_content)

        with open(srt_file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Text(.srt)",
                data=f,
                file_name="generated_text.srt",
                mime="text/plain"
            )

    os.remove(temp_audio_path)