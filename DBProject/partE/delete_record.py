# import customtkinter as ctk
# from tkinter import messagebox
#
# # פונקציה שמוחקת רשומה באופן רקורסיבי, כולל את כל הרשומות שתלויות בה בטבלאות אחרות (ביחסי foreign key)
# def delete_record(cursor, table_name, pk_col, pk_val, refresh_callback, visited=None, deleted_log=None):
#     # visited - כדי לעקוב אחרי רשומות שכבר ביקרנו בהן (למניעת לולאות)
#     if visited is None:
#         visited = set()
#     if deleted_log is None:
#         deleted_log = []
#
#     key = (table_name.lower(), pk_col.lower(), pk_val)
#     if key in visited:
#         return # אם כבר טיפלנו ברשומה הזו - לא ממשיכים
#     visited.add(key)
#     try:
#         # שלב 1: מצא את כל ה-foreign keys שמצביעים על הטבלה והעמודה הזו
#         cursor.execute("""
#             -- שליפה של כל הטבלאות והעמודות שמפנות (באמצעות foreign key) לטבלה ולעמודה מסוימת
#         SELECT
#             tc.table_name AS child_table,      -- שם הטבלה שמכילה את ה-foreign key (הטבלה התלויה)
#             kcu.column_name AS child_column,   -- שם העמודה בטבלה הזו שמכילה את ה-foreign key
#             tc.constraint_name                -- שם ה-constraint (הקשר)
#         FROM
#             information_schema.table_constraints AS tc
#             -- חיבור ל-key_column_usage כדי לדעת באיזו עמודה בטבלה נמצא ה-foreign key
#             JOIN information_schema.key_column_usage AS kcu
#               ON tc.constraint_name = kcu.constraint_name
#             -- חיבור ל-referential_constraints כדי לדעת לאיזה primary key ה-foreign key מפנה
#             JOIN information_schema.referential_constraints AS rc
#               ON rc.constraint_name = tc.constraint_name
#             -- חיבור ל-constraint_column_usage כדי לדעת על איזו טבלה ועמודה יושב ה-primary key (הטבלה שלך)
#             JOIN information_schema.constraint_column_usage AS ccu
#               ON ccu.constraint_name = rc.unique_constraint_name
#         WHERE
#             tc.constraint_type = 'FOREIGN KEY'   -- מסנן רק קשרי מפתח זר (foreign key)
#             AND ccu.table_name = %s              -- הטבלה שלך (parent table)
#             AND ccu.column_name = %s             -- העמודה שלך (primary key בעמודה הזו)
#         """, (table_name.lower(), pk_col.lower()))
#         dependencies = cursor.fetchall()
#
#         # שלב 2: עבור כל טבלת child, מחק child rows רקורסיבית
#         for child_table, child_column, constraint_name in dependencies:
#             child_pk_col = get_primary_key(cursor, child_table) # מציאת המפתח הראשי של הטבלה
#             cursor.execute(
#                 # מאתר את כל הרשומות ב-child_table שמקושרות לרשומה הנוכחית דרך ה-foreign key
#                 f"SELECT {child_pk_col} FROM {child_table} WHERE {child_column} = %s", (pk_val,)
#             )
#             child_rows = cursor.fetchall()
#             # קריאה רקורסיבית למחיקת כל שורת child
#             for (child_pk_val,) in child_rows:
#                 delete_record(cursor, child_table, child_pk_col, child_pk_val, refresh_callback, visited, deleted_log)
#
#         # שלב 4: מחיקת הרשומה הראשית עצמה מהטבלה המקורית
#         cursor.execute(
#             f"DELETE FROM {table_name.lower()} WHERE {pk_col} = %s", (pk_val,)
#         )
#         deleted_log.append(f"Deleted from {table_name} where {pk_col}={pk_val}")
#
#         # ביצוע commit לכל השינויים שבוצעו במסד הנתונים
#         cursor.connection.commit()
#
#         # הצגת סיכום רק בקריאה הראשית (ולא בקריאות הרקורסיביות)
#         if len(visited) == 1:
#             print(deleted_log)
#             summary = "The following deletions were performed:\n\n" + "\n".join(deleted_log)
#             messagebox.showinfo("Deletion Summary", summary)
#             refresh_callback()
#
#     except Exception as e:
#         # במקרה של שגיאה - rollback ומוצגת הודעת שגיאה למשתמש
#         cursor.connection.rollback()
#         messagebox.showerror("Error", f"Failed to delete record:\n{e}")
#
# # פונקציה שמחזירה את שם עמודת המפתח הראשי בטבלה מסוימת
# def get_primary_key(cursor, table_name):
#     cursor.execute("""
#         SELECT a.attname
#         FROM   pg_index i
#         JOIN   pg_attribute a ON a.attrelid = i.indrelid
#                              AND a.attnum = ANY(i.indkey)
#         WHERE  i.indrelid = %s::regclass
#         AND    i.indisprimary;
#     """, (table_name.lower(),))
#     row = cursor.fetchone()
#     if row:
#         return row[0] # מחזיר את שם עמודת המפתח הראשי
#     raise Exception(f"Primary key not found for table {table_name}")


from tkinter import messagebox

# פונקציה שמוחקת רשומה באופן רקורסיבי, כולל את כל הרשומות שתלויות בה בטבלאות אחרות (ביחסי foreign key)
def delete_record(cursor, table_name, pk_col, pk_val, refresh_callback, visited=None, deleted_log=None, level=0):
    # visited - כדי לעקוב אחרי רשומות שכבר ביקרנו בהן (למניעת לולאות)
    if visited is None:
        visited = set()
    if deleted_log is None:
        deleted_log = []

    key = (table_name.lower(), pk_col.lower(), pk_val)
    if key in visited:
        return # אם כבר טיפלנו ברשומה הזו - לא ממשיכים
    visited.add(key)
    try:
        # שלב 1: מצא את כל ה-foreign keys שמצביעים על הטבלה והעמודה הזו
        cursor.execute("""
            -- שליפה של כל הטבלאות והעמודות שמפנות (באמצעות foreign key) לטבלה ולעמודה מסוימת
        SELECT
            tc.table_name AS child_table,      -- שם הטבלה שמכילה את ה-foreign key (הטבלה התלויה)
            kcu.column_name AS child_column,   -- שם העמודה בטבלה הזו שמכילה את ה-foreign key
            tc.constraint_name                -- שם ה-constraint (הקשר)
        FROM
            information_schema.table_constraints AS tc
            -- חיבור ל-key_column_usage כדי לדעת באיזו עמודה בטבלה נמצא ה-foreign key
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            -- חיבור ל-referential_constraints כדי לדעת לאיזה primary key ה-foreign key מפנה
            JOIN information_schema.referential_constraints AS rc
              ON rc.constraint_name = tc.constraint_name
            -- חיבור ל-constraint_column_usage כדי לדעת על איזו טבלה ועמודה יושב ה-primary key (הטבלה שלך)
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = rc.unique_constraint_name
        WHERE
            tc.constraint_type = 'FOREIGN KEY'   -- מסנן רק קשרי מפתח זר (foreign key)
            AND ccu.table_name = %s              -- הטבלה שלך (parent table)
            AND ccu.column_name = %s             -- העמודה שלך (primary key בעמודה הזו)
        """, (table_name.lower(), pk_col.lower()))
        dependencies = cursor.fetchall()

        # שלב 2: עבור כל טבלת child, מחק child rows רקורסיבית
        for child_table, child_column, constraint_name in dependencies:
            child_pk_col = get_primary_key(cursor, child_table) # מציאת המפתח הראשי של הטבלה
            cursor.execute(
                # מאתר את כל הרשומות ב-child_table שמקושרות לרשומה הנוכחית דרך ה-foreign key
                f"SELECT {child_pk_col} FROM {child_table} WHERE {child_column} = %s", (pk_val,)
            )
            child_rows = cursor.fetchall()
            # קריאה רקורסיבית למחיקת כל שורת child
            for (child_pk_val,) in child_rows:
                delete_record(cursor, child_table, child_pk_col, child_pk_val, refresh_callback, visited, deleted_log, level + 1)

        # שלב 4: מחיקת הרשומה הראשית עצמה מהטבלה המקורית
        indent = "    " * level  # הזחה לפי עומק הקריאה
        deleted_log.append(f"{indent}Deleted from {table_name} where {pk_col}={pk_val}")

        # ביצוע commit לכל השינויים שבוצעו במסד הנתונים
        cursor.execute(
            f"DELETE FROM {table_name.lower()} WHERE {pk_col} = %s", (pk_val,)
        )
        cursor.connection.commit()

        # הצגת סיכום רק בקריאה הראשית (ולא בקריאות הרקורסיביות)
        if level == 0:
            summary = "The following deletions were performed:\n\n" + "\n".join(deleted_log)
            messagebox.showinfo("Deletion Summary", summary)
            refresh_callback()

    except Exception as e:
        # במקרה של שגיאה - rollback ומוצגת הודעת שגיאה למשתמש
        cursor.connection.rollback()
        messagebox.showerror("Error", f"Failed to delete record:\n{e}")

# פונקציה שמחזירה את שם עמודת המפתח הראשי בטבלה מסוימת
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
        return row[0] # מחזיר את שם עמודת המפתח הראשי
    raise Exception(f"Primary key not found for table {table_name}")


