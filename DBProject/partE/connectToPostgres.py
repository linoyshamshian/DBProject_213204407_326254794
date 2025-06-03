import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",  # כתובת השרת
            port=5432,  # מספר פורט
            database="Integrated",  # שם מסד הנתונים
            user="linoy",  # שם משתמש
            password="0566"  # סיסמה
        )
        return connection
    except Exception as e:
        print("Database connection error:", e)
        return None
