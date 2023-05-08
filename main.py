import streamlit as st
import os
from notesmaker import NotesMaker
from notesdownloader import NotesDownloader
from lda_keywords import LDAKeywords
from openai_keywords import OpenaiKeywords
from pathlib import Path

st.set_page_config(layout="wide")


@st.cache_resource
def load_models():
    nm = NotesMaker()
    lda_key = LDAKeywords()
    openai_key = OpenaiKeywords()
    return nm, lda_key, openai_key

def download_audio_file():
    duration = nm.get_aud_from_link(yt_link)
    return duration

def download_audio_file_from_vid(filename):
    duration = nm.get_aud_from_vid(filename)
    return duration

def transcript():
    return nm.gen_transcript()

def lda():
    keywords = lda_key.get_keywords()
    return keywords

def download_ppt():
    nd.download_ppt()
    
def download_docx():
    nd.download_docx()

def openai():
    return openai_key.get_keywords()

yt_link = ""
downloads_path = str(os.path.join(Path.home(), "Downloads"))
generate_notes = False
nm, lda_key, openai_key = load_models()
nd = NotesDownloader()

if "text" not in st.session_state:
    st.session_state.text = ""

if "lda_keywords" not in st.session_state:
    st.session_state.lda_keywords = ""

if "ai_keywords" not in st.session_state:
    st.session_state.ai_keywords = ""

if "input_link" not in st.session_state:
    st.session_state.input_link = ""

if "audio_btn_state" not in st.session_state:
    st.session_state.audio_btn_state = False

if "video_btn_state" not in st.session_state:
    st.session_state.video_btn_state = False

def notes():
    notes_bool = nm.gen_notes()
    return notes_bool

with open('style.css', 'r') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>Notes Generation From Video</h1>",
            unsafe_allow_html=True)
st.write('---')

with st.container():
    l, m, r = st.columns([1, 1, 1], gap="medium")
    with l:
        st.markdown(
            "<h6 style='text-align: center; color: white;'>Enter Youtube Link</h6>", unsafe_allow_html=True)
        yt_link = st.text_input('yt', label_visibility="collapsed", placeholder="Enter Link", disabled=st.session_state.audio_btn_state)
        if yt_link != "":

            if os.path.exists("audio_file.wav"):
                if st.session_state.input_link == yt_link:
                    st.success('Valid Link', icon="🚨")
                else:
                    st.warning('Audio File Already Exists', icon="🚨")

            elif "www.youtube.com" not in yt_link:
                st.warning('Invalid URL', icon="🚨")
            else:
                duration = download_audio_file()
                if duration is None:
                    print("Connection Error!")
                    st.error('Invalid URL', icon="🚨")
                elif duration == 0:
                    print("Audio Length Exceeded!")
                    st.error('Video Length must be between 5 and 10 minutes', icon="🚨")
                else: 
                    st.success('Valid Link', icon="🚨")
                    st.session_state.input_link = yt_link
                    st.session_state.video_btn_state = True
                    st.session_state.audio_btn_state = True

    with m:
        st.markdown(
            "<h2 style='text-align: center; color: white;'>OR</h2>", unsafe_allow_html=True)
    with r:

        st.markdown(
            "<h6 style='text-align: center; color: white;'>Upload *.mp4 Video</h6>", unsafe_allow_html=True)
        video_file = st.file_uploader(
            "vid", type=["mp4"], accept_multiple_files=False, label_visibility="collapsed", disabled=st.session_state.video_btn_state)

        if video_file:

            if os.path.exists("audio_file.wav"):
                st.warning('Audio File Already Exists', icon="🚨")

            else:
                with open('uploaded_file.mp4', "wb") as f:
                    f.write(video_file.getbuffer())

                vid_duration = download_audio_file_from_vid("uploaded_file.mp4")

                if vid_duration is None:
                    print("Connection Error!")
                    st.error('Invalid Link Provided', icon="🚨")
                
                elif vid_duration == 0:
                    print("Video Length Exceeded!")
                    st.error('Video Length must be between 5 and 10 minutes', icon="🚨")
                else: 
                    st.success('Valid Link', icon="🚨")
                    st.session_state.video_btn_state = True
                    st.session_state.audio_btn_state = True


st.write('---')

with st.container():

    l, m1, m2, r = st.columns([2, 1, 1, 1], gap="medium")

    with l:
        button1 = st.button("Generate Transcript", key="gentranscript")

        if button1 and not os.path.exists("audio_file.wav"):
            st.error('Provide Link or Upload Video', icon="🚨")

        elif button1 and nm.uploaded:

            if not st.session_state.text:
                st.session_state.text = transcript()
            st.write(
                f"<div style='border:2px solid white;padding:20px;height:350px;overflow-y: scroll;'>{st.session_state.text}</div>", unsafe_allow_html=True)
        elif button1 and not nm.uploaded:
            st.error('Provide Link or Upload Video', icon="🚨")

    with m1:
        button2 = st.button("Generate LDA and OpenAI Keywords ")

        if button2 and not os.path.exists("transcript.txt"):
            st.error('Generate Transcript FIrst', icon="🚨")
        elif button2 and not nm.uploaded:
            st.error('Provide Link or Upload Video', icon="🚨")
        elif button2 and not nm.transcript_generated:
            st.error('Generate Transcript First', icon="🚨")

    with m2:
        st.markdown(
            "<h6 style='text-align: center; color: white;'>LDA</h6>", unsafe_allow_html=True)
        keywords = None
        if button2 and nm.transcript_generated:
            if not st.session_state.lda_keywords:
                st.session_state.lda_keywords = lda()

            lda_keywords = st.session_state.lda_keywords.split("\n")
            st.write(f"""<h5 style='border:2px solid white;padding:20px;height:350px;overflow-y: scroll;'>
            {lda_keywords[0]} <br>
            {lda_keywords[1]} <br>
            {lda_keywords[2]} <br>
            {lda_keywords[3]} <br>
            {lda_keywords[4]} <br>
            {lda_keywords[5]} <br>
            {lda_keywords[6]} <br>
            {lda_keywords[7]} <br>
            {lda_keywords[8]} <br>
            {lda_keywords[9]} <br>
            </h5>""", unsafe_allow_html=True)

    with r:

        st.markdown(
            "<h6 style='text-align: center; color: white;'>OpenAI</h6>", unsafe_allow_html=True)
        if button2 and nm.transcript_generated:
            
            if not st.session_state.ai_keywords:
                st.session_state.ai_keywords = openai()

            st.write(f"""<h5 style='border:2px solid white;padding:20px;height:350px;overflow-y: scroll;'>
            {st.session_state.ai_keywords} <br>
            </h5>""", unsafe_allow_html=True)
st.write("---")

with st.container():

    generate_notes = st.button("Generate Notes")

    if generate_notes and not nm.uploaded:
        st.error('Provide Link or Upload Video', icon="🚨")
    elif generate_notes and not nm.transcript_generated:
        st.error('Generate Transcript First', icon="🚨")
    elif generate_notes and nm.transcript_generated:
        notes_bool = notes()

        if notes_bool:
            st.success('Notes Successfully Generated!', icon="🚨")


if nm.notes_generated:
    st.sidebar.title("Download Notes")

    ppt_download = st.sidebar.button("Download Notes in pptx", on_click=download_ppt)
    if ppt_download:
        st.success('PPT file downloaded!', icon="🚨")
        
    doc_download = st.sidebar.button("Download Notes in docx", on_click=download_docx)
    if doc_download:
        st.success('Doc file downloaded!', icon="🚨")
    
if st.button("Reset"):
    if os.path.exists('paras.txt'):
        os.remove("paras.txt")
    if os.path.exists('transcript.txt'):
        os.remove("transcript.txt")
    if os.path.exists('audio_file.wav'):
        os.remove("audio_file.wav")
    if os.path.exists('uploaded_file.mp4'):
        os.remove("uploaded_file.mp4")
    
    nm.uploaded = False
    nm.transcript_generated = False
    nm.notes_generated = False

    st.session_state.text = ""
    st.session_state.lda_keywords = ""
    st.session_state.ai_keywords = ""
    st.session_state.video_btn_state = False
    st.session_state.audio_btn_state = False
