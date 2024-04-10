# proxies.py

import sys
import os
import random
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from colorama import Fore, Style
import requests
import time

MAX_RETRIES = 2
REQUEST_TIMEOUT_CHECK_PROXY = 5

def check_proxy(proxy, conn):
    try:
        response = requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=REQUEST_TIMEOUT_CHECK_PROXY)
        if response.status_code == 200:
            insert_proxy(conn=conn, proxy=proxy)
            return proxy
    except Exception as e:
        pass

def working_proxies(conn, MAX_WORKERS):
    try:
        print(f"{Fore.CYAN}Searching and Checking proxies...{Style.RESET_ALL}")
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            proxies = list(tqdm(executor.map(lambda proxy: check_proxy(proxy, conn), get_proxies()), total=len(get_proxies()), desc="Searching and Checking proxies", unit=" proxies"))

        working_proxies_list = [proxy for proxy in proxies if proxy is not None]
        print_success(f'Encontrados {len(working_proxies_list)} proxies funcionando.')

        if not working_proxies_list:
            print_warning("CANCELADA LA VERIFICACIÓN DE CUENTAS POR FALTA DE PROXIES")
            sys.exit(0)

        return working_proxies_list
    except Exception as e:
        print_error(f"An error occurred in 'working_proxies': {e}")
        return []

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
