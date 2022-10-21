# from lsm9ds1_rjg import Driver, I2CTransport, SPITransport
import sys
import os
import time
import datetime as dt
import random as r

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class SimpleStream:
    """Streams sensor data from RPi over localhost"""
    """This example shows how to poll the sensor for new data.
    It queries the sensor to discover when the accelerometer/gyro
    has new data and then reads all the sensors."""

    def __init__(self):
        # self.driver = self._create_spi_driver()
        # self.driver = self._create_i2c_driver()
        # self.driver.configure()
        self.data = {}

    # @staticmethod
    # def _create_i2c_driver() -> Driver:
    #     return Driver(
    #         I2CTransport(1, I2CTransport.I2C_AG_ADDRESS),
    #         I2CTransport(1, I2CTransport.I2C_MAG_ADDRESS))

    # @staticmethod
    # def _create_spi_driver() -> Driver:
    #     return Driver(
    #         SPITransport(0, False),
    #         SPITransport(1, True))

    def main(self):
        try:
            count = 0
            # while True:
            while count < 500:
                # ag_data_ready = self.driver.read_ag_status().accelerometer_data_available
                # if ag_data_ready:
                if True:
                    self.generate_dummy_data()
                    self.print_data()
                    time.sleep(0.5)
                    # self.stream_data()
                    count += 1
                else:
                    time.sleep(0.00001)
        finally:
            # self.driver.close()
            pass

    # def read_data(self):
    #     temp, acc, gyro = self.driver.read_ag_data()
    #     mag = self.driver.read_magnetometer()
    #     time = datetime.datetime.now()
    #     self.data = {'temp': temp, 'acc_x': acc[0], 'acc_y': acc[1], 'acc_z': acc[2],
    #                  'gyro_x': gyro[0], 'gyro_y': gyro[1], 'gyro_z': gyro[2],
    #                  'mag_x': mag[0], 'mag_y': mag[1], 'mag_z': mag[2],
    #                                   'time': time}

    def generate_dummy_data(self):
        temp = [r.randint(80, 110)]
        acc = [1, 1, 1]
        gyro = [2, 2, 2]
        mag = [3, 3, 3]
        d_t = str(dt.datetime.now())
        self.data = {'temp': temp, 'acc_x': acc[0], 'acc_y': acc[1], 'acc_z': acc[2],
                     'gyro_x': gyro[0], 'gyro_y': gyro[1], 'gyro_z': gyro[2],
                     'mag_x': mag[0], 'mag_y': mag[1], 'mag_z': mag[2],
                                      'time': d_t}
        
    def print_data(self):
        print(self.data)


if __name__ == '__main__':
    SimpleStream().main()
