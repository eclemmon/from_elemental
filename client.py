import socket
import pickle
import time

class Client:
    def __init__(self, IP_ADDRESS):
        print("booting")
        self.server_address = (IP_ADDRESS, 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connecting to {} port {}".format(*self.server_address))

    def run(self):
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

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while True:
                data = pickle.loads(self.sock.recv(4096))
                # print('client received "{}"'.format(data))
                if data:
                    break
        finally:
            print('closing socket')
            self.sock.close()
            return data

if __name__ == "__main__":
    client = Client('192.168.178.46')
    print(client.run())
