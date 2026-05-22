import mysql.connector
from mysql.connector import Error

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def verify(username: str, password: str) -> bool:
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
    except Error:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = %s",
            (username,),
        )
        row = cursor.fetchone()
        return row is not None and row[0] == password
    except Error:
        return False
    finally:
        conn.close()
