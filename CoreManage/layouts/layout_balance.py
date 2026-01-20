import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import pandas as pd
from datetime import datetime
import threading
from services.reclasificaciones_service import (
    insertar_balance_service,
    get_reclasificaciones_balance
)

# ---------------- Función auxiliar ---------------- #
def generar_periodos(anio: int) -> list[str]:
    return [f"{anio}{mes:02d}" for mes in range(1, 13)]


# ---------------- Clase principal ---------------- #
class CsvToSqlApp(tb.Toplevel):
    def __init__(self, parent=None):
        super().__init__(master=parent, themename="superhero")
        self.title("Cargar Layout Balance")
        self.geometry("950x500")
        self.resizable(True, True)

        self.df: pd.DataFrame | None = None
        self.tree: ttk.Treeview | None = None

        # ---------------- UI ---------------- #
        self._build_ui()

        # Cargar datos iniciales
        self.load_sql_data()

    def _build_ui(self):
        # Frame superior para controles
        control_frame = tb.Frame(self)
        control_frame.pack(fill="x", padx=10, pady=10)

        # Combo de períodos
        anio_actual = datetime.now().year
        periodos = generar_periodos(anio_actual)
        self.periodo_var = tk.StringVar()
        self.combo_periodo = tb.Combobox(
            control_frame,
            textvariable=self.periodo_var,
            values=periodos,
            state="readonly",
            width=15,
            bootstyle="light"
        )
        self.combo_periodo.pack(side="left", padx=5)
        self.combo_periodo.current(datetime.now().month - 1)
        self.combo_periodo.bind("<<ComboboxSelected>>", self.filtrar_periodo)

        # Botón Insertar
        tb.Button(
            control_frame,
            text="Insertar en SQL Server",
            bootstyle="success",
            command=self.insert_to_sql
        ).pack(side="left", padx=10)

        # Treeview Frame
        self.tree_frame = tb.Frame(self)
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    # ---------------- Cargar datos SQL ---------------- #
    def load_sql_data(self):
        rows, columns = get_reclasificaciones_balance()
        if not columns:
            messagebox.showwarning("Atención", "No se pudo obtener información de SQL")
            return

        self.df = pd.DataFrame(rows, columns=columns)
        self.display_data(self.df)

    # ---------------- Mostrar datos ---------------- #
    def display_data(self, df: pd.DataFrame):
        if self.tree:
            self.tree.destroy()

        columns = list(df.columns)
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")

        # Scrollbar vertical
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", expand=True, fill="both")
        vsb.pack(side="right", fill="y")

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Insertar datos
        for row in df.itertuples(index=False, name=None):
            self.tree.insert("", "end", values=row)

    # ---------------- Filtrar por período ---------------- #
    def filtrar_periodo(self, event=None):
        if self.df is None:
            return

        periodo = self.periodo_var.get()
        if not periodo:
            filtered = self.df
        else:
            filtered = self.df[self.df['PeriodoId'].astype(str) == periodo]

        self.display_data(filtered)

    # ---------------- Insertar en SQL ---------------- #
    def insert_to_sql(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Atención", "No hay datos para insertar")
            return

        periodo = self.periodo_var.get()
        if not periodo:
            messagebox.showwarning("Atención", "Seleccione un período")
            return

        confirmar = messagebox.askyesno(
            "Confirmar operación",
            f"Se eliminarán TODOS los registros del período {periodo} en SQL.\n¿Desea continuar?"
        )
        if not confirmar:
            return

        threading.Thread(target=self._insert_worker, daemon=True).start()

    def _insert_worker(self):
        try:
            success_count = 0
            for _, row in self.df.iterrows():
                insertar_balance_service(tuple(row))
                success_count += 1

            self.after(
                0,
                lambda: messagebox.showinfo(
                    "Insertar en SQL",
                    f"{success_count} registros insertados correctamente"
                )
            )
        except Exception as e:
            self.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    f"No se pudo insertar en SQL:\n{e}"
                )
            )



