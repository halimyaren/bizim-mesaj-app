import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Bağlantısı
if not firebase_admin._apps:
    try:
        # Secrets'tan veriyi çek ve sözlüğe çevir
        key_dict = dict(st.secrets["firebase"])
        # Gizli karakterleri (\n) Python'un anlayacağı hale getir
        key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Bağlantı Kurulamadı: {e}")

db = firestore.client()

st.title("💬 Bizim Sohbet")

# Mesaj Yazma
with st.form("chat_form", clear_on_submit=True):
    user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
    text = st.text_input("Mesaj:")
    if st.form_submit_button("GÖNDER"):
        if text:
            db.collection('sohbet').add({
                'kim': user, 'metin': text, 'vakit': firestore.SERVER_TIMESTAMP
            })
            st.rerun()

# Mesajları Çekme (Hata almamak için basit sıralama)
st.write("---")
docs = db.collection('sohbet').limit(30).get()
msgs = sorted([d.to_dict() for d in docs], key=lambda x: str(x.get('vakit', '')))

for m in msgs:
    with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
        st.write(f"**{m.get('kim')}:** {m.get('metin')}")
