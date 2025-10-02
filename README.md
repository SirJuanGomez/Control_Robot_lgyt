# Control_Robot_lgyt

Este proyecto contiene la simulación y control de un robot bípedo en Webots.

## Estructura del proyecto

- **assets/**: Piezas y modelos 3D utilizados en la simulación.
- **controllers/**: Controladores para el robot, escritos en Python.
- **libraries/**: Librerías adicionales para el proyecto.
- **meshs/**: Archivos de malla STL y metadatos de las piezas del robot.
- **plugins/**: Plugins para Webots.
- **protos/**: Archivos PROTO personalizados para el robot.
- **robot_urdf/**: Modelo URDF del robot.
- **worlds/**: Mundos de simulación de Webots.

## Uso

1. Abre el mundo `worlds/Robot_CB.wbt` en Webots.
2. Ejecuta la simulación. El controlador principal es [`RBT_CONTROLLER.py`](controllers/RBT_CONTROLLER/RBT_CONTROLLER.py).
3. El robot se moverá y mostrará los valores del IMU en la consola.

## Controladores

- [`RBT_CONTROLLER.py`](controllers/RBT_CONTROLLER/RBT_CONTROLLER.py): Controlador principal, mueve los motores y lee el IMU.
- [`RBT_C.py`](controllers/biped_controller/RBT_C.py): Ejemplo de controlador para movimientos básicos.

## Modelos

El robot está definido en [`RBT_fix.proto`](protos/RBT_fix.proto) y su geometría en [`RBT_T.urdf`](robot_urdf/RBT_T.urdf).

## Requisitos

- Webots R2025a o superior.
- Python 3.x para los controladores.

## Créditos

Desarrollado por Juan Gomez.
