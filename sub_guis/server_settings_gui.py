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

class ServerSettingsGUI(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self)
        self.root = root
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.title('Server Settings')
        # Initialize variables
        # self.instrument = tk.IntVar()
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
                                            font=("Rosewood Std Regular", 20), pady=10, bg="snow", fg="steel blue")
        self.server_button.grid(row=0, column=1)
        self.client_button = tk.Radiobutton(self.server_button_frame, text="Client", variable=self.server, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10, bg="snow", fg="steel blue")
        self.client_button.grid(row=0, column=2)
        self.server_button_frame.grid_columnconfigure(0, weight=1)
        self.server_button_frame.grid_columnconfigure(3, weight=1)

        # Set up IP Address
        self.ip_label_frame = tk.Frame(self, bg="light steel blue")
        self.ip_label_frame.grid(row=2, columnspan=2, sticky="ew")
        self.ip_label = tk.Label(self.ip_label_frame, text="Type in the server IP Address here",
                                 pady=10, padx=10, fg="snow", bg="light steel blue")
        self.ip_label.grid(row=0, column=1)
        self.ip_client_entry = tk.Entry(self.ip_label_frame, textvariable=self.server_ip, fg="snow", bg="light steel blue")
        self.ip_client_entry.grid(row=0, column=2)
        self.ip_label_frame.grid_columnconfigure(0, weight=1)
        self.ip_label_frame.grid_columnconfigure(3, weight=1)

        # Create submit button
        self.submit_frame = tk.Frame(self, bg="snow")
        self.submit_frame.grid(row=3, columnspan=2, sticky="ew")
        self.submit = tk.Button(self.submit_frame, text="Submit", command=self.on_submit,
                                font=("Rosewood Std Regular", 50), bg="snow", fg="steel blue")
        self.submit.grid(column=1)
        self.submit_frame.grid_columnconfigure(0, weight=1)
        self.submit_frame.grid_columnconfigure(2, weight=1)

        # Padding at bottom
        self.padding1 = tk.Label(self.submit_frame, pady=5,  bg="snow", fg="steel blue")
        self.padding1.grid(row=2)

    def on_submit(self):
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
        ca = cell_assigner.CellAssigner(image_data_loader.get_image_paths())
        s = server.Server(ip_address, ca)
        s.run()
        print(s.get_server_cell_assignments())
        return s.get_server_cell_assignments()

    def if_client(self, ip_address):
        c = client.Client(ip_address)
        cells = c.run()
        print(cells)
        return cells







if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    settings = ServerSettingsGUI(root)
    root.mainloop()
