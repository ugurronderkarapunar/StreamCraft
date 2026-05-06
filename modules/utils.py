# modules/utils.py
import streamlit as st
from datetime import datetime, time
import pandas as pd

def init_session_state():
    """Session state başlangıç değerleri"""
    if "data" not in st.session_state:
        from data.mock_data import get_initial_data
        st.session_state.data = get_initial_data()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "selected_tenant" not in st.session_state:
        st.session_state.selected_tenant = "t1"  # demo tenant
    if "current_branch" not in st.session_state:
        st.session_state.current_branch = "b1"

def save_data(data_key, value):
    """Veriyi session state'e kaydet"""
    st.session_state.data[data_key] = value

def get_data(data_key):
    return st.session_state.data.get(data_key, [])

def add_item(data_key, item):
    items = get_data(data_key)
    item["id"] = str(len(items) + 1)  # basit id
    items.append(item)
    save_data(data_key, items)

def update_item(data_key, item_id, updated_item):
    items = get_data(data_key)
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items[i].update(updated_item)
            save_data(data_key, items)
            return True
    return False

def delete_item(data_key, item_id):
    items = get_data(data_key)
    new_items = [i for i in items if i["id"] != item_id]
    save_data(data_key, new_items)

def format_datetime(dt):
    return dt.strftime("%d.%m.%Y %H:%M")

def get_time_slots(start_hour=9, end_hour=20, interval_minutes=30):
    """Müsait zaman dilimleri üret"""
    slots = []
    for hour in range(start_hour, end_hour):
        for minute in [0, 30]:
            if hour == end_hour and minute > 0:
                continue
            slot_time = time(hour, minute)
            slots.append(slot_time.strftime("%H:%M"))
    return slots
