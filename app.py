import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Sayfa ayarı ve Bağlantı
st.set_page_config(page_title="Hızlı Sohbet", layout="centered")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")

db = firestore.client()

st.title("💬 Anlık Mesajlaşma")

# 2. Mesaj Gönderme Bölümü (Formsuz, doğrudan yapı)
user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
text = st.text_input("Mesajını buraya yaz:")

# Butona basıldığında yapılacak işlem
if st.button("GÖNDER"):
    if text:
        try:
            # Veriyi Firebase'e gönder
            db.collection('sohbet').add({
                'kim': user,
                'metin': text,
                'vakit': firestore.SERVER_TIMESTAMP
            })
            st.success("Mesaj iletildi!")
            # 1 saniye bekleyip sayfayı yenile (mesajın listede görünmesi için)
            st.rerun()
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
    else:
        st.warning("Mesaj boş olamaz!")

st.divider()

# 3. Mesajları Listeleme
st.subheader("Mesaj Geçmişi")
try:
    # Mesajları tarihe göre çek
    docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(15).get()
    
    for d in docs:
        m = d.to_dict()
        role = "user" if m.get('kim') == "Halim" else "assistant"
        with st.chat_message(role):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
except Exception as e:
    st.info("Henüz mesaj yok veya yüklenemedi.")
