"""
Client Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"


import socket
import pickle
import time

class Client:
    """
    TCP-IP client class to handle assigning scored cells.
    """
    def __init__(self, IP_ADDRESS):
        """
        Initializes client
        :param IP_ADDRESS: IP Address of server.
        """
        print("booting")
        self.server_address = (IP_ADDRESS, 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connecting to {} port {}".format(*self.server_address))

    def run(self):
        """
        Seeks out server and accepts incoming CellAssigner class. Closes connection after run.
        :return: Returns CellAssigner class.
        """
        connected = False
        while not connected:
            try:
                self.sock.connect(self.server_address)
                connected = True
            except Exception as e:
                print("Waiting for server...")
                time.sleep(1)
                pass

        try:
            # Send data
            message = 'Ready.'
            print('sending "{}"'.format(message))
            self.sock.sendall(message.encode())

            while True:
                data = pickle.loads(self.sock.recv(4096))
                if data:
                    break
        finally:
            print('closing socket')
            self.sock.close()
            if data:
                return data

if __name__ == "__main__":
    client = Client('192.168.178.46')
    print(client.run())
