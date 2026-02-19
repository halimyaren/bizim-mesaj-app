import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Bağlantısı (Secrets üzerinden)
if not firebase_admin._apps:
    try:
        # Secrets'tan bilgileri al ve sözlüğe çevir
        key_data = dict(st.secrets["firebase"])
        # Anahtar içindeki \n karakterlerini düzelt
        key_data["private_key"] = key_data["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(key_data)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Bağlantı kurulamadı: {e}")

db = firestore.client()

st.title("💬 Bizim Sohbet")

# Mesaj Gönderimi
user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
text = st.text_input("Mesaj:")

if st.button("GÖNDER"):
    if text:
        try:
            db.collection('sohbet').add({
                'kim': user,
                'metin': text,
                'vakit': firestore.SERVER_TIMESTAMP
            })
            st.success("Gitti!")
            st.rerun()
        except Exception as e:
            st.error(f"Hata: {e}")

# Mesajları Listele
st.divider()
docs = db.collection('sohbet').limit(20).get()
for d in docs:
    m = d.to_dict()
    st.write(f"**{m.get('kim')}:** {m.get('metin')}")
