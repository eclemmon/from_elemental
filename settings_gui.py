import tkinter as tk

class SettingsGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Settings')
        # Initialize variables
        self.instrument = tk.IntVar()
        self.server_ip = tk.StringVar()
        self.server = tk.IntVar()

        # Initialize header
        self.v_vcl_selector = tk.Label(self, text="Select your instrument", font=("Rosewood Std Regular", 50), pady=10, padx=10)
        self.v_vcl_selector.grid(row=0, columnspan=2)

        # Set up radio buttons
        self.cello_button = tk.Radiobutton(self, text="Cello", variable=self.instrument, value=1,
                                           font=("Rosewood Std Regular", 20), pady=10)
        self.cello_button.grid(row=1, column=0)
        self.violin_button = tk.Radiobutton(self, text="Violin", variable=self.instrument, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10)
        self.violin_button.grid(row=1, column=1)
        self.padding1 = tk.Label(self, pady=5).grid(row=3, columnspan=2)
        self.server_button = tk.Radiobutton(self, text="Server", variable=self.server, value=1,
                                            font=("Rosewood Std Regular", 20), pady=10)
        self.server_button.grid(row=2, column=0)
        self.client_button = tk.Radiobutton(self, text="Client", variable=self.server, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10)
        self.client_button.grid(row=2, column=1)

        # Set up IP Address
        self.ip_label = tk.Label(self, text="Type in your IP Address here", pady=10)
        self.ip_label.grid(row=4, column=0)
        self.ip_client_entry = tk.Entry(self, textvariable=self.server_ip)
        self.ip_client_entry.grid(row=4, column=1)

        # Create submit button
        self.submit = tk.Button(self, text="Submit", command=self.on_submit, font=("Rosewood Std Regular", 50), padx=7)
        self.submit.grid(row=5, columnspan=2)

        # Padding at bottom
        self.padding1 = tk.Label(self, pady=5).grid(row=6, columnspan=2)

    def on_submit(self):
        print("instrument: ", self.instrument.get())
        print("Server: ", self.server.get())
        print("IP ADDRESS: ", self.server_ip.get())





if __name__ == "__main__":
    settings = SettingsGUI()
    settings.mainloop()
