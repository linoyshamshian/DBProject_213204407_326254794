#connectToPostgres.py
import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",  # כתובת השרת
            port=5432,  # מספר פורט
            database="FinalIntegrated",  # שם מסד הנתונים
            user="chen",  # שם משתמש
            password="2711"  # סיסמה
        )
        return connection
    except Exception as e:
        print("Database connection error:", e)
        return None