# insert_form.py
import customtkinter as ctk
from tkinter import messagebox
from insert_person_form import open_person_insert_form
import psycopg2


def open_insert_form(cursor, table_name, refresh_callback):
    # בדיקה אם זו טבלת Person
    if table_name.lower() == "person":
        open_person_insert_form(cursor, refresh_callback)
        return
    """
    פותח טופס הוספת רשומה חדשה לטבלה
    """
    form_window = ctk.CTkToplevel()
    form_window.title(f"Add New Record - {table_name}")
    form_window.geometry("500x600")
    form_window.configure(fg_color="#eaf0ff")

    # מנע מהחלון להיסגר בטעות
    form_window.grab_set()

    try:
        # קבל מידע על עמודות הטבלה כולל מפתחות ראשיים
        cursor.execute(f"""
            SELECT 
                c.column_name, 
                c.data_type, 
                c.is_nullable, 
                c.column_default,
                CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END as is_primary_key
            FROM information_schema.columns c
            LEFT JOIN (
                SELECT ku.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage ku
                ON tc.constraint_name = ku.constraint_name
                WHERE tc.table_name = '{table_name.lower()}'
                AND tc.constraint_type = 'PRIMARY KEY'
            ) pk ON c.column_name = pk.column_name
            WHERE c.table_name = '{table_name.lower()}'
            ORDER BY c.ordinal_position
        """)
        columns_info = cursor.fetchall()

        if not columns_info:
            messagebox.showerror("Error", f"Could not retrieve column information for table {table_name}")
            form_window.destroy()
            return

    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching table structure: {e}")
        form_window.destroy()
        return

    # כותרת
    title_label = ctk.CTkLabel(form_window,
                               text=f"➕ Add New {table_name} Record",
                               font=("Segoe UI", 22, "bold"),
                               text_color="#2a3f77")
    title_label.pack(pady=(20, 30))

    # מסגרת לטופס עם גלילה
    form_frame = ctk.CTkScrollableFrame(form_window,
                                        fg_color="#f0f4ff",
                                        width=450,
                                        height=400,
                                        corner_radius=10)
    form_frame.pack(pady=10, padx=25, fill="both", expand=True)

    # מילון לאחסון השדות
    entry_widgets = {}

    # יצירת שדות הטופס
    for i, (col_name, data_type, is_nullable, col_default, is_primary_key) in enumerate(columns_info):
        # בדיקה אם זה מפתח ראשי עם AUTO INCREMENT
        is_auto_increment = col_default and (
                    'nextval' in str(col_default) or 'auto_increment' in str(col_default).lower())

        # אם זה מפתח ראשי עם AUTO INCREMENT, דלג עליו
        if is_primary_key and is_auto_increment:
            continue

        # אם זה מפתח ראשי ללא AUTO INCREMENT, הוסף הערה
        pk_note = ""
        if is_primary_key and not is_auto_increment:
            pk_note = " (Primary Key)"

        # תווית שדה
        is_required = (is_nullable == 'NO' and not col_default) or (is_primary_key and not is_auto_increment)
        required_mark = " *" if is_required else ""

        field_label = ctk.CTkLabel(form_frame,
                                   text=f"{col_name.replace('_', ' ').title()}{pk_note}{required_mark}:",
                                   font=("Segoe UI", 14, "bold"),
                                   anchor="w",
                                   text_color="#2a3f77" if not is_primary_key else "#d9534f")
        field_label.grid(row=i * 2, column=0, sticky="w", padx=10, pady=(15, 5))

        # יצירת שדה קלט מתאים לסוג הנתון
        if 'text' in data_type.lower() or 'varchar' in data_type.lower() or 'char' in data_type.lower():
            # שדה טקסט רגיל או אזור טקסט
            if 'text' in data_type.lower():
                entry_widget = ctk.CTkTextbox(form_frame,
                                              height=80,
                                              font=("Segoe UI", 12),
                                              corner_radius=8)
            else:
                entry_widget = ctk.CTkEntry(form_frame,
                                            font=("Segoe UI", 12),
                                            height=35,
                                            corner_radius=8)

        elif 'int' in data_type.lower() or 'numeric' in data_type.lower() or 'decimal' in data_type.lower():
            # שדה מספרי
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8,
                                        placeholder_text="Enter number...")

        elif 'date' in data_type.lower():
            # שדה תאריך
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8,
                                        placeholder_text="YYYY-MM-DD")

        elif 'time' in data_type.lower():
            # שדה זמן
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8,
                                        placeholder_text="HH:MM:SS")

        elif 'bool' in data_type.lower():
            # תיבת סימון
            entry_widget = ctk.CTkCheckBox(form_frame,
                                           text="Yes/True",
                                           font=("Segoe UI", 12))

        else:
            # ברירת מחדל - שדה טקסט רגיל
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8)

        entry_widget.grid(row=i * 2 + 1, column=0, sticky="ew", padx=10, pady=(0, 10))
        form_frame.grid_columnconfigure(0, weight=1)

        # שמור את הווידג'ט עם מידע נוסף
        entry_widgets[col_name] = {
            'widget': entry_widget,
            'data_type': data_type,
            'is_nullable': is_nullable,
            'has_default': bool(col_default),
            'is_primary_key': is_primary_key,
            'is_auto_increment': is_auto_increment
        }

    # הוראות למשתמש
    instructions_label = ctk.CTkLabel(form_frame,
                                      text="* Required fields\n🔑 Primary Key fields (manual entry required)\nLeave empty for default values where applicable",
                                      font=("Segoe UI", 11),
                                      text_color="#666666",
                                      justify="left")
    instructions_label.grid(row=len(columns_info) * 2, column=0, sticky="w", padx=10, pady=(20, 10))

    # מסגרת כפתורים
    button_frame = ctk.CTkFrame(form_window, fg_color="#eaf0ff")
    button_frame.pack(pady=20)

    def submit_form():
        """שליחת הטופס והוספת הרשומה"""
        try:
            # איסוף נתונים מהטופס
            values = {}
            columns = []
            placeholders = []
            insert_values = []

            for col_name, field_info in entry_widgets.items():
                widget = field_info['widget']
                data_type = field_info['data_type']
                is_nullable = field_info['is_nullable']
                has_default = field_info['has_default']
                is_primary_key = field_info['is_primary_key']
                is_auto_increment = field_info['is_auto_increment']

                # קבל ערך מהשדה
                if isinstance(widget, ctk.CTkTextbox):
                    value = widget.get("1.0", "end-1c").strip()
                elif isinstance(widget, ctk.CTkCheckBox):
                    value = widget.get()
                else:
                    value = widget.get().strip()

                # בדיקת תקינות - מפתח ראשי ללא AUTO INCREMENT הוא חובה
                if not value and (
                        (is_nullable == 'NO' and not has_default) or (is_primary_key and not is_auto_increment)):
                    field_display_name = col_name.replace('_', ' ').title()
                    if is_primary_key:
                        messagebox.showerror("Validation Error",
                                             f"Primary Key field '{field_display_name}' is required!")
                    else:
                        messagebox.showerror("Validation Error",
                                             f"Field '{field_display_name}' is required!")
                    return

                # אם יש ערך, הוסף לשאילתה
                if value or (isinstance(widget, ctk.CTkCheckBox) and not value):
                    columns.append(col_name)
                    placeholders.append("%s")

                    # המר ערכים לפי סוג הנתון
                    if isinstance(widget, ctk.CTkCheckBox):
                        insert_values.append(bool(value))
                    elif 'int' in data_type.lower():
                        try:
                            insert_values.append(int(value) if value else None)
                        except ValueError:
                            messagebox.showerror("Validation Error",
                                                 f"'{col_name}' must be a valid integer!")
                            return
                    elif 'numeric' in data_type.lower() or 'decimal' in data_type.lower():
                        try:
                            insert_values.append(float(value) if value else None)
                        except ValueError:
                            messagebox.showerror("Validation Error",
                                                 f"'{col_name}' must be a valid number!")
                            return
                    else:
                        insert_values.append(value if value else None)

            if not columns:
                messagebox.showwarning("Warning", "Please fill at least one field!")
                return

            # בניית שאילתת INSERT
            columns_str = ", ".join(columns)
            placeholders_str = ", ".join(placeholders)
            query = f"INSERT INTO {table_name.lower()} ({columns_str}) VALUES ({placeholders_str})"

            # ביצוע השאילתה
            cursor.execute(query, insert_values)
            cursor.connection.commit()

            messagebox.showinfo("Success", f"New {table_name} record added successfully!")

            # רענן את הטבלה וסגור את הטופס
            refresh_callback()
            form_window.destroy()

        except psycopg2.Error as e:
            cursor.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to insert record:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def cancel_form():
        """ביטול הטופס"""
        form_window.destroy()

    # כפתורי שליחה וביטול
    submit_btn = ctk.CTkButton(button_frame,
                               text="✅ Add Record",
                               command=submit_form,
                               font=("Segoe UI", 14, "bold"),
                               fg_color="#3cb371",
                               hover_color="#2e8b57",
                               width=140,
                               height=40,
                               corner_radius=8)
    submit_btn.grid(row=0, column=0, padx=10)

    cancel_btn = ctk.CTkButton(button_frame,
                               text="❌ Cancel",
                               command=cancel_form,
                               font=("Segoe UI", 14, "bold"),
                               fg_color="#dc3545",
                               hover_color="#c82333",
                               width=140,
                               height=40,
                               corner_radius=8)
    cancel_btn.grid(row=0, column=1, padx=10)

    # מרכז את החלון
    form_window.transient(form_window.master)
    form_window.focus()