#!/usr/bin/env python3
"""
movie_admin.py — Enhanced version with modern Tkinter UI
A Movie Theatre Database Admin GUI for MySQL
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ------------- CONFIG: update these to match your MySQL ----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "4567",
    "database": "movie_theatre"
}
# -----------------------------------------------------------------------

class ModernMovieAdmin(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("🎬 Movie Theatre Database Admin")
        self.parent.geometry("1100x650")
        self.parent.configure(bg="#1E1E1E")

        # Apply a modern ttk theme
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#1E1E1E")
        style.configure("TLabel", background="#1E1E1E", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI Semibold", 10), padding=6)
        style.map("TButton", background=[("active", "#3A86FF")], foreground=[("active", "white")])
        style.configure("TCombobox", padding=5, relief="flat", fieldbackground="#2D2D2D", foreground="white")
        style.configure("Treeview", background="#2D2D2D", fieldbackground="#2D2D2D", foreground="white", rowheight=25)
        style.map("Treeview", background=[("selected", "#3A86FF")])

        # Connect to DB
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            messagebox.showerror("DB connection failed", str(e))
            parent.destroy()
            return

        # Title bar
        title = tk.Label(self, text="🎞️ Movie Theatre Admin Panel", font=("Segoe UI Black", 18),
                         fg="white", bg="#3A86FF", pady=10)
        title.pack(fill="x")

        # Top control frame
        top = ttk.Frame(self)
        top.pack(side="top", fill="x", pady=10, padx=12)

        ttk.Label(top, text="Select Table:").pack(side="left")
        self.table_cb = ttk.Combobox(top, state="readonly", width=30)
        self.table_cb.pack(side="left", padx=6)
        self.table_cb.bind("<<ComboboxSelected>>", self.on_table_selected)

        ttk.Button(top, text="🔄 Refresh Tables", command=self.load_tables).pack(side="left", padx=4)
        ttk.Button(top, text="➕ Add Row", command=self.add_row).pack(side="left", padx=4)
        ttk.Button(top, text="✏️ Edit Row", command=self.edit_row).pack(side="left", padx=4)
        ttk.Button(top, text="🗑️ Delete Row", command=self.delete_row).pack(side="left", padx=4)

        # Treeview for data
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=12, pady=8)

        self.tree = ttk.Treeview(frame, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Status bar
        self.status = ttk.Label(self, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=8, pady=4)

        self.columns = []
        self.current_table = None

        self.load_tables()

    def run_query(self, query, params=None, fetch=False):
        cur = self.conn.cursor()
        cur.execute(query, params or [])
        if fetch:
            rows = cur.fetchall()
            cur.close()
            return rows
        self.conn.commit()
        cur.close()
        return None

    def load_tables(self):
        try:
            rows = self.run_query("SHOW TABLES", fetch=True)
            tables = [r[0] for r in rows]
            self.table_cb["values"] = tables
            if tables:
                self.table_cb.set(tables[0])
                self.on_table_selected()
            self.status.config(text=f"Loaded {len(tables)} tables.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_table_selected(self, event=None):
        tbl = self.table_cb.get()
        if not tbl:
            return
        self.current_table = tbl
        try:
            cols = self.run_query(f"SHOW COLUMNS FROM `{tbl}`", fetch=True)
            self.columns = [c[0] for c in cols]
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = self.columns
            for col in self.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=140, anchor="w")
            self.refresh_rows()
            self.status.config(text=f"Table: {tbl} — {len(self.columns)} columns")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_rows(self):
        try:
            rows = self.run_query(f"SELECT * FROM `{self.current_table}`", fetch=True)
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)
            self.status.config(text=f"Loaded {len(rows)} rows.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_row(self):
        self._row_dialog("Add Row", mode="insert")

    def edit_row(self):
        self._row_dialog("Edit Row", mode="update")

    def delete_row(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select row", "Please select a row to delete.")
            return
        vals = self.tree.item(sel[0], "values")
        pk = self.columns[0]
        pk_val = vals[0]
        if messagebox.askyesno("Confirm Delete", f"Delete row where {pk}={pk_val}?"):
            q = f"DELETE FROM `{self.current_table}` WHERE `{pk}`=%s"
            self.run_query(q, (pk_val,))
            self.refresh_rows()
            messagebox.showinfo("Deleted", "Row deleted successfully.")

    def _row_dialog(self, title, mode):
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.geometry("400x400")
        dlg.configure(bg="#1E1E1E")

        entries = {}
        for i, col in enumerate(self.columns):
            tk.Label(dlg, text=col, fg="white", bg="#1E1E1E", font=("Segoe UI", 10)).pack(pady=4)
            e = ttk.Entry(dlg, width=35)
            e.pack()
            entries[col] = e

        def on_submit():
            vals = [entries[c].get() for c in self.columns]
            if mode == "insert":
                placeholders = ", ".join(["%s"] * len(vals))
                cols = ", ".join([f"`{c}`" for c in self.columns])
                q = f"INSERT INTO `{self.current_table}` ({cols}) VALUES ({placeholders})"
                self.run_query(q, vals)
            else:
                sel = self.tree.selection()
                if not sel:
                    messagebox.showwarning("Select row", "Select a row to update first.")
                    dlg.destroy()
                    return
                pk_col = self.columns[0]
                pk_val = self.tree.item(sel[0], "values")[0]
                set_clause = ", ".join([f"`{c}`=%s" for c in self.columns])
                q = f"UPDATE `{self.current_table}` SET {set_clause} WHERE `{pk_col}`=%s"
                self.run_query(q, vals + [pk_val])
            self.refresh_rows()
            dlg.destroy()
            messagebox.showinfo("Success", "Operation completed successfully.")

        ttk.Button(dlg, text="Save", command=on_submit).pack(pady=12)
        ttk.Button(dlg, text="Cancel", command=dlg.destroy).pack()

def main():
    root = tk.Tk()
    app = ModernMovieAdmin(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
