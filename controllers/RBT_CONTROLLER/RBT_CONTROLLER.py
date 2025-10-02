from controller import Robot

# Crear instancia del robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Lista de motores según tu PROTO
motor_names = ["C_PD", "P_D_1", "R_D", "F_R"]
imu = robot.getDevice("SensorIMU")
imu.enable(timestep)  # habilitar el IMU

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
    # Mover motores
    for name, motor in motors.items():
        motor.setPosition(angle)
    
    # Cambiar dirección para simular oscilación
    angle += 0.01 * direction
    if angle > 1.0 or angle < -1.0:
        direction *= -1
    
    # Leer valores del IMU
    imu_values = imu.getRollPitchYaw()  # devuelve roll, pitch, yaw en radianes
    print(f"IMU Roll: {imu_values[0]:.3f}, Pitch: {imu_values[1]:.3f}, Yaw: {imu_values[2]:.3f}")
