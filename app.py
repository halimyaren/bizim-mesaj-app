import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase bağlantısı
if not firebase_admin._apps:
    # Secrets'tan firebase başlığı altındaki her şeyi al
    key_dict = dict(st.secrets["firebase"])
    # private_key içindeki satır sonlarını düzelt
    key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("💬 Özel Mesaj Paneli")

# Mesaj yazma ve gönderme
with st.container():
    kim = st.radio("Ben kimsini?", ["Halim", "Arkadaşım"], horizontal=True)
    metin = st.text_input("Mesajınız:")
    if st.button("ŞİMDİ GÖNDER") and metin:
        db.collection('sohbet').add({
            'kim': kim,
            'metin': metin,
            'vakit': firestore.SERVER_TIMESTAMP
        })
        st.rerun()

# Mesajları listeleme
st.write("---")
docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(20).get()

for d in docs:
    m = d.to_dict()
    with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
        st.write(f"**{m.get('kim')}:** {m.get('metin')}")
