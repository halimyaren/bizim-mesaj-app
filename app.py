import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. BAĞLANTI AYARLARI
if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. SAYFA VE YENİLEME (5 Saniyede Bir)
st.set_page_config(page_title="Mesaj Uygulaması")
st_autorefresh(interval=5000, key="freshtime")

# 3. KİMLİK SEÇİMİ
me = st.sidebar.selectbox("Kimsin?", ["Seçiniz", "Halim", "Arkadaşım"])

if me != "Seçiniz":
    st.title(f"Hoş geldin {me}")
    
    # MESAJ YAZMA ALANI
    yeni_mesaj = st.chat_input("Buraya yazın...")
    if yeni_mesaj:
        db.collection('sohbet').add({
            'kim': me,
            'metin': yeni_mesaj,
            'vakit': datetime.now()
        })
        st.rerun()

    # MESAJLARI GÖSTERME (EN BASİT HALİ)
    # Burada 'order_by' kullanmıyoruz çünkü index hatası verebilir
    docs = db.collection('sohbet').limit(20).get()
    
    mesaj_listesi = []
    for d in docs:
        mesaj_listesi.append(d.to_dict())
    
    # Kod içinde sıralama yapalım (Firebase hatası almamak için)
    sirali_mesajlar = sorted(mesaj_listesi, key=lambda x: str(x.get('vakit', '')))

    for m in sirali_mesajlar:
        with st.chat_message("user" if m['kim'] == me else "assistant"):
            st.write(f"**{m['kim']}:** {m['metin']}")
