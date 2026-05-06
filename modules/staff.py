# modules/staff.py
import streamlit as st
import pandas as pd
from modules.utils import get_data, add_item, update_item, delete_item

def display_staff():
    st.subheader("👨‍💼 Personel Listesi")
    users = get_data("users")
    if users:
        df = pd.DataFrame(users)
        st.dataframe(df[["first_name", "last_name", "email", "role", "is_active"]], use_container_width=True)
    else:
        st.info("Personel bulunamadı.")

def manage_staff():
    st.subheader("Personel Yönetimi")
    users = get_data("users")
    roles = ["Admin", "BranchManager", "Barber", "Cashier"]
    with st.form("new_user"):
        first_name = st.text_input("Ad")
        last_name = st.text_input("Soyad")
        email = st.text_input("E-posta")
        password = st.text_input("Şifre", type="password")
        role = st.selectbox("Rol", roles)
        branch = st.selectbox("Şube", [b["name"] for b in get_data("branches")])
        submitted = st.form_submit_button("Personel Ekle")
        if submitted and first_name and email:
            new_user = {
                "id": str(len(users)+1),
                "tenant_id": "t1",
                "branch_id": "b1",  # basit
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "is_active": True
            }
            add_item("users", new_user)
            st.success("Personel eklendi")
            st.rerun()
    
    for user in users:
        with st.expander(f"{user['first_name']} {user['last_name']} - {user['role']}"):
            active = st.checkbox("Aktif", value=user['is_active'], key=f"active_{user['id']}")
            if st.button("Durumu Güncelle", key=f"toggle_{user['id']}"):
                update_item("users", user["id"], {"is_active": active})
                st.rerun()
