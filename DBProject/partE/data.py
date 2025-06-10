import customtkinter as ctk
import math
from insert_form import open_insert_form
from update_form import open_update_form
from delete_record import delete_record


def open_table_screen(cursor, table_name,pk_col):
    window = ctk.CTkToplevel()
    window.title(f"{table_name} Table")
    window.geometry("1100x750")
    window.configure(fg_color="#eaf0ff")  # צבע רקע בהיר יותר

    table_name_lower = table_name.lower()  # שינוי שם המשתנה למניעת התנגשות עם שם הפונקציה

    page_size = 100
    current_page = [0]
    data_labels = []

    # משתנה לאחסון שמות העמודות ברמה גבוהה יותר
    column_names = []

    # כותרת הטבלה
    title_label = ctk.CTkLabel(window, text=f"📊 Table: {table_name}",  # אייקון שונה
                               font=("Segoe UI", 28, "bold"), text_color="#2a3f77")
    title_label.pack(pady=(25, 15))

    # כפתור הוספה
    insert_btn = ctk.CTkButton(window, text="➕ Add New Record", width=160, height=40,
                               font=("Segoe UI", 15, "bold"), fg_color="#3cb371", hover_color="#2e8b57",
                               command=lambda: open_insert_form(cursor, table_name, load_page),
                               corner_radius=8)
    insert_btn.pack(pady=(5, 10))

    # ספירת שורות
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name_lower}")
        total_rows = cursor.fetchone()[0]
        total_pages = math.ceil(total_rows / page_size)
        if total_pages == 0 and total_rows == 0:  # Handle empty table case
            total_pages = 1  # At least one page even if empty
    except Exception as e:
        error_label = ctk.CTkLabel(window, text=f"❌ Error fetching row count: {e}",
                                   text_color="#a94442", font=("Segoe UI", 14))
        error_label.pack(pady=20)
        return

    # מסגרת התוכן עבור הטבלה הניתנת לגלילה
    # הגדרת רוחב ספציפי כדי לשלוט בעיצוב הכללי
    table_container_frame = ctk.CTkScrollableFrame(window, fg_color="#f0f4ff",
                                                   width=1000, height=500, corner_radius=10)
    table_container_frame.pack(pady=10, padx=20, fill="x", expand=False)

    # יצירת Canvas פנימי לשליטה טובה יותר על הגלילה והעיצוב של הגריד
    # (Customtkinter's CTkScrollableFrame already handles this well enough usually,
    # but for very precise grid control, a sub-frame can be helpful. Sticking to current structure.)

    # מסגרת ניווט
    nav_frame = ctk.CTkFrame(window, fg_color="#eaf0ff")
    nav_frame.pack(pady=(15, 20))

    # כפתורים ותווית עמוד
    prev_btn = ctk.CTkButton(nav_frame, text="← Previous", width=140, height=40,
                             font=("Segoe UI", 15, "bold"), fg_color="#4a69bd", hover_color="#3a519b",
                             command=lambda: go_page(-1), corner_radius=8)
    prev_btn.grid(row=0, column=0, padx=15)

    page_label = ctk.CTkLabel(nav_frame, text="", font=("Segoe UI", 16, "bold"), text_color="#2a3f77")
    page_label.grid(row=0, column=1, padx=20)

    next_btn = ctk.CTkButton(nav_frame, text="Next →", width=140, height=40,
                             font=("Segoe UI", 15, "bold"), fg_color="#4a69bd", hover_color="#3a519b",
                             command=lambda: go_page(1), corner_radius=8)
    next_btn.grid(row=0, column=2, padx=15)

    def load_page():
        # ניקוי תוויות קיימות
        for label in data_labels:
            label.destroy()
        data_labels.clear()

        offset = current_page[0] * page_size
        try:
            # שלוף נתונים כולל שמות עמודות
            cursor.execute(f"SELECT * FROM {table_name_lower} OFFSET {offset} LIMIT {page_size}")
            rows = cursor.fetchall()
            nonlocal column_names  # נצהיר שזה המשתנה החיצוני
            column_names = [desc[0] for desc in cursor.description]

            # הגדרת רוחב עמודות דינמי
            # ניתן להתאים את זה יותר - כרגע זה רוחב קבוע לכל העמודות
            col_width_factor = 1.0 / len(column_names) if len(column_names) > 0 else 0.1

            # --- כותרות הטבלה (שורת הכותרות) ---
            for col_index, col_name in enumerate(column_names):
                header_label = ctk.CTkLabel(table_container_frame, text=col_name.replace('_', ' ').title(),  # כותרת יפה
                                            font=("Segoe UI", 13, "bold"),
                                            text_color="#1f3b73",
                                            fg_color="#dbe4ff",  # צבע רקע לכותרות
                                            height=35,
                                            corner_radius=5)
                # שימוש ב-grid עם sticky "ew" כדי למתוח את התוויות ברוחב
                table_container_frame.grid_columnconfigure(col_index, weight=1)
                header_label.grid(row=0, column=col_index, sticky="ew", padx=2, pady=2)
                data_labels.append(header_label)

            # --- שורות הנתונים ---
            row_colors = ["#ffffff", "#f5f8ff"]  # צבעים לסירוגין

            if not rows and current_page[0] == 0:  # If table is empty and on first page
                empty_label = ctk.CTkLabel(table_container_frame, text="No data available in this table.",
                                           font=("Segoe UI", 14), text_color="#666666", pady=50)
                empty_label.grid(row=1, column=0, columnspan=len(column_names), sticky="nsew")
                data_labels.append(empty_label)

            # for row_index, row in enumerate(rows, start=1):
            #     bg_color = row_colors[row_index % 2]  # בחירת צבע לסירוגין
            #     for col_index, value in enumerate(row):
            #         # נבטיח שהטקסט לא יהיה None
            #         display_value = str(value) if value is not None else ""
            #
            #         data_label = ctk.CTkLabel(table_container_frame, text=display_value,
            #                                   font=("Segoe UI", 11),
            #                                   text_color="#333333",
            #                                   fg_color=bg_color,  # צבע רקע לשורה
            #                                   height=30,
            #                                   corner_radius=3)
            #         data_label.grid(row=row_index, column=col_index, sticky="ew", padx=2, pady=1)
            #         data_labels.append(data_label)

            for row_index, row in enumerate(rows, start=1):
                bg_color = row_colors[row_index % 2]
                for col_index, value in enumerate(row):
                    display_value = str(value) if value is not None else ""
                    data_label = ctk.CTkLabel(table_container_frame, text=display_value,
                                              font=("Segoe UI", 11),
                                              text_color="#333333",
                                              fg_color=bg_color,
                                              height=30,
                                              corner_radius=3)
                    data_label.grid(row=row_index, column=col_index, sticky="ew", padx=2, pady=1)
                    data_labels.append(data_label)
                # כפתור Edit
                edit_btn = ctk.CTkButton(
                    table_container_frame,
                    text="Edit",
                    width=70,
                    height=30,
                    fg_color="#ffb347",
                    hover_color="#ffa500",
                    font=("Segoe UI", 11, "bold"),
                    command=lambda r=row: open_update_form(cursor, table_name, column_names, r, load_page, pk_col)
                )
                edit_btn.grid(row=row_index, column=len(column_names), padx=4, pady=1)
                data_labels.append(edit_btn)
                # כפתור Delete
                delete_btn = ctk.CTkButton(
                    table_container_frame,
                    text="Delete",
                    width=70,
                    height=30,
                    fg_color="#e57373",
                    hover_color="#c62828",
                    font=("Segoe UI", 11, "bold"),
                    command=lambda r=row: delete_record(cursor, table_name, pk_col, r[column_names.index(pk_col)],
                                                        load_page)
                )
                delete_btn.grid(row=row_index, column=len(column_names) + 1, padx=4, pady=1)
                data_labels.append(delete_btn)

            # for row_index, row in enumerate(rows, start=1):
            #     bg_color = row_colors[row_index % 2]
            #     for col_index, value in enumerate(row):
            #         display_value = str(value) if value is not None else ""
            #         data_label = ctk.CTkLabel(table_container_frame, text=display_value,
            #                                   font=("Segoe UI", 11),
            #                                   text_color="#333333",
            #                                   fg_color=bg_color,  # צבע רקע לשורה
            #                                   height=30,
            #                                   corner_radius=3)
            #         data_label.grid(row=row_index, column=col_index, sticky="ew", padx=2, pady=1)
            #
            #         data_labels.append(data_label)
            #
            #
            #     # כפתור Edit בסוף כל שורה
            #     edit_btn = ctk.CTkButton(
            #         table_container_frame,
            #         text="Edit",
            #         width=70,
            #         height=30,
            #         fg_color="#ffb347",
            #         hover_color="#ffa500",
            #         font=("Segoe UI", 11, "bold"),
            #         # command=lambda r=row: open_update_form(cursor, table_name, column_names, r, load_page)
            #         command = lambda r=row: open_update_form( cursor, table_name, column_names, r, load_page, pk_col)
            #     )
            #     edit_btn.grid(row=row_index, column=len(column_names), padx=4, pady=1)
            #     data_labels.append(edit_btn)

            # עדכון כפתורים ותווית עמוד
            prev_btn.configure(state="normal" if current_page[0] > 0 else "disabled")
            next_btn.configure(state="normal" if current_page[0] < total_pages - 1 else "disabled")
            page_label.configure(text=f"Page {current_page[0] + 1} of {total_pages}")

            # וודא שהגלילה חוזרת לראש העמוד עם טעינת עמוד חדש
            table_container_frame._parent_canvas.yview_moveto(0)

        except Exception as e:
            error_message = f"❌ Error loading data: {e}"
            # אם יש שגיאה אחרי שכבר נכנסנו ללופ, ננקה את הנתונים הקיימים
            for label in data_labels:
                label.destroy()
            data_labels.clear()

            error_label_in_frame = ctk.CTkLabel(table_container_frame, text=error_message,
                                                text_color="#a94442", font=("Segoe UI", 14),
                                                pady=50)
            # אם יש עמודות, נמרכז את הודעת השגיאה על פני כל העמודות
            if column_names:
                error_label_in_frame.grid(row=1, column=0, columnspan=len(column_names), sticky="nsew")
            else:  # אם אין עמודות, פשוט נשים אותה במקום הראשון
                error_label_in_frame.grid(row=1, column=0, sticky="nsew")
            data_labels.append(error_label_in_frame)  # הוסף לרשימה כדי שיימחק בניקוי הבא

            # השבת את כפתורי הניווט במקרה של שגיאה
            prev_btn.configure(state="disabled")
            next_btn.configure(state="disabled")
            page_label.configure(text="Error loading page")

    def go_page(delta):
        new_page = current_page[0] + delta
        if 0 <= new_page < total_pages:
            current_page[0] = new_page
            load_page()
        elif new_page < 0:
            # This case is usually handled by button state, but good for explicit message
            pass
        elif new_page >= total_pages:
            # This case is usually handled by button state, but good for explicit message
            pass

    load_page()  # טעינה ראשונית של העמוד הראשון