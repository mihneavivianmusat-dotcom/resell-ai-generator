import streamlit as st
import google.generativeai as genai

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Vinted Pro Style 2026", page_icon="👗", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #008291, #00a5b5);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); background: #005f69; }
    .description-box {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #333;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCȚIE GENERARE ---
def generate_vinted_text(api_key, data):
    try:
        genai.configure(api_key=api_key)
        
        # Am actualizat modelul la versiunea 2.0 Flash, care este mult mai stabilă acum
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Ești un vânzător de elită pe Vinted. Stilul tău este {data['stil']}.
        Produs: {data['nume']}
        Brand: {data['brand']} | Mărime: {data['marime']} | Stare: {data['stare']} | Preț: {data['pret']}
        Detalii importante: {data['detalii']}
        
        Cerințe:
        1. Structură clară cu emoji-uri.
        2. Ton prietenos și convingător.
        3. Menționează că livrarea se face rapid.
        4. Adaugă 5 hashtag-uri relevante.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Dacă nici 2.0 nu merge, încercăm varianta "flash-latest" automat
        try:
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(prompt)
            return response.text
        except:
            return f"Eroare tehnică: {str(e)}. Verifică dacă ai activat Gemini API în Google AI Studio."

# --- UI ---
st.title("👗 Vinted AI Stylist")
st.write("Generăm descrieri profesionale în timp ce tu pregătești coletul.")

with st.sidebar:
    st.header("🔑 Setări")
    api_key = st.text_input("Cheie API Google:", type="password")
    st.info("Sfat: Folosește Gemini 2.0 pentru rezultate mai bune.")

col1, col2 = st.columns(2)
with col1:
    nume = st.text_input("📦 Ce vinzi?", placeholder="ex: Blazer elegant")
    brand = st.text_input("🏷️ Brand", placeholder="ex: Massimo Dutti")
with col2:
    marime = st.text_input("📏 Mărime", placeholder="ex: L / 40")
    pret = st.text_input("💰 Preț", placeholder="ex: 120 RON")

stare = st.select_slider("💎 Stare", options=["Satisfăcătoare", "Bună", "Foarte bună", "Nou fără etichetă", "Nou cu etichetă"])
stil = st.radio("🎨 Stil text", ["Persuasiv", "Minimalist", "Prietenos"], horizontal=True)
detalii = st.text_area("📝 Detalii extra (material, defecte)")

if st.button("🚀 GENEREAZĂ"):
    if not api_key:
        st.error("Introdu cheia API!")
    elif not nume:
        st.warning("Introdu numele produsului!")
    else:
        with st.spinner("🪄 Se scrie descrierea..."):
            text_final = generate_vinted_text(api_key, {
                "nume": nume, "brand": brand, "marime": marime, 
                "pret": pret, "stare": stare, "stil": stil, "detalii": detalii
            })
            st.markdown("### ✨ Rezultat:")
            st.markdown(f'<div class="description-box">{text_final}</div>', unsafe_allow_html=True)
        
