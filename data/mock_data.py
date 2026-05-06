# data/mock_data.py
from datetime import datetime, timedelta
import uuid

# Başlangıç verileri (gerçek DB yok, session state'te tutulacak)

def get_initial_data():
    return {
        "tenants": [
            {"id": "t1", "name": "Güzellik Salonu", "subdomain": "demo", "is_active": True}
        ],
        "branches": [
            {"id": "b1", "tenant_id": "t1", "name": "Merkez Şube", "address": "İstanbul", "phone": "5551234", "is_active": True}
        ],
        "users": [
            {"id": "u1", "tenant_id": "t1", "branch_id": "b1", "email": "admin@demo.com", "password": "admin123", "first_name": "Admin", "last_name": "User", "role": "Admin", "is_active": True},
            {"id": "u2", "tenant_id": "t1", "branch_id": "b1", "email": "barber@demo.com", "password": "barber123", "first_name": "Ahmet", "last_name": "Usta", "role": "Barber", "is_active": True},
            {"id": "u3", "tenant_id": "t1", "branch_id": "b1", "email": "kasiyer@demo.com", "password": "kasiyer123", "first_name": "Ayşe", "last_name": "Yılmaz", "role": "Cashier", "is_active": True}
        ],
        "services": [
            {"id": "s1", "tenant_id": "t1", "category": "Saç", "name": "Saç Kesimi", "duration_minutes": 30, "default_price": 150.0, "is_active": True},
            {"id": "s2", "tenant_id": "t1", "category": "Sakal", "name": "Sakal Tıraşı", "duration_minutes": 20, "default_price": 80.0, "is_active": True},
            {"id": "s3", "tenant_id": "t1", "category": "Cilt Bakımı", "name": "Cilt Temizliği", "duration_minutes": 45, "default_price": 250.0, "is_active": True}
        ],
        "customers": [
            {"id": "c1", "tenant_id": "t1", "name": "Mehmet Demir", "phone": "5551111", "email": "mehmet@mail.com", "loyalty_points": 120, "total_spent": 750, "notes": "Saç kısa, sakal ister"},
            {"id": "c2", "tenant_id": "t1", "name": "Zeynep Kaya", "phone": "5552222", "email": "zeynep@mail.com", "loyalty_points": 50, "total_spent": 300, "notes": ""}
        ],
        "appointments": [
            {
                "id": "a1", "tenant_id": "t1", "branch_id": "b1", "customer_name": "Mehmet Demir", "customer_phone": "5551111",
                "barber_name": "Ahmet Usta", "service_ids": ["s1"], "start_time": datetime.now() + timedelta(days=1, hours=10),
                "end_time": datetime.now() + timedelta(days=1, hours=10, minutes=30),
                "status": "confirmed", "total_price": 150.0, "created_at": datetime.now()
            }
        ],
        "shifts": []  # Kasa vardiyaları
    }
