"""Reads data stream from RPi (IMU, camera)"""
import socket
import sys          

class SimpleStreamClient:
    def __init__(self):
        self.data = {}
        self.s = socket.socket()
        self.port = 8888
        self.ip = '192.168.5.103'
        self.inputs()

    def inputs(self):
        try:
            if len(sys.argv) > 1:
                self.ip = sys.argv[1]
                self.port = sys.argv[2]
        except (ValueError, IndexError):
            print("Check input values.")
        
    def connect(self):
        self.s.connect((self.ip, self.port))

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
