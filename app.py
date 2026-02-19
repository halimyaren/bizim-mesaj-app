import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. BAĞLANTI
if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("Mesaj Test Paneli")

# 2. MESAJ GÖNDERME
kim = st.selectbox("Ben kimsini?", ["Halim", "Arkadaşım"])
metin = st.text_input("Mesajın:")
if st.button("GÖNDER"):
    db.collection('sohbet').add({'kim': kim, 'metin': metin})
    st.success("Veritabanına yazıldı!")

st.write("---")
st.subheader("Gelen Mesajlar:")

# 3. MESAJLARI ÇEKME (En ilkel ve garantili yol)
docs = db.collection('sohbet').get()
for d in docs:
    m = d.to_dict()
    st.write(f"{m.get('kim')}: {m.get('metin')}")

# 4. YENİLEME BUTONU (Otomatik yenilemeyi şimdilik kapattık, sorun çıkmasın)
if st.button("MESAJLARI TAZELE"):
    st.rerun()
