import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. ANAHTARI DOĞRUDAN KODA YAZDIK
# Fazladan olan dıştaki süslü parantezleri kaldırdık
key_dict = {
  "type": "service_account",
  "project_id": "ozel-mesaj-app",
  "private_key_id": "94192de7b0d4555b799de6fadb5027feb4d8a42a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDXOOEzb3rMOqiJ\nngp7oqLNPgiVsJKbzW/CxDMQqVo+U6xqjxtf9rybD0jx5gnV2hLtxS51AsZQcbspK\nnnWYuxN0ToOH1f+jx/SkJ1kAuPfa5L1svqMXF1MIF9WiZ...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@ozel-mesaj-app.iam.gserviceaccount.com",
  "client_id": "108796016460187663405",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ozel-mesaj-app.iam.gserviceaccount.com",
  "universe_domain": "googleapi.com"
}

# 2. BAĞLANTI (Hata riskini sıfıra indirdik)
if not firebase_admin._apps:
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("🚀 Kesin Çalışan Panel")

# 3. MESAJ GÖNDERME
with st.container():
    kim = st.selectbox("Ben kimsini?", ["Halim", "Arkadaşım"])
    metin = st.text_input("Mesajınız:")
    if st.button("ŞİMDİ GÖNDER"):
        if metin:
            db.collection('sohbet').add({
                'kim': kim, 
                'metin': metin,
                'vakit': firestore.SERVER_TIMESTAMP # Zamanı Firebase kendisi versin
            })
            st.success("Veri başarıyla iletildi!")
            st.rerun()

# 4. LİSTELEME
st.write("---")
docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(10).get()

for d in docs:
    m = d.to_dict()
    st.info(f"**{m.get('kim')}:** {m.get('metin')}")
