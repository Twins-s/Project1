import os
import sqlite3

db_file = os.path.join(os.path.dirname(__file__), '../flights.db')

def create_database():
    db_file = os.path.join(os.path.dirname(__file__), '../flights.db')
    with sqlite3.connect(db_file) as conn:
        # Создание курсора для выполнения SQL-запросов
        c = conn.cursor()
        # Создание таблицы "users"
        c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    user_type TEXT NOT NULL
                )
            """)
        # Создание таблицы "flights"
        c.execute("""
                    CREATE TABLE IF NOT EXISTS flights (
                        flight_number TEXT,
                        date TEXT,
                        time TEXT,
                        `from` TEXT,
                        `to` TEXT
                    )
                """)
        # Создание таблицы "bookings"
        c.execute("""
                    CREATE TABLE IF NOT EXISTS bookings (
                        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flight_number TEXT,
                        passenger_name TEXT,
                        ticket_price REAL
                    )
                """)
        # Создание таблицы "complaints"
        c.execute("""
                    CREATE TABLE IF NOT EXISTS complaints (
                        complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name TEXT,
                        complaint_text TEXT,
                        status TEXT
                    )
                """)
        conn.commit()

def get_flights():
    conn = sqlite3.connect('../flights.db')
    c = conn.cursor()
    c.execute("SELECT rowid, flight_number, date FROM flights")  # Используйте rowid для идентификатора
    flights = c.fetchall()
    conn.close()
    return flights

def get_bookings():
    conn = sqlite3.connect('../flights.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return bookings

def calculate_revenue_and_profit(bookings):
    total_revenue = sum(b[3] for b in bookings)  # Предполагается, что цена - это четвертый элемент в кортеже
    total_profit = total_revenue * 0.8  # Например, 80% от выручки
    return total_revenue, total_profit

def add_complaint(customer_name, complaint_text):
    conn = sqlite3.connect('../flights.db')
    c = conn.cursor()
    c.execute("INSERT INTO complaints (customer_name, complaint_text, status) VALUES (?, ?, ?)", (customer_name, complaint_text, 'Открыта'))
    conn.commit()
    conn.close()

def get_complaints():
    conn = sqlite3.connect('../flights.db')
    c = conn.cursor()
    c.execute("SELECT * FROM complaints")
    complaints = c.fetchall()
    conn.close()
    return complaints

def resolve_complaint(complaint_id):
    conn = sqlite3.connect('../flights.db')
    c = conn.cursor()
    c.execute("UPDATE complaints SET status = 'Решена' WHERE complaint_id = ?", (complaint_id,))
    conn.commit()
    conn.close()

def create_user(username, password, user_type):
    db_file = os.path.join(os.path.dirname(__file__), '../flights.db')
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", (username, password, user_type))
        conn.commit()

def authenticate_user(username, password):
    db_file = os.path.join(os.path.dirname(__file__), '../flights.db')
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("SELECT user_type FROM users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            return None

__all__ = ['create_database', 'get_flights', 'get_bookings', 'calculate_revenue_and_profit', 'add_complaint', 'get_complaints', 'resolve_complaint']