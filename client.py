import socket

class Client:
    def __init__(self, IP_ADDRESS):
        print("booting")
        self.server_address = (IP_ADDRESS, 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connecting to {} port {}".format(*self.server_address))
        self.sock.connect(self.server_address)

    def run(self):
        try:
            # Send data
            message = 'This is the message.  It will be repeated.'
            print('sending "{}"'.format(message))
            self.sock.sendall(message.encode())

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.sock.recv(4096).decode()
                amount_received += len(data)
                print('received "{}"'.format(amount_received))

        finally:
            print('closing socket')
            self.sock.close()

if __name__ == "__main__":
    client = Client('192.168.178.46')
    client.run()
