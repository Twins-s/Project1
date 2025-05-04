from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton
from my_app.flight_management import FlightsTab
from my_app.passenger_management import PassengersTab
from my_app.customer_support import ComplaintsTab
from my_app.reporting import ReportsTab
from my_app.booking import BookingTab

class AdminWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авиакомпания - Администратор")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.flights_tab = FlightsTab()
        self.passengers_tab = PassengersTab()
        self.complaints_tab = ComplaintsTab()
        self.reports_tab = ReportsTab()

        self.tab_widget.addTab(self.flights_tab, "Управление рейсами")
        self.tab_widget.addTab(self.passengers_tab, "Управление пассажирами")
        self.tab_widget.addTab(self.complaints_tab, "Обработка жалоб")
        self.tab_widget.addTab(self.reports_tab, "Отчетность")

        # Добавляем кнопки для управления рейсами
        self.add_flight_button = QPushButton("Добавить рейс")
        self.add_flight_button.clicked.connect(self.flights_tab.show_add_flight_window)
        self.add_flight_button.setVisible(self.tab_widget.currentIndex() == 0)
        self.layout.addWidget(self.add_flight_button)

        self.edit_flight_button = QPushButton("Изменить рейс")
        self.edit_flight_button.clicked.connect(self.flights_tab.show_edit_flight_window)
        self.edit_flight_button.setVisible(self.tab_widget.currentIndex() == 0)
        self.layout.addWidget(self.edit_flight_button)

        self.delete_flight_button = QPushButton("Удалить рейс")
        self.delete_flight_button.clicked.connect(self.flights_tab.delete_flight)
        self.delete_flight_button.setVisible(self.tab_widget.currentIndex() == 0)
        self.layout.addWidget(self.delete_flight_button)

        # Подключаем сигнал о смене вкладки, чтобы обновлять видимость кнопок
        self.tab_widget.currentChanged.connect(self.update_button_visibility)

        self.resolve_complaint_button = QPushButton("Разрешить жалобу")
        self.resolve_complaint_button.clicked.connect(self.complaints_tab.resolve_complaint)
        self.resolve_complaint_button.setVisible(False)  # Делаем кнопку невидимой изначально
        self.layout.addWidget(self.resolve_complaint_button)

    def update_button_visibility(self, index):
        self.add_flight_button.setVisible(index == 0)
        self.edit_flight_button.setVisible(index == 0)
        self.delete_flight_button.setVisible(index == 0)
        self.resolve_complaint_button.setVisible(index == 2)
class PassengerWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авиакомпания - Пассажир")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.flights_tab = FlightsTab()
        self.booking_tab = BookingTab()
        self.complaints_tab = ComplaintsTab()

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.tab_widget.addTab(self.flights_tab, "Доступные рейсы")
        self.tab_widget.addTab(self.booking_tab, "Бронирование билетов")
        self.tab_widget.addTab(self.complaints_tab, "Жалобы")

        self.add_complaint_button = QPushButton("Добавить жалобу")
        self.add_complaint_button.clicked.connect(self.complaints_tab.add_complaint_window.show)
        self.add_complaint_button.setVisible(False)  # Делаем кнопку невидимой изначально
        self.layout.addWidget(self.add_complaint_button)

        # Подключаем сигнал о смене вкладки, чтобы обновлять видимость кнопки
        self.tab_widget.currentChanged.connect(self.update_button_visibility)

    def update_button_visibility(self, index):
        self.add_complaint_button.setVisible(index == 2)