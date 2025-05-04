import os
import sqlite3
import pytest
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore
from my_app.flight_management import FlightsTab

# Путь к временной базе данных для тестов
TEST_DB_FILE = 'test_flights.db'

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    # Создание тестовой базы данных
    with sqlite3.connect(TEST_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        conn.commit()  # Исправлено с cursor.commit() на conn.commit()

    # Создание таблиц
    create_test_database()

    yield  # Тесты выполняются здесь

    # Удаление тестовой базы данных после тестов
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def create_test_database():
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                flight_number TEXT PRIMARY KEY,
                date TEXT,
                time TEXT,
                `from` TEXT,
                `to` TEXT
            )
        """)
        conn.commit()

def test_add_flight(qtbot):
    flights_tab = FlightsTab()
    qtbot.addWidget(flights_tab)

    # Открытие окна добавления рейса
    flights_tab.show_add_flight_window()

    # Заполнение данных рейса
    add_flight_window = flights_tab.children()[-1]  # Получаем последнее открытое окно
    add_flight_window.flight_number_input.setText("FL123")
    add_flight_window.date_input.setText("2025-05-01")
    add_flight_window.time_input.setText("10:00")
    add_flight_window.from_input.setText("Москва")
    add_flight_window.to_input.setText("Санкт-Петербург")

    # Сохранение рейса
    qtbot.mouseClick(add_flight_window.findChild(QPushButton, "Сохранить"), QtCore.Qt.LeftButton)

    # Проверка, что рейс добавлен в таблицу
    flights_tab.populate_flights_table()
    assert flights_tab.flights_table.rowCount() == 1
    assert flights_tab.flights_table.item(0, 0).text() == "FL123"

def test_edit_flight(qtbot):
    flights_tab = FlightsTab()
    qtbot.addWidget(flights_tab)

    # Добавляем рейс для редактирования
    flights_tab.get_flights = lambda: [{"flight_number": "FL123", "date": "2025-05-01", "time": "10:00", "from": "Москва", "to": "Санкт-Петербург"}]
    flights_tab.populate_flights_table()

    # Открытие окна редактирования рейса
    flights_tab.show_edit_flight_window()

    # Изменение данных рейса
    edit_flight_window = flights_tab.children()[-1]  # Получаем последнее открытое окно
    edit_flight_window.flight_number_input.setText("FL123")
    edit_flight_window.date_input.setText("2025-05-02")
    edit_flight_window.time_input.setText("12:00")
    edit_flight_window.from_input.setText("Санкт-Петербург")
    edit_flight_window.to_input.setText("Москва")

    # Сохранение изменений
    qtbot.mouseClick(edit_flight_window.findChild(QPushButton, "Сохранить"), QtCore.Qt.LeftButton)

    # Проверка, что рейс обновлён в таблице
    flights_tab.populate_flights_table()
    assert flights_tab.flights_table.item(0, 1).text() == "2025-05-02"

def test_delete_flight(qtbot):
    flights_tab = FlightsTab()
    qtbot.addWidget(flights_tab)

    # Добавляем рейс для удаления
    flights_tab.get_flights = lambda: [{"flight_number": "FL123", "date": "2025-05-01", "time": "10:00", "from": "Москва", "to": "Санкт-Петербург"}]
    flights_tab.populate_flights_table()

    # Удаление рейса
    flights_tab.delete_flight()

    # Проверка, что таблица пуста
    flights_tab.populate_flights_table()
    assert flights_tab.flights_table.rowCount() == 0