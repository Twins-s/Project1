from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QDateEdit
from db_utils import get_flights, get_bookings, calculate_revenue_and_profit

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(5)
        self.reports_table.setHorizontalHeaderLabels(["Рейс", "Дата", "Количество пассажиров", "Выручка", "Прибыль"])
        self.layout.addWidget(self.reports_table)

        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)

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

        self.generate_report_button.clicked.connect(self.generate_report)

        self.populate_reports_table()
        self.populate_flight_filter()

    def populate_reports_table(self):
        # Загрузка списка рейсов и бронирований из базы данных
        flights = get_flights()
        bookings = get_bookings()

        # Очистка таблицы
        self.reports_table.setRowCount(0)

        # Заполнение таблицы отчетов
        row = 0
        for flight in flights:
            flight_bookings = [b for b in bookings if b.flight_id == flight.id]
            num_passengers = len(flight_bookings)
            revenue, profit = calculate_revenue_and_profit(flight_bookings)

            self.reports_table.insertRow(row)
            self.reports_table.setItem(row, 0, QTableWidgetItem(flight.number))
            self.reports_table.setItem(row, 1, QTableWidgetItem(flight.date.strftime("%Y-%m-%d")))
            self.reports_table.setItem(row, 2, QTableWidgetItem(str(num_passengers)))
            self.reports_table.setItem(row, 3, QTableWidgetItem(str(revenue)))
            self.reports_table.setItem(row, 4, QTableWidgetItem(str(profit)))
            row += 1

    def populate_flight_filter(self):
        # Загрузка списка рейсов из базы данных
        flights = get_flights()

        # Заполнение выпадающего списка рейсов
        self.flight_filter_combo.clear()
        self.flight_filter_combo.addItem("Все рейсы")
        for flight in flights:
            self.flight_filter_combo.addItem(flight.number)

    def generate_report(self):
        # Получение выбранных фильтров
        selected_flight = self.flight_filter_combo.currentText()
        selected_date = self.date_filter_input.date().toString("yyyy-MM-dd")

        # Загрузка списка рейсов и бронирований из базы данных
        flights = get_flights()
        bookings = get_bookings()

        # Фильтрация данных
        filtered_flights = [f for f in flights if (selected_flight == "Все рейсы" or f.number == selected_flight) and f.date.strftime("%Y-%m-%d") == selected_date]
        filtered_bookings = [b for b in bookings if b.flight_id in [f.id for f in filtered_flights]]

        # Очистка таблицы
        self.reports_table.setRowCount(0)

        # Заполнение таблицы отчетов
        row = 0
        for flight in filtered_flights:
            flight_bookings = [b for b in filtered_bookings if b.flight_id == flight.id]
            num_passengers = len(flight_bookings)
            revenue, profit = calculate_revenue_and_profit(flight_bookings)

            self.reports_table.insertRow(row)
            self.reports_table.setItem(row, 0, QTableWidgetItem(flight.number))
            self.reports_table.setItem(row, 1, QTableWidgetItem(flight.date.strftime("%Y-%m-%d")))
            self.reports_table.setItem(row, 2, QTableWidgetItem(str(num_passengers)))
            self.reports_table.setItem(row, 3, QTableWidgetItem(str(revenue)))
            self.reports_table.setItem(row, 4, QTableWidgetItem(str(profit)))
            row += 1