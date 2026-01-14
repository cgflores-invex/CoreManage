import os
import tkinter as tk
import ttkbootstrap as tb
from ui.main_ui import App
from ui.csv_to_sql import CsvToSqlApp
from ui.csv_to_sql_resultado import CsvToSqlResultadoApp  # Ventana para cargar Layout Resultado

class MainMenu(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")  # <-- CORRECCIÓN AQUÍ
        self.title("Menú Principal")
        self.geometry("1000x1000")

        self.configure(bg="#f2f2f2")

        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "assets", "invex_logo.png")

        try:
            self.logo_img = tk.PhotoImage(file=image_path)
            tb.Label(self, image=self.logo_img).pack(pady=20)
        except Exception as e:
            tb.Label(self, text=f"No se pudo cargar el logo:\n{e}", foreground="red").pack(pady=20)

        tb.Label(self, text="Bienvenido al sistema", font=("Helvetica", 16)).pack(pady=10)

        # Botón Reclasificaciones
        tb.Button(
            self,
            text="Reclasificaciones",
            bootstyle="dark",
            command=self.abrir_reclasificaciones
        ).pack(pady=20)

        # Botón Layout Balance
        tb.Button(
            self,
            text="Cargar Layout Balance",
            bootstyle="dark",
            command=self.abrir_layout_balance
        ).pack(pady=20)
        # Botón Layout Resultado
        tb.Button(
            self,
            text="Layout Resultado",
            bootstyle="dark",
            command=self.abrir_layout_resultado
        ).pack(pady=15)

    def abrir_reclasificaciones(self):
        App(self)

    def abrir_layout_balance(self):
        CsvToSqlApp(self)

    def abrir_layout_resultado(self):
        CsvToSqlResultadoApp(self)
if __name__ == "__main__":
    menu = MainMenu()
    menu.mainloop()

