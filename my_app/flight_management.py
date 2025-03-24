import sqlite3
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog, QMessageBox

class FlightsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.flights_table = QTableWidget()
        self.flights_table.setColumnCount(5)
        self.flights_table.setHorizontalHeaderLabels(["Номер рейса", "Дата", "Время", "Откуда", "Куда"])
        layout.addWidget(self.flights_table)

        self.populate_flights_table()

        self.setLayout(layout)

    def populate_flights_table(self):
        # Получаем список рейсов из базы данных
        flights = self.get_flights()

        # Очищаем таблицу
        self.flights_table.setRowCount(0)

        # Заполняем таблицу данными
        row = 0
        for flight in flights:
            self.flights_table.insertRow(row)
            self.flights_table.setItem(row, 0, QTableWidgetItem(flight["flight_number"]))
            self.flights_table.setItem(row, 1, QTableWidgetItem(flight["date"]))
            self.flights_table.setItem(row, 2, QTableWidgetItem(flight["time"]))
            self.flights_table.setItem(row, 3, QTableWidgetItem(flight["from"]))
            self.flights_table.setItem(row, 4, QTableWidgetItem(flight["to"]))
            row += 1

    def get_flights(self):
        conn = sqlite3.connect('../flights.db')
        c = conn.cursor()
        c.execute("SELECT * FROM flights")
        flights = c.fetchall()
        conn.close()

        result = []
        for flight in flights:
            flight_data = {
                "flight_number": flight[0],
                "date": flight[1],
                "time": flight[2],
                "from": flight[3],
                "to": flight[4]
            }
            result.append(flight_data)
        return result

    def show_add_flight_window(self):
        add_flight_window = AddFlightWindow(self)
        add_flight_window.exec_()

    def show_edit_flight_window(self):
        selected = self.flights_table.selectedItems()
        if selected:
            flight_number = selected[0].text()
            flight_data = self.get_flight_data(flight_number)
            edit_flight_window = EditFlightWindow(self, flight_data)
            edit_flight_window.exec_()

    def get_flight_data(self, flight_number):
        conn = sqlite3.connect('../flights.db')
        c = conn.cursor()
        c.execute("SELECT * FROM flights WHERE flight_number = ?", (flight_number,))
        flight = c.fetchone()
        conn.close()

        if flight:
            return {
                "flight_number": flight[0],
                "date": flight[1],
                "time": flight[2],
                "from": flight[3],
                "to": flight[4]
            }
        else:
            return None

    def delete_flight(self):
        selected = self.flights_table.selectedItems()
        if selected:
            flight_number = selected[0].text()
            reply = QMessageBox.question(self, 'Подтверждение', f"Вы уверены, что хотите удалить рейс {flight_number}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delete_flight_from_db(flight_number)
                self.populate_flights_table()

    def delete_flight_from_db(self, flight_number):
        conn = sqlite3.connect('../flights.db')
        c = conn.cursor()
        c.execute("DELETE FROM flights WHERE flight_number = ?", (flight_number,))
        conn.commit()
        conn.close()

class AddFlightWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.flight_number_input = QLineEdit()
        self.date_input = QLineEdit()
        self.time_input = QLineEdit()
        self.from_input = QLineEdit()
        self.to_input = QLineEdit()

        layout.addWidget(QLabel("Номер рейса:"))
        layout.addWidget(self.flight_number_input)
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.date_input)
        layout.addWidget(QLabel("Время:"))
        layout.addWidget(self.time_input)
        layout.addWidget(QLabel("Откуда:"))
        layout.addWidget(self.from_input)
        layout.addWidget(QLabel("Куда:"))
        layout.addWidget(self.to_input)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_flight)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_flight(self):
        flight_data = {
            "flight_number": self.flight_number_input.text(),
            "date": self.date_input.text(),
            "time": self.time_input.text(),
            "from": self.from_input.text(),
            "to": self.to_input.text()
        }
        self.parent().add_flight(flight_data)
        self.close()

class EditFlightWindow(QDialog):
    def __init__(self, parent=None, flight_data=None):
        super().__init__(parent)
        self.initUI(flight_data)

    def initUI(self, flight_data):
        layout = QVBoxLayout()

        self.flight_number_input = QLineEdit(flight_data["flight_number"])
        self.date_input = QLineEdit(flight_data["date"])
        self.time_input = QLineEdit(flight_data["time"])
        self.from_input = QLineEdit(flight_data["from"])
        self.to_input = QLineEdit(flight_data["to"])

        layout.addWidget(QLabel("Номер рейса:"))
        layout.addWidget(self.flight_number_input)
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.date_input)
        layout.addWidget(QLabel("Время:"))
        layout.addWidget(self.time_input)
        layout.addWidget(QLabel("Откуда:"))
        layout.addWidget(self.from_input)
        layout.addWidget(QLabel("Куда:"))
        layout.addWidget(self.to_input)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_flight)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_flight(self):
        flight_data = {
            "flight_number": self.flight_number_input.text(),
            "date": self.date_input.text(),
            "time": self.time_input.text(),
            "from": self.from_input.text(),
            "to": self.to_input.text()
        }
        self.parent().edit_flight(flight_data)
        self.close()