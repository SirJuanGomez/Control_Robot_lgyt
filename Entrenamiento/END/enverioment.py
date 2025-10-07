import math
import numpy as np

class MATH:
    @staticmethod
    def normalize_angle(angle):
        """Normaliza un ángulo al rango [-pi, pi]."""
        return (angle + math.pi) % (2 * math.pi) - math.pi

    @staticmethod
    def matrix_kinematic(a, theta, alpha):
        """Calcula la matriz cinemática para un robot con parámetros a, theta, alpha."""
        mh = np.array([
            [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
            [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), 0],
            [0, 0, 0, 1]
        ])
        return mh


class RobotEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        """Inicializa el estado del robot."""
        self.state = np.array([0, 0, 0, 0])  # [x, y, theta, velocidad angular]

    def step(self, action):
        """Simula el paso del robot en el entorno."""
        linear_velocity = action[0]  # Velocidad lineal
        angular_velocity = action[1]  # Velocidad angular
        
        delta_t = 1  # Supongamos que cada paso es 1 segundo
        
        # Calculamos el movimiento utilizando cinemática simple
        delta_x = linear_velocity * np.cos(self.state[2]) * delta_t
        delta_y = linear_velocity * np.sin(self.state[2]) * delta_t
        delta_theta = angular_velocity * delta_t
        
        # Actualizamos el estado
        self.state[0] += delta_x
        self.state[1] += delta_y
        self.state[2] = MATH.normalize_angle(self.state[2] + delta_theta)  # Normalizamos el ángulo
        
        # Verificamos si el robot se ha caído
        if abs(self.state[2]) > math.pi / 2:  # Si el ángulo supera 90 grados, el robot se ha caído
            reward = -10  # Penalización por caída
            self.reset()  # Reiniciamos el robot
        else:
            reward = -abs(linear_velocity) - abs(angular_velocity)  # Penalizamos por mover rápidamente (ajustable)
        
        done = False
        return self.state, reward, done, {}

    def check_fall(self):
        """Verifica si el robot está en una posición caída."""
        return abs(self.state[2]) > math.pi / 2
