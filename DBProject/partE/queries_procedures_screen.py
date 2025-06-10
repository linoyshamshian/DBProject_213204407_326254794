import customtkinter as ctk
from tkinter import messagebox, simpledialog


def open_queries_procedures_screen(cursor):
    window = ctk.CTkToplevel()
    window.title("Queries & Procedures")
    window.geometry("1100x750")
    window.configure(fg_color="#eaf0ff")
    window.grab_set()

    result_textbox = None
    data_labels = []

    title = ctk.CTkLabel(window,
                         text="📊 Queries & Procedures Management",
                         font=("Segoe UI", 28, "bold"),
                         text_color="#2a3f77")
    title.pack(pady=(25, 15))

    btn_frame = ctk.CTkFrame(window, fg_color="#eaf0ff")
    btn_frame.pack(pady=10)

    results_scroll_frame = ctk.CTkScrollableFrame(window, fg_color="#f0f4ff",
                                                  width=1000, height=400, corner_radius=10)
    results_scroll_frame.pack(pady=10, padx=20, fill="x", expand=False)

    def clear_results_display():
        nonlocal result_textbox, data_labels
        for widget in results_scroll_frame.winfo_children():
            widget.destroy()
        data_labels.clear()
        result_textbox = None

    def update_results_display(content, is_query_results=False, column_names=None):
        nonlocal result_textbox, data_labels

        clear_results_display()

        if is_query_results and column_names:
            for col_index, col_name in enumerate(column_names):
                header_label = ctk.CTkLabel(results_scroll_frame, text=col_name.replace('_', ' ').title(),
                                            font=("Segoe UI", 13, "bold"),
                                            text_color="#1f3b73",
                                            fg_color="#dbe4ff",
                                            height=35,
                                            corner_radius=5)
                results_scroll_frame.grid_columnconfigure(col_index, weight=1)
                header_label.grid(row=0, column=col_index, sticky="ew", padx=2, pady=2)
                data_labels.append(header_label)

            row_colors = ["#ffffff", "#f5f8ff"]

            if not content:
                empty_label = ctk.CTkLabel(results_scroll_frame, text="No data available for this query.",
                                           font=("Segoe UI", 14), text_color="#666666", pady=50)
                empty_label.grid(row=1, column=0, columnspan=len(column_names) if column_names else 1, sticky="nsew")
                data_labels.append(empty_label)
            else:
                for row_idx, row_data in enumerate(content):
                    bg_color = row_colors[row_idx % 2]
                    for col_idx, value in enumerate(row_data):
                        display_value = str(value) if value is not None else ""
                        data_label = ctk.CTkLabel(results_scroll_frame, text=display_value,
                                                  font=("Segoe UI", 11),
                                                  text_color="#333333",
                                                  fg_color=bg_color,
                                                  height=30,
                                                  corner_radius=3)
                        results_scroll_frame.grid_columnconfigure(col_idx, weight=1)
                        data_label.grid(row=row_idx + 1, column=col_idx, sticky="ew", padx=2, pady=1)
                        data_labels.append(data_label)

        else:
            result_textbox = ctk.CTkTextbox(results_scroll_frame, wrap="word", width=980, height=380)
            result_textbox.pack(expand=True, fill="both", padx=5, pady=5)
            result_textbox.insert("1.0", content)
            result_textbox.configure(state="disabled")

    def run_query_internal(cursor, query):
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            update_results_display(results, is_query_results=True, column_names=column_names)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))
            update_results_display(f"Error running query:\n{e}")

    def run_procedure_internal(cursor, procedure):
        try:
            cursor.execute(procedure)
            cursor.connection.commit()
            update_results_display("Procedure executed successfully.")
        except Exception as e:
            messagebox.showerror("Procedure Error", str(e))
            update_results_display(f"Error running procedure:\n{e}")

    def call_calculate_avg_experience_with_input(cursor_obj):
        airline_id_str = show_custom_input_dialog("Enter Airline ID:")
        if airline_id_str is not None:
            try:
                airline_id = float(airline_id_str)
                calculate_avg_experience_logic(cursor_obj, airline_id)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for Airline ID.")
        else:
            update_results_display("Operation cancelled by user.")

    def calculate_avg_experience_logic(cursor, airlineid):
        try:
            cursor.execute("SELECT calculate_avg_experience_and_update_service(%s)", (airlineid,))
            result = cursor.fetchone()

            if result and result[0] is not None:
                avg_exp = result[0]
                messagebox.showinfo("Success", f"Average experience for Airline ID {airlineid} is {avg_exp} years.\nServices updated.")
                update_results_display(f"Function result: Average experience for Airline ID {airlineid} is {avg_exp} years. Services updated.")
            else:
                messagebox.showwarning("No Data", f"No pilots found for airline ID {airlineid}.")
                update_results_display(f"Function result: No pilots found for airline ID {airlineid}.")

        except Exception as e:
            cursor.connection.rollback()
            messagebox.showerror("Error", str(e))
            update_results_display(f"Error running function:\n{e}")

    # הגדרת סגנונות כפתורים
    BUTTON_WIDTH = 600 # רוחב אחיד לכל הכפתורים
    BUTTON_HEIGHT = 45 # גובה אחיד לכל הכפתורים
    BUTTON_FONT = ("Segoe UI", 16, "bold") # גופן אחיד

    # הגדרת צבעים שונים לסוגי פעולות
    QUERY_COLORS = {"fg_color": "#A8B5E0", "hover_color": "#B4CBF0"}
    PROCEDURE_COLORS = {"fg_color": "#A8B5E0", "hover_color": "#B4CBF0"}
    FUNCTION_COLORS = {"fg_color": "#A8B5E0", "hover_color": "#B4CBF0"}

    # כפתורים עם פעולות לדוגמה
    buttons_info = [
        ("Query 1 - Security Personnel in Flights (after 2024-03-21)",
         lambda: run_query_internal(cursor, """SELECT
    f.flightid,
    f.flightdestination,
    f.flightsource,
    f.departure,
    f.landing,
    p.fullname AS securitypersonname
FROM
    flight f
JOIN personinflight pif ON f.flightid = pif.flightid
JOIN securityperson sp ON pif.personid = sp.personid
JOIN person p ON sp.personid = p.personid
WHERE
    f.departure > '2024-03-21';"""),
         "query", # סוג הפעולה
         "Displays flight details and the full name of security personnel assigned to flights departing after March 21, 2024."
        ),
        ("Query 2 - Incidents by Security Person in High-Incident Areas",
         lambda: run_query_internal(cursor, """SELECT
    P.FullName AS SecurityPersonName,
    A.AreaName,
    COUNT(I.IncidentID) AS NumberOfIncidents
FROM
    Person P
JOIN SecurityPerson SP ON P.PersonID = SP.PersonID
JOIN Assigment ASG ON SP.PersonID = ASG.PersonID
JOIN Area A ON ASG.AreaID = A.AreaID
JOIN Incident I ON A.AreaID = I.AreaID
WHERE
    A.AreaID IN (
        SELECT AreaID
        FROM Incident
        GROUP BY AreaID
        HAVING COUNT(IncidentID) > 3
    )
GROUP BY
    P.FullName, A.AreaName
ORDER BY
    NumberOfIncidents DESC;"""),
         "query",
         "Shows security personnel assigned to areas with more than 3 incidents, counting incidents per person and area."
        ),
        ("Procedure - Add Flight Attendant",
         lambda: open_add_flightattendant_form(cursor),
         "procedure",
         "Opens a form to add a new Flight Attendant record, including personal and flight attendant specific details, and their associated language."
        ),
        ("Function - Calculate Avg Experience",
         lambda: call_calculate_avg_experience_with_input(cursor),
         "function",
         "Calculates the average experience in years for pilots belonging to a specified Airline ID and updates their service records."
        )
    ]

    for i, (text, cmd, action_type, description) in enumerate(buttons_info):
        btn_colors = {}
        if action_type == "query":
            btn_colors = QUERY_COLORS
        elif action_type == "procedure":
            btn_colors = PROCEDURE_COLORS
        elif action_type == "function":
            btn_colors = FUNCTION_COLORS

        btn = ctk.CTkButton(btn_frame,
                            text=text,
                            command=cmd,
                            width=BUTTON_WIDTH, # שימוש ברוחב אחיד
                            height=BUTTON_HEIGHT, # שימוש בגובה אחיד
                            font=BUTTON_FONT, # שימוש בגופן אחיד
                            fg_color=btn_colors["fg_color"], # צבע קדמה
                            hover_color=btn_colors["hover_color"], # צבע בריחוף
                            corner_radius=8)
        btn.pack(pady=8)

    # יצירת טקסט ההסבר
    explanation_text = "Select an operation to perform:\n\n"
    for text, _, action_type, description in buttons_info:
        explanation_text += f"• {text}: {description}\n\n"

    # הצגת טקסט ההסבר באזור התוצאות
    update_results_display(explanation_text)

    return window


# --- פונקציה חדשה ליצירת חלון קלט מותאם אישית (כמו simpledialog אבל מעוצב) ---
def show_custom_input_dialog(prompt_text, title="Input Required"):
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.geometry("350x200")
    dialog.configure(fg_color="#eaf0ff")
    dialog.grab_set()

    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width // 2) - (dialog.winfo_width() // 2)
    y = (screen_height // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")


    result_value = None

    def on_ok():
        nonlocal result_value
        result_value = entry.get()
        dialog.destroy()

    def on_cancel():
        nonlocal result_value
        result_value = None
        dialog.destroy()

    label = ctk.CTkLabel(dialog, text=prompt_text, font=("Segoe UI", 16, "bold"), text_color="#2a3f77")
    label.pack(pady=20, padx=20)

    entry = ctk.CTkEntry(dialog, width=250, height=40, corner_radius=10,
                         fg_color="#ffffff", text_color="#333333",
                         border_color="#a8b9e0", border_width=1,
                         font=("Segoe UI", 14))
    entry.pack(pady=(0, 20), padx=20)
    entry.focus_set()

    button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    button_frame.pack(pady=(0, 15))

    ok_button = ctk.CTkButton(button_frame, text="OK", command=on_ok,
                              width=100, height=35, font=("Segoe UI", 14, "bold"),
                              fg_color="#4CAF50", hover_color="#45a049", corner_radius=8)
    ok_button.grid(row=0, column=0, padx=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=on_cancel,
                                  width=100, height=35, font=("Segoe UI", 14, "bold"),
                                  fg_color="#e57373", hover_color="#c62828", corner_radius=8)
    cancel_button.grid(row=0, column=1, padx=10)

    dialog.wait_window()
    return result_value


def open_add_flightattendant_form(cursor):
    form_window = ctk.CTkToplevel()
    form_window.title("Add Flight Attendant")
    form_window.geometry("500x550")
    form_window.grab_set()
    form_window.configure(fg_color="#eaf0ff")

    title_label = ctk.CTkLabel(form_window, text="✈️ Add New Flight Attendant",
                               font=("Segoe UI", 24, "bold"), text_color="#2a3f77")
    title_label.pack(pady=(25, 15))

    input_frame = ctk.CTkFrame(form_window, fg_color="transparent")
    input_frame.pack(pady=(0, 20), padx=20, fill="x", expand=False)

    input_frame.grid_columnconfigure(0, weight=2)
    input_frame.grid_columnconfigure(1, weight=3)

    fields_data = [
        ("Person ID", "p_personid", ctk.CTkEntry),
        ("Full Name", "p_fullname", ctk.CTkEntry),
        ("Mail", "p_mail", ctk.CTkEntry),
        (" Employment Date (YYYY-MM-DD)", "p_employmentdate", ctk.CTkEntry),
        ("Airline ID", "p_airlineid", ctk.CTkEntry),
        ("Rank", "p_rank", ctk.CTkEntry),
        ("Language", "p_language", ctk.CTkEntry),
    ]

    entries = {}

    for i, (label_text, var_name, entry_widget) in enumerate(fields_data):
        label = ctk.CTkLabel(input_frame, text=label_text + ":", font=("Segoe UI", 13), text_color="#333333")
        label.grid(row=i, column=0, sticky="w", padx=10, pady=8)

        entry = entry_widget(input_frame, width=250, height=35, corner_radius=8,
                             fg_color="#ffffff", text_color="#333333",
                             border_color="#a8b9e0", border_width=1)
        entry.grid(row=i, column=1, sticky="ew", padx=(0, 10), pady=8)
        entries[var_name] = entry

    def submit_data():
        try:
            p_personid = int(entries["p_personid"].get())
            p_fullname = entries["p_fullname"].get()
            p_mail = entries["p_mail"].get()
            p_employmentdate = entries["p_employmentdate"].get()
            p_airlineid = float(entries["p_airlineid"].get())
            p_rank = entries["p_rank"].get()
            p_language = entries["p_language"].get()

            cursor.execute("""
                CALL add_flightattendant_with_language(%s, %s, %s, %s, %s, %s, %s)
            """, (p_personid, p_fullname, p_mail, p_employmentdate, p_airlineid, p_rank, p_language))
            cursor.connection.commit()

            messagebox.showinfo("Success", f"Flight Attendant '{p_fullname}' added successfully.")
            form_window.destroy()

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure Person ID and Airline ID are valid numbers and Date is in YYYY-MM-DD format.")
        except Exception as e:
            cursor.connection.rollback()
            messagebox.showerror("Database Error", str(e))

    submit_btn = ctk.CTkButton(form_window, text="✅ Submit", command=submit_data,
                               width=180, height=45,
                               font=("Segoe UI", 16, "bold"),
                               fg_color="#4CAF50", hover_color="#45a049",
                               corner_radius=10)
    submit_btn.pack(pady=20)