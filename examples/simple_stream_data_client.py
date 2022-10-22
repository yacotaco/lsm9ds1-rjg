"""Reads data stream from RPi (IMU, camera)"""
import socket            

class SimpleStreamClient:
    def __init__(self):
        self.data = {}
        self.s = socket.socket()
        self.port = 8888
        
    def connect(self):
        self.s.connect(('127.0.0.1', self.port))

    def read_data(self):
        print(self.s.recv(1024).decode())

    def close_connection(self):
        self.s.close()   
    
    def main(self):
        self.connect()

        while True:
            self.read_data()
              
        self.close_connection()

if __name__ == '__main__':
    SimpleStreamClient().main()
