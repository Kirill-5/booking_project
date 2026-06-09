import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal

client = TestClient(app)





def test_login_success():
    response = client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200

def test_login_fail():
    response = client.post("/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_create_booking_success():
    # Логин
    login_response = client.post("/login", json={
        "username": "employee1",
        "password": "pass123"
    })
    token = login_response.json()["access_token"]

    # Создание брони
    response = client.post(
        "/bookings",
        json={
            "room_id": 17,
            "slot_id": 49,
            "date": "2026-12-31"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "id" in response.json()


def test_create_booking_conflict():
    # Логин
    login_response = client.post("/login", json={
        "username": "employee1",
        "password": "pass123"
    })
    token = login_response.json()["access_token"]

    booking_data = {
        "room_id": 17,
        "slot_id": 49,
        "date": "2026-12-31"
    }

    # первый запрос - успех
    resp1 = client.post("/bookings", json=booking_data, headers={"Authorization": f"Bearer {token}"})
    #print(resp1.status_code)
    #print(resp1.json())
    assert resp1.status_code == 200

    # второй запрос - конфликт
    response2 = client.post("/bookings", json=booking_data, headers={"Authorization": f"Bearer {token}"})
    assert response2.status_code == 409
    assert "already booked" in response2.json()["detail"]