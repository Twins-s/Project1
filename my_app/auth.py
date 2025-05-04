from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from my_app.db_utils import create_user, authenticate_user, create_database

class AuthWindow(QWidget):
    def __init__(self, admin_window, passenger_window, parent=None):
        super().__init__(parent)
        self.admin_window = admin_window
        self.passenger_window = passenger_window
        self.initUI()

        # Создаем предустановленный аккаунт администратора
        self.admin_account = {
            "username": "admin",
            "password": "admin"
        }

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Войти")
        self.register_button = QPushButton("Зарегистрироваться")

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Проверяем, является ли пользователь администратором
        if username == self.admin_account["username"] and password == self.admin_account["password"]:
            self.admin_window.show()
        else:
            user_type = authenticate_user(username, password)
            if user_type == "user":
                self.passenger_window.show()
            else:
                QMessageBox.critical(self, "Ошибка входа", "Неверное имя пользователя или пароль.")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        create_database()  # Вызываем create_database() перед созданием пользователя
        create_user(username, password, "user")
        QMessageBox.information(self, "Регистрация", "Вы успешно зарегистрировались.")