import os
import sqlite3
import pytest
from my_app.db_utils import create_database, get_flights, get_bookings, add_complaint, get_complaints, \
    resolve_complaint, create_user, authenticate_user

# Путь к временной базе данных для тестов
TEST_DB_FILE = 'test_flights.db'


@pytest.fixture(scope='module', autouse=True)
def setup_database():
    # Создание тестовой базы данных
    with sqlite3.connect(TEST_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        conn.commit()

    # Создание таблиц
    create_database()

    yield  # Тесты выполняются здесь

    # Удаление тестовой базы данных после тестов
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


def test_create_user():
    # Очищаем таблицу users перед тестом
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM users")
        conn.commit()

    create_user("test_user", "password123", "admin")

    # Проверка, что пользователь был добавлен
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", ("test_user",))
        user = c.fetchone()

    assert user is not None
    assert user[1] == "test_user"
    assert user[2] == "password123"
    assert user[3] == "admin"


def test_authenticate_user():
    # Очищаем таблицу users перед тестом
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM users")
        conn.commit()

    create_user("test_user", "password123", "admin")

    user_type = authenticate_user("test_user", "password123")
    assert user_type == "admin"

    # Проверка неправильного пароля
    user_type = authenticate_user("test_user", "wrong_password")
    assert user_type is None


def test_add_and_get_complaint():
    # Очищаем таблицу complaints перед тестом
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM complaints")
        conn.commit()

    add_complaint("Иван Иванов", "Проблема с рейсом")

    complaints = get_complaints()
    assert len(complaints) == 1
    assert complaints[0][1] == "Иван Иванов"
    assert complaints[0][2] == "Проблема с рейсом"
    assert complaints[0][3] == "Открыта"


def test_resolve_complaint():
    add_complaint("Иван Иванов", "Проблема с рейсом")
    complaints = get_complaints()
    complaint_id = complaints[0][0]

    resolve_complaint(complaint_id)

    updated_complaints = get_complaints()
    assert updated_complaints[0][3] == "Решена"


def test_get_flights():
    # Проверяем, что изначально нет рейсов
    flights = get_flights()
    assert len(flights) == 0

    # Добавим рейс для проверки
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO flights (flight_number, date, time, `from`, `to`) VALUES (?, ?, ?, ?, ?)",
                  ("FL123", "2025-05-01", "10:00", "Москва", "Санкт-Петербург"))
        conn.commit()

    # Проверяем, что рейс добавился
    flights = get_flights()
    assert len(flights) == 1
    assert flights[0][0] == "FL123"


def test_get_bookings():
    # Проверяем, что изначально нет бронирований
    bookings = get_bookings()
    assert len(bookings) == 0

    # Добавим бронирование для проверки
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO bookings (flight_number, passenger_name, ticket_price) VALUES (?, ?, ?)",
                  ("FL123", "Иван Иванов", 100.0))
        conn.commit()

    bookings = get_bookings()
    assert len(bookings) == 1
    assert bookings[0][1] == "Иван Иванов"