# StepperMotorSerial

Control a stepper motor with an Arduino via Serial.

## Serial commands

- `?` Get current state.

- `s` Stop the motor.

- `id` Board should reply `Stepper`

- `>>200,10,-1` Run the motor backwards for ten steps with a 200 ms time interval.

## Install

`Arduino/StepperSerial/StepperSerial.ino` should be installed on the Arduino board.

## Usage

Either use the Arduino Serial Monitor, or the `StepperControl` library.

```python
import StepperMotorSerial as SMS
stepper = SMS.Stepper()
stepper.move( N = 500, direction = -1 )
stepper.close()
```
