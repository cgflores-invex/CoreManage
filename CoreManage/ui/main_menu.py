import os
import tkinter as tk
import ttkbootstrap as tb
from ui.main_ui import App  # Importa tu ventana de Reclasificaciones

class MainMenu(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Menú Principal")
        self.geometry("1000x600")

        # ------------------ IMAGEN ------------------
        base_path = os.path.dirname(__file__)  # carpeta ui
        image_path = os.path.join(base_path, "assets", "invex_logo.png")

        try:
            self.logo_img = tk.PhotoImage(file=image_path)
            label_logo = tb.Label(self, image=self.logo_img)
            label_logo.pack(pady=20)
        except Exception as e:
            tb.Label(self, text=f"No se pudo cargar el logo:\n{e}", foreground="red").pack(pady=20)

        # ------------------ TEXTO DE BIENVENIDA ------------------
        tb.Label(self, text="Bienvenido al sistema", font=("Helvetica", 16)).pack(pady=10)

        # ------------------ BOTÓN ------------------
        tb.Button(
            self,
            text="Reclasificaciones",
            bootstyle="primary",
            command=self.abrir_reclasificaciones
        ).pack(pady=20)

    def abrir_reclasificaciones(self):
        # Abrir la ventana de reclasificaciones
        reclas_window = App()
        reclas_window.mainloop()

# ------------------ EJECUTAR ------------------
if __name__ == "__main__":
    menu = MainMenu()
    menu.mainloop()

