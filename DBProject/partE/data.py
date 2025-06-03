import customtkinter as ctk
# Make sure psycopg2 is imported where this function is used or passed in
# import psycopg2
from CTkMessagebox import CTkMessagebox # Assuming you have CTkMessagebox installed for error messages

def get_table_columns(cursor, table_name):
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position;
        """,
        (table_name.lower(),)
    )
    return [row[0] for row in cursor.fetchall()]

def get_primary_key_column(cursor, table_name):
    """
    Retrieves the primary key column name for a given table.
    Needed for consistent ordering across pages.
    """
    try:
        cursor.execute(
            """
            SELECT a.attname
            FROM pg_index ix
                     JOIN pg_attribute a ON a.attrelid = ix.indrelid
                AND a.attnum = ANY (ix.indkey)
            WHERE ix.indrelid = %s::regclass
            AND    ix.indisprimary;
            """,
            (table_name.lower(),)
        )
        pk_col = cursor.fetchone()
        return pk_col[0] if pk_col else None
    except Exception as e:
        print(f"Error fetching primary key for {table_name}: {e}")
        return None


def open_table_screen(cursor, table_name, conn): # conn is not directly used in this version but good to keep if needed later
    columns = get_table_columns(cursor, table_name)
    pk_col = get_primary_key_column(cursor, table_name) # Get primary key for consistent ordering

    screen = ctk.CTkToplevel()
    screen.title(f"{table_name.capitalize()} Data")
    screen.geometry("1100x700") # Increased size to accommodate pagination
    screen.configure(fg_color="#f5f9ff")

    title = ctk.CTkLabel(screen, text=f"Table: {table_name.capitalize()}",
                         font=("Segoe UI", 24, "bold"), text_color="#2a3f77")
    title.pack(pady=20)

    # --- Pagination Variables ---
    rows_per_page = 100  # Display 100 rows per page
    current_page = 0     # Start from the first page (index 0)
    total_rows = 0       # Will be populated after initial fetch

    data_frame = ctk.CTkScrollableFrame(screen, fg_color="#ffffff", width=1050, height=500)
    data_frame.pack(padx=20, pady=10, fill="both", expand=True)

    table_data_labels = [] # To store references to row labels for easy clearing

    # --- Pagination Controls ---
    pagination_frame = ctk.CTkFrame(screen, fg_color="#f5f9ff")
    pagination_frame.pack(pady=10)

    prev_button = ctk.CTkButton(pagination_frame, text="< Previous", command=lambda: change_page(-1),
                                font=("Segoe UI", 14), fg_color="#2a3f77", hover_color="#3a4f87", text_color="white",
                                width=100, height=35)
    prev_button.pack(side="left", padx=10)

    page_info_label = ctk.CTkLabel(pagination_frame, text="Page 1 of 1", font=("Segoe UI", 14, "bold"),
                                   text_color="#2a3f77")
    page_info_label.pack(side="left", padx=10)

    next_button = ctk.CTkButton(pagination_frame, text="Next >", command=lambda: change_page(1),
                                font=("Segoe UI", 14), fg_color="#2a3f77", hover_color="#3a4f87", text_color="white",
                                width=100, height=35)
    next_button.pack(side="left", padx=10)


    def update_pagination_buttons():
        """Updates the state of pagination buttons and page info label."""
        prev_button.configure(state="normal" if current_page > 0 else "disabled")
        max_pages = (total_rows + rows_per_page - 1) // rows_per_page # Ceiling division
        next_button.configure(state="normal" if current_page < max_pages - 1 else "disabled")
        page_info_label.configure(text=f"Page {current_page + 1} of {max_pages if max_pages > 0 else 1}")


    def refresh_table_data():
        """Refreshes the data displayed in the table for the current page."""
        nonlocal total_rows # Allows modification of total_rows in the outer scope

        # Clear existing data labels
        for row_labels in table_data_labels:
            for label in row_labels:
                label.destroy()
        table_data_labels.clear()

        # Add column headers
        for idx, col_name in enumerate(columns):
            ctk.CTkLabel(
                data_frame,
                text=col_name,
                width=150,
                anchor="center",
                font=("Segoe UI", 14, "bold"),
                fg_color="#dbe4ff",
                text_color="#2a3f77",
                padx=5, pady=8
            ).grid(row=0, column=idx, padx=2, pady=2, sticky="ew")

        # --- Count total rows for pagination ---
        cursor.execute(f"SELECT COUNT(*) FROM {table_name.lower()}")
        total_rows = cursor.fetchone()[0]

        # --- Fetch data for the current page ---
        offset = current_page * rows_per_page
        order_clause = f"ORDER BY {pk_col}" if pk_col else ""

        # Fallback if no PK is found, order by first column, or no order if no columns
        if not pk_col:
            if columns:
                order_clause = f"ORDER BY {columns[0]}"
            else:
                order_clause = ""

        # Execute query with LIMIT and OFFSET
        cursor.execute(f"SELECT * FROM {table_name.lower()} {order_clause} LIMIT %s OFFSET %s",
                       (rows_per_page, offset))
        rows = cursor.fetchall()

        for r_idx, row in enumerate(rows, start=1):
            row_labels = []
            for c_idx, value in enumerate(row):
                label = ctk.CTkLabel(
                    data_frame,
                    text=str(value),
                    width=150,
                    anchor="center",
                    font=("Segoe UI", 12),
                    fg_color="#ffffff",
                    text_color="black",
                    padx=5, pady=4
                )
                label.grid(row=r_idx, column=c_idx, padx=2, pady=1, sticky="ew")
                row_labels.append(label)
            table_data_labels.append(row_labels)

        # Scroll to the top of the frame when page changes
        data_frame.after(100, lambda: data_frame._parent_canvas.yview_moveto(0.0))
        update_pagination_buttons()


    def change_page(direction):
        """Changes the current page and refreshes the table data."""
        nonlocal current_page
        max_pages = (total_rows + rows_per_page - 1) // rows_per_page

        new_page = current_page + direction
        if 0 <= new_page < max_pages:
            current_page = new_page
            refresh_table_data()
        elif new_page < 0: # If trying to go before first page
            CTkMessagebox(title="Navigation", message="You are already on the first page.", icon="info")
        elif new_page >= max_pages: # If trying to go beyond last page
            CTkMessagebox(title="Navigation", message="You are already on the last page.", icon="info")


    # Initial display of data
    refresh_table_data()

    screen.mainloop()