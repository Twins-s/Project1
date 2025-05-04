import pytest
from PyQt5.QtCore import QDate
from my_app.booking import BookingTab

@pytest.fixture
def booking_tab(qtbot):
    """Фикстура для создания экземпляра BookingTab."""
    tab = BookingTab()
    qtbot.addWidget(tab)
    tab.show()
    return tab

def test_initial_ui(booking_tab):
    """Тест на начальное состояние интерфейса."""
    assert booking_tab.flight_number_input.text() == ""
    assert booking_tab.passenger_name_input.text() == ""
    assert booking_tab.passenger_email_input.text() == ""

def test_book_flight(booking_tab, qtbot):
    """Тест на добавление нового бронирования."""
    # Заполнение полей ввода
    booking_tab.flight_number_input.setText("123")
    booking_tab.flight_date_input.setDate(QDate(2025, 5, 3))
    booking_tab.passenger_name_input.setText("Иван Иванов")
    booking_tab.passenger_email_input.setText("ivan@example.com")

    # Вызов метода book_flight (нужно будет реализовать логику)
    booking_tab.book_flight()

    # Проверка, что данные добавлены в таблицу
    assert booking_tab.bookings_table.rowCount() == 1
    assert booking_tab.bookings_table.item(0, 0).text() == "123"
    assert booking_tab.bookings_table.item(0, 2).text() == "Иван Иванов"
    assert booking_tab.bookings_table.item(0, 3).text() == "ivan@example.com"

def test_cancel_booking(booking_tab, qtbot):
    """Тест на отмену бронирования."""
    # Добавляем бронирование для отмены
    booking_tab.flight_number_input.setText("123")
    booking_tab.passenger_name_input.setText("Иван Иванов")
    booking_tab.passenger_email_input.setText("ivan@example.com")
    booking_tab.book_flight()

    # Проверяем, что бронирование добавлено
    assert booking_tab.bookings_table.rowCount() == 1

    # Выбор строки для отмены
    booking_tab.bookings_table.selectRow(0)

    # Вызов метода cancel_booking (нужно будет реализовать логику)
    booking_tab.cancel_booking()

    # Проверка, что таблица пуста
    assert booking_tab.bookings_table.rowCount() == 0