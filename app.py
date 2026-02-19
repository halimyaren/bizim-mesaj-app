import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Bağlantı Fonksiyonu
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Secrets'tan verileri al
            key_data = dict(st.secrets["firebase"])
            # Anahtardaki yazım hatalarını temizle
            fixed_key = key_data["private_key"].replace("\\n", "\n")
            key_data["private_key"] = fixed_key
            
            cred = credentials.Certificate(key_data)
            firebase_admin.initialize_app(cred)
            return True
        except Exception as e:
            st.error(f"Anahtar Hatası: {e}")
            return False
    return True

if init_firebase():
    db = firestore.client()
    st.success("✅ Bağlantı Başarılı!")
    
    st.title("💬 Bizim Mesaj Paneli")

    # Mesaj Gönderme
    with st.form("mesaj_formu", clear_on_submit=True):
        kim = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
        mesaj = st.text_input("Mesajın:")
        if st.form_submit_button("GÖNDER"):
            if mesaj:
                db.collection('sohbet').add({
                    'kim': kim,
                    'metin': mesaj,
                    'vakit': firestore.SERVER_TIMESTAMP
                })
                st.rerun()

    # Mesajları Görüntüleme
    st.write("---")
    try:
        docs = db.collection('sohbet').order_by('vakit', direction=firestore.Query.DESCENDING).limit(10).get()
        for d in docs:
            m = d.to_dict()
            with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
                st.write(f"**{m.get('kim')}:** {m.get('metin')}")
    except:
        st.info("Mesajlar yüklenirken bekleyin...")
