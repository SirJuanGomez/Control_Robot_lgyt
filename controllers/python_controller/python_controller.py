from controller import Robot
import socket
import struct
import numpy as np

HOST = 'localhost'
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Esperando conexión en puerto {PORT}...")
conn, addr = server_socket.accept()
print(f"Conectado a {addr}")

robot = Robot()
time_step = int(robot.getBasicTimeStep())

# Define tus motores y sensores según tu robot
motor_names = [
    'C_PD', 'C_PI', 'P_D', 'P_I', 'R_D', 'R_I', 'F_R', 'F_L',
    'H_D', 'H_I', 'B_D', 'B_I', 'M_D', 'M_I',
    'Head'
]

# Obtener motores existentes
motors = []
valid_motor_names = []
for name in motor_names:
    motor = robot.getDevice(name)
    if motor is not None:
        motors.append(motor)
        valid_motor_names.append(name)
    else:
        print(f"Motor {name} no encontrado")

# Obtener sensores (posición) correspondientes a motores
sensors = []
for name in valid_motor_names:
    sensor_name = name + "_sensor"
    sensor = robot.getDevice(sensor_name)
    if sensor is not None:
        sensor.enable(time_step)
        sensors.append(sensor)
    else:
        sensors.append(None)  # Para mantener índices

# Habilitar IMU si tienes
imu = robot.getDevice("SensorIMU")
imu.enable(time_step)

def normalize_position(val_rad):
    # Normaliza de [-1.5708, 1.5708] a [0,1]
    return (val_rad + 1.5708) / (2 * 1.5708)

def read_sensors():
    obs = []
    for i, sensor in enumerate(sensors):
        if sensor is not None:
            val = sensor.getValue()
            obs.append(normalize_position(val))
        else:
            # Si no hay sensor, tomar la posición objetivo actual (convertida a grados)
            pos = motors[i].getTargetPosition()
            if pos is None:
                pos = 0.0
            # Convertir de radianes a grados
            motor_angle_deg = np.degrees(pos)  # Conversión a grados
            obs.append(motor_angle_deg)
    
    # Leer IMU orientación roll, pitch, yaw y normalizar de [-pi, pi] a [0, 1]
    imu_data = imu.getRollPitchYaw()
    imu_norm = [ (angle + np.pi) / (2 * np.pi) for angle in imu_data ]
    obs.extend(imu_norm)

    return obs

def send_data(conn, data):
    packed = struct.pack(f'{len(data)}f', *data)
    conn.sendall(packed)

while robot.step(time_step) != -1:
    # No recibimos ni aplicamos acción, solo enviamos sensores
    obs = read_sensors()
    send_data(conn, obs)

conn.close()
server_socket.close()
print("Servidor cerrado.")
