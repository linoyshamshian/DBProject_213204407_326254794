# insert_person_form.py
import customtkinter as ctk
from tkinter import messagebox
import psycopg2


def open_person_insert_form(cursor, refresh_callback):
    """
    פותח טופס הוספת רשומה חדשה לטבלת Person עם בחירת תפקיד
    """
    form_window = ctk.CTkToplevel()
    form_window.title("Add New Person")
    form_window.geometry("600x750")
    form_window.configure(fg_color="#eaf0ff")

    # מנע מהחלון להיסגר בטעות
    form_window.grab_set()

    try:
        # קבל מידע על עמודות טבלת Person
        cursor.execute("""
                       SELECT c.column_name,
                              c.data_type,
                              c.is_nullable,
                              c.column_default,
                              CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END as is_primary_key
                       FROM information_schema.columns c
                                LEFT JOIN (SELECT ku.column_name
                                           FROM information_schema.table_constraints tc
                                                    JOIN information_schema.key_column_usage ku
                                                         ON tc.constraint_name = ku.constraint_name
                                           WHERE tc.table_name = 'person'
                                             AND tc.constraint_type = 'PRIMARY KEY') pk
                                          ON c.column_name = pk.column_name
                       WHERE c.table_name = 'person'
                       ORDER BY c.ordinal_position
                       """)
        person_columns_info = cursor.fetchall()

        if not person_columns_info:
            messagebox.showerror("Error", "Could not retrieve Person table structure")
            form_window.destroy()
            return

    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching table structure: {e}")
        form_window.destroy()
        return

    # כותרת
    title_label = ctk.CTkLabel(form_window,
                               text="👤 Add New Person",
                               font=("Segoe UI", 22, "bold"),
                               text_color="#2a3f77")
    title_label.pack(pady=(20, 30))

    # מסגרת לטופס עם גלילה
    form_frame = ctk.CTkScrollableFrame(form_window,
                                        fg_color="#f0f4ff",
                                        width=550,
                                        height=500,
                                        corner_radius=10)
    form_frame.pack(pady=10, padx=25, fill="both", expand=True)

    # מילון לאחסון השדות של Person
    person_entry_widgets = {}
    current_row = 0

    # יצירת שדות הטופס עבור Person
    for col_name, data_type, is_nullable, col_default, is_primary_key in person_columns_info:
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
        field_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=(15, 5))

        # יצירת שדה קלט מתאים לסוג הנתון
        if 'text' in data_type.lower() or 'varchar' in data_type.lower() or 'char' in data_type.lower():
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8)
        elif 'int' in data_type.lower() or 'numeric' in data_type.lower() or 'decimal' in data_type.lower():
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8,
                                        placeholder_text="Enter number...")
        elif 'date' in data_type.lower():
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8,
                                        placeholder_text="YYYY-MM-DD")
        elif 'bool' in data_type.lower():
            entry_widget = ctk.CTkCheckBox(form_frame,
                                           text="Yes/True",
                                           font=("Segoe UI", 12))
        else:
            entry_widget = ctk.CTkEntry(form_frame,
                                        font=("Segoe UI", 12),
                                        height=35,
                                        corner_radius=8)

        entry_widget.grid(row=current_row + 1, column=0, sticky="ew", padx=10, pady=(0, 10))
        form_frame.grid_columnconfigure(0, weight=1)

        # שמור את הווידג'ט עם מידע נוסף
        person_entry_widgets[col_name] = {
            'widget': entry_widget,
            'data_type': data_type,
            'is_nullable': is_nullable,
            'has_default': bool(col_default),
            'is_primary_key': is_primary_key,
            'is_auto_increment': is_auto_increment
        }

        current_row += 2

    # קו הפרדה
    separator = ctk.CTkFrame(form_frame, height=2, fg_color="#c9d2ff")
    separator.grid(row=current_row, column=0, sticky="ew", padx=10, pady=20)
    current_row += 1

    # בחירת תפקיד
    role_label = ctk.CTkLabel(form_frame,
                              text="👔 Select Person Role:",
                              font=("Segoe UI", 16, "bold"),
                              text_color="#2a3f77")
    role_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=(10, 15))
    current_row += 1

    # משתנה לאחסון הבחירה
    role_var = ctk.StringVar(value="passenger")

    # RadioButtons לבחירת תפקיד
    roles = [
        ("passenger", "🧳 Passenger"),
        ("flightattendant", "✈️ Flight Attendant"),
        ("pilot", "👨‍✈️ Pilot"),
        ("securityperson", "🛡️ Security Person")
    ]

    role_frame = ctk.CTkFrame(form_frame, fg_color="#e8f0ff", corner_radius=8)
    role_frame.grid(row=current_row, column=0, sticky="ew", padx=10, pady=10)
    current_row += 1

    for i, (role_value, role_text) in enumerate(roles):
        radio_btn = ctk.CTkRadioButton(role_frame,
                                       text=role_text,
                                       variable=role_var,
                                       value=role_value,
                                       font=("Segoe UI", 12),
                                       command=lambda: update_role_fields())
        radio_btn.grid(row=i // 2, column=i % 2, sticky="w", padx=15, pady=8)

    role_frame.grid_columnconfigure(0, weight=1)
    role_frame.grid_columnconfigure(1, weight=1)

    # מסגרת לשדות נוספים לפי תפקיד
    role_fields_frame = ctk.CTkFrame(form_frame, fg_color="#f8faff", corner_radius=8)
    role_fields_frame.grid(row=current_row, column=0, sticky="ew", padx=10, pady=15)
    current_row += 1

    # מילון לשדות נוספים
    role_entry_widgets = {}

    def clear_role_fields():
        """ניקוי שדות תפקיד קיימים"""
        for widget in role_fields_frame.winfo_children():
            widget.destroy()
        role_entry_widgets.clear()

    def create_role_field(field_name, field_label, field_type="text", placeholder="", row_num=0):
        """יצירת שדה עבור תפקיד ספציפי"""
        label = ctk.CTkLabel(role_fields_frame,
                             text=f"{field_label}:",
                             font=("Segoe UI", 13, "bold"),
                             text_color="#2a3f77")
        label.grid(row=row_num, column=0, sticky="w", padx=10, pady=(10, 5))

        if field_type == "number":
            entry = ctk.CTkEntry(role_fields_frame,
                                 font=("Segoe UI", 12),
                                 height=35,
                                 placeholder_text=placeholder or "Enter number...")
        else:
            entry = ctk.CTkEntry(role_fields_frame,
                                 font=("Segoe UI", 12),
                                 height=35,
                                 placeholder_text=placeholder)

        entry.grid(row=row_num + 1, column=0, sticky="ew", padx=10, pady=(0, 10))
        role_fields_frame.grid_columnconfigure(0, weight=1)

        role_entry_widgets[field_name] = {
            'widget': entry,
            'field_type': field_type
        }

    def update_role_fields():
        """עדכון שדות לפי התפקיד הנבחר"""
        clear_role_fields()
        selected_role = role_var.get()

        if selected_role == "securityperson":
            role_title = ctk.CTkLabel(role_fields_frame,
                                      text="🛡️ Security Person Details:",
                                      font=("Segoe UI", 14, "bold"),
                                      text_color="#d9534f")
            role_title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            create_role_field("securitylevel", "Security Level *", "text", "e.g., Level 1, Level 2", 1)
            create_role_field("contactinfo", "Contact Info *", "text", "Phone/Email", 3)

        elif selected_role == "pilot":
            role_title = ctk.CTkLabel(role_fields_frame,
                                      text="👨‍✈️ Pilot Details:",
                                      font=("Segoe UI", 14, "bold"),
                                      text_color="#3cb371")
            role_title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            create_role_field("licensenumber", "License Number *", "text", "e.g., PIL123456", 1)
            create_role_field("experienceyears", "Experience Years *", "number", "Years of experience", 3)
            create_role_field("airlineid", "Airline ID *", "number", "Airline identifier", 5)

        elif selected_role == "flightattendant":
            role_title = ctk.CTkLabel(role_fields_frame,
                                      text="✈️ Flight Attendant Details:",
                                      font=("Segoe UI", 14, "bold"),
                                      text_color="#4a69bd")
            role_title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            create_role_field("rank", "Rank *", "text", "e.g., Senior, Junior", 1)
            create_role_field("airlineid", "Airline ID *", "number", "Airline identifier", 3)

        elif selected_role == "passenger":
            role_title = ctk.CTkLabel(role_fields_frame,
                                      text="🧳 Passenger - No additional details required",
                                      font=("Segoe UI", 14, "bold"),
                                      text_color="#6c757d")
            role_title.grid(row=0, column=0, sticky="w", padx=10, pady=20)

    # טעינה ראשונית של שדות התפקיד
    update_role_fields()

    # הוראות למשתמש
    instructions_label = ctk.CTkLabel(form_frame,
                                      text="* Required fields\n🔑 Choose a role and fill the corresponding details\nAll information will be saved to appropriate tables",
                                      font=("Segoe UI", 11),
                                      text_color="#666666",
                                      justify="left")
    instructions_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=(20, 10))

    # מסגרת כפתורים
    button_frame = ctk.CTkFrame(form_window, fg_color="#eaf0ff")
    button_frame.pack(pady=20)



    def submit_form():
        try:
            # איסוף נתונים מהטופס של Person
            person_values = {}
            person_columns = []
            person_placeholders = []
            person_insert_values = []

            for col_name, field_info in person_entry_widgets.items():
                widget = field_info['widget']
                data_type = field_info['data_type']
                is_nullable = field_info['is_nullable']
                has_default = field_info['has_default']
                is_primary_key = field_info['is_primary_key']
                is_auto_increment = field_info['is_auto_increment']

                if isinstance(widget, ctk.CTkCheckBox):
                    value = widget.get()
                else:
                    value = widget.get().strip() if widget.get() else ""

                if not value and (
                        (is_nullable == 'NO' and not has_default) or (is_primary_key and not is_auto_increment)):
                    field_display_name = col_name.replace('_', ' ').title()
                    messagebox.showerror("Validation Error", f"Field '{field_display_name}' is required!")
                    return

                if value or (isinstance(widget, ctk.CTkCheckBox) and not value):
                    person_columns.append(col_name)
                    person_placeholders.append("%s")
                    if isinstance(widget, ctk.CTkCheckBox):
                        person_insert_values.append(bool(value))
                    elif 'int' in data_type.lower():
                        try:
                            person_insert_values.append(int(value) if value else None)
                        except ValueError:
                            messagebox.showerror("Validation Error", f"'{col_name}' must be a valid integer!")
                            return
                    elif 'numeric' in data_type.lower() or 'decimal' in data_type.lower():
                        try:
                            person_insert_values.append(float(value) if value else None)
                        except ValueError:
                            messagebox.showerror("Validation Error", f"'{col_name}' must be a valid number!")
                            return
                    else:
                        person_insert_values.append(value if value else None)

            if not person_columns:
                messagebox.showwarning("Warning", "Please fill at least one field!")
                return

            # בדיקת שדות תפקיד
            selected_role = role_var.get()
            role_data = {}

            if selected_role in ["securityperson", "pilot", "flightattendant"]:
                for field_name, field_info in role_entry_widgets.items():
                    widget = field_info['widget']
                    value = widget.get().strip() if widget.get() else ""

                    if not value:
                        messagebox.showerror("Validation Error",
                                             f"Field '{field_name.replace('_', ' ').title()}' is required for {selected_role}!")
                        return

                    if field_info['field_type'] == "number":
                        try:
                            role_data[field_name] = int(value)
                        except ValueError:
                            messagebox.showerror("Validation Error", f"'{field_name}' must be a valid number!")
                            return
                    else:
                        role_data[field_name] = value

            # טרנזקציה
            cursor.execute("BEGIN")

            try:
                # הכנס לטבלת Person
                person_columns_str = ", ".join(person_columns)
                person_placeholders_str = ", ".join(person_placeholders)
                person_query = f"INSERT INTO person ({person_columns_str}) VALUES ({person_placeholders_str}) RETURNING personid"
                cursor.execute(person_query, person_insert_values)
                personid = cursor.fetchone()[0]  # <-- כאן אתה מקבל את ה-id שנוצר[2][5][7]

                # הכנס לטבלת התפקיד המתאימה
                if selected_role == "securityperson":
                    cursor.execute(
                        "INSERT INTO securityperson (personid, securitylevel, contactinfo) VALUES (%s, %s, %s)",
                        (personid, role_data['securitylevel'], role_data['contactinfo']))
                elif selected_role == "pilot":
                    cursor.execute(
                        "INSERT INTO pilot (personid, licensenumber, experienceyears, airlineid) VALUES (%s, %s, %s, %s)",
                        (personid, role_data['licensenumber'], role_data['experienceyears'], role_data['airlineid']))
                elif selected_role == "flightattendant":
                    cursor.execute(
                        "INSERT INTO flightattendant (personid, rank, airlineid) VALUES (%s, %s, %s)",
                        (personid, role_data['rank'], role_data['airlineid']))
                elif selected_role == "passenger":
                    cursor.execute(
                        "INSERT INTO passenger (personid) VALUES (%s)", (personid,))

                cursor.execute("COMMIT")
                messagebox.showinfo("Success", f"New {selected_role} added successfully with ID: {personid}")
                refresh_callback()
                form_window.destroy()
            except Exception as e:
                cursor.execute("ROLLBACK")
                raise e

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def cancel_form():
        """ביטול הטופס"""
        form_window.destroy()

    # כפתורי שליחה וביטול
    submit_btn = ctk.CTkButton(button_frame,
                               text="✅ Add Person",
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