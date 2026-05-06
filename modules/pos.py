# modules/pos.py
import streamlit as st
from modules.utils import get_data, update_item
from datetime import datetime

def pos_payment():
    st.subheader("💰 Kasa / Ödeme Alma")
    appointments = get_data("appointments")
    # Sadece tamamlanmamış randevular
    pending_apps = [a for a in appointments if a["status"] in ["confirmed", "pending"]]
    if not pending_apps:
        st.info("Ödeme alınacak randevu yok.")
        return
    
    selected_app = st.selectbox("Randevu Seç", pending_apps, format_func=lambda x: f"{x['customer_name']} - {x['start_time']} - {x['total_price']} TL")
    if selected_app:
        st.write(f"Müşteri: {selected_app['customer_name']}")
        st.write(f"Toplam Tutar: {selected_app['total_price']} TL")
        tip = st.number_input("Bahşiş (TL)", min_value=0.0, value=0.0, step=5.0)
        payment_method = st.selectbox("Ödeme Yöntemi", ["Nakit", "Kredi Kartı", "Havale/EFT", "QR Kod"])
        if st.button("Ödemeyi Tamamla"):
            # Ödeme işlemi
            update_item("appointments", selected_app["id"], {"status": "completed"})
            # Müşteri puan ekle (her 10 TL'ye 1 puan gibi)
            customers = get_data("customers")
            for c in customers:
                if c["name"] == selected_app["customer_name"] and c["phone"] == selected_app["customer_phone"]:
                    points_to_add = int(selected_app["total_price"] // 10)
                    new_points = c["loyalty_points"] + points_to_add
                    new_spent = c["total_spent"] + selected_app["total_price"]
                    update_item("customers", c["id"], {"loyalty_points": new_points, "total_spent": new_spent})
                    st.success(f"Ödeme alındı! {points_to_add} sadakat puanı eklendi.")
                    break
            else:
                st.success("Ödeme alındı.")
            st.rerun()

def cashier_shift():
    st.subheader("Gün Sonu Kasası")
    # Basit shift yönetimi
    shifts = get_data("shifts")
    today = datetime.now().date()
    open_shift = next((s for s in shifts if s.get("closed_at") is None and s["date"] == today), None)
    if open_shift is None:
        if st.button("Vardiya Aç"):
            new_shift = {
                "id": str(len(shifts)+1),
                "branch_id": "b1",
                "cashier_name": st.session_state.current_user["first_name"],
                "date": today,
                "opened_at": datetime.now(),
                "closed_at": None,
                "starting_cash": 1000.0,  # örnek
                "expected_cash": None,
                "actual_cash": None
            }
            add_item("shifts", new_shift)
            st.success("Vardiya açıldı")
            st.rerun()
    else:
        st.write(f"Vardiya açık: {open_shift['opened_at']}")
        # Bugün tamamlanan randevulardan toplam tahsilat
        appointments = get_data("appointments")
        today_completed = [a for a in appointments if a["status"] == "completed" and a["start_time"].date() == today]
        total_today = sum(a["total_price"] for a in today_completed)
        st.metric("Günlük Tahsilat", f"{total_today} TL")
        expected = open_shift["starting_cash"] + total_today
        st.write(f"Beklenen Kasa: {expected} TL")
        actual = st.number_input("Kasa Sayımı (TL)", value=float(expected))
        if st.button("Vardiyayı Kapat"):
            update_item("shifts", open_shift["id"], {"closed_at": datetime.now(), "expected_cash": expected, "actual_cash": actual, "difference": actual - expected})
            st.success(f"Vardiya kapandı. Fark: {actual - expected} TL")
            st.rerun()
