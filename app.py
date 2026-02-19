import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. SAYFA AYARLARI (En üstte olmalı)
st.set_page_config(page_title="Bizim Sohbet", layout="centered")

# 2. FIREBASE BAĞLANTISI
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('key.json')
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")

db = firestore.client()

# 3. ŞİFRE SİSTEMİ (Hafızada tutma odaklı)
if "login_ok" not in st.session_state:
    st.session_state.login_ok = False

if not st.session_state.login_ok:
    st.title("🔒 Giriş")
    sifre_input = st.text_input("Şifre Girin", type="password")
    if st.button("Giriş Yap"):
        if sifre_input == "1234": # Şifreniz
            st.session_state.login_ok = True
            st.rerun()
        else:
            st.error("Hatalı Şifre!")
    st.stop()

# 4. OTOMATİK YENİLEME (Şifreden sonra çalışsın)
st_autorefresh(interval=5000, key="chat_refresh")

# 5. SOHBET ARAYÜZÜ
st.title("💬 Özel Mesaj Hattı")
me = st.sidebar.selectbox("Kimsin?", ["Seçiniz", "Halim", "Arkadaşım"])

if me != "Seçiniz":
    yeni_mesaj = st.chat_input("Mesajınızı buraya yazın...")
    
    if yeni_mesaj:
        # Veriyi sözlük olarak hazırla
        data = {
            'kim': me,
            'metin': yeni_mesaj,
            'vakit': datetime.now()
        }
        # Firestore'a gönder
        db.collection('sohbet').add(data)
        st.rerun()

    # Mesajları listele
    docs = db.collection('sohbet').limit(30).stream()
    
    mesajlar = []
    for d in docs:
        m_data = d.to_dict()
        mesajlar.append(m_data)
    
    # Zamana göre sırala (Vakit bilgisi olmayanları sona at)
    mesajlar.sort(key=lambda x: x.get('vakit', datetime.now()))

    for m in mesajlar:
        is_me = (m.get('kim') == me)
        with st.chat_message("user" if is_me else "assistant"):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
