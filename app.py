import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# FIREBASE BAĞLANTI (Secrets'tan Okuma)
if not firebase_admin._apps:
    # Secrets içindeki bilgileri sözlük formatına çeviriyoruz
    key_dict = dict(st.secrets["firebase"])
    # private_key içindeki çift kaçış karakterlerini (\n) düzeltiyoruz
    key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("💬 Güvenli Sohbet Hattı")

# Mesaj Gönderimi
with st.form("mesaj_formu", clear_on_submit=True):
    kim = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
    metin = st.text_area("Mesajın:")
    gonder = st.form_submit_button("GÖNDER")
    
    if gonder and metin:
        db.collection('sohbet').add({
            'kim': kim,
            'metin': metin,
            'vakit': firestore.SERVER_TIMESTAMP
        })
        st.rerun()

# Mesaj Listeleme
st.write("---")
docs = db.collection('sohbet').limit(40).get()
mesajlar = [d.to_dict() for d in docs]
sirali = sorted(mesajlar, key=lambda x: str(x.get('vakit', '')))

for m in sirali:
    with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
        st.write(f"**{m.get('kim')}:** {m.get('metin')}")
