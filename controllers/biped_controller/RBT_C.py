from controller import Robot

# Crear instancia del robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Lista de motores según tu PROTO
motor_names = ["C_PD", "P_D_1", "R_D", "F_R"]
motors = {}

# Inicializar motores
for name in motor_names:
    motor = robot.getDevice(name)
    motor.setPosition(0.0)   # posición inicial en radianes
    motor.setVelocity(1.0)   # velocidad
    motors[name] = motor

# Loop principal de simulación
angle = 0.5  # ejemplo: mover a 0.5 rad
direction = 1

while robot.step(timestep) != -1:
    # Hacer un movimiento de prueba oscilante
    for name, motor in motors.items():
        motor.setPosition(angle)
    
    # Cambiar dirección para simular oscilación
    angle += 0.01 * direction
    if angle > 1.0 or angle < -1.0:
        direction *= -1
