import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import time

st.set_page_config(page_title="Hızlı Sohbet", layout="centered")

# 1. Firebase Bağlantısı (Dosyadan okuma garantili)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)
        st.toast("Firebase bağlantısı hazır!", icon="🔌")
    except Exception as e:
        st.error(f"⚠️ Kritik Bağlantı Hatası: {e}")

db = firestore.client()

st.title("💬 Sohbet Paneli")

# 2. Mesaj Gönderimi
with st.container():
    user = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
    text = st.text_input("Mesajını yaz:", placeholder="Merhaba...")
    
    if st.button("GÖNDER", use_container_width=True):
        if text:
            try:
                # Gönderiliyor bildirimi
                with st.spinner('Mesaj iletiliyor...'):
                    doc_ref = db.collection('sohbet').add({
                        'kim': user,
                        'metin': text,
                        'vakit': firestore.SERVER_TIMESTAMP
                    })
                st.success(f"✅ Mesaj başarıyla gitti! (ID: {doc_ref[1].id})")
                time.sleep(1) # Başarı mesajını gör diye kısa bir bekleme
                st.rerun()
            except Exception as e:
                st.error(f"❌ Mesaj GİTMEDİ: {e}")
        else:
            st.warning("Boş mesaj gönderemezsin.")

st.divider()

# 3. Mesajları Listeleme
st.subheader("Son Mesajlar")
try:
    # order_by bazen yeni veritabanlarında hata verebilir, önce basit çekelim
    docs = db.collection('sohbet').limit(20).get()
    
    # Python ile sıralayalım (Hata riskini azaltmak için)
    msgs = [d.to_dict() for d in docs]
    # Vakit bilgisi olmayan mesajlar için hata almamak için kontrol
    msgs.sort(key=lambda x: str(x.get('vakit')), reverse=True)
    
    for m in msgs:
        with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
except Exception as e:
    st.info("Henüz mesaj yok veya bir yükleme hatası oluştu.")
