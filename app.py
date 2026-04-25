import streamlit as st
import google.generativeai as genai

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Vinted Pro Style", page_icon="👗", layout="centered")

# CSS corectat (am schimbat unsafe_allow_index cu unsafe_allow_html la final)
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
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCȚIE GENERARE ---
def generate_vinted_text(api_key, data):
    try:
        genai.configure(api_key=api_key)
        # Folosim varianta cea mai sigură de nume pentru model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Ești un expert în vânzări pe Vinted cu stil {data['stil']}. 
        Creează o descriere pentru: {data['nume']}.
        Detalii: Brand: {data['brand']}, Mărime: {data['marime']}, Stare: {data['stare']}, Preț: {data['pret']}.
        Info extra: {data['detalii']}.
        Folosește emoji-uri, bullet points și un ton care să convingă cumpărătorul.
        Adaugă 5 hashtag-uri la final.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Atenție! AI-ul a raportat o eroare: {str(e)}"

# --- UI APLICAȚIE ---
st.title("👗 Vinted AI Stylist")
st.write("Creează descrieri care vând, în câteva secunde!")

with st.sidebar:
    st.header("🔑 Setări")
    api_key = st.text_input("Cheie API Google:", type="password", help="Ia cheia de pe AI Studio")
    st.divider()
    st.caption("Aplicația ta este acum live! 🚀")

# Layout Formular
col1, col2 = st.columns(2)
with col1:
    nume = st.text_input("📦 Produs", placeholder="ex: Rochie de vară")
    brand = st.text_input("🏷️ Brand", placeholder="ex: H&M")
with col2:
    marime = st.text_input("📏 Mărime", placeholder="ex: S / 36")
    pret = st.text_input("💰 Preț", placeholder="ex: 45 RON")

stare = st.select_slider("💎 Stare produs", options=["Satisfăcătoare", "Bună", "Foarte bună", "Nou fără etichetă", "Nou cu etichetă"])
stil = st.radio("🎨 Tonul descrierii", ["Persuasiv", "Minimalist", "Prietenos"], horizontal=True)
detalii = st.text_area("📝 Alte detalii (material, defecte, etc.)")

if st.button("🚀 GENEREAZĂ DESCRIEREA"):
    if not api_key:
        st.error("Te rugăm să introduci cheia API în meniul din stânga!")
    elif not nume:
        st.warning("Te rog introdu numele produsului.")
    else:
        with st.spinner("🪄 Se scrie descrierea..."):
            text_final = generate_vinted_text(api_key, {
                "nume": nume, "brand": brand, "marime": marime, 
                "pret": pret, "stare": stare, "stil": stil, "detalii": detalii
            })
            st.markdown("### ✨ Rezultat:")
            # Afișăm rezultatul frumos în cutia noastră stilizată
            st.markdown(f'<div class="description-box">{text_final}</div>', unsafe_allow_html=True)
