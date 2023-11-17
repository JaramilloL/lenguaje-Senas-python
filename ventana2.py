import tkinter as tk
import inference_classifier

def procesar_senal():
    # Llama a las funciones de tu proyecto de lenguaje de señas aquí
    resultado = inference_classifier.procesar_senal()
    resultado_label.config(text=resultado)

# Crea una ventana
ventana = tk.Tk()
ventana.title("Aplicación de Lenguaje de Señas")

# Elementos de interfaz de usuario
senal_entry = tk.Entry(ventana)
procesar_button = tk.Button(ventana, text="Procesar Señal", command=procesar_senal)
resultado_label = tk.Label(ventana, text="Resultado")

# Coloca los elementos en la ventana con opciones de empaquetado
senal_entry.pack(fill=tk.X, padx=100, pady=5)
procesar_button.pack(fill=tk.X, padx=100, pady=50)
resultado_label.pack(fill=tk.X, padx=100, pady=50)

ventana.mainloop()
