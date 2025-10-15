import random
import streamlit as st
import base64
import json
import streamlit.components.v1 as components

# --- Hjelpefunksjon for å laste og base64-kode bakgrunnsbilde ---
def get_base64_image(path: str) -> str:
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Sti til bildet i samme mappe som programmet
bg_image_path = "vaffel.png"
bg_image_base64 = get_base64_image(bg_image_path)

# --- Sett opp side ---
st.set_page_config(page_title="Golden ways", layout="wide")

# --- Global CSS (uten absolutt posisjonering av knapper) ---
st.markdown(
    f"""
    <style>
      /* Bakgrunn */
      .stApp {{
        background-image: url("data:image/png;base64,{bg_image_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
      }}

      /* Fjern grå "tap"-blink på mobil */
      * {{ -webkit-tap-highlight-color: rgba(0,0,0,0); }}

      /* Knappestil (gjeld begge) */
      .top-btn > button,
      .top-btn > button:focus,
      .top-btn > button:active,
      .top-btn > button:hover {{
        background: #ffffff !important;
        color: #333 !important;
        border: 2px solid #333 !important;
        opacity: 1 !important;
        box-shadow: none !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        min-width: 140px !important;
        height: auto !important;
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        padding: 10px 20px !important;
        border-radius: 6px !important;
        font-size: 18px !important;
        line-height: 1.2 !important;
      }}

      /* Kopi-knappen laget i HTML/JS */
      .copy-btn > button {{
        background: #ffffff;
        color: #333;
        border: 2px solid #333;
        padding: 10px 20px;
        font-size: 18px;
        cursor: pointer;
        border-radius: 6px;
        white-space: nowrap;
        min-width: 120px;
      }}

      /* Sentral boks for setningen */
      .center-wrap {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 70vh;        /* gir plass under knappene */
        padding: 2rem 1rem;
      }}
      .sentence-box {{
        border: 2px solid #333;
        padding: 20px;
        font-family: Arial, sans-serif;
        font-size: 24px;
        text-align: center;
        max-width: 900px;
        background-color: rgba(249, 249, 249, 0.85);
        border-radius: 8px;
        color: #333 !important;
      }}

      @media (max-width: 600px) {{
        .top-btn > button, .copy-btn > button {{
          width: 100%;
          box-sizing: border-box;
          background: rgba(255,255,255,0.98);
        }}
        .center-wrap {{ min-height: 60vh; }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_sentences(path="sentences.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [linje.strip() for linje in f if linje.strip()]

sentences = load_sentences()

if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)

# ---- TOPP: to kolonner med knapper (ingen absolutte posisjoner) ----
col1, col2 = st.columns([1, 1])

with col1:
    # gi Streamlit-knappen en wrapper-klasse for styling
    btn_placeholder = st.empty()
    with btn_placeholder.container():
        # Bruk standard st.button, men gi parent en klasse via markdown-hack
        st.markdown('<div class="top-btn">', unsafe_allow_html=True)
        if st.button("Nytt tema", key="nytt_tema"):
            st.session_state.sentence = random.choice(sentences)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    safe_sentence = json.dumps(st.session_state.sentence)
    components.html(
        f"""
        <div class="copy-btn" style="display:flex; justify-content:flex-start;">
          <button id="copy-btn">Kopier</button>
        </div>
        <script>
          const text = {safe_sentence};
          const btn = document.getElementById('copy-btn');
          btn.onclick = () => {{
            navigator.clipboard.writeText(text);
            btn.innerText = 'Kopiert!';
            setTimeout(() => btn.innerText = 'Kopier', 1500);
          }};
        </script>
        """,
        height=60,
    )

# ---- SENTRAL TEKSTBOKS ----
st.markdown(
    f"""
    <div class="center-wrap">
      <div class="sentence-box">
        {st.session_state.sentence}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
