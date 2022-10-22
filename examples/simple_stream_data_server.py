import sys
import os
import time
import datetime as dt
import random as r
import socket

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lsm9ds1_rjg import Driver, I2CTransport, SPITransport

class SimpleStreamServer:
    """Streams sensor data from RPi over localhost"""
    """This example shows how to poll the sensor for new data.
    It queries the sensor to discover when the accelerometer/gyro
    has new data and then reads all the sensors."""

    def __init__(self):
        # self.driver = self._create_spi_driver()
        self.driver = self._create_i2c_driver()
        self.driver.configure()
        self.data = {}
        self.s = socket.socket()
        self.port = 8888
        self.init_socket()

    def init_socket(self):
        try:
            self.s.bind(('192.168.5.103',int(self.port)))
        except Exception as Error:
            print(Error)

        self.s.listen(5)
        print("init socket")

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
            c, addr = self.s.accept()
            print("connection from {0}".format(addr))
            while True:
            # while count < 100:
                ag_data_ready = self.driver.read_ag_status().accelerometer_data_available
                if ag_data_ready:
                    try:
                        # self.generate_dummy_data()
                        # self.print_data()
                        self.read_data()
                        self.stream_data(c)
                    except:
                        self.init_socket()
                        self.stream_data(c)
                    count += 1
                else:
                    time.sleep(0.00001)
        finally:
            self.driver.close()
            c.close()

    def stream_data(self, c):
        c.send(str(self.data).encode())

    def read_data(self):
        temp, acc, gyro = self.driver.read_ag_data()
        mag = self.driver.read_magnetometer()
        t = dt.datetime.now()
        self.data = {'temp': temp, 'acc_x': acc[0], 'acc_y': acc[1], 'acc_z': acc[2],
                     'gyro_x': gyro[0], 'gyro_y': gyro[1], 'gyro_z': gyro[2],
                     'mag_x': mag[0], 'mag_y': mag[1], 'mag_z': mag[2],
                                      'time': t}

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
    SimpleStreamServer().main()
