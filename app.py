import streamlit as st

from utils.file_handler import save_uploaded_file
from models.speech_to_text import convert_speech_to_text
from models.summarizer import generate_summary
from models.quiz_generator import generate_quiz
from models.flashcards import generate_flashcards


# ── page config ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="VoiceNotes",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── custom CSS ─────────────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
  }

  /* scrub default Streamlit padding */
  .block-container { padding-top: 2.5rem; max-width: 860px; }

  /* header strip */
  .vn-header {
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    margin-bottom: 2rem;
    border-bottom: 2px solid #1a1a1a;
    padding-bottom: 0.75rem;
  }
  .vn-header h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin: 0;
    color: #1a1a1a;
  }
  .vn-header span {
    font-size: 0.78rem;
    color: #888;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* section labels */
  .vn-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 0.4rem;
  }

  /* transcript block */
  .vn-transcript {
    background: #f7f6f2;
    border-left: 3px solid #1a1a1a;
    padding: 1.1rem 1.3rem;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #2d2d2d;
    border-radius: 0 4px 4px 0;
    margin-bottom: 2rem;
  }

  /* notes block */
  .vn-notes {
    background: #fff;
    border: 1px solid #e0e0e0;
    padding: 1.1rem 1.3rem;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #2d2d2d;
    border-radius: 4px;
    margin-bottom: 2rem;
  }

  /* quiz card */
  .vn-quiz-card {
    border: 1px solid #e8e8e8;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    background: #fff;
  }
  .vn-quiz-q {
    font-size: 0.93rem;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
  }
  .vn-quiz-a {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    background: #f0f7ee;
    color: #2a6b1f;
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 3px;
  }

  /* flashcard */
  .vn-flash {
    background: #1a1a1a;
    color: #f5f5f5;
    border-radius: 6px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.75rem;
  }
  .vn-flash-q {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.5rem;
  }
  .vn-flash-a {
    font-size: 0.9rem;
    line-height: 1.6;
    color: #e8e8e8;
  }

  /* divider */
  .vn-divider {
    border: none;
    border-top: 1px solid #ebebeb;
    margin: 2rem 0;
  }
</style>
""", unsafe_allow_html=True)


# ── header ─────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="vn-header">
  <h1>🎙 VoiceNotes</h1>
  <span>lecture audio → study materials</span>
</div>
""", unsafe_allow_html=True)


# ── upload ─────────────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader(
    "Drop a lecture recording here",
    type=["wav", "mp3", "m4a"],
    help="Supports WAV, MP3, and M4A. Longer recordings take more time to transcribe.",
)

if not uploaded_file:
    st.markdown(
        "<p style='color:#aaa;font-size:0.85rem;margin-top:0.5rem'>"
        "No file yet — upload one above to get started."
        "</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ── transcription ──────────────────────────────────────────────────────────────

file_path = save_uploaded_file(uploaded_file)

with st.spinner("Transcribing audio…"):
    transcript = convert_speech_to_text(file_path)

st.markdown('<p class="vn-label">Transcript</p>', unsafe_allow_html=True)
st.markdown(f'<div class="vn-transcript">{transcript}</div>', unsafe_allow_html=True)
st.markdown('<hr class="vn-divider">', unsafe_allow_html=True)


# ── summary ────────────────────────────────────────────────────────────────────

with st.spinner("Summarising…"):
    summary = generate_summary(transcript)

st.markdown('<p class="vn-label">Study Notes</p>', unsafe_allow_html=True)
st.markdown(f'<div class="vn-notes">{summary}</div>', unsafe_allow_html=True)
st.markdown('<hr class="vn-divider">', unsafe_allow_html=True)


# ── quiz ───────────────────────────────────────────────────────────────────────

st.markdown('<p class="vn-label">Fill-in-the-blank Quiz</p>', unsafe_allow_html=True)

quiz = generate_quiz(transcript)
if quiz:
    for i, item in enumerate(quiz, start=1):
        st.markdown(f"""
        <div class="vn-quiz-card">
          <div class="vn-quiz-q">Q{i}: {item['question']}</div>
          <div class="vn-quiz-a">→ {item['answer']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown(
        "<p style='color:#aaa;font-size:0.85rem'>Not enough content to build a quiz.</p>",
        unsafe_allow_html=True,
    )

st.markdown('<hr class="vn-divider">', unsafe_allow_html=True)


# ── flashcards ─────────────────────────────────────────────────────────────────

st.markdown('<p class="vn-label">Flashcards</p>', unsafe_allow_html=True)

cards = generate_flashcards(transcript)
if cards:
    cols = st.columns(2)
    for i, card in enumerate(cards):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="vn-flash">
              <div class="vn-flash-q">{card['question']}</div>
              <div class="vn-flash-a">{card['answer']}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown(
        "<p style='color:#aaa;font-size:0.85rem'>Not enough content for flashcards.</p>",
        unsafe_allow_html=True,
    )
