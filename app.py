import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Bizim Sohbet", layout="centered")

# 1. FIREBASE BAĞLANTISI (ZORLAMALI MOD)
@st.cache_resource # Bağlantıyı bir kez kur ve hafızada tut
def init_db():
    if not firebase_admin._apps:
        try:
            # Dosya adının tam olarak 'key.json' olduğundan emin ol
            cred = credentials.Certificate("key.json")
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            st.error(f"Bağlantı Kurulamadı: {e}")
            return None
    return firestore.client()

db = init_db()

st.title("💬 Özel Mesaj Paneli")

# 2. MESAJ GÖNDERME (HATA AYIKLAMALI)
with st.form("mesaj_formu", clear_on_submit=True):
    user = st.selectbox("Ben Kimim?", ["Halim", "Arkadaşım"])
    text = st.text_input("Mesajını yaz:")
    submit = st.form_submit_button("ŞİMDİ GÖNDER")
    
    if submit:
        if not text:
            st.warning("Lütfen bir mesaj yaz!")
        elif db is None:
            st.error("Veritabanı bağlantısı yok!")
        else:
            try:
                # Firebase'e veri ekleme denemesi
                yeni_mesaj = {
                    'kim': user,
                    'metin': text,
                    'vakit': firestore.SERVER_TIMESTAMP
                }
                db.collection('sohbet').add(yeni_mesaj)
                st.success("Mesaj başarıyla gönderildi!")
                # Sayfayı hemen yenilemek yerine biraz bekle veya rerun kullan
                st.rerun()
            except Exception as e:
                st.error(f"Gönderim sırasında hata oluştu: {e}")

st.divider()

# 3. MESAJLARI GÖSTERME
if db:
    try:
        # Mesajları tarihe göre çek
        docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(15).get()
        
        for d in docs:
            m = d.to_dict()
            with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
                st.write(f"**{m.get('kim')}:** {m.get('metin')}")
    except Exception as e:
        st.info("Mesajlar yüklenirken bir sorun oluştu veya henüz mesaj yok.")
