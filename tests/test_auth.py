import pytest
from PyQt5.QtWidgets import QApplication
from my_app.auth import AuthWindow
from my_app.db_utils import create_database, authenticate_user

@pytest.fixture(scope='session')
def app():
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def auth_window(qtbot, app):
    window = AuthWindow(None, None)  # Передайте None или создайте моки для окон
    qtbot.addWidget(window)
    window.show()
    yield window

def test_login_with_valid_admin_credentials(auth_window):
    auth_window.username_input.setText("admin")
    auth_window.password_input.setText("admin")
    auth_window.login()
    assert auth_window.admin_window.isVisible()
    assert not auth_window.passenger_window.isVisible()

def test_login_with_valid_user_credentials(auth_window):
    create_database()
    auth_window.register_button.click()
    auth_window.username_input.setText("newuser")
    auth_window.password_input.setText("newpassword")
    auth_window.register()
    auth_window.login_button.click()
    auth_window.username_input.setText("newuser")
    auth_window.password_input.setText("newpassword")
    auth_window.login()
    assert auth_window.passenger_window.isVisible()
    assert not auth_window.admin_window.isVisible()

def test_login_with_invalid_credentials(auth_window, capsys):
    auth_window.username_input.setText("invalid")
    auth_window.password_input.setText("invalid")
    auth_window.login()
    out, err = capsys.readouterr()
    assert "Неверное имя пользователя или пароль" in out
    assert not auth_window.admin_window.isVisible()
    assert not auth_window.passenger_window.isVisible()

def test_register_new_user(auth_window):
    create_database()
    auth_window.username_input.setText("newuser")
    auth_window.password_input.setText("newpassword")
    auth_window.register()
    assert authenticate_user("newuser", "newpassword") == "user"
    assert auth_window.passenger_window.isVisible()
    assert not auth_window.admin_window.isVisible()

def test_cannot_register_existing_user(auth_window, capsys):
    create_database()
    auth_window.username_input.setText("admin")
    auth_window.password_input.setText("admin")
    auth_window.register()
    out, err = capsys.readouterr()
    assert "Пользователь с таким именем уже существует" in out