# api.py

import random
import sqlite3
import requests
from colorama import Fore, Style
import time

MAX_RETRIES = 2
REQUEST_TIMEOUT = 3

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

def get_usernames(proxy):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            response = requests.get(USER_API_URL, proxies={'http': proxy, 'https': proxy}, timeout=REQUEST_TIMEOUT)
            usernames = random.sample(response.json(), 100)
            insert_usernames(conn, usernames)
            return usernames
    except Exception as e:
        return []

def get_passwords(proxy):
    try:
        retries = 0
        while retries < MAX_RETRIES:
            try:
                with sqlite3.connect(DATABASE_PATH) as conn:
                    response = requests.get(PASS_API_URL, proxies={'http': proxy, 'https': proxy}, timeout=REQUEST_TIMEOUT)
                    passwords = random.sample(response.json(), 100)
                    insert_passwords(conn, passwords)
                    return passwords
            except Exception as e:
                retries += 1
        return []
    except KeyboardInterrupt:
        time.sleep(2)
        print(f"{Fore.YELLOW}Ctrl+C presionado. Cancelando la ejecución...{Style.RESET_ALL}")

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
