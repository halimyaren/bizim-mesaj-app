import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# 1. VERİTABANI BAĞLANTISI
if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. SAYFA AYARLARI
st.set_page_config(page_title="Bizim Sohbet", layout="centered")

# 3. GİRİŞ SİSTEMİ (Şifre Paneli)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Giriş Yap")
    sifre = st.text_input("Giriş Şifresini Yazın:", type="password")
    if sifre == "bizim-ozel-sifre": # Şifreni buradan değiştirebilirsin
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()

# 4. SOHBET ARAYÜZÜ (Şifre geçildikten sonra burası çalışır)
st.title("💬 Özel Mesaj Hattı")

# Sol menüden kimlik seçimi
me = st.sidebar.selectbox("Sen kimsini?", ["Seçiniz", "Halim", "Arkadaşım"], key="user_select")

# Mesaj yazma kutusu (HER ZAMAN GÖRÜNSÜN)
yeni_mesaj = st.chat_input("Mesajınızı buraya yazın...")

if me != "Seçiniz":
    st.write(f"Hoş geldin, **{me}**")
    
    # Mesaj gönderme işlemi
    if yeni_mesaj:
        db.collection('sohbet').add({
            'kim': me,
            'metin': yeni_mesaj,
            'vakit': datetime.now()
        })
        st.rerun()

    # Mesajları veritabanından çekme
    st.write("---")
    messages_ref = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(30)
    messages = messages_ref.stream()
st_autorefresh(interval=5000, key="datarefresh")
    # Mesajları baloncuk şeklinde göster
    for msg in reversed(list(messages)):
        data = msg.to_dict()
        with st.chat_message("user" if data['kim'] == me else "assistant"):
            st.write(f"**{data['kim']}:** {data['metin']}")
else:
    st.info("Lütfen soldaki menüden isminizi seçerek sohbete başlayın.")

