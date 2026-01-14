import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import ttkbootstrap as tb
from datetime import datetime
import threading

from services.reclasificaciones_service import (
    insertar_balance_service,
    eliminar_balance_service_periodo
)


def generar_periodos(anio: int) -> list[str]:
    return [f"{anio}{mes:02d}" for mes in range(1, 13)]


class CsvToSqlApp(tb.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Cargar Layout Balance")
        self.geometry("900x500")

        self.df: pd.DataFrame | None = None
        self.tree: ttk.Treeview | None = None

        self._build_ui()

    # ---------------- UI ---------------- #

    def _build_ui(self):
        control_frame = tb.Frame(self)
        control_frame.pack(fill="x", padx=10, pady=10)

        tb.Button(
            control_frame,
            text="Seleccionar CSV Balance",
            bootstyle="primary",
            command=self.load_csv
        ).pack(side="left", padx=5)

        anio_actual = datetime.now().year
        periodos = generar_periodos(anio_actual)

        # ⚠️ StringVar SIEMPRE con master
        self.periodo_var = tk.StringVar(master=self)

        self.combo_periodo = tb.Combobox(
            control_frame,
            textvariable=self.periodo_var,
            values=periodos,
            state="readonly",
            width=15,
            bootstyle="info"
        )
        self.combo_periodo.pack(side="left", padx=5)
        self.combo_periodo.current(datetime.now().month - 1)

        tb.Button(
            control_frame,
            text="Insertar en SQL Server",
            bootstyle="success",
            command=self.insert_to_sql
        ).pack(side="left", padx=5)

        self.tree_frame = tb.Frame(self)
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    # ---------------- CSV ---------------- #

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            initialdir=r"C:\EDSA",
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            self.df = pd.read_csv(
                filepath,
                encoding="utf-8",
                dtype=str
            )
            self.display_data(self.df)
            messagebox.showinfo("Éxito", "Archivo cargado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    # ---------------- TREEVIEW ---------------- #

    def display_data(self, df: pd.DataFrame):
        if self.tree:
            self.tree.destroy()

        columns = list(df.columns)

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings"
        )

        vsb = ttk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", expand=True, fill="both")
        vsb.pack(side="right", fill="y")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        for row in df.itertuples(index=False, name=None):
            self.tree.insert("", "end", values=row)

    # ---------------- SQL ---------------- #

    def insert_to_sql(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Atención", "Primero cargue un CSV")
            return

        periodo = self.periodo_var.get()
        if not periodo:
            messagebox.showwarning("Atención", "Seleccione un período")
            return

        confirmar = messagebox.askyesno(
            "Confirmar operación",
            f"Se eliminarán TODOS los registros del período {periodo}.\n\n¿Desea continuar?"
        )
        if not confirmar:
            return

        threading.Thread(
            target=self._insert_worker,
            args=(periodo,),
            daemon=True
        ).start()

    def _insert_worker(self, periodo: str):
        try:
            # El combo SOLO define qué período eliminar
            eliminar_balance_service_periodo(periodo)

            df = self.df.copy()

            success = 0
            for row in df.itertuples(index=False, name=None):
                insertar_balance_service(row)
                success += 1

            self.after(
                0,
                lambda: messagebox.showinfo(
                    "Proceso finalizado",
                    f"{success} registros insertados correctamente"
                )
            )

        except Exception as e:
            self.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    f"Ocurrió un error durante la inserción:\n{e}"
                )
            )


