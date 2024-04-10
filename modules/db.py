# db.py

import sqlite3
from colorama import Fore, Style
import random
import sys

def create_tables(conn, config):
    try:
        cursor = conn.cursor()

        for table_name, columns in config["database"]["tables"].items():
            columns_definition = ', '.join(columns)
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")

        conn.commit()
        cursor.close()
        print_success("Tablas creadas correctamente.")
    except Exception as e:
        print_error(f"Error al crear las tablas en la base de datos: {e}")
        sys.exit(1)

def insert_proxy(conn, proxy):
    try:
        cursor = conn.cursor()
        ip, port = proxy.split(':') if ':' in proxy else (proxy, None)
        cursor.execute("INSERT INTO proxys (ip, port) VALUES (?, ?)", (ip, port))
        conn.commit()
        cursor.close()
        print_success(f"Proxy insertado en la base de datos: {proxy}")
    except Exception as e:
        pass

def insert_usernames(conn, usernames):
    try:
        cursor = conn.cursor()
        for username in usernames:
            cursor.execute("INSERT INTO Usernames (username) VALUES (?)", (username,))
        conn.commit()
        cursor.close()
        print_success("Usernames insertados correctamente.")
    except Exception as e:
        print_error(f"Error al insertar los usernames en la base de datos: {e}")

def insert_passwords(conn, passwords):
    try:
        cursor = conn.cursor()
        for password in passwords:
            cursor.execute("INSERT INTO Passwords (password) VALUES (?)", (password,))
        conn.commit()
        cursor.close()
        print_success("Passwords insertados correctamente.")
    except Exception as e:
        print_error(f"Error al insertar los passwords en la base de datos: {e}")

def generate_combos(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Combos")
        cursor.execute("SELECT username FROM Usernames")
        usernames = [record[0] for record in cursor.fetchall()]
        cursor.execute("SELECT password FROM Passwords")
        passwords = [record[0] for record in cursor.fetchall()]

        for _ in range(100):
            username = random.choice(usernames)
            password = random.choice(passwords)
            cursor.execute("INSERT INTO Combos (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        cursor.close()
        print_success("Combos generados correctamente.")

    except Exception as e:
        print_error(f"Error al generar combos: {e}")

# ... Otras funciones de la base de datos ...

def print_error(message):
    print(f"{Fore.RED}[✕] {message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}[‼] {message}{Style.RESET_ALL}")

def print_process(message):
    print(f"{Fore.BLUE}[ↂ]{message}{Style.RESET_ALL}")
