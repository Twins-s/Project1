from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QDateEdit
from my_app.db_utils import get_flights, get_bookings, calculate_revenue_and_profit

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.controls_layout = QHBoxLayout()
    
        self.flight_filter_label = QLabel("Рейс:")
        self.flight_filter_combo = QComboBox()
        self.date_filter_label = QLabel("Дата:")
        self.date_filter_input = QDateEdit()
        self.generate_report_button = QPushButton("Сгенерировать отчет")

        self.controls_layout.addWidget(self.flight_filter_label)
        self.controls_layout.addWidget(self.flight_filter_combo)
        self.controls_layout.addWidget(self.date_filter_label)
        self.controls_layout.addWidget(self.date_filter_input)
        self.controls_layout.addWidget(self.generate_report_button)

        self.layout.addLayout(self.controls_layout)

        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(5)
        self.reports_table.setHorizontalHeaderLabels(["Рейс", "Дата", "Количество пассажиров", "Выручка", "Прибыль"])
        self.layout.addWidget(self.reports_table)

        self.generate_report_button.clicked.connect(self.generate_report)

        self.populate_reports_table()
        self.populate_flight_filter()

    def populate_reports_table(self):
        try:
            flights = get_flights()  # Теперь это список кортежей
            bookings = get_bookings()

            self.reports_table.setRowCount(0)

            row = 0
            for flight in flights:
                flight_id, flight_number, flight_date = flight  # Распаковываем кортеж
                flight_bookings = [b for b in bookings if b[1] == flight_number]  # Измените на b[1], чтобы использовать flight_number
                num_passengers = len(flight_bookings)
                revenue, profit = calculate_revenue_and_profit(flight_bookings)  # Передаем flight_bookings

                self.reports_table.insertRow(row)
                self.reports_table.setItem(row, 0, QTableWidgetItem(flight_number))
                self.reports_table.setItem(row, 1, QTableWidgetItem(flight_date))
                self.reports_table.setItem(row, 2, QTableWidgetItem(str(num_passengers)))
                self.reports_table.setItem(row, 3, QTableWidgetItem(str(revenue)))
                self.reports_table.setItem(row, 4, QTableWidgetItem(str(profit)))
                row += 1
        except Exception as e:
            print(f"Ошибка при заполнении таблицы отчетов: {e}")

    def populate_flight_filter(self):
        flights = get_flights()  # Теперь это список кортежей

        self.flight_filter_combo.clear()
        self.flight_filter_combo.addItem("Все рейсы")
        for flight in flights:
            flight_id, flight_number, flight_date = flight  # Распаковываем кортеж
            self.flight_filter_combo.addItem(flight_number)

    def generate_report(self):
        selected_flight = self.flight_filter_combo.currentText()
        selected_date = self.date_filter_input.date().toString("yyyy-MM-dd")

        flights = get_flights()
        bookings = get_bookings()

        filtered_flights = [f for f in flights if (selected_flight == "Все рейсы" or f[1] == selected_flight) and f[2] == selected_date]

        # Очистка таблицы
        self.reports_table.setRowCount(0)

        row = 0
        for flight in filtered_flights:
            flight_number = flight[1]
            flight_bookings = [b for b in bookings if b[1] == flight_number]
            num_passengers = len(flight_bookings)
            revenue, profit = calculate_revenue_and_profit(flight_bookings)

            self.reports_table.insertRow(row)
            self.reports_table.setItem(row, 0, QTableWidgetItem(flight_number))
            self.reports_table.setItem(row, 1, QTableWidgetItem(flight[2]))  # Дата
            self.reports_table.setItem(row, 2, QTableWidgetItem(str(num_passengers)))
            self.reports_table.setItem(row, 3, QTableWidgetItem(str(revenue)))
            self.reports_table.setItem(row, 4, QTableWidgetItem(str(profit)))
            row += 1