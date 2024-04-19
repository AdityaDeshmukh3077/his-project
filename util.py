import psycopg2
import pandas as pd

def check_username_password(username, password):
    try:
        conn = psycopg2.connect(
            dbname="his",
            user="dadb",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM USERS WHERE USERID = %s", (username,))
        row = cur.fetchone()  
        if row:  
            stored_password = row[0]
            if stored_password == password:
                return True
        return False
    except psycopg2.Error as e:
        print("Database error:", e)
        return False
    finally:
        if conn:
            conn.close()
