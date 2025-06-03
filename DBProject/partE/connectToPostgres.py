import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",        # כתובת השרת
        port=5432,               # מספר פורט
        database="Integrated",   # שם מסד הנתונים
        user="linoy",            # שם משתמש
        password="0566"          # סיסמה
    )
    print("Connected to PostgreSQL!")

    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Database version: {db_version[0]}")

except Exception as error:
    print("Error while connecting to PostgreSQL:", error)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
