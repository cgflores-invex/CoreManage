# ui/main_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from services.reclasificaciones_service import (
    listar_balance,
    listar_resultado,
    insertar_balance_service,
    eliminar_balance_service,
    insertar_resultado_service,
    eliminar_resultado_service
)

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Reclasificaciones")
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

    # --------------------- AGREGAR REGISTRO ---------------------
    def agregar_balance(self):
        popup = tb.Toplevel(self)
        popup.title("Agregar Balance")
        popup.geometry("400x500")

        columns = self.tree_balance["columns"]
        entradas = []

        # Crear labels y entradas
        for col in columns:
            tk.Label(popup, text=col).pack(pady=5)
            entry = tk.Entry(popup)
            entry.pack(pady=5)
            entradas.append(entry)

        # Guardar en SQL
        def guardar_nuevo():
            nuevos_valores = [e.get() for e in entradas]

            # Convertir campos numéricos
            try:

                nuevos_valores[1] = int(nuevos_valores[1])  # PeriodoId
                nuevos_valores[3] = int(nuevos_valores[3])  # NumIntercompania
                nuevos_valores[4] = int(nuevos_valores[4])  # NumLineaNegocio
                nuevos_valores[5] = int(nuevos_valores[5])  # NumProyecto
                nuevos_valores[6] = int(nuevos_valores[6])  # Reclasificacion
            except Exception:
                messagebox.showerror("Error", "Verifica los campos numéricos")
                return

            try:
                insertar_balance_service(tuple(nuevos_valores))
                self.tree_balance.insert('', 'end', values=self.clean_row(nuevos_valores))
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tb.Button(popup, text="Guardar", bootstyle="success", command=guardar_nuevo).pack(pady=15)

    def agregar_resultado(self):
        popup = tb.Toplevel(self)
        popup.title("Agregar Resultado")
        popup.geometry("400x500")

        columns = self.tree_resultado["columns"]
        entradas = []

        for col in columns:
            tk.Label(popup, text=col).pack(pady=5)
            entry = tk.Entry(popup)
            entry.pack(pady=5)
            entradas.append(entry)

        def guardar_nuevo():
            nuevos_valores = [e.get() for e in entradas]

            # Validar vacíos
            if any(v == "" for v in nuevos_valores):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            # Convertir campos numéricos
            try:

                nuevos_valores[1] = int(nuevos_valores[1])  # PeriodoId
                nuevos_valores[6] = int(nuevos_valores[6])  # Reclasificacion
            except Exception:
                messagebox.showerror("Error", "Verifica los campos numéricos")
                return

            try:
                insertar_resultado_service(tuple(nuevos_valores))
                self.tree_resultado.insert('', 'end', values=self.clean_row(nuevos_valores))
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tb.Button(popup, text="Guardar", bootstyle="success", command=guardar_nuevo).pack(pady=15)

    # --------------------- TREEVIEW ---------------------
    def crear_tree(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        tree.pack(expand=True, fill='both')
        for col in columns:
            tree.heading(col, text=col)
            # Ajustar anchos según columnas o un valor base
            if col.lower() in ['dataareaid', 'descripcion']:
                tree.column(col, width=150, anchor='center')
            elif col.lower() in ['periodoid', 'numintercompania', 'numlineanegocio', 'numproyecto']:
                tree.column(col, width=100, anchor='center')
            else:
                tree.column(col, width=120, anchor='center')
        return tree

    def clean_row(self, row):
        cleaned = []
        for val in row:
            if val is None:
                cleaned.append("")
            elif hasattr(val, 'to_eng_string'):
                cleaned.append(float(val))
            else:
                val_str = str(val)
                if val_str.startswith("'") and val_str.endswith("'"):
                    val_str = val_str[1:-1]
                cleaned.append(val_str)
        return tuple(cleaned)

    # --------------------- CARGAR DATOS ---------------------
    def cargar_balance(self):
        rows, columns = listar_balance()
        if self.tree_balance:
            self.tree_balance.destroy()

        container = tb.Frame(self.tab_balance)
        container.pack(expand=1, fill='both', padx=10, pady=10)

        self.tree_balance = self.crear_tree(container, columns)
        for row in rows:
            self.tree_balance.insert('', 'end', values=self.clean_row(row))

        tb.Button(container, text="Agregar registro", bootstyle="success", command=self.agregar_balance).pack(pady=10)
        tb.Button(container, text="Eliminar registro", bootstyle="danger", command=self.eliminar_balance).pack(pady=5)

    def cargar_resultado(self):
        rows, columns = listar_resultado()
        if self.tree_resultado:
            self.tree_resultado.destroy()

        container = tb.Frame(self.tab_resultado)
        container.pack(expand=1, fill='both', padx=10, pady=10)

        self.tree_resultado = self.crear_tree(container, columns)
        for row in rows:
            self.tree_resultado.insert('', 'end', values=self.clean_row(row))

        tb.Button(container, text="Agregar registro", bootstyle="success", command=self.agregar_resultado).pack(pady=10)
        tb.Button(container, text="Eliminar registro", bootstyle="danger", command=self.eliminar_resultado).pack(pady=5)

    # --------------------- ELIMINAR ---------------------
    def eliminar_balance(self):
        seleccion = self.tree_balance.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro para eliminar")
            return

        item_id = seleccion[0]
        valores = self.tree_balance.item(item_id)["values"]
        dataareaid, periodoid, reclasificacion = valores[0], valores[1], valores[6]

        if not messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
            return

        try:
            eliminar_balance_service(dataareaid, periodoid, reclasificacion)
            self.tree_balance.delete(item_id)
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_resultado(self):
        seleccion = self.tree_resultado.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro para eliminar")
            return

        item_id = seleccion[0]
        valores = self.tree_resultado.item(item_id)["values"]
        dataareaid, periodoid, reclasificacion = valores[0], valores[1], valores[8]

        # Convertir tipos correctamente
        try:
            dataareaid = str(dataareaid).strip()  # VARCHAR
            periodoid = int(periodoid)  # INT
            reclasificacion = float(reclasificacion)  # DECIMAL
        except ValueError:
            messagebox.showerror("Error", "Error en los tipos de PeriodoId o Reclasificación")
            return

        if not messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
            return

        try:
            eliminar_resultado_service(dataareaid, periodoid, reclasificacion)
            self.tree_resultado.delete(item_id)  # Eliminar del TreeView
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))


