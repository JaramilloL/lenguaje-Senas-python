import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import hola

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 400, 300)  # Establecer posición y tamaño de la ventana
        self.setWindowTitle('Lenguaje de señas')  # Establecer el título de la ventana

        # Crear elementos de interfaz adicionales
        self.resultado_label = QLabel('Resultado:')
        self.boton_procesar = QPushButton('Procesar Señal')
        self.boton_procesar.clicked.connect(self.procesar_senal)

        # Diseño de la interfaz con QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.resultado_label)
        layout.addWidget(self.boton_procesar)

        # Establecer el diseño principal de la ventana
        self.setLayout(layout)

    def procesar_senal(self):
        # Llama a las funciones de tu proyecto de lenguaje de señas aquí
        resultado = hola.procesar_senal()
        self.resultado_label.setText(f'Resultado: {resultado}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())
