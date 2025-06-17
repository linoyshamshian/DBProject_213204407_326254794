import customtkinter as ctk
import math
from insert_form import open_insert_form
from update_form import open_update_form
from delete_record import delete_record

# פונקציה לפתיחת מסך טבלה עבור טבלת SQL מסוימת
def open_table_screen(cursor, table_name,pk_col):
    # יצירת חלון חדש
    window = ctk.CTkToplevel()
    window.title(f"{table_name} Table")
    window.geometry("1100x750")
    window.configure(fg_color="#eaf0ff")

    table_name_lower = table_name.lower()  # לוודא ששמות הטבלאות תואמים למסד הנתונים

    page_size = 50 # מספר שורות לעמוד
    current_page = [0] # עוקב אחרי העמוד הנוכחי
    data_labels = []  # רשימת תוויות שמוצגות (כדי לנקות בעת מעבר עמוד)

    # משתנה לאחסון שמות העמודות
    column_names = []

    # כותרת הטבלה
    title_label = ctk.CTkLabel(window, text=f"📊 Table: {table_name}",  # אייקון שונה
                               font=("Segoe UI", 28, "bold"), text_color="#2a3f77")
    title_label.pack(pady=(25, 15))

    # כפתור הוספה
    insert_btn = ctk.CTkButton(window, text="➕ Add New Record", width=160, height=40,
                               font=("Segoe UI", 15, "bold"), fg_color="#000080", hover_color="#272757",
                               command=lambda: open_insert_form(cursor, table_name, load_page),
                               corner_radius=8)
    insert_btn.pack(pady=(5, 10))

    # ספירת סך השורות בטבלה כדי לחשב כמה עמודים יש
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name_lower}") #שאילתת SQL לספירת כל השורות בטבלה
        total_rows = cursor.fetchone()[0] #מביא את הנתונים ולא את האוביקט
        total_pages = math.ceil(total_rows / page_size)
        if total_pages == 0 and total_rows == 0:
            total_pages = 1  # מוודא שתמיד יהיה לפחות עמוד 1
    except Exception as e:
        error_label = ctk.CTkLabel(window, text=f"❌ Error fetching row count: {e}",
                                   text_color="#a94442", font=("Segoe UI", 14))
        error_label.pack(pady=20)
        return

    # יצירת מסגרת לגלילה – תכיל את הטבלה
    table_container_frame = ctk.CTkScrollableFrame(window, fg_color="#f0f4ff",
                                                   width=1000, height=500, corner_radius=10)
    table_container_frame.pack(pady=10, padx=20, fill="x", expand=False)

    # מסגרת לניווט בין עמודים
    nav_frame = ctk.CTkFrame(window, fg_color="#eaf0ff")
    nav_frame.pack(pady=(15, 20))

    # כפתור עמוד קודם
    prev_btn = ctk.CTkButton(nav_frame, text="← Previous", width=140, height=40,
                             font=("Segoe UI", 15, "bold"), fg_color="#4a69bd", hover_color="#3a519b",
                             command=lambda: go_page(-1), corner_radius=8)
    prev_btn.grid(row=0, column=0, padx=15)

    # תווית מציינת את מספר העמוד
    page_label = ctk.CTkLabel(nav_frame, text="", font=("Segoe UI", 16, "bold"), text_color="#2a3f77")
    page_label.grid(row=0, column=1, padx=20)

    # כפתור עמוד הבא
    next_btn = ctk.CTkButton(nav_frame, text="Next →", width=140, height=40,
                             font=("Segoe UI", 15, "bold"), fg_color="#4a69bd", hover_color="#3a519b",
                             command=lambda: go_page(1), corner_radius=8)
    next_btn.grid(row=0, column=2, padx=15)

    # טוען את הנתונים של העמוד הנוכחי מהטבלה
    def load_page():
        # נקה תוויות ישנות מהטבלה
        for label in data_labels:
            label.destroy()
        data_labels.clear()

        # חישוב מאיפה להתחיל לשלוף נתונים עבור הדף הנוכחי של הטבלה
        offset = current_page[0] * page_size

        try:
            # שליפת שורות כולל שמות עמודות
            cursor.execute(f"SELECT * FROM {table_name_lower} "
                           f"ORDER BY {pk_col} OFFSET {offset} LIMIT {page_size}")

            #החזרת כל השורות שנשלפו מהשאילתה כמערך (list) של טאפלים (tuples)
            rows = cursor.fetchall()
            # שימוש במשתנה החיצוני
            nonlocal column_names
            #השורה הזאת בונה רשימה של שמות העמודות שהשאילתה החזירה
            column_names = [desc[0] for desc in cursor.description]

            # הגדרת רוחב עמודות דינמי
            col_width_factor = 1.0 / len(column_names) if len(column_names) > 0 else 0.1

            # שורת כותרות הטבלה
            for col_index, col_name in enumerate(column_names):
                header_label = ctk.CTkLabel(table_container_frame, text=col_name.replace('_', ' ').title(),
                                            font=("Segoe UI", 13, "bold"),
                                            text_color="#1f3b73",
                                            fg_color="#dbe4ff",
                                            height=35,
                                            corner_radius=5)
                table_container_frame.grid_columnconfigure(col_index, weight=1)
                header_label.grid(row=0, column=col_index, sticky="ew", padx=2, pady=2)
                data_labels.append(header_label)

            # שורות עם הנתונים בפועל
            row_colors = ["#ffffff", "#f5f8ff"]  # צבעים לסירוגין

            # אם אין שורות (הטבלה ריקה) ואנחנו בעמוד הראשון בלבד, מציגים הודעה מתאימה למשתמש
            if not rows and current_page[0] == 0:
                empty_label = ctk.CTkLabel(table_container_frame, text="No data available in this table.",
                                           font=("Segoe UI", 14), text_color="#666666", pady=50)
                empty_label.grid(row=1, column=0, columnspan=len(column_names), sticky="nsew")
                data_labels.append(empty_label)


            for row_index, row in enumerate(rows, start=1):
                # הגדרת צבע רקע לסירוגין לשורות הטבלה (לשפר קריאות)
                bg_color = row_colors[row_index % 2]
                # לולאה על כל עמודה בשורה הנוכחית להצגת הערך המתאים
                for col_index, value in enumerate(row):
                    display_value = str(value) if value is not None else ""
                    # יצירת תווית להצגת הערך בטבלה עם עיצוב מתאים
                    data_label = ctk.CTkLabel(table_container_frame, text=display_value,
                                              font=("Segoe UI", 11),
                                              text_color="#333333",
                                              fg_color=bg_color,
                                              height=30,
                                              corner_radius=3)
                    data_label.grid(row=row_index, column=col_index, sticky="ew", padx=2, pady=1)
                    data_labels.append(data_label)
                # יצירת כפתור 'עריכה' לכל שורה עם קריאה לפונקציה לפתיחת טופס עריכה
                edit_btn = ctk.CTkButton(
                    table_container_frame,
                    text="Edit",
                    width=70,
                    height=30,
                    fg_color="#678DC6",
                    hover_color="#3E577D",
                    font=("Segoe UI", 11, "bold"),
                    command=lambda r=row: open_update_form(cursor, table_name, column_names, r, load_page, pk_col)
                )
                edit_btn.grid(row=row_index, column=len(column_names), padx=4, pady=1)
                data_labels.append(edit_btn)

                # כפתור מחיקה לכל שורה
                delete_btn = ctk.CTkButton(
                    table_container_frame,
                    text="Delete",
                    width=70,
                    height=30,
                    fg_color="#898989",
                    hover_color="#353839",
                    font=("Segoe UI", 11, "bold"),
                    command=lambda r=row: delete_record(cursor, table_name, pk_col, r[column_names.index(pk_col)],
                                                        load_page)
                )
                delete_btn.grid(row=row_index, column=len(column_names) + 1, padx=4, pady=1)
                data_labels.append(delete_btn)

            # עדכון מצב כפתורי ניווט ותווית עמוד
            prev_btn.configure(state="normal" if current_page[0] > 0 else "disabled")
            next_btn.configure(state="normal" if current_page[0] < total_pages - 1 else "disabled")
            page_label.configure(text=f"Page {current_page[0] + 1} of {total_pages}")

            # חזרה לראש הגלילה
            table_container_frame._parent_canvas.yview_moveto(0)

        except Exception as e:
            # טיפול בשגיאה בזמן טעינת נתונים
            error_message = f"❌ Error loading data: {e}"
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

            # השבתת כפתורי ניווט
            prev_btn.configure(state="disabled")
            next_btn.configure(state="disabled")
            page_label.configure(text="Error loading page")

    # מעבר בין עמודים
    def go_page(delta):
        new_page = current_page[0] + delta
        if 0 <= new_page < total_pages:
            current_page[0] = new_page
            load_page()
        elif new_page < 0:
            pass
        elif new_page >= total_pages:
            pass

    load_page()  # טעינה ראשונית של העמוד הראשון