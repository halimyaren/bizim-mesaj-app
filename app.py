import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_autorefresh import st_autorefresh

# 1. BAĞLANTI (Hata mesajlarını gizle, sadece çalışmaya odaklan)
if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. AYARLAR
st.set_page_config(page_title="Hızlı Mesaj")
st_autorefresh(interval=3000, key="refresh")

# 3. KİMLİK
me = st.sidebar.selectbox("Kimsin?", ["Seçiniz", "Halim", "Arkadaşım"])

if me != "Seçiniz":
    # MESAJ GÖNDERME
    yeni = st.chat_input("Mesaj yaz...")
    if yeni:
        db.collection('sohbet').add({'kim': me, 'metin': yeni})
        st.rerun()

    # MESAJLARI ÇEKME (Hatasız en basit yöntem)
    docs = db.collection('sohbet').get() # Hiçbir sıralama kuralı koymadık!
    
    for d in docs:
        m = d.to_dict()
        with st.chat_message("user" if m['kim'] == me else "assistant"):
            st.write(f"**{m['kim']}:** {m['metin']}")
