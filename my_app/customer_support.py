from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QTextEdit
from my_app.db_utils import add_complaint, get_complaints, resolve_complaint

class ComplaintsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.add_complaint_window = AddComplaintWindow(self)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.complaints_table = QTableWidget()
        self.complaints_table.setColumnCount(4)
        self.complaints_table.setHorizontalHeaderLabels(["Пассажир", "Дата", "Тема", "Описание"])
        self.layout.addWidget(self.complaints_table)

        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)

    def populate_complaints_table(self):
        # Загрузка списка жалоб из базы данных
        complaints = get_complaints()

        # Очистка таблицы
        self.complaints_table.setRowCount(0)

        # Заполнение таблицы жалоб
        row = 0
        for complaint in complaints:
            self.complaints_table.insertRow(row)
            self.complaints_table.setItem(row, 0, QTableWidgetItem(complaint.passenger))
            self.complaints_table.setItem(row, 1, QTableWidgetItem(complaint.date))
            self.complaints_table.setItem(row, 2, QTableWidgetItem(complaint.subject))
            self.complaints_table.setItem(row, 3, QTableWidgetItem(complaint.description))
            row += 1
    def add_complaint_window(self):
        return self.add_complaint_window
    def resolve_complaint_window(self):
        return self
    def add_complaint(self, complaint_data):
        # Добавление новой жалобы в базу данных
        add_complaint(complaint_data)

        # Обновление таблицы жалоб
        self.populate_complaints_table()

    def resolve_complaint(self):
        # Получение выбранной строки в таблице жалоб
        selected_row = self.complaints_table.currentRow()
        if selected_row >= 0:
            # Получение ID жалобы из выбранной строки
            complaint_id = self.complaints_table.item(selected_row, 0).text()

            # Разрешение жалобы в базе данных
            resolve_complaint(complaint_id)

            # Обновление таблицы жалоб
            self.populate_complaints_table()

class AddComplaintWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.passenger_label = QLabel("Пассажир:")
        self.passenger_input = QLineEdit()
        self.date_label = QLabel("Дата:")
        self.date_input = QLineEdit()
        self.subject_label = QLabel("Тема:")
        self.subject_input = QLineEdit()
        self.description_label = QLabel("Описание:")
        self.description_input = QTextEdit()

        self.layout.addWidget(self.passenger_label)
        self.layout.addWidget(self.passenger_input)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_input)
        self.layout.addWidget(self.subject_label)
        self.layout.addWidget(self.subject_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)

        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.save_button.clicked.connect(self.save_complaint)
        self.cancel_button.clicked.connect(self.close)

    def save_complaint(self):
        complaint_data = {
            "passenger": self.passenger_input.text(),
            "date": self.date_input.text(),
            "subject": self.subject_input.text(),
            "description": self.description_input.toPlainText()
        }
        self.parent().add_complaint(complaint_data)
        self.close()