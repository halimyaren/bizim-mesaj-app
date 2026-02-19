import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Sayfa Ayarları
st.set_page_config(page_title="Bizim Sohbet", layout="centered")

# 1. Firebase Bağlantısını Kur (Dosyadan Okuma)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"❌ Firebase anahtar dosyası (key.json) bulunamadı veya hatalı: {e}")

db = firestore.client()

st.title("💬 Özel Mesaj Paneli")

# 2. Mesaj Gönderimi
with st.container():
    # Kimlik seçimi
    user = st.selectbox("Ben Kimim?", ["Halim", "Arkadaşım"])
    # Mesaj girişi
    text = st.text_input("Mesajını yaz ve Enter'a bas:")
    
    if st.button("ŞİMDİ GÖNDER") and text:
        try:
            # Firebase'e ekle
            db.collection('sohbet').add({
                'kim': user,
                'metin': text,
                'vakit': firestore.SERVER_TIMESTAMP
            })
            st.success("Mesaj gönderildi!")
            st.rerun() # Sayfayı yenile ki mesaj listede görünsün
        except Exception as e:
            st.error(f"⚠️ Mesaj gönderilemedi: {e}")

st.divider()

# 3. Mesajları Listeleme
st.subheader("Mesaj Geçmişi")
try:
    # Mesajları tarihe göre tersten çek
    docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(20).get()
    
    for d in docs:
        m = d.to_dict()
        # Halim'in mesajları sağda, arkadaşınınki solda gibi göster
        is_halim = m.get('kim') == "Halim"
        with st.chat_message("user" if is_halim else "assistant"):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
except Exception as e:
    st.info("Henüz mesaj yok, ilk mesajı sen yaz!")
