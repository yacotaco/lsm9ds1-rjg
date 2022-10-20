import sys
import os
import time
import pandas as pd
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lsm9ds1_rjg import Driver, I2CTransport, SPITransport

class SimpleExample:
    """This example shows how to poll the sensor for new data.
    It queries the sensor to discover when the accelerometer/gyro
    has new data and then reads all the sensors."""

    def __init__(self):
        # self.driver = self._create_spi_driver()
        self.driver = self._create_i2c_driver()
        self.driver.configure()
        self.data = pd.DataFrame(columns=['temp', 'acc_x', 'acc_y', 'acc_z',
                                          'gyro_x', 'gyro_y', 'gyro_z', 'mag_x',
                                          'mag_y', 'mag_z', 'time'])

    @staticmethod
    def _create_i2c_driver() -> Driver:
        return Driver(
            I2CTransport(1, I2CTransport.I2C_AG_ADDRESS),
            I2CTransport(1, I2CTransport.I2C_MAG_ADDRESS))

    @staticmethod
    def _create_spi_driver() -> Driver:
        return Driver(
            SPITransport(0, False),
            SPITransport(1, True))

    def main(self):
        try:
            count = 0
            while count < 1000:
                ag_data_ready = self.driver.read_ag_status().accelerometer_data_available
                if ag_data_ready:
                    self.write_data()
                    count += 1
                else:
                    time.sleep(0.00001)
        finally:
            self.driver.close()
            self.save_data_to_csv()

    def read_ag(self):
        temp, acc, gyro = self.driver.read_ag_data()
        print('Temp:{} Acc:{} Gryo:{}'.format(temp, acc, gyro))

    def read_magnetometer(self):
        mag = self.driver.read_magnetometer()
        print('Mag {}'.format(mag))

    def write_data(self):
        temp, acc, gyro = self.driver.read_ag_data()
        mag = self.driver.read_magnetometer()
        time = datetime.datetime.now()
        self.data = self.data.append({'temp': temp, 'acc_x': acc[0], 'acc_y': acc[1], 'acc_z': acc[2],
                                      'gyro_x': gyro[0], 'gyro_y': gyro[1], 'gyro_z': gyro[2],
                                      'mag_x': mag[0], 'mag_y': mag[1], 'mag_z': mag[2],
                                      'time': time}, ignore_index=True)

    def save_data_to_csv(self):
        self.data.to_csv("data.csv")


if __name__ == '__main__':
    SimpleExample().main()
