import customtkinter as ctk
from tkinter import messagebox, simpledialog


def open_queries_procedures_screen(cursor):
    window = ctk.CTkToplevel()
    window.title("Queries & Procedures")
    window.geometry("1100x750")
    window.configure(fg_color="#eaf0ff")
    window.grab_set()

    # הגדרת משתנים גלובליים לתוך הסקופ של הפונקציה
    result_textbox = None
    data_labels = [] # List to keep track of result labels for dynamic clearing

    # עיצוב הכותרת
    title = ctk.CTkLabel(window,
                         text="📊 Queries & Procedures Management",
                         font=("Segoe UI", 28, "bold"),
                         text_color="#2a3f77")
    title.pack(pady=(25, 15))

    # מסגרת לכפתורים
    btn_frame = ctk.CTkFrame(window, fg_color="#eaf0ff")
    btn_frame.pack(pady=10)

    # מסגרת גלילה לתוצאות - מוגדרת כאן כדי שנוכל לארוז אותה מראש
    results_scroll_frame = ctk.CTkScrollableFrame(window, fg_color="#f0f4ff",
                                                  width=1000, height=400, corner_radius=10)
    results_scroll_frame.pack(pady=10, padx=20, fill="x", expand=False)

    # פונקציה כללית לניקוי אזור התצוגה
    def clear_results_display():
        nonlocal result_textbox, data_labels
        for widget in results_scroll_frame.winfo_children():
            widget.destroy()
        data_labels.clear()
        result_textbox = None

    # פונקציה לעדכון התוצאות באזור התצוגה המאוחד
    def update_results_display(content, is_query_results=False, column_names=None):
        nonlocal result_textbox, data_labels

        clear_results_display()

        if is_query_results and column_names:
            # --- כותרות הטבלה ---
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

            # --- שורות הנתונים ---
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

    def run_function_internal(cursor, function):
        try:
            cursor.execute(function)
            result = cursor.fetchone()
            display_result = result[0] if result and len(result) > 0 else "No result"
            update_results_display(f"Function result: {display_result}")
        except Exception as e:
            messagebox.showerror("Function Error", str(e))
            update_results_display(f"Error running function:\n{e}")

    # כפתורים עם פעולות לדוגמה
    buttons = [
        ("Query 1 - Security Personnel in Flights (after 2024-03-21)", lambda: run_query_internal(cursor, """SELECT
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
    f.departure > '2024-03-21';""")), # <--- כאן השאילתה החדשה
        ("Query 2 - Incidents by Security Person in High-Incident Areas", lambda: run_query_internal(cursor, """SELECT
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
    NumberOfIncidents DESC;""")),
        ("Procedure - Add Flight Attendant", lambda: open_add_flightattendant_form(cursor)),
        ("Function - Calculate Avg Experience", lambda: calculate_avg_experience(cursor))
    ]

    for i, (text, cmd) in enumerate(buttons):
        btn = ctk.CTkButton(btn_frame,
                            text=text,
                            command=cmd,
                            width=300,
                            height=40,
                            fg_color="#c9d2ff",
                            hover_color="#abbcff",
                            corner_radius=8)
        btn.pack(pady=8)

    update_results_display("Click a button to run a query, procedure, or function.")

    return window

def open_add_flightattendant_form(cursor):
    form_window = ctk.CTkToplevel()
    form_window.title("Add Flight Attendant")
    form_window.geometry("500x600")
    form_window.grab_set()
    form_window.configure(fg_color="#f2f5ff")

    fields = {
        "Person ID": ctk.CTkEntry(form_window),
        "Airline ID": ctk.CTkEntry(form_window),
        "Rank": ctk.CTkEntry(form_window),
        "Language": ctk.CTkEntry(form_window),
        "Mail": ctk.CTkEntry(form_window),
        "Employment Date (YYYY-MM-DD)": ctk.CTkEntry(form_window),
        "Full Name": ctk.CTkEntry(form_window),
    }

    # יצירת הטופס
    for label_text, entry in fields.items():
        label = ctk.CTkLabel(form_window, text=label_text, font=("Segoe UI", 14))
        label.pack(pady=(12, 2))
        entry.pack(pady=(0, 8), ipadx=10, ipady=5)



    def submit_data():
        try:
            # שליפת ערכים
            p_personid = int(fields["Person ID"].get())
            p_airlineid = float(fields["Airline ID"].get())
            p_rank = fields["Rank"].get()
            p_language = fields["Language"].get()
            p_mail = fields["Mail"].get()
            p_employmentdate = fields["Employment Date (YYYY-MM-DD)"].get()
            p_fullname = fields["Full Name"].get()

            # קריאה לפרוצדורה
            cursor.execute("""
                CALL add_flightattendant_with_language(%s, %s, %s, %s, %s, %s, %s)
            """, (p_personid, p_airlineid, p_rank, p_language, p_mail, p_employmentdate, p_fullname))
            cursor.connection.commit()

            messagebox.showinfo("Success", f"Flight Attendant '{p_fullname}' added with language '{p_language}'.")
            form_window.destroy()

        except Exception as e:
            cursor.connection.rollback()
            messagebox.showerror("Error", str(e))

    submit_btn = ctk.CTkButton(form_window, text="Submit", command=submit_data,
                               fg_color="#87a7ff", hover_color="#6f94ff", corner_radius=10, height=40)
    submit_btn.pack(pady=20)



def calculate_avg_experience(cursor):
    try:
        airlineid = simpledialog.askfloat("Input", "Enter Airline ID:")
        if airlineid is None:
            return  # אם המשתמש סגר את החלונית או לחץ Cancel

        cursor.execute("SELECT calculate_avg_experience_and_update_service(%s)", (airlineid,))
        result = cursor.fetchone()

        if result and result[0] is not None:
            avg_exp = result[0]
            messagebox.showinfo("Success", f"Average experience is {avg_exp} years.\nServices updated.")
        else:
            messagebox.showwarning("No Data", f"No pilots found for airline ID {airlineid}.")

    except Exception as e:
        cursor.connection.rollback()
        messagebox.showerror("Error", str(e))
