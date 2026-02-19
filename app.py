import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. FIREBASE BAĞLANTISI (Hata Payı Sıfır)
if not firebase_admin._apps:
    # Karakter hatalarını önlemek için anahtarı temiz bir şekilde tanımlıyoruz
    key_info = {
        "type": "service_account",
        "project_id": "ozel-mesaj-app",
        "private_key_id": "94192de7b0d4555b799de6fadb5027feb4d8a42a",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDXOOEzb3rMOqiJ\nngp7oqLNPgiVsJKbzW/CxDMQqVo+U6xqjxtf9rybD0jx5gnV2hLtxS51AsZQcbspK\nnnWYuxN0ToOH1f+jx/SkJ1kAuPfa5L1svqMXF1MIF9WiZ\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-fbsvc@ozel-mesaj-app.iam.gserviceaccount.com",
        "client_id": "108796016460187663405",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ozel-mesaj-app.iam.gserviceaccount.com"
    }
    
    try:
        cred = credentials.Certificate(key_info)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"⚠️ Anahtar Hatası: {e}")

db = firestore.client()

# 2. ARAYÜZ
st.title("💬 Canlı Sohbet Paneli")

# Mesaj Gönderimi
with st.container():
    user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
    msg = st.text_input("Mesajını yaz ve Enter'a bas:")
    
    if msg:
        db.collection('sohbet').add({
            'kim': user,
            'metin': msg,
            'vakit': firestore.SERVER_TIMESTAMP # Zamanı Firebase ayarlar
        })
        st.rerun()

# 3. MESAJLARI GÖSTER
st.write("---")
try:
    # En yeni 25 mesajı çek (Sıralama hatasını önlemek için sade tutuldu)
    docs = db.collection('sohbet').limit(25).get()
    
    for d in docs:
        m = d.to_dict()
        with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
except Exception as e:
    st.info("Mesajlar yükleniyor...")

# Yenileme Butonu
if st.button("🔄 Mesajları Tazele"):
    st.rerun()
