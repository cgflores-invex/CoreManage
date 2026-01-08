import os
import pandas as pd
import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.reclasificaciones_service import insertar_balance_service

class CsvToSqlApp(tb.Window):
    def __init__(self, csv_path=None):
        super().__init__(themename="superhero")
        self.title("Cargar Layout Balance")
        self.geometry("900x500")

        # Ruta por defecto si no se pasa csv_path
        if csv_path is None:
            self.csv_path = r"C:\EDSA\Reclasificaciones_layout_Balance.csv"
        else:
            self.csv_path = csv_path

        self.tree = None
        self.df = None  # Guardaremos el DataFrame cargado

        # Botón para insertar en SQL
        tb.Button(self, text="Insertar en SQL Server", bootstyle="success", command=self.insert_to_sql).pack(pady=5)

        # Cargar automáticamente CSV
        self.load_csv()

    def load_csv(self):
        if not os.path.exists(self.csv_path):
            messagebox.showerror("Error", f"No se encontró el archivo:\n{self.csv_path}")
            return

        try:
            self.df = pd.read_csv(self.csv_path)
            self.display_data(self.df)
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
            messagebox.showwarning("Atención", "No hay datos para insertar")
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
