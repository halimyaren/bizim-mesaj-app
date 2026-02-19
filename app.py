import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Bağlantısı
if not firebase_admin._apps:
    try:
        # Secrets'tan verileri çek
        key_dict = dict(st.secrets["firebase"])
        
        # ANAHTAR DÜZELTME: \n karakterlerini gerçek satır sonuna çevirir
        raw_key = key_dict["private_key"]
        key_dict["private_key"] = raw_key.replace("\\n", "\n")
        
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"⚠️ Bağlantı Hatası: {e}")

db = firestore.client()

# ARAYÜZ
st.title("💬 Bizim Özel Sohbet")

# Mesaj Gönderimi
with st.form("chat_form", clear_on_submit=True):
    user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
    msg = st.text_input("Mesajını yaz:")
    if st.form_submit_button("GÖNDER"):
        if msg:
            db.collection('sohbet').add({
                'kim': user,
                'metin': msg,
                'vakit': firestore.SERVER_TIMESTAMP
            })
            st.rerun()

# Mesajları Listele
st.write("---")
try:
    docs = db.collection('sohbet').limit(30).get()
    # Zaman damgasına göre sırala
    msgs = sorted([d.to_dict() for d in docs], key=lambda x: str(x.get('vakit', '')))
    
    for m in msgs:
        with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
except:
    st.info("Henüz mesaj yok.")
