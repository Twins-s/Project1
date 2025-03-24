import sys
sys.path.append('D:\\Python programs\\Project1\\my_app')
from PyQt5.QtWidgets import QApplication, QWidget
from my_app.db_utils import create_database
from my_app.auth import AuthWindow
from my_app.main_windows import AdminWindow, PassengerWindow

class MainWindow(QWidget):
    def __init__(self, args):
        super().__init__()
        self.admin_window = AdminWindow(self)
        self.passenger_window = PassengerWindow(self)
        self.auth_window = AuthWindow(self.admin_window, self.passenger_window, self)
        self.auth_window.show()

    def show_admin_window(self):
        self.auth_window.close()
        self.admin_window.show()

    def show_passenger_window(self):
        self.auth_window.close()
        self.passenger_window.show()

if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    main_window = MainWindow(sys.argv)
    main_window.show()
    sys.exit(app.exec_())