import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Bizim Sohbet", layout="centered")

# 2. ŞİFRE KONTROLÜ (Yenilemede gitmemesi için)
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False

if not st.session_state.giris_yapildi:
    st.title("🔒 Giriş")
    sifre = st.text_input("Şifrenizi yazın:", type="password")
    if st.button("Giriş Yap"):
        if sifre == "1234": # Buraya kendi şifreni yaz
            st.session_state.giris_yapildi = True
            st.rerun()
        else:
            st.error("Hatalı şifre!")
    st.stop()

# 3. FIREBASE BAĞLANTISI
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('key.json')
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")

db = firestore.client()

# 4. OTOMATİK YENİLEME (5 saniyede bir)
st_autorefresh(interval=5000, key="chat_update")

# 5. SOHBET ARAYÜZÜ
st.title("💬 Özel Mesaj Hattı")
me = st.sidebar.selectbox("Kimsin?", ["Seçiniz", "Halim", "Arkadaşım"])

if me != "Seçiniz":
    yeni_mesaj = st.chat_input("Mesajınızı yazın...")
    
    if yeni_mesaj:
        # Mesajı veritabanına ekle
        db.collection('sohbet').add({
            'kim': me,
            'metin': yeni_mesaj,
            'vakit': datetime.now()
        })
        st.rerun()

    # Mesajları en basit şekilde çek (Sıralama hatası almamak için)
    docs = db.collection('sohbet').limit(20).get()
    
    mesajlar = []
    for d in docs:
        mesajlar.append(d.to_dict())
    
    # Vakit bilgisine göre kod içinde sırala
    mesajlar.sort(key=lambda x: str(x.get('vakit', '')))

    for m in mesajlar:
        kim = m.get('kim', 'Bilinmeyen')
        metin = m.get('metin', '')
        with st.chat_message("user" if kim == me else "assistant"):
            st.write(f"**{kim}:** {metin}")
