# modules/appointments.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.utils import get_data, add_item, update_item, delete_item, get_time_slots
from modules.customers import get_or_create_customer

def display_appointment_calendar():
    st.subheader("📅 Randevu Takvimi")
    # Basit liste görünümü (takvim için daha gelişmiş eklenebilir)
    appointments = get_data("appointments")
    if appointments:
        df = pd.DataFrame(appointments)
        df["start_time"] = pd.to_datetime(df["start_time"])
        df = df.sort_values("start_time")
        st.dataframe(df[["start_time", "customer_name", "barber_name", "status", "total_price"]], use_container_width=True)
    else:
        st.info("Henüz randevu yok.")

def create_appointment_form():
    st.subheader("➕ Yeni Randevu")
    customers = get_data("customers")
    services = get_data("services")
    users = get_data("users")
    barbers = [u for u in users if u["role"] == "Barber"]
    
    col1, col2 = st.columns(2)
    with col1:
        customer_options = {c["id"]: f"{c['name']} ({c['phone']})" for c in customers}
        customer_choice = st.selectbox("Müşteri Seç", options=["Yeni Müşteri"] + list(customer_options.keys()), format_func=lambda x: "Yeni Müşteri" if x=="Yeni Müşteri" else customer_options.get(x, ""))
        if customer_choice == "Yeni Müşteri":
            new_name = st.text_input("Ad Soyad")
            new_phone = st.text_input("Telefon")
            new_email = st.text_input("E-posta")
        else:
            selected_customer = next((c for c in customers if c["id"] == customer_choice), None)
            if selected_customer:
                new_name = selected_customer["name"]
                new_phone = selected_customer["phone"]
                new_email = selected_customer.get("email", "")
    with col2:
        barber_options = {b["id"]: b["first_name"] + " " + b["last_name"] for b in barbers}
        barber_id = st.selectbox("Berber", options=list(barber_options.keys()), format_func=lambda x: barber_options[x])
        selected_service_ids = st.multiselect("Hizmetler", options=[s["id"] for s in services if s["is_active"]], format_func=lambda x: next((s["name"] for s in services if s["id"]==x), x))
        date = st.date_input("Tarih", min_value=datetime.today())
        time_slot = st.selectbox("Saat", get_time_slots())
    
    if st.button("Randevu Oluştur"):
        # Hesaplamalar
        selected_services = [s for s in services if s["id"] in selected_service_ids]
        total_duration = sum(s["duration_minutes"] for s in selected_services)
        total_price = sum(s["default_price"] for s in selected_services)
        start_dt = datetime.combine(date, datetime.strptime(time_slot, "%H:%M").time())
        end_dt = start_dt + timedelta(minutes=total_duration)
        
        # Çakışma kontrolü (basit)
        appointments = get_data("appointments")
        conflict = False
        for app in appointments:
            if app["barber_name"] == barber_options[barber_id] and app["status"] in ["pending","confirmed"]:
                app_start = app["start_time"]
                app_end = app["end_time"]
                if not (end_dt <= app_start or start_dt >= app_end):
                    conflict = True
                    break
        if conflict:
            st.error("Bu berber seçtiğiniz saatte meşgul!")
            return
        
        # Müşteri kaydı (yeni ise oluştur)
        if customer_choice == "Yeni Müşteri":
            customer_id = get_or_create_customer(new_name, new_phone, new_email)
        else:
            customer_id = customer_choice
        
        new_app = {
            "id": str(len(appointments)+1),
            "tenant_id": "t1",
            "branch_id": "b1",
            "customer_name": new_name,
            "customer_phone": new_phone,
            "barber_name": barber_options[barber_id],
            "service_ids": selected_service_ids,
            "start_time": start_dt,
            "end_time": end_dt,
            "status": "pending",
            "total_price": total_price,
            "created_at": datetime.now()
        }
        add_item("appointments", new_app)
        st.success("Randevu oluşturuldu, onay bekliyor.")
        st.rerun()

def manage_appointments():
    st.subheader("📋 Randevu Yönetimi")
    appointments = get_data("appointments")
    status_options = ["pending", "confirmed", "completed", "cancelled"]
    for app in appointments:
        with st.expander(f"{app['start_time']} - {app['customer_name']} ({app['status']})"):
            col1, col2 = st.columns(2)
            with col1:
                new_status = st.selectbox("Durum", status_options, index=status_options.index(app["status"]), key=f"status_{app['id']}")
            with col2:
                if st.button("Güncelle", key=f"update_{app['id']}"):
                    update_item("appointments", app["id"], {"status": new_status})
                    st.success("Güncellendi")
                    st.rerun()
            if st.button("Sil", key=f"del_{app['id']}"):
                delete_item("appointments", app["id"])
                st.rerun()
