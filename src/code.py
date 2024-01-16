import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mat73
import numpy as np
import random
import string

width_graph = 16
height_graph = 6

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Señal Temporal")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.archivo_path = ""  # Variable para almacenar la ruta del archivo

        self.label = tk.Label(self.frame, text="Selecciona un archivo MAT:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.button_cargar = tk.Button(self.frame, text="Cargar archivo", command=self.cargar_archivo_mat)
        self.button_cargar.grid(row=1, column=0, padx=10, pady=10)

        self.transmisor_label = tk.Label(self.frame, text="Transmisor:")
        self.transmisor_label.grid(row=0, column=1, padx=10, pady=5)

        self.transmisor_spinbox = tk.Spinbox(self.frame, from_=0, to=11, command=self.actualizar_var_y_plotear)
        self.transmisor_spinbox.grid(row=1, column=1, padx=10, pady=5)

        self.receptor_label = tk.Label(self.frame, text="Receptor:")
        self.receptor_label.grid(row=0, column=2, padx=10, pady=5)

        self.receptor_spinbox = tk.Spinbox(self.frame, from_=0, to=11, command=self.actualizar_var_y_plotear)
        self.receptor_spinbox.grid(row=1, column=2, padx=10, pady=5)

        # Aumenté el tamaño del gráfico al doble
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(width_graph, height_graph), sharex=True, gridspec_kw={'hspace': 0.5})
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Inicializamos las variables
        self.transmisor = 0
        self.receptor = 0

        # Botón para añadir señal al segundo gráfico
        self.button_anadir = tk.Button(self.frame, text="Añadir señal", command=self.anadir_senal)
        self.button_anadir.grid(row=0, column=6, columnspan=3, padx=10, pady=10)

        # Lista para almacenar las señales añadidas al segundo gráfico
        self.señales_anadidas = []
        
        # Lista para almacenar las leyendas añadidas
        self.leyendas_anadidas = []
        
        # Botón para borrar la última señal añadida
        self.button_borrar_ultima = tk.Button(self.frame, text="Borrar última señal", command=self.borrar_ultima_senal)
        self.button_borrar_ultima.grid(row=1, column=4, padx=10, pady=10)

        # Botón para borrar todas las señales añadidas
        self.button_borrar_todas = tk.Button(self.frame, text="Borrar todas las señales", command=self.borrar_todas_las_senales)
        self.button_borrar_todas.grid(row=0, column=4, padx=10, pady=10)
        
        self.trans_receptor_anadidos = []
        
    def cargar_archivo_mat(self):
        if not self.archivo_path:
            self.archivo_path = filedialog.askopenfilename(filetypes=[("MAT files", "*.mat")],initialdir = '~/Downloads')

        try:
            data = mat73.loadmat(self.archivo_path)
            self.signal = data['data'][:, self.transmisor, self.receptor]
            self.plotear_grafico()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo MAT: {str(e)}")

    def generar_etiqueta_aleatoria(self):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(5))
    
    def generar_etiqueta_formato(self, transmisor, receptor):
        return "t = {}; r = {}".format(transmisor, receptor)


    def plotear_grafico(self):
        self.ax1.clear()
        leyenda_grafica_1 = self.generar_etiqueta_formato(self.transmisor, self.receptor)
        self.ax1.plot(self.signal, label=leyenda_grafica_1)
        self.ax1.set_title("Señal Temporal")
        self.ax1.set_xlabel("Muestras")
        self.ax1.set_ylabel("Valor")
        self.ax1.legend()

        # Limpia el segundo gráfico para evitar duplicaciones al añadir señales
        self.ax2.clear()
        for signal, leyenda in zip(self.señales_anadidas, self.leyendas_anadidas):
            self.ax2.plot(signal, alpha=0.5, label=leyenda)  # Añade las señales con transparencia
        self.ax2.set_title("Señales Añadidas")
        self.ax2.set_xlabel("Muestras")
        self.ax2.set_ylabel("Valor")
        self.ax2.legend()

        self.canvas.draw()

    def actualizar_var_y_plotear(self):
        self.transmisor = int(self.transmisor_spinbox.get())
        self.receptor = int(self.receptor_spinbox.get())
        self.cargar_archivo_mat()
        
    def anadir_senal(self):
        if hasattr(self, 'signal'):
            leyenda_grafica_2 = self.generar_etiqueta_formato(self.transmisor, self.receptor)
            self.leyendas_anadidas.append(leyenda_grafica_2)
            self.señales_anadidas.append(self.signal.copy())
            self.plotear_grafico()

    def borrar_ultima_senal(self):
        if self.señales_anadidas:
            self.señales_anadidas.pop()
            self.plotear_grafico()

    def borrar_todas_las_senales(self):
        self.señales_anadidas = []
        self.plotear_grafico()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()
