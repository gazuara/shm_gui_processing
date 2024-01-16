import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mat73
import numpy as np

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Señal Temporal")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.archivo_path = ""  # Variable para almacenar la ruta del archivo

        self.label = tk.Label(self.frame, text="Selecciona un archivo MAT:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.button = tk.Button(self.frame, text="Cargar archivo", command=self.cargar_archivo_mat)
        self.button.grid(row=0, column=1, padx=10, pady=10)

        self.transmisor_label = tk.Label(self.frame, text="Transmisor:")
        self.transmisor_label.grid(row=1, column=0, padx=10, pady=5)

        self.transmisor_spinbox = tk.Spinbox(self.frame, from_=0, to=11, command=self.actualizar_var_y_plotear)
        self.transmisor_spinbox.grid(row=1, column=1, padx=10, pady=5)

        self.receptor_label = tk.Label(self.frame, text="Receptor:")
        self.receptor_label.grid(row=2, column=0, padx=10, pady=5)

        self.receptor_spinbox = tk.Spinbox(self.frame, from_=0, to=11, command=self.actualizar_var_y_plotear)
        self.receptor_spinbox.grid(row=2, column=1, padx=10, pady=5)

        # Aumenté el tamaño del gráfico al doble
        self.fig, self.ax = plt.subplots(figsize=(16, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Inicializamos las variables
        self.transmisor = 0
        self.receptor = 0

    def cargar_archivo_mat(self):
        if not self.archivo_path:
            self.archivo_path = filedialog.askopenfilename(filetypes=[("MAT files", "*.mat")])

        try:
            data = mat73.loadmat(self.archivo_path)
            self.signal = data['data'][:, self.transmisor, self.receptor]
            self.plotear_grafico()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo MAT: {str(e)}")

    def plotear_grafico(self):
        self.ax.clear()
        self.ax.plot(self.signal)
        self.ax.set_title("Señal Temporal")
        self.ax.set_xlabel("Muestras")
        self.ax.set_ylabel("Valor")
        self.canvas.draw()

    def actualizar_var_y_plotear(self):
        self.transmisor = int(self.transmisor_spinbox.get())
        self.receptor = int(self.receptor_spinbox.get())
        self.cargar_archivo_mat()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()
