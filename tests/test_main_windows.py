import pytest
from PyQt5.QtWidgets import QApplication
from my_app.main_windows import AdminWindow, PassengerWindow

@pytest.fixture(scope='session')
def app():
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def admin_window(qtbot, app):
    window = AdminWindow()
    qtbot.addWidget(window)
    window.show()
    yield window

def test_admin_window_initial_state(admin_window):
    assert admin_window.add_flight_button.isVisible()
    assert admin_window.edit_flight_button.isVisible()
    assert admin_window.delete_flight_button.isVisible()
    assert not admin_window.resolve_complaint_button.isVisible()

def test_admin_window_tab_change(admin_window):
    admin_window.tab_widget.setCurrentIndex(2)
    assert not admin_window.add_flight_button.isVisible()
    assert not admin_window.edit_flight_button.isVisible()
    assert not admin_window.delete_flight_button.isVisible()
    assert admin_window.resolve_complaint_button.isVisible()

@pytest.fixture
def passenger_window(qtbot, app):
    window = PassengerWindow()
    qtbot.addWidget(window)
    window.show()
    yield window

def test_passenger_window_initial_state(passenger_window):
    assert not passenger_window.add_complaint_button.isVisible()

def test_passenger_window_tab_change(passenger_window):
    passenger_window.tab_widget.setCurrentIndex(2)
    assert passenger_window.add_complaint_button.isVisible()

def test_passenger_window_tab_change_to_flights(passenger_window):
    passenger_window.tab_widget.setCurrentIndex(0)
    assert not passenger_window.add_complaint_button.isVisible()