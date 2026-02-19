import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. BAĞLANTIYI KONTROL ET (Hata yakalayıcı ekledik)
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate('key.json')
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    st.error(f"Veritabanı bağlantı hatası: {e}")
    st.stop()

# 2. SAYFA AYARLARI VE OTOMATİK YENİLEME
st.set_page_config(page_title="Bizim Sohbet", layout="centered")
st_autorefresh(interval=3000, key="datarefresh") # 3 saniyede bir kontrol eder

# 3. GİRİŞ KONTROLÜ
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    sifre = st.text_input("Giriş Şifresini Yazın:", type="password")
    if sifre == "1234": # Şifreni buraya ne yazdıysan o olmalı!
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()

# 4. SOHBET
st.title("💬 Özel Mesaj Hattı")
me = st.sidebar.selectbox("Sen kimsin?", ["Seçiniz", "Halim", "Arkadaşım"], key="user_choice")

yeni_mesaj = st.chat_input("Mesajınızı buraya yazın...")

if me != "Seçiniz":
    if yeni_mesaj:
        try:
            # Firestore'a veri ekleme denemesi
            db.collection('sohbet').add({
                'kim': me,
                'metin': yeni_mesaj,
                'vakit': datetime.now()
            })
        except Exception as e:
            st.error(f"Mesaj gönderilemedi: {e}")

    # Mesajları Göster
    messages_ref = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(20)
    messages = messages_ref.stream()
    
    for msg in reversed(list(messages)):
        data = msg.to_dict()
        with st.chat_message("user" if data['kim'] == me else "assistant"):
            st.write(f"**{data['kim']}:** {data['metin']}")
