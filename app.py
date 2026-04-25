import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Vinted Pro O2 Studio", page_icon="🏜️", layout="wide")

# --- 2. STILIZARE AVANSATĂ (GLASSMORPHISM) ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1509316785289-025f5b846b35?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    header {visibility: hidden;}
    h1, h2, h3, p, label {
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
    }
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        background-color: #ffffff;
        color: #1a1a1a !important;
        font-weight: 800;
        font-size: 16px;
        border: none;
        padding: 12px;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button:hover { background-color: #e0e0e0; transform: translateY(-2px); }
    .result-box {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px; padding: 25px; color: white;
        border: 1px solid rgba(255,255,255,0.2); font-family: sans-serif; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCȚIA DE INTELIGENȚĂ ARTIFICIALĂ ---
def genereaza_descriere_premium(api_key, date_text, imagini_incarcate):
    genai.configure(api_key=api_key)
    
    poze_procesate = []
    for fisier in imagini_incarcate:
        poze_procesate.append(Image.open(fisier))

    prompt = f"""
    Ești un expert Vinted. Produsul: '{date_text['nume']}', Brand: '{date_text['brand']}', Mărime: '{date_text['marime']}', Preț: '{date_text['pret']}', Stare: '{date_text['stare']}'.
    Detalii: {date_text['detalii']}.

    Analizează imaginile atașate (culoare, textură, defecte). Scrie o descriere super atractivă, prietenoasă, cu emoji-uri și 5-7 hashtag-uri bune.
    """

    lista_continut = [prompt] + poze_procesate

    try:
        # Încercăm modelul Suprem (Gemini 2.0 Flash)
        model = genai.GenerativeModel('gemini-2.0-flash', tools='google_search')
        raspuns = model.generate_content(lista_continut)
        return raspuns.text
    except Exception as e_20:
        try:
            # Sistemul de rezervă corectat (fără "-latest" care dădea eroare 404)
            model_fallback = genai.GenerativeModel('gemini-1.5-flash')
            raspuns = model_fallback.generate_content(lista_continut)
            return raspuns.text + "\n\n*(Notă: Generat cu AI-ul de rezervă deoarece modelul principal este momentan ocupat).* "
        except Exception as e_15:
            return f"Eroare: Ai depășit limita gratuită a cheii API (Quota Exceeded). Te rog generează o cheie nouă în Google AI Studio și pune-o în stânga."

# --- 4. INTERFAȚA VIZUALĂ (UI) ---
st.markdown("<h1 style='text-align: center; font-size: 3em;'>O2 STUDIO // VINTED</h1>", unsafe_allow_html=True)

col_stanga, col_dreapta = st.columns([1, 1.2], gap="large")

with col_stanga:
    st.markdown("### 🔑 AUTENTIFICARE")
    api_key = st.text_input("Introdu Cheia API Google:", type="password")
    
    st.markdown("### 📸 UPLOAD IMAGINI")
    imagini_upload = st.file_uploader("Încarcă 1-3 poze cu produsul", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

with col_dreapta:
    st.markdown("### 🏷️ DETALII PRODUS")
    c1, c2 = st.columns(2)
    with c1:
        nume = st.text_input("Nume Produs", placeholder="ex: Hanorac")
        brand = st.text_input("Brand")
        marime = st.text_input("Mărime")
    with c2:
        pret = st.text_input("Preț Dorit")
        stare = st.selectbox("Stare", ["Nou cu etichetă", "Foarte bună", "Bună", "Prezintă defecte"])
    
    detalii = st.text_area("Detalii Extra pentru AI")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ ANALIZEAZĂ ȘI GENEREAZĂ"):
    if not api_key:
        st.error("Pune Cheia API!")
    elif not nume:
        st.warning("Introdu numele produsului!")
    else:
        with st.spinner("🔍 Analizăm..."):
            date_produs = {
                "nume": nume, "brand": brand, "marime": marime, 
                "pret": pret, "stare": stare, "detalii": detalii
            }
            rezultat = genereaza_descriere_premium(api_key, date_produs, imagini_upload)
            st.markdown("### 📝 DESCRIEREA TA PREMIUM:")
            st.markdown(f'<div class="result-box">{rezultat}</div>', unsafe_allow_html=True)
