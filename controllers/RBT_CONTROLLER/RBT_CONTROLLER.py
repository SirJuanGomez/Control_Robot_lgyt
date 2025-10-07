from controller import Robot

# Conectar con Webots
robot = Robot(Robot_Bipedo)

# Configuración del tiempo de simulación
time_step = int(robot.getBasicTimeStep())  # Tiempo por paso de simulación

# Obtener los actuadores, sensores, etc.
motor1 = robot.getMotor('motor1')  # Usa el nombre de tu motor en Webots
motor2 = robot.getMotor('motor2')
# (Reemplaza con los motores o actuadores reales que tenga tu robot)

# Configurar los motores en modo de velocidad
motor1.setPosition(float('inf'))  # Modo velocidad
motor2.setPosition(float('inf'))

# Lógica de control simple, por ejemplo, mantener la velocidad de los motores
while robot.step(time_step) != -1:
    motor1.setVelocity(1.0)  # Establece velocidad (ejemplo)
    motor2.setVelocity(1.0)
