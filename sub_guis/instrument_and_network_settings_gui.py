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
from sub_guis import scrollable_frame


class InstrumentNetworkSettingsGui(tk.Toplevel):
    """
    A subclass of tkinter's Toplevel class to build a GUI for the instrument, network, section and preroll
    settings. The instrument selector will define which instrument, and therefore which cells are given
    to the player. The network options determine whether the cells will be distributed automatically via a
    TCP-IP server and client or set manually by the players. The preroll option determines how long players
    have to get ready before the section timer starts. The section selection determines which section
    of the piece players want to start at for rehearsal purposes.
    """
    def __init__(self, root, color_1="light steel blue", color_2="snow", color_3="steel blue",
                 font_header="Rosewood Std Regular", font_text="Rosewood Std Regular"):
        """
        Initializes all the GUI classes and positions them in the window.
        :param root: the root GUI class in tkinter (tk.Tk())
        """
        tk.Toplevel.__init__(self)
        self.root = root
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.title('Instrument and Network Selection')

        # variable selectors
        self.instrument = tk.IntVar()
        self.local_network_or_not = tk.IntVar()
        self.preroll = tk.StringVar()
        self.image_trigger = tk.IntVar()

        # Scrollable frame
        self.scrollable_frame = scrollable_frame.ScrollableFrame(self)
        self.scrollable_frame.grid()

        # Initialize header
        self.header_frame = tk.Frame(self.scrollable_frame, bg=color_1)
        self.header_frame.grid(row=0, columnspan=3, sticky='ew')
        self.v_vcl_selector = tk.Label(self.header_frame, text="SELECT YOUR INSTRUMENT",
                                       font=(font_header, 40), pady=10, padx=10, fg=color_2, bg=color_1)
        self.v_vcl_selector.grid(row=1, columnspan=3)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)

        # Set up radio buttons for instruments
        self.instrument_buttons_frame = tk.Frame(self.scrollable_frame, bg=color_2)
        self.instrument_buttons_frame.grid(row=1, columnspan=3, sticky='ew')
        self.cello_button = tk.Radiobutton(self.instrument_buttons_frame, text="Cello", variable=self.instrument, value=1,
                                           font=(font_text, 20), pady=10, fg=color_3, bg=color_2)
        self.cello_button.grid(row=0, column=1, sticky=tk.EW)
        self.violin_button = tk.Radiobutton(self.instrument_buttons_frame, text="Violin", variable=self.instrument, value=2,
                                            font=(font_text, 20), pady=10, fg=color_3, bg=color_2)
        self.violin_button.grid(row=0, column=2, sticky=tk.EW)
        self.instrument_buttons_frame.grid_columnconfigure(0, weight=1)
        self.instrument_buttons_frame.grid_columnconfigure(3, weight=1)

        # Initialize networked or randomized selection
        self.networked_or_not_text_frame = tk.Frame(self.scrollable_frame, bg=color_1)
        self.networked_or_not_text_frame.grid(row=2, columnspan=3, sticky='ew')
        self.networked_or_not_text = tk.Label(self.networked_or_not_text_frame, text="NETWORK SETTINGS",
                                              font=(font_header, 20), pady=5, padx=10,
                                              fg=color_2, bg =color_1)
        self.networked_or_not_text.grid(row=1, columnspan=3)
        self.networked_or_not_text_frame.grid_columnconfigure(0, weight=1)
        self.networked_or_not_text_frame.grid_columnconfigure(2, weight=1)

        # Set up radio buttons for network selection
        self.network_button_frame = tk.Frame(self.scrollable_frame, bg=color_2)
        self.network_button_frame.grid(row=3, columnspan=3, sticky='ew')
        self.local_button = tk.Radiobutton(self.network_button_frame, text="Local Network", variable=self.local_network_or_not, value=1,
                                           font=(font_text, 20), pady=10, fg=color_3, bg=color_2)
        self.local_button.grid(row=0, column=1)
        self.not_local_button = tk.Radiobutton(self.network_button_frame, text="No Local Network", variable=self.local_network_or_not, value=2,
                                               font=(font_text, 20), pady=10, fg=color_3, bg=color_2)
        self.not_local_button.grid(row=0, column=2)
        self.network_button_frame.grid_columnconfigure(0, weight=1)
        self.network_button_frame.grid_columnconfigure(3, weight=1)

        # Initialize label for next image trigger selection
        self.image_trigger_selection_frame = tk.Frame(self.scrollable_frame, bg=color_1)
        self.image_trigger_selection_frame.grid(row=4, columnspan=3, sticky='ew')
        self.image_trigger_selection_label = tk.Label(self.image_trigger_selection_frame, text="TRIGGER NEXT IMAGE OPTIONS",
                                                      font=(font_header, 20), pady=5, padx=10,
                                                      fg=color_2, bg=color_1)
        self.image_trigger_selection_label.grid(row=0, column=1)
        self.image_trigger_selection_frame.grid_columnconfigure(0, weight=1)
        self.image_trigger_selection_frame.grid_columnconfigure(2, weight=1)

        # Radio buttons for image trigger selection
        self.image_trigger_button_frame = tk.Frame(self.scrollable_frame, bg=color_2)
        self.image_trigger_button_frame.grid(row=5, columnspan=3, sticky="ew")
        image_trigger_label_texts = ["Foot Pedal: ", "Space Bar: ", "Next Button: "]
        img_trig_row = 0
        for i in image_trigger_label_texts:
            label1 = tk.Label(self.image_trigger_button_frame, text=i, font=(font_text, 20),
                              pady=5, fg=color_3, bg=color_2)
            label1.grid(row=img_trig_row, column=1, sticky="w")
            button = tk.Radiobutton(self.image_trigger_button_frame, variable=self.image_trigger, value=img_trig_row+1,
                                    pady=5, fg=color_3, bg=color_2)
            button.grid(row=img_trig_row, column=2, sticky="w")
            img_trig_row += 1

        # Pre-roll option
        self.preroll_label_frame = tk.Frame(self.scrollable_frame, bg=color_1)
        self.preroll_label_frame.grid(row=6, columnspan=3, sticky='ew')
        self.preroll_label = tk.Label(self.preroll_label_frame, text="AMOUNT OF PRE-ROLL", pady=10, padx=5,
                                      font=(font_header, 20), fg=color_2,
                                      bg=color_1)
        self.preroll_label.grid(row=1, columnspan=2)
        self.preroll_entry = tk.Entry(self.preroll_label_frame, textvariable=self.preroll)
        self.preroll_entry.grid(row=1, column=2)
        self.preroll_label_frame.grid_columnconfigure(0, weight=1)
        self.preroll_label_frame.grid_columnconfigure(3, weight=1)

        # Section selection buttons
        row = 0
        self.section_selection = tk.IntVar()
        self.fill_frame = tk.Frame(self.scrollable_frame, bg=color_2)
        self.fill_frame.grid(row=7, columnspan=3, sticky='ew')
        self.section_selection_canvas = tk.Canvas(self.fill_frame, width=self.winfo_width(), height=self.winfo_height())
        self.section_selection_canvas.grid(row=0, sticky='ew')
        self.section_selection_frame = tk.Frame(self.section_selection_canvas, bg=color_2)
        self.section_selection_frame.grid(row=0, sticky="ew")

        for i in range(len(self.root.sections_manager.sections)):
            string1 = "Section {}:".format(i+1)
            string2 = "{}".format(self.root.sections_manager.sections[i+1][0])
            # print(string)
            label1 = tk.Label(self.section_selection_frame, text=string1, font=(font_text, 15),
                              pady=10, fg=color_3, bg=color_2)
            label1.grid(row=row, column=1, sticky="w")
            button = tk.Radiobutton(self.section_selection_frame, variable=self.section_selection, value=i+1,
                                    pady=10, fg=color_3, bg=color_2)
            button.grid(row=row, column=2, sticky="w")
            label2 = tk.Label(self.section_selection_frame, text=string2, font=(font_text, 15), pady=10,
                              fg=color_3, bg=color_2)
            label2.grid(row=row, column=3, sticky="w")
            row += 1

        # Submit button
        self.submit_button_frame = tk.Frame(self.scrollable_frame, bg=color_1)
        self.submit_button_frame.grid(row=8, columnspan=3, sticky='ew')
        self.submit = tk.Button(self.submit_button_frame, text="Submit", command=self.on_submit, font=(font_text, 20))
        self.submit.grid(row=1, column=1)
        self.submitpad1 = tk.Label(self.submit_button_frame, bg=color_1, pady=5)
        self.submitpad1.grid(row=0, columnspan=3)
        self.submitpad2 = tk.Label(self.submit_button_frame, bg=color_1, pady=5)
        self.submitpad2.grid(row=2, columnspan=3)
        self.submit_button_frame.grid_columnconfigure(0, weight=1)
        self.submit_button_frame.grid_columnconfigure(2, weight=1)

        # Window padding
        self.padding1 = tk.Label(self.scrollable_frame, pady=5)
        self.padding1.grid(row=row+1, columnspan=2)
        self.padding2 = tk.Label(self.scrollable_frame, padx=5)
        self.padding2.grid(rowspan=row+1, column=2)

        self.update()
        self.scrollable_frame.resize("fit_width", height=800)

    def on_submit(self):
        """
        On submit will set program variables at the root level. Checks some of the inputs to ensure that
        all options have been set prior to starting.
        :return: None
        """
        print("instrument: ", self.instrument.get())
        print("section selection: ", self.section_selection.get())
        print("Trigger Option: ", self.image_trigger.get())
        try:
            if not (int(self.preroll.get()) > 0):
                tk.Label(self, text="You must select an instrument!").grid(row=6, columnspan=2)
            else:
                self.root.preroll = int(self.preroll.get())
                self.root.section_start = self.section_selection.get()
                self.root.image_trigger = self.image_trigger.get()
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
        """
        If the instrument selected is cello, it will set root.instrument to cello and call the function that
        checks whether there is a local network or not so that the root knows which settings GUI to
        call next.
        :return: None
        """
        self.root.instrument = "cello"
        self.nol()

    def if_violin(self):
        """
        If the instrument selected is violin, it will set root.instrument to violin and call the function that
        checks whether there is a local network or not so that the root knows which settings GUI to
        call next.
        :return: None
        """
        self.root.instrument = "violin"
        self.nol()

    def nol(self):
        """
        Calls the next setting GUI from root.
        :return: None
        """
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