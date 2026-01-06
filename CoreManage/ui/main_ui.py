# ui/main_ui.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from services.reclasificaciones_service import (
    listar_balance,
    listar_resultado,
    insertar_balance_service,
    eliminar_balance_service
)

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

    # --------------------- AGREGAR REGISTRO ---------------------
    def agregar_balance(self):
        popup = tb.Toplevel(self)
        popup.title("Agregar registro")
        popup.geometry("400x500")

        columns = self.tree_balance["columns"]
        entradas = []

        # Crear labels y entradas
        for col in columns:
            tk.Label(popup, text=col).pack(pady=5)
            entry = tk.Entry(popup)
            entry.pack(pady=5)
            entradas.append(entry)

        # Función que guarda el registro en SQL
        def guardar_nuevo():
            nuevos_valores = [e.get() for e in entradas]

            # Convertir campos numéricos a int
            try:
                nuevos_valores[0] = int(nuevos_valores[0])  # DataAreaId
                nuevos_valores[1] = int(nuevos_valores[1])  # PeriodoId
                nuevos_valores[3] = int(nuevos_valores[3])  # NumIntercompania
                nuevos_valores[4] = int(nuevos_valores[4])  # NumLineaNegocio
                nuevos_valores[5] = int(nuevos_valores[5])  # NumProyecto
                nuevos_valores[6] = int(nuevos_valores[6])  # Reclasificacion
            except Exception as conv_err:
                print("❌ Error al convertir tipos:", conv_err)
                return

            try:
                insertar_balance_service(tuple(nuevos_valores))
                print("✅ Registro insertado correctamente en SQL:", nuevos_valores)

                self.tree_balance.insert(
                    '',
                    'end',
                    values=self.clean_row(nuevos_valores)
                )

                popup.destroy()
            except Exception as e:
                print("❌ Error al insertar en SQL:", e)

        # Botón Guardar
        btn_guardar = tb.Button(
            popup,
            text="Guardar",
            bootstyle="success",
            command=guardar_nuevo
        )
        btn_guardar.pack(pady=15)

    # --------------------- TREEVIEW ---------------------
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
                if val_str.startswith("'") and val_str.endswith("'"):
                    val_str = val_str[1:-1]
                cleaned.append(val_str)
        return tuple(cleaned)

    # --------------------- CARGAR DATOS ---------------------
    def cargar_balance(self):
        rows, columns = listar_balance()
        if not rows:
            return
        if self.tree_balance:
            self.tree_balance.destroy()

        container = tb.Frame(self.tab_balance)
        container.pack(expand=1, fill='both', padx=10, pady=10)

        self.tree_balance = self.crear_tree(container, columns)
        for row in rows:
            self.tree_balance.insert('', 'end', values=self.clean_row(row))

        # Botón Agregar
        btn_agregar = tb.Button(
            container,
            text="Agregar registro",
            bootstyle="success",
            command=self.agregar_balance
        )
        btn_agregar.pack(pady=10)

        # Botón Eliminar
        btn_eliminar = tb.Button(
            container,
            text="Eliminar registro",
            bootstyle="danger",
            command=self.eliminar_balance
        )
        btn_eliminar.pack(pady=5)

    def cargar_resultado(self):
        rows, columns = listar_resultado()
        if not rows:
            return
        if self.tree_resultado:
            self.tree_resultado.destroy()
        self.tree_resultado = self.crear_tree(self.tab_resultado, columns)
        for row in rows:
            self.tree_resultado.insert('', 'end', values=self.clean_row(row))

    # --------------------- ELIMINAR ---------------------
    def eliminar_balance(self):
        seleccion = self.tree_balance.selection()
        if not seleccion:
            print("No hay fila seleccionada")
            return

        item_id = seleccion[0]
        valores = self.tree_balance.item(item_id)["values"]

        dataareaid = valores[0]
        periodoid = valores[1]
        reclasificacion = valores[6]

        try:
            eliminar_balance_service(dataareaid, periodoid, reclasificacion)
            self.tree_balance.delete(item_id)
            print("✅ Registro eliminado correctamente")
        except Exception as e:
            print("❌ Error al eliminar:", e)


# --------------------- MAIN ---------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
