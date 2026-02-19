import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase'i temiz bir şekilde başlat
if not firebase_admin._apps:
    try:
        # Yeni key.json dosyasını kullanıyoruz
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Bağlantı kurulamadı: {e}")

db = firestore.client()

st.title("💬 Sohbet Paneli")

# Mesaj Gönderimi
user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
text = st.text_input("Mesajını yaz:")

if st.button("GÖNDER"):
    if text:
        try:
            # Zaman aşımı riskine karşı basit bir ekleme
            db.collection('sohbet').add({
                'kim': user,
                'metin': text,
                'vakit': firestore.SERVER_TIMESTAMP
            })
            st.success("Mesaj başarıyla iletildi!")
            st.rerun()
        except Exception as e:
            st.error(f"Gönderim hatası: {e}")
