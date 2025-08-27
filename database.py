import os
import sys
import sqlite3
from typing import List, Tuple, Optional


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller exe."""
    try:
        # When bundled by PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # When running normally
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


DB_FILE = resource_path("flights.db")


class Database:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self._ensure_table()

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def _ensure_table(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_reservation(self, name: str, flight_number: str, departure: str,
                        destination: str, date: str, seat_number: str) -> int:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, flight_number, departure, destination, date, seat_number))
        conn.commit()
        rowid = cur.lastrowid
        conn.close()
        return rowid

    def get_all_reservations(self) -> List[Tuple]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, name, flight_number, departure, destination, date, seat_number FROM reservations ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_reservation(self, reservation_id: int) -> Optional[Tuple]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, name, flight_number, departure, destination, date, seat_number FROM reservations WHERE id = ?", (reservation_id,))
        row = cur.fetchone()
        conn.close()
        return row

    def update_reservation(self, reservation_id: int, name: str, flight_number: str, departure: str,
                           destination: str, date: str, seat_number: str) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE reservations
            SET name = ?, flight_number = ?, departure = ?, destination = ?, date = ?, seat_number = ?
            WHERE id = ?
        """, (name, flight_number, departure, destination, date, seat_number, reservation_id))
        conn.commit()
        conn.close()

    def delete_reservation(self, reservation_id: int) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        conn.commit()
        conn.close()


# Provide a global db instance convenient for imports
db = Database()
