import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. FIREBASE BAĞLANTISI
if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. SAYFA AYARLARI VE OTOMATİK YENİLEME
st.set_page_config(page_title="Bizim Sohbet", layout="centered")
st_autorefresh(interval=3000, key="datarefresh") # 3 saniyede bir ekranı günceller

# 3. ŞİFRE GİRİŞİ
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    sifre = st.text_input("Giriş Şifresi", type="password")
    if sifre == "1234": # Şifreniz
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# 4. SOHBET EKRANI
st.title("💬 Özel Mesaj Hattı")
me = st.sidebar.selectbox("Sen kimsini?", ["Seçiniz", "Halim", "Arkadaşım"])

if me != "Seçiniz":
    yeni_mesaj = st.chat_input("Mesajınızı buraya yazın...")
    
    # Mesaj Gönderme
    if yeni_mesaj:
        db.collection('sohbet').add({
            'kim': me,
            'metin': yeni_mesaj,
            'vakit': datetime.now()
        })
        st.rerun()

    # Mesajları Getirme (Sıralama hatası almamak için şimdilik sadeleştirdik)
    messages = db.collection('sohbet').limit(20).stream()
    
    # Mesajları Vakit Bilgisine Göre Elimizle Sıralayalım
    chat_list = []
    for m in messages:
        chat_list.append(m.to_dict())
    
    # Mesajları zamana göre diz (Eski en üstte, yeni en altta)
    sorted_chat = sorted(chat_list, key=lambda x: x.get('vakit', datetime.now()))

    for data in sorted_chat:
        with st.chat_message("user" if data['kim'] == me else "assistant"):
            st.write(f"**{data['kim']}:** {data['metin']}")
else:
    st.info("Sohbete başlamak için soldan isminizi seçin.")
