import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy,  QTextBrowser,  QDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import cv2

import pickle
import mediapipe as mp
import numpy as np

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.iniciar_ui()

    def iniciar_ui(self):
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle('lenguaje de senas')

        # Ajustar el diseño para centrar verticalmente y espacio entre elementos
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setAlignment(QtCore.Qt.AlignVCenter)
        self.layout_principal.setSpacing(5)  # Espacio de 5 píxeles entre elementos

        # Etiqueta para mostrar en qué apartado estamos
        self.etiqueta_apartado = QLabel('Bienvenido al apartado de Inicio')
        self.layout_principal.addWidget(self.etiqueta_apartado)
        self.etiqueta_apartado.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.etiqueta_apartado.setAlignment(Qt.AlignCenter)
        
        self.etiqueta_conocenos = QLabel('En el apartado de "Conócenos", encontrará información sobre nosotros.')
        self.layout_principal.addWidget(self.etiqueta_conocenos)
        self.etiqueta_conocenos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.etiqueta_conocenos.setAlignment(Qt.AlignCenter)
        
        #agregamos la nueva ventana para mostrar el uso de la camara 
        
        
        # Agregar una imagen
        self.imagen_conocenos = QLabel(self)
        pixmap = QPixmap('./img/cut.jpg')  # Reemplaza 'ruta_de_la_imagen.jpg' con la ruta de tu imagen
        self.imagen_conocenos.setPixmap(pixmap)
        self.imagen_conocenos.setAlignment(Qt.AlignCenter)
        self.imagen_conocenos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_principal.addWidget(self.imagen_conocenos)
        self.imagen_conocenos.setPixmap(pixmap)
        self.imagen_conocenos.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(self.imagen_conocenos)

        # Botones de navegación
        self.boton_inicio = QPushButton('Inicio', self)
        self.boton_youtube = QPushButton('Ver tutorial', self)
        self.boton_info_adicional = QPushButton('Conocenos', self)
        self.boton_capturar_senas = QPushButton('capturar_senas', self)


        # Asignar estilos a los botones
        self.boton_inicio.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.boton_youtube.setStyleSheet("QPushButton { background-color: #FF0000; color: white; }")
        self.boton_info_adicional.setStyleSheet("QPushButton { background-color: #336699; color: white; }")
        self.boton_capturar_senas.setStyleSheet("QPushButton { background-color: #104691; color: white; }")

        self.boton_inicio.clicked.connect(self.mostrar_inicio)
        self.boton_youtube.clicked.connect(self.abrir_youtube)
        self.boton_info_adicional.clicked.connect(self.mostrar_info_adicional)
        self.boton_capturar_senas.clicked.connect(self.mostrar_capturar_senas)

        # Añadir botones al diseño
        self.layout_principal.addWidget(self.boton_inicio)
        self.layout_principal.addWidget(self.boton_youtube)
        self.layout_principal.addWidget(self.boton_info_adicional)
        self.layout_principal.addWidget(self.boton_capturar_senas)
        

    def mostrar_inicio(self):
        self.etiqueta_apartado.setText('Bienvenido al apartado de Inicio')


    def abrir_youtube(self):
        # Abre el enlace a YouTube en el navegador predeterminado
        QDesktopServices.openUrl(QUrl('https://www.youtube.com/watch?v=Jrbd-jkaUAk&list=PLi8XpZVEKlLqqqR2-J4gxqxyP0KtahNPw&index=1&pp=iAQB'))
        
        #creamos la funcion de ejecucion de la ventana nueva
    def mostrar_info_adicional(self):
        # Crear e instanciar la ventana de información adicional como un QDialog
        ventana_info_adicional = VentanaInfoAdicional()
        ventana_info_adicional.exec_()
        
    def mostrar_capturar_senas(self):
        # Crear e instanciar la ventana de información adicional como un QDialog
        ventana_info_adicional = VentanaCapturarSenas()
        ventana_info_adicional.exec_()
        
        #creamos la clase para ejecutar el widget para mostrar la ventana nueva
class VentanaInfoAdicional(QDialog):
    def __init__(self):
        super().__init__()

        self.iniciar_ui()

    def iniciar_ui(self):
        self.setGeometry(200,200,300,300)
        self.setWindowTitle('Información Adicional')

        layout = QVBoxLayout(self)

        texto_info = (
            "Aquí puedes agregar información adicional en texto plano. "
            "Puedes personalizar este texto según tus necesidades."
        )

        # Utilizamos QTextBrowser para mostrar texto con formato
        texto_browser = QTextBrowser(self)
        texto_browser.setPlainText(texto_info)

        layout.addWidget(texto_browser)       

class VentanaCapturarSenas(QDialog):
    def __init__(self):
        super().__init__()

        self.setGeometry(100,100,800,600)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_camara)
        
        self.iniciar_ui()

    def iniciar_ui(self):
        self.setWindowTitle('Ventana de Cámara')

        layout = QVBoxLayout(self)

        self.label_camara = QLabel(self)
        layout.addWidget(self.label_camara)

        self.boton_iniciar_camara = QPushButton('Iniciar Cámara', self)
        self.boton_iniciar_camara.clicked.connect(self.iniciar_camara)
        layout.addWidget(self.boton_iniciar_camara)

        self.boton_detener_camara = QPushButton('Detener Cámara', self)
        self.boton_detener_camara.clicked.connect(self.detener_camara)
        layout.addWidget(self.boton_detener_camara)

        #########################################################################3
        #aqui ponemos la parte del lenguaje de señas
        #####################################################
        self.model_dict = pickle.load(open('./model.p', 'rb'))
        self.model = self.model_dict['model']

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

        self.labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 9: 'K', 10: 'L', 11: 'M', 12: 'N', 13: 'O', 14: 'P', 15: 'Q', 16: 'R', 17: 'S', 18: 'T', 22: 'X', 23: 'Y'}

        self.num_landmarks = 21
        
    def iniciar_camara(self):
        self.cap = cv2.VideoCapture(0)  # Abre la cámara, 0 representa la cámara predeterminada

        self.timer.start(30)  # Configura el temporizador para actualizar la cámara cada 30 milisegundos
        
    def detener_camara(self):
        self.timer.stop()
        self.cap.release()  # Libera los recursos de la cámara

    def actualizar_camara(self):
        ret, frame = self.cap.read()  # Lee un frame de la cámara
        
        ############################################################
        #segunda parte del analisis
        #############################################################
        if ret:
            H, W, _ = frame.shape

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    data_aux = []
                    x_ = []
                    y_ = []

                    for i in range(self.num_landmarks):
                        if i < len(hand_landmarks.landmark):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                        else:
                            x = 0  
                            y = 0
                        x_.append(x)
                        y_.append(y)

                    for i in range(self.num_landmarks):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10

                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10

                    if len(data_aux) == self.num_landmarks * 2:
                        prediction = self.model.predict([np.asarray(data_aux)])
                        predicted_character = self.labels_dict[int(prediction[0])]
                    else:
                        predicted_character = "Desconocido"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)


        if ret:
            # Convierte el frame de BGR a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convierte la matriz de imagen de OpenCV a un objeto QImage
            imagen_qt = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
            # Crea un QPixmap a partir del QImage
            pixmap = QPixmap.fromImage(imagen_qt)
            # Escala el QPixmap para que se ajuste al tamaño del QLabel
            pixmap = pixmap.scaled(self.label_camara.size(), Qt.KeepAspectRatio)
            # Muestra el QPixmap en el QLabel
            self.label_camara.setPixmap(pixmap)       


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
