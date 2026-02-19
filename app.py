import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Basit bir giriş sistemi
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    sifre = st.text_input("Giriş Şifresini Yazın:", type="password")
    if sifre == "bizim-ozel-sifre": # Burayı istediğin bir şifreyle değiştir
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop() # Şifre doğru değilse uygulamayı burada durdur
# 1. VERİTABANI BAĞLANTISI (Burada hata alırsan dosya adı yanlıştır)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('key.json')
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Anahtar dosyası bulunamadı veya hatalı: {e}")

db = firestore.client()

# 2. SAYFA TASARIMI
st.set_page_config(page_title="Bizim Sohbet", layout="centered")
st.title("🔒 Özel Mesaj Hattı")

# Kimlik Seçimi
me = st.sidebar.selectbox("Sen kimsin?", ["Seçiniz", "Halim", "Arkadaşım"])

if me != "Seçiniz":
    # 3. MESAJLARI ÇEKME VE GÖSTERME
    st.write(f"Hoş geldin, **{me}**")
    
    # Veritabanından son 20 mesajı oku
    messages_ref = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(20)
    messages = messages_ref.stream()

    # Mesajları ekrana yazdır (En yeni en altta görünsün diye ters çeviriyoruz)
    chat_history = list(messages)
    for msg in reversed(chat_history):
        data = msg.to_dict()
        with st.chat_message("user" if data['kim'] == me else "assistant"):
            st.write(f"{data['kim']}: {data['metin']}")

    # 4. YENİ MESAJ GÖNDERME
    yeni_mesaj = st.chat_input("Mesajını buraya yaz...")
    if yeni_mesaj:
        db.collection('sohbet').add({
            'kim': me,
            'metin': yeni_mesaj,
            'vakit': datetime.now()
        })
        st.rerun() # Sayfayı yenile ki mesaj hemen görünsün
else:
    st.info("Lütfen soldan ismini seçerek sohbete katıl.")