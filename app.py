import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. ANAHTARI DÜZELTTİK (Fazla parantezler kaldırıldı)
key_dict = {
  "type": "service_account",
  "project_id": "ozel-mesaj-app",
  "private_key_id": "94192de7b0d4555b799de6fadb5027feb4d8a42a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDXOOEzb3rMOqiJ\nngp7oqLNPgiVsJKbzW/CxDMQqVo+U6xqjxtf9rybD0jx5gnV2hLtxS51AsZQcbspK\nnnWYuxN0ToOH1f+jx/SkJ1kAuPfa5L1svqMXF1MIF9WiZ\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@ozel-mesaj-app.iam.gserviceaccount.com",
  "client_id": "108796016460187663405",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ozel-mesaj-app.iam.gserviceaccount.com",
  "universe_domain": "googleapi.com"
}

# 2. FIREBASE BAĞLANTISI
if not firebase_admin._apps:
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# 3. ARAYÜZ
st.title("💬 Özel Mesaj Paneli")

# Mesaj Gönderme
with st.form("mesaj_formu", clear_on_submit=True):
    kim = st.selectbox("Ben kimsin?", ["Halim", "Arkadaşım"])
    metin = st.text_area("Mesajınız:")
    gonder = st.form_submit_button("ŞİMDİ GÖNDER")
    
    if gonder and metin:
        db.collection('sohbet').add({
            'kim': kim,
            'metin': metin,
            'vakit': firestore.SERVER_TIMESTAMP
        })
        st.success("Mesaj başarıyla iletildi!")
        st.rerun()

# 4. MESAJLARI LİSTELEME
st.write("---")
st.subheader("Gelen Mesajlar")

# En yeni 20 mesajı çekiyoruz
docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(20).get()

for d in docs:
    m = d.to_dict()
    # Kimden geldiyse ona göre balon rengi
    if m.get('kim') == "Halim":
        st.info(f"**Halim:** {m.get('metin')}")
    else:
        st.warning(f"**Arkadaşım:** {m.get('metin')}")

# Sayfayı manuel yenilemek için buton
if st.sidebar.button("Mesajları Tazele"):
    st.rerun()
