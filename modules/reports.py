# modules/reports.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.utils import get_data

def revenue_report():
    st.subheader("📊 Ciro Raporu")
    appointments = get_data("appointments")
    completed = [a for a in appointments if a["status"] == "completed"]
    if completed:
        df = pd.DataFrame(completed)
        df["date"] = pd.to_datetime(df["start_time"]).dt.date
        daily = df.groupby("date")["total_price"].sum().reset_index()
        st.bar_chart(daily.set_index("date"))
        st.write("Detaylı Tablo:")
        st.dataframe(df[["start_time", "customer_name", "total_price"]])
        total_revenue = df["total_price"].sum()
        st.metric("Toplam Ciro", f"{total_revenue} TL")
    else:
        st.info("Henüz tamamlanmış randevu yok.")

def barber_performance():
    st.subheader("💈 Berber Performansı")
    appointments = get_data("appointments")
    completed = [a for a in appointments if a["status"] == "completed"]
    if completed:
        df = pd.DataFrame(completed)
        barber_stats = df.groupby("barber_name")["total_price"].sum().reset_index()
        barber_stats.columns = ["Berber", "Toplam Ciro"]
        st.dataframe(barber_stats)
        # Basit prim hesaplama (ciro * 0.10)
        barber_stats["Prim (TL)"] = barber_stats["Toplam Ciro"] * 0.10
        st.dataframe(barber_stats)
    else:
        st.info("Veri yok.")
