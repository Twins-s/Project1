import pytest
import sqlite3
from PyQt5.QtWidgets import QApplication
import sys
from my_app.passenger_management import PassengersTab

@pytest.fixture(scope="session")
def app():
    app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def passengers_tab(app):
    # Создаем временную базу данных в памяти
    conn = sqlite3.connect(':memory:')
    
    # Создаем таблицу
    c = conn.cursor()
    c.execute("CREATE TABLE bookings (booking_id INTEGER PRIMARY KEY AUTOINCREMENT, passenger_name TEXT, ticket_price REAL)")
    conn.commit()

    tab = PassengersTab(conn)  # Передаем соединение с БД
    tab.show()  # Обязательно показываем окно
    yield tab

    conn.close()  # Закрываем соединение после тестов

class TestPassengersTab:
    def test_load_passengers(self, passengers_tab):
        # Добавление тестовых данных в базу данных
        conn = passengers_tab.db_connection
        c = conn.cursor()
        c.execute("INSERT INTO bookings (passenger_name, ticket_price) VALUES (?, ?)", ('John Doe', 100.0))
        c.execute("INSERT INTO bookings (passenger_name, ticket_price) VALUES (?, ?)", ('Jane Smith', 150.0))
        conn.commit()

        # Вызов метода load_passengers()
        passengers_tab.load_passengers()

        # Проверка, что таблица заполнена правильно
        assert passengers_tab.passengers_table.rowCount() == 2
        assert passengers_tab.passengers_table.item(0, 0).text() == 'John Doe'
        assert passengers_tab.passengers_table.item(0, 1).text() == '1'
        assert passengers_tab.passengers_table.item(0, 2).text() == '100.0'
        assert passengers_tab.passengers_table.item(1, 0).text() == 'Jane Smith'
        assert passengers_tab.passengers_table.item(1, 1).text() == '2'
        assert passengers_tab.passengers_table.item(1, 2).text() == '150.0'

    def test_edit_passenger(self, passengers_tab):
        # Добавление тестовых данных в базу данных
        conn = passengers_tab.db_connection
        c = conn.cursor()
        c.execute("INSERT INTO bookings (passenger_name, ticket_price) VALUES (?, ?)", ('John Doe', 100.0))
        conn.commit()

        # Вызов метода load_passengers()
        passengers_tab.load_passengers()

        # Вызов метода edit_passenger()
        passengers_tab.passengers_table.selectRow(0)
        passengers_tab.edit_passenger()

        # Проверка, что данные пассажира были обновлены
        c.execute("SELECT passenger_name, ticket_price FROM bookings WHERE booking_id = 1")
        updated_passenger = c.fetchone()
        assert updated_passenger[0] == 'John Doe'
        assert updated_passenger[1] == 100.0

    def test_delete_passenger(self, passengers_tab):
        # Добавление тестовых данных в базу данных
        conn = passengers_tab.db_connection
        c = conn.cursor()
        c.execute("INSERT INTO bookings (passenger_name, ticket_price) VALUES (?, ?)", ('John Doe', 100.0))
        conn.commit()

        # Вызов метода load_passengers()
        passengers_tab.load_passengers()

        # Вызов метода delete_passenger()
        passengers_tab.passengers_table.selectRow(0)
        passengers_tab.delete_passenger()

        # Проверка, что пассажир был удален
        c.execute("SELECT COUNT(*) FROM bookings")
        assert c.fetchone()[0] == 0