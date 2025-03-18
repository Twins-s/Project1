import sqlite3

def create_database():
    # Создание соединения с базой данных
    conn = sqlite3.connect('flights.db')

    # Создание курсора для выполнения SQL-запросов
    c = conn.cursor()

    # Создание таблицы "flights"
    c.execute("""CREATE TABLE IF NOT EXISTS flights (
                 flight_number TEXT,
                 date TEXT,
                 time TEXT,
                 `from` TEXT,
                 `to` TEXT
             )""")

    # Создание таблицы "bookings"
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
                 booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 flight_number TEXT,
                 passenger_name TEXT,
                 ticket_price REAL
             )""")

    # Создание таблицы "complaints"
    c.execute("""CREATE TABLE IF NOT EXISTS complaints (
                    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    complaint_text TEXT,
                    status TEXT
                )""")

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

def get_flights():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute("SELECT * FROM flights")
    flights = c.fetchall()
    conn.close()
    return flights

def get_bookings():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return bookings

def calculate_revenue_and_profit():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute("SELECT SUM(ticket_price) AS total_revenue FROM bookings")
    revenue = c.fetchone()[0]
    c.execute("SELECT SUM(ticket_price) * 0.8 AS total_profit FROM bookings")
    profit = c.fetchone()[0]
    conn.close()
    return revenue, profit

def add_complaint(customer_name, complaint_text):
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute("INSERT INTO complaints (customer_name, complaint_text, status) VALUES (?, ?, ?)", (customer_name, complaint_text, 'Открыта'))
    conn.commit()
    conn.close()

def get_complaints():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute("SELECT * FROM complaints")
    complaints = c.fetchall()
    conn.close()
    return complaints

def resolve_complaint(complaint_id):
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute("UPDATE complaints SET status = 'Решена' WHERE complaint_id = ?", (complaint_id,))
    conn.commit()
    conn.close()

__all__ = ['create_database', 'get_flights', 'get_bookings', 'calculate_revenue_and_profit', 'add_complaint', 'get_complaints', 'resolve_complaint']