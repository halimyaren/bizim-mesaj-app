import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. FIREBASE ANAHTARI (HAM METİN FORMATINDA)
# 'r' harfi ve üçlü tırnak kullanarak karakter bozulmasını engelliyoruz
private_key_raw = r"""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDXOOEzb3rMOqiJ
gp7oqLNPgiVsJKbzW/CxDMQqVo+U6xqjxtf9rybD0jx5gnV2hLtxS51AsZQcbspK
nWYuxN0ToOH1f+jx/SkJ1kAuPfa5L1svqMXF1MIF9WiZ5LTSRsE5KOjAbplZjESG
/jP4HS0cicvEolXxiwvMkjWbjh2G7t/wj9F/QPfK2NTGHYH4rdBb/Tc7khtDkYbL
x0OGr9P6U/komaaZXrz48dQQeHJyifoWamfSsp6hrZAaWLWpM+pSutbP5cU+SfWe
UM9X6ms3plhVLIMa+AoyoKrJo/Y/l9jab5DDVAHoubjWs0Zi2Iyw+4apRRVetGsG
DmOqmygdAgMBAAECggEAB6k4lqe96m3GQoMifC5uXMy134n8TnWAXNgc88l6F2Yb
pQlDCjmz81GVMG0qeu3FilUdRB71evXtGLjYOLK9GlLrNbYuRn+B7rF6Pk2bbgMG
YE9jlVAIyjEMNyYqcK29x4CPrLz5ROpeJS07wWwS6bR0cn7g0V/nK2NAqgahGkmW
gJNBpaxz963ezAidAlHAtlkeDKGjfdZyierIzB0piw/BgI9UO7dWTH/3h8BAbVcS
P3c9JOojPXfXkn29GXSoqGVuaV5QYI0Rml+QC+KxXeScbvuEOdoP+sypLc3et2fg
PrhYHo5EnNOOBcxpfLIsoDx5SUKNAZfA72Jc8hWbVQKBgQD/HVOPeJxDHJ0a0uvI
99ff+qxDYjYY86uMTLKdTDijgrzGHj+UxGg/xYbAu6g0o+cYFWJqRU/kv+g3k76i
6JxDMN6hwPEDj5XYPr1+8DddbFIDmI+2KrQf82LcNxiT5PMqC4tg3fe6/Kx6WAvK
B7jutvqP2pI7HtF/wlbhHMgGGwKBgQDX+Bu1hx4l9QPEaS8pBuoNGnP/3yriSLrc
co98KwFpUfoe1udS+iBht4eR8sZHK9MNUQ1cFjJu5hEi0bzarjvVI88NK3nE41hq
p+HsnPv+NNTdbfQLR4z57eXo6LMelQr6tvRjAJMx15jQCPff+h6EplbdYKrA4EXG
yGpcvzJOJwKBgDE+DeUBmNfza/fDgrOV81tOXXXcPSjvz8sS+t8V2VDmaV2sdQVY
K+8zR2FoV31hrbeeWRK+Mj+rMz2XDRMQ5yipBDAgt+TCEGBfK+CWqXkk8We0SPkW
oRIRvqFXGS1i4fTZqZuW/LxhDUHIQO5MM0wQkai2vccfmbyZXH+zOIDFAoGAf0iy
BAWzZgmGg96+Nb7meHyLu1Tq8FyPDNfT6wlplooDEOP1h/j01sKU+xaLd2zDwYhw
iEJozOV5Wf0lAflIODEXmZpy9PBMrudtBsfq2IKIpkxkVbWAx9hG9UMYNkD/LI5h
cGvpVKnNXWa7uFywWduzPFv5px1G4oZB8ZGZ82cCgYEAjBBaMo3uBilqbu8WjmjU
nw1xzJ3opbgAujz/2tzWII3cRRrV4Oq/jaQABo4ehx3KggSWkDu9ctwExokH4GDjC
NMBpYo6yN5Hw3JhvF36rfeQSGEea5OIG+12dwoUeBEiQjXAC0JbhXsTk3yr8AeDy
nuR87nFmjPIfPWMymVp5Nsm4=
-----END PRIVATE KEY-----"""

if not firebase_admin._apps:
    key_dict = {
        "type": "service_account",
        "project_id": "ozel-mesaj-app",
        "private_key_id": "94192de7b0d4555b799de6fadb5027feb4d8a42a",
        "private_key": private_key_raw.replace("\\n", "\n"), # Karakterleri doğru formata sok
        "client_email": "firebase-adminsdk-fbsvc@ozel-mesaj-app.iam.gserviceaccount.com",
        "client_id": "108796016460187663405",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ozel-mesaj-app.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. ARAYÜZ
st.set_page_config(page_title="Bizim Sohbet", layout="centered")
st.title("💬 Özel Mesaj Hattı")

# 3. MESAJ YAZMA
with st.form("mesaj_kutusu", clear_on_submit=True):
    kim = st.radio("Kimsin?", ["Halim", "Arkadaşım"], horizontal=True)
    yeni_mesaj = st.text_area("Mesajın:")
    gonder = st.form_submit_button("GÖNDER")
    
    if gonder and yeni_mesaj:
        db.collection('sohbet').add({
            'kim': kim,
            'metin': yeni_mesaj,
            'vakit': firestore.SERVER_TIMESTAMP
        })
        st.rerun()

# 4. MESAJLARI GÖSTERME
st.write("---")
try:
    # Verileri çek (Index hatası olmasın diye basit çekiyoruz)
    docs = db.collection('sohbet').limit(50).get()
    
    mesajlar = []
    for d in docs:
        mesajlar.append(d.to_dict())
    
    # Koda dayalı sıralama (Zaman damgasına göre)
    sirali = sorted(mesajlar, key=lambda x: str(x.get('vakit', '')))

    for m in sirali:
        with st.chat_message("user" if m.get('kim') == "Halim" else "assistant"):
            st.write(f"**{m.get('kim')}:** {m.get('metin')}")
            
except Exception as e:
    st.info("Mesajlar yükleniyor...")
