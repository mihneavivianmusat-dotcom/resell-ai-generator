import streamlit as st
import google.generativeai as genai

# Configurare Pagina
st.set_page_config(page_title="Vinted Pro Seller Tool", page_icon="🛍️")

# Titlu și Design
st.title("🛍️ Generator de Descrieri Vinted AI")
st.markdown("Introdu detaliile mai jos și lasă AI-ul să facă magia!")

# Introducerea cheii API (o vei pune aici)
api_key = st.text_input("Introdu Cheia ta Google API:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Interfața de tip Formular
    col1, col2 = st.columns(2)

    with col1:
        nume = st.text_input("Ce vinzi?", placeholder="ex: Geacă de piele Levi's")
        brand = st.text_input("Brand", placeholder="ex: Levi's")
        pret = st.text_input("Preț (RON/EUR)", placeholder="ex: 150 RON")

    with col2:
        stare = st.selectbox("Starea produsului", ["Nou cu etichetă", "Nou fără etichetă", "Foarte bună", "Bună", "Satisfăcătoare"])
        marime = st.text_input("Mărime", placeholder="ex: M / 38")
        stil = st.multiselect("Stil / Vibes", ["Vintage", "Casual", "Elegant", "Sport", "Streetwear", "Minimalist"])

    defecte = st.text_area("Defecte sau detalii extra", placeholder="ex: Are o mică pată pe mâneca stângă, invizibilă la purtare.")

    # Butonul Magic
    if st.button("✨ Generează Descrierea"):
        if nume:
            with st.spinner('AI-ul scrie descrierea...'):
                prompt = f"""
                Ești un vânzător de top pe Vinted. Scrie o descriere extrem de atractivă, 
                onestă și structurată pentru: {nume}.
                Brand: {brand}, Mărime: {marime}, Stare: {stare}, Preț: {pret}.
                Detalii suplimentare: {defecte}. Stil: {', '.join(stil)}.
                Folosește emoji-uri, bullet points și un ton prietenos. 
                Include și 5 hashtag-uri relevante la final.
                """
                response = model.generate_content(prompt)
                
                st.success("Gata! Iată descrierea ta:")
                st.text_area("Copy-Paste de aici:", value=response.text, height=300)
        else:
            st.error("Te rog introdu măcar numele produsului!")
