import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. BAĞLANTI
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('key.json')
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Bağlantı Dosyası Hatası: {e}")

db = firestore.client()

# 2. SAYFA AYARLARI
st.set_page_config(page_title="Bizim Sohbet", layout="centered")
st_autorefresh(interval=3000, key="datarefresh")

# 3. GİRİŞ
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    sifre = st.text_input("Şifre", type="password")
    if sifre == "1234": # Şifren
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# 4. SOHBET
st.title("💬 Özel Mesaj")
me = st.sidebar.selectbox("Kimsin?", ["Seçiniz", "Halim", "Arkadaşım"])

if me != "Seçiniz":
    yeni_mesaj = st.chat_input("Mesaj yaz...")
    if yeni_mesaj:
        try:
        db.collection('sohbet').add({
                'kim': me,
                'metin': yeni_mesaj,
                'vakit': datetime.now()
            })
            st.toast(f"Mesaj gönderildi: {yeni_mesaj}") # Sağ altta küçük bir balon çıkar
            st.rerun()
        except Exception as e:
            st.error(f"Gönderim hatası: {e}")

    # Mesajları listeleme
    docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(20).stream()
    for msg in reversed(list(docs)):
        d = msg.to_dict()
        with st.chat_message("user" if d['kim'] == me else "assistant"):
            st.write(f"**{d['kim']}:** {d['metin']}")

