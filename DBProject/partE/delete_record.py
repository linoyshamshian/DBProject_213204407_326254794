import customtkinter as ctk
from tkinter import messagebox

def delete_record(cursor, table_name, pk_col, pk_val, refresh_callback, visited=None, deleted_log=None):
    if visited is None:
        visited = set()
    if deleted_log is None:
        deleted_log = []

    key = (table_name.lower(), pk_col.lower(), pk_val)
    if key in visited:
        return
    visited.add(key)
    try:
        # שלב 1: מצא את כל ה-foreign keys שמצביעים על הטבלה והעמודה הזו
        cursor.execute("""
            SELECT
                tc.table_name AS child_table,
                kcu.column_name AS child_column,
                tc.constraint_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.referential_constraints AS rc
                  ON rc.constraint_name = tc.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = rc.unique_constraint_name
            WHERE
                tc.constraint_type = 'FOREIGN KEY'
                AND ccu.table_name = %s
                AND ccu.column_name = %s
        """, (table_name.lower(), pk_col.lower()))
        dependencies = cursor.fetchall()

        # שלב 2: עבור כל טבלת child, מחק child rows רקורסיבית
        for child_table, child_column, constraint_name in dependencies:
            child_pk_col = get_primary_key(cursor, child_table)
            cursor.execute(
                f"SELECT {child_pk_col} FROM {child_table} WHERE {child_column} = %s", (pk_val,)
            )
            child_rows = cursor.fetchall()
            for (child_pk_val,) in child_rows:
                delete_record(cursor, child_table, child_pk_col, child_pk_val, refresh_callback, visited, deleted_log)

        # שלב 3: מחק את כל הרשומות הישירות בטבלאות child (למקרה שאין primary key)
        for child_table, child_column, constraint_name in dependencies:
            cursor.execute(
                f"DELETE FROM {child_table} WHERE {child_column} = %s", (pk_val,)
            )
            deleted_log.append(f"Deleted from {child_table} where {child_column}={pk_val}")

        # שלב 4: מחק את הרשומה הראשית
        cursor.execute(
            f"DELETE FROM {table_name.lower()} WHERE {pk_col} = %s", (pk_val,)
        )
        deleted_log.append(f"Deleted from {table_name} where {pk_col}={pk_val}")

        cursor.connection.commit()

        # רק בקריאה הראשית (לא ברקורסיה) מציגים את הסיכום
        if len(visited) == 1:
            summary = "The following deletions were performed:\n\n" + "\n".join(deleted_log)
            messagebox.showinfo("Deletion Summary", summary)
            refresh_callback()

    except Exception as e:
        cursor.connection.rollback()
        messagebox.showerror("Error", f"Failed to delete record:\n{e}")

def get_primary_key(cursor, table_name):
    cursor.execute("""
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = %s::regclass
        AND    i.indisprimary;
    """, (table_name.lower(),))
    row = cursor.fetchone()
    if row:
        return row[0]
    raise Exception(f"Primary key not found for table {table_name}")

