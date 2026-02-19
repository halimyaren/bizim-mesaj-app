import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Firebase'i dosyadan başlat
if not firebase_admin._apps:
    try:
        # Dosya adının 'key.json' olduğundan emin ol
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Dosya okunamadı! Hata: {e}")

db = firestore.client()

# 2. Arayüz
st.set_page_config(page_title="Bizim Mesajlar", page_icon="💬")
st.title("💬 Özel Mesajlaşma")

# Mesaj Yazma Bölümü
with st.container():
    user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
    text = st.text_input("Mesajını buraya yaz...")
    
    if st.button("GÖNDER") and text:
        db.collection('sohbet').add({
            'kim': user,
            'metin': text,
            'vakit': firestore.SERVER_TIMESTAMP
        })
        st.rerun()

st.divider()

# 3. Mesajları Listeleme
try:
    # Son 20 mesajı çek
    docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(20).get()
    
    for d in docs:
        m = d.to_dict()
        role = "user" if m.get('kim') == "Halim" else "assistant"
        with st.chat_message(role):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
except Exception as e:
    st.info("İlk mesajı sen yaz!")
