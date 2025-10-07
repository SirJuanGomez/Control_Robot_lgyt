import socket
import struct
import tkinter as tk
from tkinter import ttk
import numpy as np
import threading

# Configuración básica del servidor
HOST = 'localhost'
PORT = 1234

NUM_FLOATS = 17  # 14 motores + 3 IMU (normalizado entre 0 y 1)
BYTES_PER_FLOAT = 4
TOTAL_BYTES = NUM_FLOATS * BYTES_PER_FLOAT

# Etiquetas de los sensores
labels = [
    'C_PD', 'C_PI', 'P_D', 'P_I', 'R_D', 'R_I', 'F_R', 'F_L',
    'H_D', 'H_I', 'B_D', 'B_I', 'M_D', 'M_I',
    'IMU_Roll', 'IMU_Pitch', 'IMU_Yaw'
]

# Conectar al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class RealTimeGraphApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Monitor de Motores e IMU")
        self.geometry("600x600")

        # Crear un frame para contener las barras de progreso
        self.frame = ttk.Frame(self)
        self.frame.pack(pady=20)

        # Crear las barras de progreso para los motores y el IMU
        self.progress_bars = []
        self.labels_widgets = []

        for i in range(NUM_FLOATS):
            label = ttk.Label(self.frame, text=labels[i], width=20)
            label.grid(row=i, column=0, padx=10, pady=5)
            self.labels_widgets.append(label)

            progress_bar = ttk.Progressbar(self.frame, length=200, maximum=1, value=0)
            progress_bar.grid(row=i, column=1, padx=10, pady=5)
            self.progress_bars.append(progress_bar)

        # Añadir un botón para cerrar la aplicación
        self.quit_button = ttk.Button(self, text="Cerrar", command=self.quit)
        self.quit_button.pack(pady=20)

    def update_bars(self, data):
        """ Actualiza las barras de progreso con los valores de los sensores """
        for i, value in enumerate(data):
            if i < NUM_FLOATS - 3:  # Para los motores (14 primeros valores)
                # Normalizar el rango de los motores de -90° a 90° en una barra [0, 1]
                self.progress_bars[i].config(maximum=180, value=np.clip(value, -90, 90) + 90)
            else:  # Para el IMU (últimos 3 valores)
                # El IMU está normalizado entre 0 y 1
                self.progress_bars[i].config(maximum=1, value=np.clip(value, 0, 1))

    def run_client(self):
        """ Lee los datos del servidor y actualiza las barras de progreso """
        try:
            client_socket.connect((HOST, PORT))  # Conectarse al servidor

            while True:
                data = b''
                while len(data) < TOTAL_BYTES:
                    packet = client_socket.recv(TOTAL_BYTES - len(data))
                    if not packet:
                        raise ConnectionError("Servidor desconectado.")
                    data += packet

                # Desempaquetar los datos recibidos
                obs = struct.unpack(f'{NUM_FLOATS}f', data)
                obs = list(obs)

                # Actualizar las barras de progreso en el hilo principal
                self.after(0, self.update_bars, obs)

        except KeyboardInterrupt:
            print("Interrumpido.")
        finally:
            client_socket.close()

def start_client():
    """ Inicia la función del cliente en un hilo separado """
    app = RealTimeGraphApp()
    client_thread = threading.Thread(target=app.run_client)
    client_thread.daemon = True  # Permite cerrar el hilo cuando la ventana se cierra
    client_thread.start()
    app.mainloop()  # Inicia la interfaz gráfica de Tkinter

if __name__ == '__main__':
    start_client()  # Inicia la aplicación Tkinter y la conexión cliente
