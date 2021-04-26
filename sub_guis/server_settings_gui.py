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
        self.server_label = tk.Label(self, text="Select server or client, wait for server to submit first",
                                     font=("Rosewood Std Regular", 50), pady=10, padx=10)
        self.server_label.grid(row=0, columnspan=2)
        self.padding1 = tk.Label(self, pady=5).grid(row=3, columnspan=2)
        self.server_button = tk.Radiobutton(self, text="Server", variable=self.server, value=1,
                                            font=("Rosewood Std Regular", 20), pady=10)
        self.server_button.grid(row=2, column=0)
        self.client_button = tk.Radiobutton(self, text="Client", variable=self.server, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10)
        self.client_button.grid(row=2, column=1)

        # Set up IP Address
        self.ip_label = tk.Label(self, text="Type in the server IP Address here", pady=10)
        self.ip_label.grid(row=4, column=0)
        self.ip_client_entry = tk.Entry(self, textvariable=self.server_ip)
        self.ip_client_entry.grid(row=4, column=1)

        # Create submit button
        self.submit = tk.Button(self, text="Submit", command=self.on_submit, font=("Rosewood Std Regular", 50), padx=7)
        self.submit.grid(row=5, columnspan=2)

        # Padding at bottom
        self.padding1 = tk.Label(self, pady=5).grid(row=6, columnspan=2)

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
