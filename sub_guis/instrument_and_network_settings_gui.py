"""
Instrument and Network Settings GUI Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"

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
        self.preroll = tk.StringVar()

        # Initialize header
        self.header_frame = tk.Frame(self, bg="light steel blue")
        self.header_frame.grid(row=0, columnspan=3, sticky='ew')
        self.v_vcl_selector = tk.Label(self.header_frame, text="SELECT YOUR INSTRUMENT",
                                       font=("Rosewood Std Regular", 50), pady=10, padx=10, fg="snow", bg="light steel blue")
        self.v_vcl_selector.grid(row=0, columnspan=3)

        # Set up radio buttons
        self.instrument_buttons_frame = tk.Frame(self, bg="snow")
        self.instrument_buttons_frame.grid(row=1, columnspan=3, sticky='ew')
        self.cello_button = tk.Radiobutton(self.instrument_buttons_frame, text="Cello", variable=self.instrument, value=1,
                                           font=("Rosewood Std Regular", 20), pady=10, fg="steel blue", bg="snow")
        self.cello_button.grid(row=0, column=1, sticky=tk.EW)
        self.violin_button = tk.Radiobutton(self.instrument_buttons_frame, text="Violin", variable=self.instrument, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10, fg="steel blue", bg="snow")
        self.violin_button.grid(row=0, column=2, sticky=tk.EW)
        self.instrument_buttons_frame.grid_columnconfigure(0, weight=1)
        self.instrument_buttons_frame.grid_columnconfigure(3, weight=1)

        # Initialize networked or randomized selection
        self.networked_or_not_text_frame = tk.Frame(self, bg="light steel blue")
        self.networked_or_not_text_frame.grid(row=2, columnspan=3, sticky='ew')
        self.networked_or_not_text = tk.Label(self.networked_or_not_text_frame, text="NETWORK SETTINGS",
                                            font=("Rosewood Std Regular", 50), pady=10, padx=10,
                                            fg="snow", bg ="light steel blue")
        self.networked_or_not_text.grid(row=1, columnspan=3)
        self.networked_or_not_text_frame.grid_columnconfigure(0, weight=1)
        self.networked_or_not_text_frame.grid_columnconfigure(2, weight=1)

        # Set up radio buttons
        self.network_button_frame = tk.Frame(self, bg="snow")
        self.network_button_frame.grid(row=3, columnspan=3, sticky='ew')
        self.local_button = tk.Radiobutton(self.network_button_frame, text="Local Network", variable=self.local_network_or_not, value=1,
                                           font=("Rosewood Std Regular", 20), pady=10, fg="steel blue", bg="snow")
        self.local_button.grid(row=0, column=1)
        self.not_local_button = tk.Radiobutton(self.network_button_frame, text="No Local Network", variable=self.local_network_or_not, value=2,
                                            font=("Rosewood Std Regular", 20), pady=10, fg="steel blue", bg="snow")
        self.not_local_button.grid(row=0, column=2)
        self.network_button_frame.grid_columnconfigure(0, weight=1)
        self.network_button_frame.grid_columnconfigure(3, weight=1)

        # Pre-roll option
        self.preroll_label_frame = tk.Frame(self, bg="light steel blue")
        self.preroll_label_frame.grid(row=4, columnspan=3, sticky='ew')
        self.preroll_label = tk.Label(self.preroll_label_frame, text="AMOUNT OF PRE-ROLL", pady=10, padx=5,
                                      font=("Rosewood Std Regular", 25), fg="snow",
                                      bg="light steel blue")
        self.preroll_label.grid(row=1, columnspan=2)
        self.preroll_entry = tk.Entry(self.preroll_label_frame, textvariable=self.preroll)
        self.preroll_entry.grid(row=1, column=2)
        self.preroll_label_frame.grid_columnconfigure(0, weight=1)
        self.preroll_label_frame.grid_columnconfigure(3, weight=1)

        # Section selection buttons
        row = 0
        self.section_selection = tk.IntVar()
        self.fill_frame = tk.Frame(self, bg="snow")
        self.fill_frame.grid(row=5, columnspan=3, sticky='ew')
        self.section_selection_canvas = tk.Canvas(self.fill_frame, width=self.winfo_width(), height=self.winfo_height())
        self.section_selection_canvas.grid(row=0, sticky='ew')
        self.section_selection_frame = tk.Frame(self.section_selection_canvas, bg="snow")
        self.section_selection_frame.grid(row=0, sticky="ew")

        for i in range(len(self.root.sections_manager.sections)):
            string1 = "Section {}:".format(i+1)
            string2 = "{}".format(self.root.sections_manager.sections[i+1][0])
            # print(string)
            label1 = tk.Label(self.section_selection_frame, text=string1, font=("Rosewood Std Regular", 20),
                              pady=10, fg="steel blue", bg="snow")
            label1.grid(row=row, column=1, sticky="w")
            button = tk.Radiobutton(self.section_selection_frame, variable=self.section_selection, value=i+1,
                                    pady=10, fg="steel blue", bg="snow")
            button.grid(row=row, column=2, sticky="w")
            label2 = tk.Label(self.section_selection_frame, text=string2, font=("Rosewood Std Regular", 20), pady=10,
                              fg="steel blue", bg="snow")
            label2.grid(row=row, column=3, sticky="w")
            row += 1

        # Submit button
        self.submit_button_frame = tk.Frame(self, bg="light steel blue")
        self.submit_button_frame.grid(row=6, columnspan=3, sticky='ew')
        self.submit = tk.Button(self.submit_button_frame, text="Submit", command=self.on_submit, font=("Rosewood Std Regular", 50))
        self.submit.grid(row=1, column=1)
        self.submitpad1 = tk.Label(self.submit_button_frame, bg="light steel blue", pady=5)
        self.submitpad1.grid(row=0, columnspan=3)
        self.submitpad2 = tk.Label(self.submit_button_frame, bg="light steel blue", pady=5)
        self.submitpad2.grid(row=2, columnspan=3)
        self.submit_button_frame.grid_columnconfigure(0, weight=1)
        self.submit_button_frame.grid_columnconfigure(2, weight=1)

        # Window padding
        self.padding1 = tk.Label(self, pady=5)
        self.padding1.grid(row=row+1, columnspan=2)
        self.padding2 = tk.Label(self, padx=5)
        self.padding2.grid(rowspan=row+1, column=2)

    def on_submit(self):
        print("instrument: ", self.instrument.get())
        print("section selection: ", self.section_selection.get())
        try:
            if not (int(self.preroll.get()) > 0):
                tk.Label(self, text="You must select an instrument!").grid(row=6, columnspan=2)
            else:
                self.root.preroll = int(self.preroll.get())
                self.root.section_start = self.section_selection.get()
                if self.instrument.get() == 1:
                    self.if_cello()
                elif self.instrument.get() == 2:
                    self.if_violin()
                else:
                    tk.Label(self, text="You must select an instrument!").grid(row=6, columnspan=2)
        except:
            print("You need to select all the options here!")
            pass

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