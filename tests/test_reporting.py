import pytest
import sqlite3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDate
from my_app.reporting import ReportsTab
from unittest.mock import patch
from my_app.db_utils import create_database  # Импортируем функцию создания базы данных

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    create_database()  # Создаем базу данных

    # Добавление тестовых данных
    conn = sqlite3.connect('../flights.db')
    c = conn.cursor()
    c.execute("INSERT INTO flights (flight_number, date) VALUES ('FL123', '2023-05-01')")
    c.execute("INSERT INTO flights (flight_number, date) VALUES ('FL456', '2023-05-02')")
    c.execute("INSERT INTO bookings (flight_number, passenger_name, ticket_price) VALUES ('FL123', 'John Doe', 100)")
    c.execute("INSERT INTO bookings (flight_number, passenger_name, ticket_price) VALUES ('FL123', 'Jane Doe', 100)")
    c.execute("INSERT INTO bookings (flight_number, passenger_name, ticket_price) VALUES ('FL456', 'Bob Smith', 100)")
    conn.commit()
    conn.close()

@pytest.fixture(scope='function', autouse=True)
def app(qtbot):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Создаем экземпляр QApplication
    yield app  # Просто возвращаем приложение, не добавляем его в qtbot

@pytest.fixture(scope='function')
def reports_tab(qtbot):
    tab = ReportsTab()
    qtbot.addWidget(tab)  # Добавляем ReportsTab в qtbot
    yield tab
    tab.deleteLater()  # Используем deleteLater для безопасного удаления

def test_reports_tab_initial_state(reports_tab):
    reports_tab.show()  # Убедитесь, что таб виден
    assert reports_tab.reports_table.isVisible()
    assert reports_tab.flight_filter_combo.isVisible()
    assert reports_tab.date_filter_input.isVisible()
    assert reports_tab.generate_report_button.isVisible()
    assert reports_tab.reports_table.rowCount() == 0

def test_populate_reports_table(reports_tab):
    with patch('my_app.db_utils.get_flights') as mock_get_flights, \
         patch('my_app.db_utils.get_bookings') as mock_get_bookings, \
         patch('my_app.db_utils.calculate_revenue_and_profit') as mock_calculate:

        # Подготовка данных для моков
        mock_get_flights.return_value = [
            (1, 'FL123', QDate(2023, 5, 1)),
            (2, 'FL456', QDate(2023, 5, 2)),
        ]
        mock_get_bookings.return_value = [
            (1, 'FL123', 'John Doe', 100.0),  # booking_id, flight_number, passenger_name, ticket_price
            (2, 'FL123', 'Jane Doe', 100.0),
            (3, 'FL456', 'Bob Smith', 100.0),
        ]
        mock_calculate.return_value = (200, 100)

        reports_tab.populate_reports_table()

        assert reports_tab.reports_table.rowCount() == 2
        assert reports_tab.reports_table.item(0, 0).text() == 'FL123'
        assert reports_tab.reports_table.item(0, 2).text() == '2'
        assert reports_tab.reports_table.item(0, 3).text() == '200'
        assert reports_tab.reports_table.item(0, 4).text() == '100'
        assert reports_tab.reports_table.item(1, 0).text() == 'FL456'
        assert reports_tab.reports_table.item(1, 2).text() == '1'
        assert reports_tab.reports_table.item(1, 3).text() == '200'
        assert reports_tab.reports_table.item(1, 4).text() == '100'

def test_generate_report(reports_tab):
    with patch('my_app.db_utils.get_flights') as mock_get_flights, \
         patch('my_app.db_utils.get_bookings') as mock_get_bookings, \
         patch('my_app.db_utils.calculate_revenue_and_profit') as mock_calculate:

        mock_get_flights.return_value = [
            type('Flight', (object,), {'id': 1, 'number': 'FL123', 'date': QDate(2023, 5, 1)}),
            type('Flight', (object,), {'id': 2, 'number': 'FL456', 'date': QDate(2023, 5, 2)}),
        ]
        mock_get_bookings.return_value = [
            type('Booking', (object,), {'flight_id': 1}),
            type('Booking', (object,), {'flight_id': 1}),
            type('Booking', (object,), {'flight_id': 2}),
        ]
        mock_calculate.return_value = (200, 100)

        reports_tab.populate_flight_filter()

        reports_tab.flight_filter_combo.setCurrentText('FL123')
        reports_tab.date_filter_input.setDate(QDate(2023, 5, 1))

        reports_tab.generate_report()

        assert reports_tab.reports_table.rowCount() == 1
        assert reports_tab.reports_table.item(0, 0).text() == 'FL123'
        assert reports_tab.reports_table.item(0, 2).text() == '2'
        assert reports_tab.reports_table.item(0, 3).text() == '200'
        assert reports_tab.reports_table.item(0, 4).text() == '100'