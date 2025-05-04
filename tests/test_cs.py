import pytest
from my_app.customer_support import ComplaintsTab
from unittest.mock import patch, MagicMock

@pytest.fixture
def complaints_tab(qtbot):
    """Фикстура для создания экземпляра ComplaintsTab."""
    tab = ComplaintsTab()
    qtbot.addWidget(tab)
    tab.show()
    return tab

@patch('my_app.db_utils.get_complaints')
def test_populate_complaints_table(mock_get_complaints, complaints_tab):
    """Тест на заполнение таблицы жалоб."""
    # Настройка мок-объекта
    mock_get_complaints.return_value = [
        MagicMock(passenger="Иван Иванов", date="2025-05-01", subject="Проблема с рейсом", description="Описание проблемы"),
        MagicMock(passenger="Мария Петрова", date="2025-05-02", subject="Отмена рейса", description="Описание отмены")
    ]

    # Заполнение таблицы
    complaints_tab.populate_complaints_table()

    # Проверка, что таблица заполнена корректно
    assert complaints_tab.complaints_table.rowCount() == 2
    assert complaints_tab.complaints_table.item(0, 0).text() == "Иван Иванов"
    assert complaints_tab.complaints_table.item(1, 0).text() == "Мария Петрова"

def test_add_complaint(complaints_tab, qtbot):
    """Тест на добавление новой жалобы."""
    # Открытие окна для добавления жалобы
    add_complaint_window = complaints_tab.add_complaint_window
    add_complaint_window.passenger_input.setText("Иван Иванов")
    add_complaint_window.date_input.setText("2025-05-01")
    add_complaint_window.subject_input.setText("Проблема с рейсом")
    add_complaint_window.description_input.setPlainText("Описание проблемы")

    # Мокаем функцию добавления жалобы
    with patch('my_app.db_utils.add_complaint') as mock_add_complaint:
        add_complaint_window.save_complaint()

        # Проверяем, что функция добавления жалобы была вызвана
        mock_add_complaint.assert_called_once()

    # Проверка, что таблица обновилась
    complaints_tab.populate_complaints_table()
    assert complaints_tab.complaints_table.rowCount() == 1
    assert complaints_tab.complaints_table.item(0, 0).text() == "Иван Иванов"

@patch('my_app.db_utils.resolve_complaint')
def test_resolve_complaint(mock_resolve_complaint, complaints_tab, qtbot):
    """Тест на разрешение жалобы."""
    # Добавляем жалобу для разрешения
    complaints_tab.add_complaint({
        "passenger": "Иван Иванов",
        "date": "2025-05-01",
        "subject": "Проблема с рейсом",
        "description": "Описание проблемы"
    })

    # Выбор строки для разрешения
    complaints_tab.complaints_table.selectRow(0)

    # Вызов метода разрешения жалобы
    complaints_tab.resolve_complaint()

    # Проверка, что функция разрешения жалобы была вызвана
    mock_resolve_complaint.assert_called_once_with("Иван Иванов")

    # Проверка, что таблица пуста после разрешения
    complaints_tab.populate_complaints_table()
    assert complaints_tab.complaints_table.rowCount() == 0