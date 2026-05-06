# modules/services.py
import streamlit as st
import pandas as pd
from modules.utils import get_data, add_item, update_item, delete_item

def display_services():
    st.subheader("💇 Hizmet Kataloğu")
    services = get_data("services")
    if services:
        df = pd.DataFrame(services)
        st.dataframe(df[["name", "category", "duration_minutes", "default_price", "is_active"]], use_container_width=True)
    else:
        st.info("Hizmet tanımlı değil.")

def manage_services():
    st.subheader("Hizmet Yönetimi")
    services = get_data("services")
    with st.form("new_service"):
        name = st.text_input("Hizmet Adı")
        category = st.selectbox("Kategori", ["Saç", "Sakal", "Cilt Bakımı", "Diğer"])
        duration = st.number_input("Süre (dakika)", min_value=5, step=5, value=30)
        price = st.number_input("Fiyat (TL)", min_value=0.0, step=10.0, value=100.0)
        submitted = st.form_submit_button("Ekle")
        if submitted and name:
            new_service = {
                "id": str(len(services)+1),
                "tenant_id": "t1",
                "category": category,
                "name": name,
                "duration_minutes": duration,
                "default_price": price,
                "is_active": True
            }
            add_item("services", new_service)
            st.success("Hizmet eklendi")
            st.rerun()
    
    # Mevcut hizmetleri düzenleme
    for svc in services:
        with st.expander(f"{svc['name']} ({svc['default_price']} TL)"):
            new_price = st.number_input("Yeni Fiyat", value=float(svc['default_price']), key=f"price_{svc['id']}")
            active = st.checkbox("Aktif", value=svc['is_active'], key=f"active_{svc['id']}")
            if st.button("Güncelle", key=f"upd_{svc['id']}"):
                update_item("services", svc["id"], {"default_price": new_price, "is_active": active})
                st.success("Güncellendi")
                st.rerun()
            if st.button("Sil", key=f"del_{svc['id']}"):
                delete_item("services", svc["id"])
                st.rerun()
