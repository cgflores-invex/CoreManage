import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from services.reclasificaciones_service import listar_balance, listar_resultado

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Reclasificaciones PLANFIN")
        self.geometry("1000x600")

        tab_control = ttk.Notebook(self)
        self.tab_balance = ttk.Frame(tab_control)
        self.tab_resultado = ttk.Frame(tab_control)
        tab_control.add(self.tab_balance, text='Balance')
        tab_control.add(self.tab_resultado, text='Resultado')
        tab_control.pack(expand=1, fill="both")

        self.tree_balance = None
        self.tree_resultado = None

        self.cargar_balance()
        self.cargar_resultado()

    def crear_tree(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        tree.pack(expand=1, fill='both')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        return tree

    def clean_row(self, row):
        cleaned = []
        for val in row:
            if val is None:
                cleaned.append("")
            elif hasattr(val, 'to_eng_string'):  # para Decimal
                cleaned.append(float(val))
            else:
                val_str = str(val)
                # Quitar comillas simples al inicio y final si existen
                if val_str.startswith("'") and val_str.endswith("'"):
                    val_str = val_str[1:-1]
                cleaned.append(val_str)
        return tuple(cleaned)

    def cargar_balance(self):
        rows, columns = listar_balance()
        if not rows:
            return
        if self.tree_balance:
            self.tree_balance.destroy()
        self.tree_balance = self.crear_tree(self.tab_balance, columns)
        for row in rows:
            self.tree_balance.insert('', 'end', values=self.clean_row(row))

    def cargar_resultado(self):
        rows, columns = listar_resultado()
        if not rows:
            return
        if self.tree_resultado:
            self.tree_resultado.destroy()
        self.tree_resultado = self.crear_tree(self.tab_resultado, columns)
        for row in rows:
            self.tree_resultado.insert('', 'end', values=self.clean_row(row))


if __name__ == "__main__":
    app = App()
    app.mainloop()

