import sqlite3
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog

class FlightsTab(QWidget):
    def __init__(self):
        super().__init__()
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
        conn = sqlite3.connect('flights.db')
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

    def add_flight(self, flight_data):
        conn = sqlite3.connect('flights.db')
        c = conn.cursor()
        c.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?)", (
            flight_data["flight_number"],
            flight_data["date"],
            flight_data["time"],
            flight_data["from"],
            flight_data["to"]
        ))
        conn.commit()
        conn.close()
        self.populate_flights_table()

    def edit_flight(self, flight_data):
        conn = sqlite3.connect('flights.db')
        c = conn.cursor()
        c.execute("UPDATE flights SET date = ?, time = ?, `from` = ?, `to` = ? WHERE flight_number = ?", (
            flight_data["date"],
            flight_data["time"],
            flight_data["from"],
            flight_data["to"],
            flight_data["flight_number"]
        ))
        conn.commit()
        conn.close()
        self.populate_flights_table()

    def delete_flight(self):
        selected = self.flights_table.selectedItems()
        if selected:
            flight_number = selected[0].text()
            conn = sqlite3.connect('flights.db')
            c = conn.cursor()
            c.execute("DELETE FROM flights WHERE flight_number = ?", (flight_number,))
            conn.commit()
            conn.close()
            self.populate_flights_table()

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
        self.parent().edit_flight(flight_data)
        self.close()