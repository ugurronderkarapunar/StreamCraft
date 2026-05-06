# modules/auth.py
import streamlit as st
from modules.utils import get_data

def login(email, password):
    users = get_data("users")
    for user in users:
        if user["email"] == email and user["password"] == password and user["is_active"]:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

def is_authorized(roles_allowed):
    if not st.session_state.logged_in:
        return False
    user_role = st.session_state.current_user["role"]
    return user_role in roles_allowed

def get_current_user_role():
    if st.session_state.logged_in:
        return st.session_state.current_user["role"]
    return None
