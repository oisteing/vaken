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

# --- Legg inn CSS for bakgrunn, knapper, tekstboks og mobiljusteringer ---
st.markdown(
    f"""
    <style>
      /* Bakgrunnsbilde for hele appen */
      .stApp {{
        background-image: url("data:image/png;base64,{bg_image_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
      }}

      /* Nytt tema-knapp på desktop */
      .stButton {{
        position: absolute;
        top: 70px;
        left: 20px;
        z-index: 1000;
      }}
      .stButton > button {{
        background-color: white;
        color: #333;
        border: 2px solid #333;
        padding: 10px 20px;
        font-size: 18px;
        cursor: pointer;
        border-radius: 4px;
      }}

      /* Kopi-knapp på desktop */
      .copy-btn {{
        position: absolute;
        top: 70px;
        left: 200px; /* juster etter knappens bredde */
        z-index: 1000;
      }}
      .copy-btn > button {{
        background-color: white;
        color: #333;
        border: 2px solid #333;
        padding: 10px 20px;
        font-size: 18px;
        cursor: pointer;
        border-radius: 4px;
      }}

      /* Sentral beholder for setning */
      .container {{
        position: absolute;
        top: 70px;
        left: 0; right: 0; bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
      }}
      .sentence-box {{
        border: 2px solid #333;
        padding: 20px;
        font-family: Arial, sans-serif;
        font-size: 24px;
        text-align: center;
        max-width: 80%;
        background-color: rgba(249, 249, 249, 0.8);
        border-radius: 8px;
        z-index: 1000;
        color: #333 !important;
      }}

      /* Mobiljusteringer for skjermer inntil 600px brede */
      @media (max-width: 600px) {{
        .stButton, .copy-btn {{
          position: relative !important;
          top: 0 !important;
          left: 0 !important;
          margin: 10px auto;
          display: block;
        }}
        .stButton > button, .copy-btn > button {{
          width: 90%;
          box-sizing: border-box;
        }}
        .container {{
          top: 200px !important; /* header + 2 knapper + margin */
        }}
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

# «Nytt tema»-knapp
if st.button("Nytt tema"):
    st.session_state.sentence = random.choice(sentences)

# «Kopier»-knapp via komponent med JS som kopierer kun setningen
safe_sentence = json.dumps(st.session_state.sentence)
components.html(
    f"""
    <div class="copy-btn">
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

# Render setningsboksen
st.markdown(
    f"""
    <div class="container">
      <div class="sentence-box">
        {st.session_state.sentence}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
