from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from my_app.db_utils import create_database
from my_app.flight_management import FlightsTab
from my_app.passenger_management import PassengersTab
from my_app.customer_support import ComplaintsTab
from my_app.reporting import ReportsTab
from my_app.booking import BookingTab

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

class PassengerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

if __name__ == "__main__":
    app = QApplication([])
    create_database()
    admin_window = AdminWindow()
    admin_window.show()
    app.exec_()