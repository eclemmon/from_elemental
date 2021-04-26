import tkinter as tk


class InstrumentNetworkSettingsGui(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self)
        self.root = root
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.title('Instrument and Network Selection')

        #variable selectors
        self.instrument = tk.IntVar()
        self.local_network_or_not = tk.IntVar()

        # Initialize header
        self.v_vcl_selector = tk.Label(self, text="Select your instrument",
                                       font=("Rosewood Std Regular", 50), pady=10, padx=10)
        self.v_vcl_selector.grid(row=0, columnspan=2)

        # Set up radio buttons
        self.cello_button = tk.Radiobutton(self, text="Cello", variable=self.instrument, value=1,
                                           font=("Rosewood Std Regular", 20), pady=10)
        self.cello_button.grid(row=1, column=0)
        self.violin_button = tk.Radiobutton(self, text="Violin", variable=self.instrument, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10)
        self.violin_button.grid(row=1, column=1)

        # Initialize networked or randomized selection
        self.networked_or_not_text = tk.Label(self, text="Local network or not?",
                                       font=("Rosewood Std Regular", 50), pady=10, padx=10)
        self.networked_or_not_text.grid(row=2, columnspan=2)

        # Set up radio buttons
        self.local_button = tk.Radiobutton(self, text="Local Network", variable=self.local_network_or_not, value=1,
                                           font=("Rosewood Std Regular", 20), pady=10)
        self.local_button.grid(row=3, column=0)
        self.not_local_button = tk.Radiobutton(self, text="No Local Network", variable=self.local_network_or_not, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10)
        self.not_local_button.grid(row=3, column=1)

        self.submit = tk.Button(self, text="Submit", command=self.on_submit, font=("Rosewood Std Regular", 50), padx=7)
        self.submit.grid(row=4, columnspan=2)

        self.padding1 = tk.Label(self, pady=5).grid(row=5, columnspan=2)

    def on_submit(self):
        print("instrument: ", self.instrument.get())
        if self.instrument.get() == 1:
            self.if_cello()
        elif self.instrument.get() == 2:
            self.if_violin()
        else:
            tk.Label(self, text="You must select an instrument!").grid(row=6, columnspan=2)

    def if_cello(self):
        self.root.instrument = "cello"
        self.nol()

    def if_violin(self):
        self.root.instrument = "violin"
        self.nol()

    def nol(self):
        print("Network Status: ", self.local_network_or_not.get())
        if self.local_network_or_not.get() == 1:
            self.root.get_settings_automatically_via_local_network()
        elif self.local_network_or_not.get() == 2:
            self.root.manually_set_settings()



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    insettingsgui = InstrumentNetworkSettingsGui(root)
    root.mainloop()