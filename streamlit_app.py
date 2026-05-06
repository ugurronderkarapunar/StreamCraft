# streamlit_app.py
import streamlit as st
from modules.auth import login, logout, is_authorized, get_current_user_role
from modules.utils import init_session_state
from modules.appointments import display_appointment_calendar, create_appointment_form, manage_appointments
from modules.customers import display_customers, add_customer_form
from modules.services import display_services, manage_services
from modules.staff import display_staff, manage_staff
from modules.pos import pos_payment, cashier_shift
from modules.reports import revenue_report, barber_performance

# Sayfa yapılandırması (mobil uyumlu)
st.set_page_config(page_title="Berber SaaS Demo", layout="wide", initial_sidebar_state="auto")

init_session_state()

# CSS ile mobil uyum (opsiyonel)
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
        }
        .stSelectbox, .stTextInput, .stNumberInput {
            margin-bottom: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Giriş ve navigasyon
with st.sidebar:
    st.image("https://via.placeholder.com/150x80?text=Barber+Logo", use_column_width=True)
    st.title("Berber SaaS")
    if not st.session_state.logged_in:
        st.subheader("Giriş Yap")
        email = st.text_input("E-posta")
        password = st.text_input("Şifre", type="password")
        if st.button("Giriş"):
            if login(email, password):
                st.success("Hoş geldiniz!")
                st.rerun()
            else:
                st.error("Hatalı giriş")
    else:
        user = st.session_state.current_user
        st.write(f"👋 Merhaba, {user['first_name']} ({user['role']})")
        if st.button("Çıkış Yap"):
            logout()
        
        # Rol bazlı menü
        role = user["role"]
        menu_items = []
        if role in ["Admin", "BranchManager"]:
            menu_items = ["📅 Randevular", "➕ Yeni Randevu", "👥 Müşteriler", "💇 Hizmetler", "👨‍💼 Personel", "💰 Kasa", "📊 Raporlar"]
        elif role == "Barber":
            menu_items = ["📅 Randevular", "➕ Yeni Randevu", "👥 Müşteriler"]
        elif role == "Cashier":
            menu_items = ["💰 Kasa", "📅 Randevular", "📊 Raporlar"]
        else:
            menu_items = ["📅 Randevular"]
        
        choice = st.radio("Menü", menu_items)

# Ana içerik
if st.session_state.logged_in:
    if choice == "📅 Randevular":
        tab1, tab2 = st.tabs(["Takvim", "Yönetim"])
        with tab1:
            display_appointment_calendar()
        with tab2:
            manage_appointments()
    elif choice == "➕ Yeni Randevu":
        create_appointment_form()
    elif choice == "👥 Müşteriler":
        tab1, tab2 = st.tabs(["Liste", "Yeni Müşteri"])
        with tab1:
            display_customers()
        with tab2:
            add_customer_form()
    elif choice == "💇 Hizmetler":
        tab1, tab2 = st.tabs(["Liste", "Yönetim"])
        with tab1:
            display_services()
        with tab2:
            manage_services()
    elif choice == "👨‍💼 Personel":
        tab1, tab2 = st.tabs(["Liste", "Yönetim"])
        with tab1:
            display_staff()
        with tab2:
            manage_staff()
    elif choice == "💰 Kasa":
        tab1, tab2 = st.tabs(["Ödeme Al", "Gün Sonu Kasası"])
        with tab1:
            pos_payment()
        with tab2:
            cashier_shift()
    elif choice == "📊 Raporlar":
        tab1, tab2 = st.tabs(["Ciro Raporu", "Berber Performansı"])
        with tab1:
            revenue_report()
        with tab2:
            barber_performance()
else:
    st.info("Lütfen giriş yapın. Demo hesaplar: admin@demo.com / admin123 , barber@demo.com / barber123 , kasiyer@demo.com / kasiyer123")
