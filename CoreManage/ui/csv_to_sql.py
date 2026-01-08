# ui/csv_to_sql.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import ttkbootstrap as tb
from services.reclasificaciones_service import insertar_balance_service

class CsvToSqlApp(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Cargar Layout Balance")
        self.geometry("900x500")

        # Botón para seleccionar CSV
        tb.Button(self, text="Seleccionar CSV Balance", bootstyle="primary", command=self.load_csv).pack(pady=10)

        # Botón para insertar en SQL
        tb.Button(self, text="Insertar en SQL Server", bootstyle="success", command=self.insert_to_sql).pack(pady=5)

        self.tree = None
        self.df = None  # Guardaremos el DataFrame cargado

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            initialdir=r"C:\EDSA",  # Carpeta inicial
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            self.df = pd.read_csv(filepath)
            self.display_data(self.df)
            messagebox.showinfo("Éxito", f"Archivo cargado: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def display_data(self, df):
        if self.tree:
            self.tree.destroy()

        columns = list(df.columns)
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def insert_to_sql(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Atención", "Primero carga un CSV")
            return

        success_count = 0
        for _, row in self.df.iterrows():
            try:
                data = tuple(row)
                insertar_balance_service(data)
                success_count += 1
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo insertar fila:\n{e}")

        messagebox.showinfo("Insertar en SQL", f"{success_count} registros insertados correctamente")
