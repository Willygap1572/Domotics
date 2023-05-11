# Domotics
## Contexto
Este proyecto dorma parte de las practicas de `Redes2`de Ingeniería informática de la Universidad Autónoma de Madrid.

## Descripcion
El proyecto consiste en un sistema de domótica que simula dispositivos como interruptores (Switch), sensores (Sensor) y un reloj (Clock), gestionados por un controlador (Controller) mediante reglas (Rule) definidas. También se incluye una interfaz web basada en Django para administrar y visualizar el estado de las reglas.

## Componentes
### Switch (dummy_switch.py)

El programa [dummy_switch.py](https://github.com/Willygap1572/Domotics/blob/main/dummy_switch.py) describe la clase Switch que simula un dispositivo con dos estados: encendido y apagado. Este dispositivo puede representar, por ejemplo, una lámpara o una caldera. Su objetivo principal es cambiar su estado cuando recibe un mensaje de encendido o apagado. También cuenta con la función de "toggle" que permite cambiar de estado automáticamente. Además, se puede especificar un porcentaje de fallo para simular errores.

### Sensor (dummy_sensor.py)

El programa [dummy_sensor.py](https://github.com/Willygap1572/Domotics/blob/main/dummy_sensor.py) describe la clase Sensor que simula cualquier tipo de sensor que devuelve valores numéricos, como un sensor de temperatura o luz. Se pueden establecer valores máximos, mínimos e incrementos, que se comportan como un contador cíclico (volviendo al valor mínimo cuando se alcanza el máximo). El sensor emite valores en saltos específicos dentro del rango establecido.

### Clock (dummy_clock.py)

El programa [dummy_clock.py](https://github.com/Willygap1572/Domotics/blob/main/dummy_clock.py) describe la clase Clock que simula un reloj. Se puede especificar una hora de inicio predeterminada. Básicamente, el reloj envía mensajes en intervalos regulares (especificados) con incrementos de tiempo.

## Django
### Modelos

#### Actuator
Los actuadores son clases abstractas que agrupan a todos los dispositivos, ya que comparten atributos comunes como el nombre y el tema.

#### Switch
Representa un dummy_switch, pero no implementa su comportamiento completo. Funciona como un valor en una tabla y no simula completamente un dispositivo real.

#### Sensor
Representa un dummy_sensor, pero no implementa su comportamiento completo. Funciona como un valor en una tabla y no simula completamente un dispositivo real.

#### Clock
Representa un dummy_clock, pero no implementa su comportamiento completo. Funciona como un valor en una tabla y no simula completamente un dispositivo real.

#### Rule
Define una regla que contiene un activador, un switch, un umbral (threshold) y un tipo. El activador puede ser un sensor, un interruptor o un reloj. El interruptor de la regla se activará o desactivará según el valor del activador. El umbral es el valor límite en el que cambia un elemento y el tipo es una bandera que puede ser 1 o 0. Esta bandera representa si el interruptor se activa cuando el activador está por encima o por debajo del umbral.

---

### Controller
Gestiona todos los dispositivos del sistema de domótica, como interruptores, relojes y sensores. Recibe mensajes y actúa en consecuencia aplicando las reglas definidas. Cada vez que llega un mensaje de un sensor, un reloj o un interruptor, el controlador verifica todas las reglas. Filtra los activadores que coinciden con el dispositivo que envió el mensaje y comprueba el tipo de regla. Si corresponde, envía una orden de encendido o apagado al interruptor de la regla.

## Pruebas

Para probar el servicio, existen varias opciones:

- **simulate.sh**: Este script simula el funcionamiento del sistema durante 17 segundos. Ejecuta un controlador, un sensor y un interruptor. Además, lanza el programa [rule.py](https://github.com/Willygap1572/Domotics/blob/main/rule.py) para crear una regla entre el sensor y el interruptor.

- **tests/test_devices.py**: Este programa permite probar el sistema ejecutando los dispositivos simulados que desees. Muestra por pantalla todos los mensajes recibidos.

- **tests/test_controller.py**: Este programa realiza pruebas específicas para comprobar el funcionamiento del controlador.

Además, también es posible ejecutar manualmente los dispositivos simulados y el controlador desde la línea de comandos. Para ello, se debe lanzar el servidor de Django utilizando el comando make runserver, el cual iniciará el servidor en localhost:8001. Al acceder a esa dirección, se mostrará una tabla con el estado de las reglas, que se actualizan en tiempo real y permiten crear, editar o borrar reglas.

## Consideraciones

A continuación se presentan algunas cosas a tener en cuenta:

- Un interruptor no puede activarse a sí mismo. Si se desea utilizar un interruptor como activador, debe existir una regla previa que lo active.
- Al ejecutar el comando make, se borrará la base de datos junto con todas las migraciones y se crearán desde cero. Además, se creará un superusuario con el nombre de usuario y la contraseña "alumnodb", que se puede utilizar para acceder a la consola de administración.
- La persistencia de los datos se realiza cada vez que el controlador recibe un mensaje, creando o modificando los datos del modelo Django que representa al dispositivo.
- Los mensajes contienen toda la información de la clase que envía el mensaje en formato de diccionario, codificado en bytes mediante json.dumps(), junto con un mensaje adicional. Por ejemplo, para que un interruptor informe sobre su estado, se envía:

```python
message_dict = {
    'aid': self.aid,
    'name': self.name,
    'theme': self.theme,
    'state': self.state,
    'broker_host': self.broker_host,
    'port': self.port,
    'fail': self.fail,
    'message': message,
}
```

- Ningún dispositivo persiste su propio estado de forma individual, ya que se utiliza MQTT para mantener el sistema liviano. Por ejemplo, no tiene sentido que una lámpara edite la base de datos directamente.
## Limitaciones

Este sistema de domótica tiene algunas limitaciones, como las siguientes:

- El estado de los dispositivos se representa como una cadena de texto. Esto se debe a que todos los dispositivos heredan de la clase Activator, y el reloj (Clock) tiene un estado representado por una hora.
- Un dummy_switch no puede ser lanzado antes del controlador, ya que no quedará registrado en la base de datos. La persistencia la realiza el controlador cuando recibe el mensaje del interruptor al iniciarse. Si el controlador no está en ejecución, no recibirá el mensaje.
- El sistema no permite reglas contradictorias, como "enciéndete cuando el sensor alcance 25 y apágate cuando el sensor alcance 25". Estas reglas se consideran fuera del alcance de esta práctica.
