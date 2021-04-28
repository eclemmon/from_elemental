"""
Server Module
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
import cell_assigner
import image_data_loader


class Server:
    """
    TCP-IP Server for setting the cell paths available to each player.
    """
    def __init__(self, ip_address, cell_assigner):
        """
        Initializes the server.
        :param ip_address: Local IP of the Server.
        :param cell_assigner: A CellAssigner object.
        """
        self.cell_assigner = cell_assigner
        self.IP_ADDRESS = ip_address
        self.server_address = (ip_address, 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Starting up on {} port {}".format(*self.server_address))
        self.sock.bind(self.server_address)

    def run(self):
        """
        Selects half of the cell paths randomly, and then generates another CellAssigner for the client through the
        __sub__ call. Then waits for a connection until the client (other player) connects and passes over thee
        client's CellAssigner. Ends by closing the connection.
        :return:
        """
        self.cell_assigner.select_half_of_cells_randomly()
        other_cells = cell_assigner.CellAssigner(image_data_loader.get_image_paths()) - self.cell_assigner
        self.sock.listen()
        print("Waiting for a connection...")
        while True:
            connection, client_address = self.sock.accept()
            try:
                print("Connection from", client_address)

                while True:
                    data = connection.recv(4096).decode()
                    if data:
                        print("server received {}".format(data))
                        connection.sendall(pickle.dumps(other_cells))
                    else:
                        print("No more data")
                        break
            finally:
                connection.close()
                break

    def get_server_cell_assignments(self):
        """
        :return: CellAssigner object
        """
        return self.cell_assigner


if __name__ == "__main__":
    ca = cell_assigner.CellAssigner(image_data_loader.get_image_paths())
    server = Server('192.168.178.46', ca)
    server.run()
    print(server.get_server_cell_assignments())
