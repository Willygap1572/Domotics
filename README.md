# Domotics
## Context
This project is part of the `Redes2` internship in Computer Engineering at the Universidad Autónoma de Madrid.

## Description
The project consists of a domotics system that simulates devices such as switches (Switch), sensors (Sensor) and a clock (Clock), managed by a controller (Controller) through defined rules (Rule). A Django-based web interface is also included to manage and visualize the state of the rules.

## Components
### Switch (dummy_switch.py)

The program [dummy_switch.py](https://github.com/Willygap1572/Domotics/blob/main/dummy_switch.py) describes the Switch class that simulates a device with two states: on and off. This device can represent, for example, a lamp or a boiler. Its main purpose is to change its state when it receives an on or off message. It also has a "toggle" function that allows it to change state automatically. In addition, a failure percentage can be specified to simulate errors.

### Sensor (dummy_sensor.py)

The program [dummy_sensor.py](https://github.com/Willygap1572/Domotics/blob/main/dummy_sensor.py) describes the Sensor class that simulates any type of sensor that returns numeric values, such as a temperature or light sensor. Maximum, minimum and incremental values can be set, which behave like a cyclic counter (returning to the minimum value when the maximum is reached). The sensor outputs values in specific steps within the set range.

### Clock (dummy_clock.py)

The program [dummy_clock.py](https://github.com/Willygap1572/Domotics/blob/main/dummy_clock.py) describes the Clock class that simulates a clock. A default start time can be specified. Basically, the clock sends messages at regular (specified) intervals with time increments.

## Django
### Models

#### Actuator
Actuators are abstract classes that group all devices together, since they share common attributes such as name and subject.

#### Switch
Represents a dummy_switch, but does not implement its full behavior. It works as a value in a table and does not fully simulate a real device.

#### Sensor
Represents a dummy_sensor, but does not implement its full behavior. It works as a value in a table and does not fully simulate a real device.

#### Clock
Represents a dummy_clock, but does not implement its full behavior. It works as a value in a table and does not fully simulate a real device.

#### Rule
Defines a rule containing a trigger, a switch, a threshold and a type. The trigger can be a sensor, a switch or a clock. The switch of the rule will be activated or deactivated according to the value of the trigger. The threshold is the limit value at which an element changes and the type is a flag that can be 1 or 0. This flag represents whether the switch is activated when the trigger is above or below the threshold.

---

### Controller
Manages all devices in the home automation system, such as switches, clocks and sensors. It receives messages and acts accordingly by applying the defined rules. Each time a message arrives from a sensor, clock or switch, the controller checks all the rules. It filters the triggers that match the device that sent the message and checks the type of rule. If applicable, it sends an on or off command to the rule switch.

## Testing

To test the service, there are several options:

- **simulate.sh**: This script simulates system operation for 17 seconds. It runs a controller, a sensor and a switch. In addition, it launches the program [rule.py](https://github.com/Willygap1572/Domotics/blob/main/rule.py) to create a rule between the sensor and the switch.

- tests/test_devices.py**: This program allows you to test the system by running the simulated devices of your choice. It displays on screen all the messages received.

- tests/test_controller.py**: This program performs specific tests to check the operation of the controller.

In addition, it is also possible to manually run the simulated devices and the driver from the command line. To do this, the Django server must be launched using the make runserver command, which will start the server at localhost:8001. Accessing that address will display a table with the status of the rules, which are updated in real time and allow you to create, edit or delete rules.

## Considerations

Here are a few things to keep in mind:

- A switch cannot activate itself. If you want to use a switch as a trigger, there must be a prior rule that triggers it.
- Running the make command will delete the database along with all migrations and create them from scratch. In addition, a superuser will be created with the username and password "alumnodb", which can be used to access the administration console.
- Data persistence is performed each time the driver receives a message, creating or modifying the data in the Django model representing the device.
- Messages contain all the information from the class sending the message in dictionary format, encoded in bytes using json.dumps(), along with an additional message. For example, for a switch to report its status, it sends:

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

- No device persists its own state individually, since MQTT is used to keep the system lightweight. For example, it makes no sense for a lamp to edit the database directly.
## Limitations

This home automation system has some limitations, such as the following:

- The status of the devices is represented as a text string. This is because all devices inherit from the Activator class, and the clock (Clock) has a state represented by a time.
- A dummy_switch cannot be launched before the controller, since it will not be registered in the database. Persistence is performed by the controller when it receives the message from the switch at startup. If the controller is not running, it will not receive the message.
- The system does not allow contradictory rules, such as "turn on when the sensor reaches 25 and turn off when the sensor reaches 25". These rules are considered outside the scope of this practice.
