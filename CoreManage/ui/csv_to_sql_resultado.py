import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import ttkbootstrap as tb
from datetime import datetime
from services.reclasificaciones_service import insertar_resultado_service


def generar_periodos(anio: int) -> list[str]:
    return [f"{anio}{mes:02d}" for mes in range(1, 13)]


class CsvToSqlResultadoApp(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Cargar Layout Resultado")
        self.geometry("1000x500")

        # Frame para controles (botones + combo)
        control_frame = tb.Frame(self)
        control_frame.pack(fill='x', padx=10, pady=10)

        # Botón para cargar CSV
        tb.Button(control_frame, text="Cargar CSV Resultado", bootstyle="primary", command=self.load_csv).pack(side='left', padx=5)

        # Combo periodo
        anio_actual = datetime.now().year
        periodos = generar_periodos(anio_actual)
        self.periodo_var = tk.StringVar()
        self.combo_periodo = tb.Combobox(
            control_frame,
            textvariable=self.periodo_var,
            values=periodos,
            bootstyle="info",
            state="readonly",
            width=15
        )
        self.combo_periodo.pack(side='left', padx=5)
        mes_actual = datetime.now().month
        self.combo_periodo.current(mes_actual - 1)

        # Botón para insertar en SQL
        tb.Button(control_frame, text="Insertar en SQL Server", bootstyle="success", command=self.insert_to_sql).pack(side='left', padx=5)

        # Frame para la tabla (Treeview)
        self.tree_frame = tb.Frame(self)
        self.tree_frame.pack(expand=True, fill='both', padx=10, pady=(0,10))

        self.tree = None
        self.df = None  # Guardaremos el DataFrame cargado

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            self.df = pd.read_csv(filepath, dtype=str, delimiter=',')

            # Limpiar nombres de columna (eliminar espacios extra)
            self.df.columns = [c.strip() for c in self.df.columns]

            # Revisar que tenga exactamente 9 columnas
            if len(self.df.columns) != 9:
                messagebox.showerror("Error",
                                     f"El CSV debe tener 9 columnas. Columnas detectadas: {len(self.df.columns)}")
                return

            self.display_data(self.df)
            messagebox.showinfo("Éxito", f"Archivo cargado: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def display_data(self, df):
        if self.tree:
            self.tree.destroy()

        columns = list(df.columns)
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        self.tree.pack(expand=True, fill='both')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=[str(v) for v in row])

    def insert_to_sql(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Atención", "Primero carga un CSV")
            return

        success_count = 0
        for _, row in self.df.iterrows():
            try:
                data = tuple(row)
                if len(data) != 9:
                    print("❌ Fila ignorada por longitud incorrecta:", data)
                    continue

                insertar_resultado_service(data)
                success_count += 1
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo insertar fila:\n{e}")

        messagebox.showinfo("Insertar en SQL", f"{success_count} registros insertados correctamente")


if __name__ == "__main__":
    app = CsvToSqlResultadoApp()
    app.mainloop()


