"""
Server Settings GUI Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"

import tkinter as tk
import server
import client
import cell_assigner
import image_data_loader
import socket

class ServerSettingsGUI(tk.Toplevel):
    def __init__(self, root):
        """
        Server settings GUI that takes in
        :param root: Root of tkinter app, from main.py
        """
        tk.Toplevel.__init__(self)
        self.root = root
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.title('Server Settings')
        # Initialize variables
        self.server_ip = tk.StringVar()
        self.server = tk.IntVar()
        self.cell_paths = None

        # Initialize header
        self.server_label_frame = tk.Frame(self, bg="light steel blue")
        self.server_label_frame.grid(row=0, columnspan=2, sticky='ew')
        self.server_label = tk.Label(self.server_label_frame, text="Select server or client, wait for server to submit first",
                                     font=("Rosewood Std Regular", 30), fg="snow", bg="light steel blue", pady=10, padx=10)
        self.server_label.grid(row=0, columnspan=2)
        self.padding1 = tk.Label(self.server_label_frame, pady=5, fg="snow", bg="light steel blue")
        self.padding1.grid(row=1, columnspan=2)

        # Initialize server button selectors
        self.server_button_frame = tk.Frame(self, bg="snow")
        self.server_button_frame.grid(row=1, columnspan=4, sticky="ew")
        self.server_button = tk.Radiobutton(self.server_button_frame, text="Server", variable=self.server, value=1,
                                            font=("Rosewood Std Regular", 20), pady=10, bg="snow", fg="steel blue",
                                            command=self.server_selected)
        self.server_button.grid(row=0, column=1)
        self.client_button = tk.Radiobutton(self.server_button_frame, text="Client", variable=self.server, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10, bg="snow", fg="steel blue")
        self.client_button.grid(row=0, column=2)
        self.server_button_frame.grid_columnconfigure(0, weight=1)
        self.server_button_frame.grid_columnconfigure(3, weight=1)

        # Set up IP Address
        self.ip_label_frame = tk.Frame(self, bg="light steel blue")
        self.ip_label_frame.grid(row=2, columnspan=3, sticky="ew")
        self.ip_label = tk.Label(self.ip_label_frame, font=("Rosewood Std Regular", 14),
                                 text="""Type in the server's IP Address here, it will autofill the server's IP if server has been selected""",
                                 fg="snow", bg="light steel blue")
        self.ip_label.grid(row=0, column=1)
        self.ip_client_entry = tk.Entry(self.ip_label_frame, textvariable=self.server_ip,
                                        fg="snow", bg="light steel blue")
        self.ip_client_entry.grid(row=1, column=1)
        self.ip_pad_bottom = tk.Label(self.ip_label_frame, bg="light steel blue")
        self.ip_pad_bottom.grid(row=2, columnspan=3)
        self.ip_label_frame.grid_columnconfigure(0, weight=1)
        self.ip_label_frame.grid_columnconfigure(2, weight=1)

        # Create submit button
        self.submit_frame = tk.Frame(self, bg="light steel blue")
        self.submit_frame.grid(row=3, columnspan=2, sticky="ew")
        self.submit_pad_top = tk.Label(self.submit_frame, pady=5, bg="light steel blue", fg="steel blue")
        self.submit_pad_top.grid(row=0)
        self.submit = tk.Button(self.submit_frame, text="SUBMIT", command=self.on_submit,
                                font=("Rosewood Std Regular", 50), padx=10, bg="light steel blue", fg="steel blue")
        self.submit.grid(column=1, row=1)
        self.submit_frame.grid_columnconfigure(0, weight=1)
        self.submit_frame.grid_columnconfigure(2, weight=1)

        # Padding at bottom
        self.padding1 = tk.Label(self.submit_frame, pady=5,  bg="light steel blue", fg="steel blue")
        self.padding1.grid(row=2)

    def on_submit(self):
        """
        Depending on the radio button selected (self.server_button, self.client_button), it will construct
        the TCP-IP server or client. It will call if_server or if_client and gather the file paths for the
        respective instruments and save them to self.cell_paths. Then it will run the main score GUI.
        :return: None
        """
        print("Server: ", self.server.get())
        print("IP ADDRESS: ", self.server_ip.get())
        if self.server.get() == 1:
            self.cell_paths = self.if_server(self.server_ip.get())
        if self.server.get() == 2:
            self.cell_paths = self.if_client(self.server_ip.get())
        else:
            print("You must select either server or client")
        self.root.run_score_gui()

    def if_server(self, ip_address):
        """
        If the server option is selected, it will construct a TCP-IP server that will wait for a client connection.
        The server will then randomly select half the file paths to score cells and instruct the client to take
        up the remaining cells. These will be saved in the CellAssigner object.
        :param ip_address: The server's local IP Address.
        :return: Returns the server's cell assignment object.
        """
        ca = cell_assigner.CellAssigner(image_data_loader.get_image_paths())
        s = server.Server(ip_address, ca)
        s.run()
        print(s.get_server_cell_assignments())
        return s.get_server_cell_assignments()

    def if_client(self, ip_address):
        """
        If the client option is selected, it will construct a TCP-IP client that will connect to the waiting server..
        The server will then randomly select half the file paths to score cells and instruct the client to take
        up the remaining cells. These will be saved in the CellAssigner object.
        :param ip_address: The server's local IP Address
        :return: Returns a CellAssignment object generated by the server.
        """
        c = client.Client(ip_address)
        cells = c.run()
        print(cells)
        return cells

    def server_selected(self):
        """
        A helper function to automatically set the TkVar() object and the form field to the server's ip address
        when server is selected as the option.
        :return: None
        """
        localhost = socket.gethostbyname(socket.gethostname())
        self.server_ip.set(str(localhost))







if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    settings = ServerSettingsGUI(root)
    root.mainloop()
