"""
This project was created with the purpose to implement an equivalent of github.com/DFRobot/GravityTDS with micropython.
"""
import machine
import ujson
import time

from dftds.kvalue_repository import KValueRepository


TDS_FACTOR = 0.5

class GravityTDS:
    def __init__(self, pin=0, temperature=25.0, aref=5.0, adc_range=1024.0, k_value=1.0):
        """
        GravityTDS implements an equivalent version of the C++ module created on github.com/DFRobot/GravityTDS using micropython
            with the intent to be used on raspberry pico

        Args:
            pin: An integer number representing the analog pin
            temperature: A float number used to represent the temperature on the environment/sample being tested
            aref: A float number used to represent the amps
            adc_range: A float number that represents the analog to digital converter range. With ADC we should consider 65535
            k_value_repository: An KValueRepository implementation for storing and retrieving a constant value that will be used after calibrating the TDS sensor.
                If you have a K=10 sensor (used on seawater) please create your own repository implementation or submit a PR with the implementation for reading the EEPROM. The new implementation must  follow the KValueRepository definition.
        """
        self.pin = pin
        self.temperature = temperature
        self.aref = aref
        self.adc_range = adc_range
        self.k_value = k_value
        # by default we're assuming the sensor is K=1
        self.calibrated = False

    def begin(self):
        """
        Begin initializes build the analogic pin and load the k_values if k_value_path is provided or have any content
        """
        self.sensor = machine.ADC(self.pin)


    def update(self):
        """
        update retrieve a sample from the sensor and calculate the TDS
        """
        analog_values = []
        for i in range(0, 10):
            analog_value = self.sensor.read_u16()
            analog_values.append(analog_value)
            time.sleep(0.01)
        avg_analog_value = sum(analog_values)/len(analog_values)
        self.voltage = avg_analog_value/self.adc_range*self.aref
        ec_value = calculate_ec(self.voltage, self.k_value)
        # temperature compensation
        ec_value_25 = ec_value / (1.0+0.02*(self.temperature-25.0))
        self.tds_value = ec_value_25 * TDS_FACTOR
        return self.tds_value


    def calibrate(self, raw_ecs_solution):
        """
        calibrate the sensor by setting the new k_value based on provided raw_ecs_solution value

        Args:
            raw_ecs_solution is a float value that represents the TDS value on solution. e.g. 707 ppm
        """
        ecs_solution = (raw_ecs_solution/TDS_FACTOR) * (1.0+0.02*(self.temperature-25.0))
        k_value_temp = ecs_solution / calculate_ec(self.voltage, 1.0)
        if raw_ecs_solution > 0 and raw_ecs_solution < 2000 and k_value_temp > 0.25 and k_value_temp < 4.0:
            self.k_value = k_value_temp
            self.store_k_values()
            self.calibrated = True
            return
        print("failed to calibrate")

def calculate_ec(voltage, k_value):
    return (133.42 * voltage ** 3 - 255.86 * voltage ** 2 + 857.39 * voltage) * k_value
