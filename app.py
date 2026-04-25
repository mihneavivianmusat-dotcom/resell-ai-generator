import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Vinted Pro O2 Studio", page_icon="🏜️", layout="wide")

# --- 2. STILIZARE AVANSATĂ (GLASSMORPHISM & BACKGROUND) ---
st.markdown("""
    <style>
    /* Fundalul principal - un deșert stâncos la apus similar cu imaginea ta */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1509316785289-025f5b846b35?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Ascundem elementele standard de sus pentru un look mai curat */
    header {visibility: hidden;}
    
    /* Stilizarea textului principal pentru a fi vizibil pe fundal */
    h1, h2, h3, p, label {
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
    }

    /* Efectul de Glassmorphism (Sticlă mată) pentru containere */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    /* Stilizare butoane (Stilul alb/turcoaz rotunjit) */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        background-color: #ffffff;
        color: #1a1a1a !important;
        font-weight: 800;
        font-size: 16px;
        border: none;
        padding: 12px;
        transition: 0.3s all ease-in-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #e0e0e0;
        transform: translateY(-2px);
    }
    
    /* Caseta rezultatului final */
    .result-box {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        padding: 25px;
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        font-family: 'Helvetica', sans-serif;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCȚIA DE INTELIGENȚĂ ARTIFICIALĂ ---
def genereaza_descriere_premium(api_key, date_text, imagini_incarcate):
    genai.configure(api_key=api_key)
    
    # Procesăm imaginile încărcate (le transformăm într-un format pe care AI-ul îl înțelege)
    poze_procesate = []
    for fisier in imagini_incarcate:
        poze_procesate.append(Image.open(fisier))

    # Construim instrucțiunile (Prompt-ul)
    prompt = f"""
    Ești un expert Vinted și cercetător de modă. 
    Avem produsul: '{date_text['nume']}', Brand: '{date_text['brand']}', Mărime: '{date_text['marime']}', Preț dorit: '{date_text['pret']}', Stare: '{date_text['stare']}'.
    Detalii extra date de utilizator: {date_text['detalii']}.

    Sarcini pentru tine:
    1. ANALIZĂ VIZUALĂ: Uită-te la imaginile atașate. Ce culoare exactă are? Ce textură pare să aibă materialul? Observi vreun defect sau detaliu special (fermoare, logo-uri)?
    2. DEEP RESEARCH (Căutare Web): Caută pe internet informații despre acest tip de produs de la acest brand. Ce spun pasionații? Care era prețul original estimativ în magazin? Ce cuvinte cheie folosesc brandurile pentru a-l vinde?
    3. REDACTARE: Folosind informațiile din poze, căutarea pe net și detaliile mele, scrie o descriere Vinted excepțională, sinceră, cu emoji-uri și formatare curată. Include 5-7 hashtag-uri foarte căutate.

    Nu îmi scrie procesul tău de gândire, ci DOAR descrierea finală gata de pus pe site.
    """

    lista_continut = [prompt] + poze_procesate # Combinăm textul cu pozele

    # Sistemul "Fallback" (Încearcă modelul de top, dacă e ocupat, trece la cel de rezervă)
    try:
        # Încercăm modelul Suprem (Gemini 2.0 Flash) activând Căutarea pe Google
        model = genai.GenerativeModel('gemini-2.0-flash', tools='google_search')
        raspuns = model.generate_content(lista_continut)
        return raspuns.text
    except Exception as e_20:
        try:
            # Dacă dă eroare (Quota/429), încercăm modelul 1.5 Flash (mai stabil la conturi gratuite)
            model_fallback = genai.GenerativeModel('gemini-1.5-flash-latest')
            raspuns = model_fallback.generate_content(lista_continut)
            return raspuns.text + "\n\n*(Notă: Generat cu modelul de rezervă deoarece modelul principal efectua un update).* "
        except Exception as e_15:
            return f"Ne pare rău, ambele servere AI sunt suprasolicitate acum. Eroare: {e_15}"

# --- 4. INTERFAȚA VIZUALĂ (UI) ---
st.markdown("<h1 style='text-align: center; font-size: 3em;'>O2 STUDIO // VINTED</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 2px;'>AI DEEP RESEARCH & MULTIMODAL VISION</p>", unsafe_allow_html=True)

# Layout principal în 2 coloane
col_stanga, col_dreapta = st.columns([1, 1.2], gap="large")

with col_stanga:
    st.markdown("### 🔑 AUTENTIFICARE")
    api_key = st.text_input("Introdu Cheia API Google:", type="password")
    
    st.markdown("### 📸 UPLOAD IMAGINI")
    st.caption("AI-ul va scana aceste imagini pentru detalii, culori și defecte.")
    imagini_upload = st.file_uploader("Încarcă 1-3 poze cu produsul", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if imagini_upload:
        st.success(f"Ai încărcat {len(imagini_upload)} imagini.")

with col_dreapta:
    st.markdown("### 🏷️ DETALII PRODUS")
    c1, c2 = st.columns(2)
    with c1:
        nume = st.text_input("Nume Produs", placeholder="ex: Nike Air Max 97")
        brand = st.text_input("Brand", placeholder="ex: Nike")
        marime = st.text_input("Mărime", placeholder="ex: 42.5 / US 9")
    with c2:
        pret = st.text_input("Preț Dorit", placeholder="ex: 300 RON")
        stare = st.selectbox("Stare", ["Nou cu cutie/etichetă", "Purtat o dată", "Foarte bună", "Bună", "Prezintă defecte"])
    
    detalii = st.text_area("Detalii Extra pentru AI", placeholder="Spune-i AI-ului orice altceva (ex: livrez doar cu curier, preț fix, e din colecția 2022)")

st.markdown("<br>", unsafe_allow_html=True)

# Butonul Magic
if st.button("✨ ANALIZEAZĂ ȘI GENEREAZĂ"):
    if not api_key:
        st.error("Lipsă Cheie API! Te rugăm să o introduci în stânga.")
    elif not nume:
        st.warning("Introdu măcar numele produsului!")
    else:
        with st.spinner("🔍 AI-ul analizează pozele și caută pe net... Te rog așteaptă!"):
            date_produs = {
                "nume": nume, "brand": brand, "marime": marime, 
                "pret": pret, "stare": stare, "detalii": detalii
            }
            rezultat = genereaza_descriere_premium(api_key, date_produs, imagini_upload)
            
            st.markdown("### 📝 DESCRIEREA TA PREMIUM:")
            st.markdown(f'<div class="result-box">{rezultat}</div>', unsafe_allow_html=True)
