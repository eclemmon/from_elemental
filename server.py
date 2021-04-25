import socket
import sys


class Server:
    def __init__(self, IP_ADDRESS):
        self.IP_ADDRESS = IP_ADDRESS
        self.server_address = (IP_ADDRESS, 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Starting up on {} port {}".format(*self.server_address))
        self.sock.bind(self.server_address)

    def run(self):
        self.sock.listen(3)
        print("Waiting for a connection...")
        while True:
            connection, client_address = self.sock.accept()
            try:
                print("Connection from", client_address)

                while True:
                    data = connection.recv(4096).decode()
                    if data:
                        print("received {}".format(data))
                        connection.sendall(data.encode())
                    else:
                        print("No more data")
                        break
            finally:
                connection.close()
                break

if __name__ == "__main__":
    server = Server('192.168.178.46')
    server.run()
