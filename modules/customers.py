# modules/customers.py
import streamlit as st
import pandas as pd
from modules.utils import get_data, add_item, update_item

def display_customers():
    st.subheader("👥 Müşteri Listesi")
    customers = get_data("customers")
    if customers:
        df = pd.DataFrame(customers)
        st.dataframe(df[["name", "phone", "email", "loyalty_points", "total_spent"]], use_container_width=True)
    else:
        st.info("Müşteri bulunamadı.")

def add_customer_form():
    with st.form("add_customer"):
        name = st.text_input("Ad Soyad")
        phone = st.text_input("Telefon")
        email = st.text_input("E-posta")
        notes = st.text_area("Notlar (saç tercihleri vb.)")
        submitted = st.form_submit_button("Müşteri Ekle")
        if submitted and name and phone:
            new_customer = {
                "id": str(len(get_data("customers")) + 1),
                "tenant_id": "t1",
                "name": name,
                "phone": phone,
                "email": email,
                "loyalty_points": 0,
                "total_spent": 0.0,
                "notes": notes
            }
            add_item("customers", new_customer)
            st.success("Müşteri eklendi")
            st.rerun()

def get_or_create_customer(name, phone, email=""):
    customers = get_data("customers")
    existing = next((c for c in customers if c["phone"] == phone), None)
    if existing:
        return existing["id"]
    else:
        new_id = str(len(customers) + 1)
        new_customer = {
            "id": new_id,
            "tenant_id": "t1",
            "name": name,
            "phone": phone,
            "email": email,
            "loyalty_points": 0,
            "total_spent": 0.0,
            "notes": ""
        }
        add_item("customers", new_customer)
        return new_id
