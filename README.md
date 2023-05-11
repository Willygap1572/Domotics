# Domotics

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
