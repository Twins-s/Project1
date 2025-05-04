import os
import sqlite3
import pytest
from PyQt5.QtWidgets import QApplication
from my_app.main import MainWindow  # Замените 'my_app' на имя вашего модуля

# Путь к временной базе данных для тестов
TEST_DB_FILE = 'test_flights.db'

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    # Создание тестовой базы данных
    with sqlite3.connect(TEST_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                user_type TEXT
            )
        """)
        conn.commit()

    yield  # Тесты выполняются здесь

    # Удаление тестовой базы данных после тестов
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def test_show_admin_window(qtbot):
    app = QApplication([])
    main_window = MainWindow([])
    qtbot.addWidget(main_window)

    main_window.auth_window.show()
    assert not main_window.admin_window.isVisible()

    add_test_user()

    main_window.auth_window.authenticate("admin_username", "admin_password")
    assert main_window.admin_window.isVisible()

    app.quit()  # Закрываем приложение после теста

def test_show_passenger_window(qtbot):
    app = QApplication([])
    main_window = MainWindow([])
    qtbot.addWidget(main_window)

    main_window.auth_window.show()
    assert not main_window.passenger_window.isVisible()

    add_test_user(user_type='passenger')

    main_window.auth_window.authenticate("passenger_username", "passenger_password")
    assert main_window.passenger_window.isVisible()

    app.quit()  # Закрываем приложение после теста

def add_test_user(username="admin_username", password="admin_password", user_type="admin"):
    with sqlite3.connect(TEST_DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", (username, password, user_type))
        conn.commit()