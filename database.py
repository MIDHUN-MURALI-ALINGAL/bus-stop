import sqlite3
import bcrypt
import os
from datetime import datetime

DB_FOLDER = "database"
DB_NAME = "smart_bus.db"

os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, DB_NAME)


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        # ---------------- USERS ----------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            created_at TEXT
        )
        """)

        # ---------------- SEARCH HISTORY ----------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            searched_place TEXT,
            search_time TEXT
        )
        """)

        # ---------------- FAVOURITES ----------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS favourites(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bus_stop TEXT
        )
        """)

        self.conn.commit()

    # ---------------- REGISTER ----------------

    def register_user(self, fullname, email, phone, password):

        self.cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        if self.cursor.fetchone():
            return False, "Email already registered."

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        self.cursor.execute("""
        INSERT INTO users
        (fullname,email,phone,password,created_at)
        VALUES(?,?,?,?,?)
        """, (
            fullname,
            email,
            phone,
            hashed.decode(),
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))

        self.conn.commit()

        return True, "Registration Successful"

    # ---------------- LOGIN ----------------

    def login_user(self, email, password):

        self.cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = self.cursor.fetchone()

        if user is None:
            return None

        stored_password = user[4]

        if bcrypt.checkpw(
                password.encode(),
                stored_password.encode()):

            return user

        return None

    # ---------------- PROFILE ----------------

    def get_user(self, user_id):

        self.cursor.execute(
            "SELECT * FROM users WHERE id=?",
            (user_id,)
        )

        return self.cursor.fetchone()

    # ---------------- UPDATE PROFILE ----------------

    def update_profile(self,
                       user_id,
                       fullname,
                       phone):

        self.cursor.execute("""
        UPDATE users
        SET fullname=?,
            phone=?
        WHERE id=?
        """, (
            fullname,
            phone,
            user_id
        ))

        self.conn.commit()

    # ---------------- DELETE ACCOUNT ----------------

    def delete_account(self, user_id):

        self.cursor.execute(
            "DELETE FROM users WHERE id=?",
            (user_id,)
        )

        self.conn.commit()

    # ---------------- SEARCH HISTORY ----------------

    def add_history(self,
                    user_id,
                    place):

        self.cursor.execute("""
        INSERT INTO history
        (user_id,searched_place,search_time)
        VALUES(?,?,?)
        """, (
            user_id,
            place,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))

        self.conn.commit()

    def get_history(self, user_id):

        self.cursor.execute("""
        SELECT searched_place,
               search_time
        FROM history
        WHERE user_id=?
        ORDER BY id DESC
        """, (user_id,))

        return self.cursor.fetchall()

    # ---------------- FAVOURITES ----------------

    def add_favourite(self,
                      user_id,
                      stop):

        self.cursor.execute("""
        INSERT INTO favourites
        (user_id,bus_stop)
        VALUES(?,?)
        """, (
            user_id,
            stop
        ))

        self.conn.commit()

    def get_favourites(self,
                       user_id):

        self.cursor.execute("""
        SELECT bus_stop
        FROM favourites
        WHERE user_id=?
        """, (user_id,))

        return self.cursor.fetchall()


db = Database()