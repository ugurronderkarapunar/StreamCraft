import streamlit as st
import json
import os
import datetime
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import tempfile

# -------------------------------
# CLOUDINARY YAPILANDIRMASI
# -------------------------------
load_dotenv()  # .env dosyasından ortam değişkenlerini yükle

# Cloudinary'yi yapılandır
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# -------------------------------
# VERİ YÖNETİMİ (JSON)
# -------------------------------
DATA_FILE = "streamcraft_data.json"

def verileri_yukle():
    """JSON dosyasından verileri yükler. Dosya yoksa mock veri oluşturur."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return mock_data_olustur()
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {str(e)}")
        return mock_data_olustur()

def verileri_kaydet(veri):
    """Verileri JSON dosyasına anında yazar."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        st.error(f"Veri kaydedilemedi: {str(e)}")
        return False

def mock_data_olustur():
    """Örnek veri seti oluşturur. 'Sıfırla' butonu bu fonksiyonu çağırır."""
    return {
        "clips": [
            {
                "id": 1,
                "oyun_adi": "Valorant",
                "baslik": "Ace!",
                "aciklama": "Rakip takımın tamamını tek başıma temizledim.",
                "tarih": "2025-03-15 20:30:00",
                "video_url": "https://res.cloudinary.com/demo/video/upload/sample.mp4"  # Örnek video URL'si
            },
            {
                "id": 2,
                "oyun_adi": "League of Legends",
                "baslik": "Pentakill",
                "aciklama": "Dörtlü çatışmadan beşli öldürme çıkardım.",
                "tarih": "2025-03-14 18:45:00",
                "video_url": "https://res.cloudinary.com/demo/video/upload/sample.mp4"
            },
            {
                "id": 3,
                "oyun_adi": "Counter-Strike 2",
                "baslik": "1v5 Clutch",
                "aciklama": "Son oyuncu olarak tüm rakipleri tek tek avladım.",
                "tarih": "2025-03-13 22:15:00",
                "video_url": "https://res.cloudinary.com/demo/video/upload/sample.mp4"
            }
        ]
    }

def sifirla():
    """Tüm veriyi mock veri ile değiştirir ve kaydeder."""
    yeni_veri = mock_data_olustur()
    if verileri_kaydet(yeni_veri):
        st.session_state["clips"] = yeni_veri["clips"]
        st.success("✅ Veriler başarıyla sıfırlandı (mock veri yüklendi).")
        st.rerun()
    else:
        st.error("❌ Sıfırlama sırasında hata oluştu.")

# -------------------------------
# VİDEO YÜKLEME YARDIMCILARI
# -------------------------------
def video_yukle(video_dosyasi):
    """
    Video dosyasını Cloudinary'ye yükler ve URL'sini döndürür.
    """
    try:
        # Geçici bir dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(video_dosyasi.getbuffer())
            tmp_path = tmp_file.name

        # Cloudinary'ye yükle
        upload_result = cloudinary.uploader.upload_large(
            tmp_path,
            resource_type="video",
            folder="streamcraft_clips"
        )

        # Geçici dosyayı temizle
        os.unlink(tmp_path)

        return upload_result.get("secure_url")
    except Exception as e:
        st.error(f"Video yüklenirken hata oluştu: {str(e)}")
        return None

def video_url_ekle(clip_id, video_url):
    """Bir klibe video URL'sini ekler ve JSON'u günceller."""
    try:
        mevcut_veri = verileri_yukle()
        for clip in mevcut_veri["clips"]:
            if clip["id"] == clip_id:
                clip["video_url"] = video_url
                break
        if verileri_kaydet(mevcut_veri):
            st.session_state["clips"] = mevcut_veri["clips"]
            return True
        return False
    except Exception as e:
        st.error(f"Video URL'si eklenirken hata: {str(e)}")
        return False

# -------------------------------
# YARDIMCI FONKSİYONLAR
# -------------------------------
def yeni_an_ekle(oyun_adi, baslik, aciklama, video_url=None):
    """Yeni bir oyun anını JSON'a ekler."""
    try:
        mevcut_veri = verileri_yukle()
        yeni_id = max((k["id"] for k in mevcut_veri["clips"]), default=0) + 1
        yeni_clip = {
            "id": yeni_id,
            "oyun_adi": oyun_adi,
            "baslik": baslik,
            "aciklama": aciklama,
            "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "video_url": video_url  # Artık video URL'si burada saklanacak
        }
        mevcut_veri["clips"].append(yeni_clip)
        if verileri_kaydet(mevcut_veri):
            st.session_state["clips"] = mevcut_veri["clips"]
            return True
        return False
    except Exception as e:
        st.error(f"An eklenirken hata: {str(e)}")
        return False

def an_sil(clip_id):
    """ID'ye göre bir anı siler."""
    try:
        mevcut_veri = verileri_yukle()
        mevcut_veri["clips"] = [c for c in mevcut_veri["clips"] if c["id"] != clip_id]
        if verileri_kaydet(mevcut_veri):
            st.session_state["clips"] = mevcut_veri["clips"]
            st.success("🗑️ An başarıyla silindi.")
            st.rerun()
        else:
            st.error("Silme işlemi başarısız.")
    except Exception as e:
        st.error(f"Silme hatası: {str(e)}")

def yedekle():
    """Veri JSON dosyasını kullanıcıya indirtir."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "rb") as f:
                st.download_button(
                    label="📥 Yedeği İndir",
                    data=f,
                    file_name=f"streamcraft_yedek_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        else:
            st.warning("Yedeklenecek veri dosyası bulunamadı.")
    except Exception as e:
        st.error(f"Yedekleme hatası: {str(e)}")

def yedekten_geri_yukle(uploaded_file):
    """Kullanıcının yüklediği yedek JSON dosyasını geri yükler."""
    try:
        if uploaded_file is not None:
            icerik = json.load(uploaded_file)
            if "clips" in icerik:
                if verileri_kaydet(icerik):
                    st.session_state["clips"] = icerik["clips"]
                    st.success("✅ Yedek başarıyla geri yüklendi.")
                    st.rerun()
                else:
                    st.error("Yedek kaydedilemedi.")
            else:
                st.error("Geçersiz yedek dosyası: 'clips' anahtarı eksik.")
    except Exception as e:
        st.error(f"Yedek yükleme hatası: {str(e)}")

# -------------------------------
# SAYFA BİLEŞENLERİ
# -------------------------------
def anlari_listele():
    st.subheader("🎥 Kaydedilen Anlar")
    clips = st.session_state.get("clips", [])
    if not clips:
        st.info("Henüz hiç an eklenmemiş. Yeni an ekle sayfasından başlayabilirsin.")
        return

    for clip in clips:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**🎮 {clip['oyun_adi']}** – *{clip['baslik']}*")
                st.caption(f"📅 {clip['tarih']}")
                st.write(f"📝 {clip['aciklama']}")
                if clip.get("video_url"):
                    st.video(clip["video_url"])
                else:
                    st.caption("🎬 Video yüklenmemiş.")
            with col2:
                if st.button("🗑️ Sil", key=f"sil_{clip['id']}"):
                    an_sil(clip['id'])
            st.divider()

def yeni_an_ekle_sayfasi():
    st.subheader("✨ Yeni Oyun Anı Ekle")
    with st.form(key="yeni_an_formu"):
        oyun_adi = st.text_input("Oyun Adı", placeholder="Örn: Valorant, LoL, CS2")
        baslik = st.text_input("Başlık", placeholder="Örn: Ace, Pentakill, Clutch")
        aciklama = st.text_area("Açıklama", placeholder="Neler olduğunu kısaca anlat...")
        video_file = st.file_uploader("Video Yükle (opsiyonel)", type=["mp4", "mov", "avi", "mkv"])
        submitted = st.form_submit_button("🚀 Anı Kaydet")
        
        if submitted:
            if not oyun_adi or not baslik:
                st.warning("Lütfen oyun adı ve başlık girin.")
            else:
                video_url = None
                if video_file:
                    with st.spinner("Video yükleniyor..."):
                        video_url = video_yukle(video_file)
                        if video_url is None:
                            st.error("Video yüklenirken bir hata oluştu. An metin olarak kaydedilecek.")
                
                if yeni_an_ekle(oyun_adi, baslik, aciklama, video_url):
                    st.success("An başarıyla eklendi!")
                    st.rerun()
                else:
                    st.error("An eklenirken bir hata oluştu.")

def profil_sayfasi():
    st.subheader("👤 Hesap ve Yedekleme")
    st.write("Demo sürümünde yalnızca tek kullanıcı (admin) bulunmaktadır.")
    st.markdown("---")
    st.subheader("💾 Veri Yedekleme")
    col1, col2 = st.columns(2)
    with col1:
        yedekle()
    with col2:
        uploaded_file = st.file_uploader("Yedekten Geri Yükle", type=["json"])
        if uploaded_file:
            yedekten_geri_yukle(uploaded_file)
    st.markdown("---")
    st.subheader("🔄 Verileri Sıfırla")
    if st.button("⚠️ Tüm Verileri Mock Veriyle Değiştir (Sıfırla)"):
        sifirla()
    st.markdown("---")
    st.subheader("🔧 Cloudinary Kurulum Notları")
    st.info("""
    **Video yükleme özelliğini kullanmak için:**
    1. [Cloudinary](https://cloudinary.com/)'ye ücretsiz bir hesap oluşturun.
    2. Proje kök dizinine `.env` dosyası oluşturun ve aşağıdaki bilgileri ekleyin:
