"""
@fileoverview Lógica visual de la mascota animada usando PyQt5.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Define la ventana y las animaciones de la mascota de J.A.R.V.I.S.
             Se comunica con el backend a través de una cola de mensajes para
             actualizar su estado visual en tiempo real.
"""

import sys
import math
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QTimer, QPoint, QRectF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen

class MascotWindow(QMainWindow):
    """
    @class MascotWindow
    @description Ventana de la mascota, sin bordes y siempre visible.
                 Renderiza animaciones basadas en el estado del asistente.
    """
    def __init__(self, comm_queue=None):
        super().__init__()
        self.comm_queue = comm_queue
        self.state = "idle"
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(30) # ~33 FPS

        # Configuración de la ventana para que sea un HUD
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 200, 200)

        # Variables para controlar las animaciones
        self.pulse_value = 0
        self.pulse_direction = 1
        self.rotation_angle = 0

        # Timer para leer mensajes del backend
        if self.comm_queue:
            self.queue_timer = QTimer(self)
            self.queue_timer.timeout.connect(self.check_queue)
            self.queue_timer.start(100)

    def check_queue(self):
        """Revisa la cola de comunicación en busca de cambios de estado."""
        if self.comm_queue and not self.comm_queue.empty():
            message = self.comm_queue.get()
            if "state" in message:
                self.state = message["state"]
                print(f"GUI: Cambiando a estado -> {self.state}")

    def update_animation(self):
        """Actualiza los parámetros de la animación en cada frame."""
        self.rotation_angle = (self.rotation_angle + 1) % 360
        if self.state == "listening":
            self.pulse_value += 0.05 * self.pulse_direction
            if self.pulse_value > 1 or self.pulse_value < 0:
                self.pulse_direction *= -1
        else:
             self.pulse_value = 0
        self.update() # Vuelve a llamar a paintEvent para redibujar

    def paintEvent(self, event):
        """Método principal de dibujado, se llama en cada frame."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        base_color = QColor(0, 150, 255, 200)
        center = QPoint(self.width() // 2, self.height() // 2)
        radius = min(self.width(), self.height()) // 3
        
        painter.translate(center)
        painter.rotate(self.rotation_angle)

        if self.state == "idle":
            painter.setPen(QPen(QColor(0, 150, 255, 100), 2))
            painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        elif self.state == "listening":
            pulse_radius = radius + (10 * self.pulse_value)
            pulse_alpha = 150 - (100 * self.pulse_value)
            painter.setPen(QPen(QColor(0, 200, 255, int(pulse_alpha)), 3))
            painter.drawEllipse(-int(pulse_radius), -int(pulse_radius), int(pulse_radius) * 2, int(pulse_radius) * 2)
        elif self.state == "processing":
            painter.setPen(QPen(base_color, 4))
            rect = QRectF(-radius, -radius, radius * 2, radius * 2)
            start_angle = (self.rotation_angle * 3) % 360
            painter.drawArc(rect, start_angle * 16, 90 * 16)
            painter.drawArc(rect, (start_angle + 180) * 16, 90 * 16)
        elif self.state == "speaking":
            painter.setPen(QPen(base_color, 2))
            for i in range(3):
                wave_radius = radius + (i * 15) + (math.sin(self.rotation_angle / 20 + i) * 5)
                wave_alpha = 150 - (i * 40)
                painter.setPen(QPen(QColor(0, 150, 255, wave_alpha), 2))
                painter.drawEllipse(-int(wave_radius), -int(wave_radius), int(wave_radius) * 2, int(wave_radius) * 2)