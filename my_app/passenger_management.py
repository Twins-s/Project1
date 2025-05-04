import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class PassengersTab(QWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection  # Сохраняем соединение с БД
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Таблица для отображения списка пассажиров
        self.passengers_table = QTableWidget()
        self.passengers_table.setColumnCount(3)
        self.passengers_table.setHorizontalHeaderLabels(["Имя", "Email", "Телефон"])
        layout.addWidget(self.passengers_table)

        # Кнопки для управления пассажирами
        buttons_layout = QHBoxLayout()
        self.edit_passenger_button = QPushButton("Редактировать пассажира")
        self.delete_passenger_button = QPushButton("Удалить пассажира")
        buttons_layout.addWidget(self.edit_passenger_button)
        buttons_layout.addWidget(self.delete_passenger_button)
        layout.addLayout(buttons_layout)

        # Заполнение таблицы пассажиров
        self.load_passengers()

    def load_passengers(self):
        try:
            c = self.db_connection.cursor()

            # Получение списка пассажиров
            c.execute("SELECT passenger_name, booking_id, ticket_price FROM bookings")
            passengers = c.fetchall()

            # Заполнение таблицы
            self.passengers_table.setRowCount(len(passengers))
            for i, passenger in enumerate(passengers):
                self.passengers_table.setItem(i, 0, QTableWidgetItem(passenger[0]))
                self.passengers_table.setItem(i, 1, QTableWidgetItem(str(passenger[1])))
                self.passengers_table.setItem(i, 2, QTableWidgetItem(str(passenger[2])))

        except sqlite3.Error as e:
            print(f"Ошибка при загрузке пассажиров: {e}")

    def edit_passenger(self):
        try:
            # Получение выбранной строки
            selected_row = self.passengers_table.currentRow()
            if selected_row == -1:
                return

            # Получение данных пассажира
            passenger_name = self.passengers_table.item(selected_row, 0).text()
            booking_id = int(self.passengers_table.item(selected_row, 1).text())
            ticket_price = float(self.passengers_table.item(selected_row, 2).text())

            # Обновление данных пассажира в базе данных
            conn = sqlite3.connect('../flights.db')
            c = conn.cursor()
            c.execute("UPDATE bookings SET passenger_name = ?, ticket_price = ? WHERE booking_id = ?", (passenger_name, ticket_price, booking_id))
            conn.commit()
            conn.close()

            # Обновление таблицы
            self.load_passengers()
        except sqlite3.Error as e:
            print(f"Ошибка при редактировании пассажира: {e}")

    def delete_passenger(self):
        try:
            # Получение выбранной строки
            selected_row = self.passengers_table.currentRow()
            if selected_row == -1:
                return

            # Получение booking_id пассажира
            booking_id = int(self.passengers_table.item(selected_row, 1).text())

            # Удаление пассажира из базы данных
            conn = sqlite3.connect('../flights.db')
            c = conn.cursor()
            c.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
            conn.commit()
            conn.close()

            # Обновление таблицы
            self.load_passengers()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пассажира: {e}")