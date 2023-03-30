import Phishing_Detection.assessment_engine.assessment as phish
import customtkinter
import threading
import tkinter
from tkinter import ttk
import pandas as pd
import concurrent.futures
import APT_Detection.assessment_engine.assessment as apt
import PrintLogger
import sys
from tkinter import filedialog
import textwrap

class APTFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="Phishing detection", **kwargs):
        super().__init__(*args, **kwargs)
        self.toplevel_window = None
        self.pcap_file = ""
        self.grid_rowconfigure(3, weight=1)

        self.fourth_frame_label = customtkinter.CTkLabel(self, text="APT traffic detection",
                                                         font=customtkinter.CTkFont(family="Arial", size=30), )
        self.fourth_frame_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="w")

        self.tabview = customtkinter.CTkTabview(self, height=100)
        self.tabview.grid(row=1, column=0, columnspan=7, padx=(20, 0), pady=0, sticky="nw")
        self.tabview.add("live scan")
        self.tabview.add("csv file")

        # Live scan tabview
        self.interface_label = customtkinter.CTkLabel(self.tabview.tab("live scan"), text="network interface",
                                                      font=customtkinter.CTkFont(family="Arial", size=15,
                                                                                 weight="bold"))
        self.interface_label.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=0, sticky="sw")

        self.interface_entry = customtkinter.CTkEntry(self.tabview.tab("live scan"),
                                                      placeholder_text="en0")
        self.interface_entry.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=0, sticky="nw")

        self.start_scan_button = customtkinter.CTkButton(master=self.tabview.tab("live scan"), fg_color="green",
                                                         hover_color="#1F9F3A",
                                                         border_width=0,
                                                         text_color=("white", "#DCE4EE"), text="Start scan",
                                                         corner_radius=8, command=self.scan_apt_event)
        self.start_scan_button.grid(row=2, column=3, padx=(20, 0), pady=0, sticky="new")

        # Pcap file tabview
        self.pcap_file_selection = customtkinter.CTkButton(master=self.tabview.tab("csv file"), fg_color="#2E6770",
                                                           border_width=0,
                                                           text_color=("white", "#DCE4EE"), text="Select file",
                                                           corner_radius=10,
                                                           command=self.choose_file)
        self.pcap_file_selection.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.label_file = customtkinter.CTkLabel(self.tabview.tab("csv file"), text="Chosen file",
                                                 font=customtkinter.CTkFont(family="Arial", size=15,
                                                                            weight="bold"))
        self.label_file.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("csv file"), fg_color="green",
                                                     hover_color="#1F9F3A",
                                                     border_width=0,
                                                     text_color=("white", "#DCE4EE"), text="Start scan",
                                                     corner_radius=8,
                                                     command=self.scan_pcap_apt_event)
        self.main_button_1.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        # Lower part of screen
        self.scrolloutput = customtkinter.CTkTextbox(self, width=550, state="disabled")
        self.scrolloutput.grid(row=3, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        self.show_result_button = customtkinter.CTkButton(self, fg_color="gray", border_width=2,
                                                          text_color=("white", "#DCE4EE"), text="Show result",
                                                          corner_radius=8, command=self.display_result, state="DISABLED")
        self.show_result_button.grid(row=3, column=7, padx=20, pady=20, sticky="s")
        self.logger = PrintLogger.PrintLogger(self.scrolloutput)
        self.flowlist=''
        self.percentage=''

    def choose_file(self):
        self.pcap_file = filedialog.askopenfilename(initialdir="/",
                                                    title="Select a csv file",
                                                    filetypes=(("comma separated file", "*.csv"),))
        # Change label contents
        self.label_file.configure(self.tabview.tab("csv file"), text="Selected file:\n" + "\n".join(textwrap.wrap(self.pcap_file, width=50)))

    def scan_pcap_apt_event(self):
        self.logger.clear()
        if not self.pcap_file:
            print("please select a file")
            return
        # Run prediction and display in seperate thread so the mainloop doesn't freeze
        detectionthread = threading.Thread(target=self.scan_apt_pcap, args=[self.pcap_file])
        detectionthread.start()
        self.main_button_1.configure(state="disabled")

    def scan_apt_event(self):
        self.logger.clear()
        interface = self.interface_entry.get()
        if not interface:
            self.interface_entry.configure(border_color="red")
            return
        else:
            self.interface_entry.configure(border_color="gray")

        # Run prediction and display in seperate thread so the mainloop doesn't freeze
        detectionthread = threading.Thread(target=self.scan_apt, args=[interface])
        detectionthread.start()
        self.main_button_1.configure(state="disabled")

    def scan_apt(self,interface):
        print("starting Apt scan")
        self.percentage,self.flowlist = apt.predict_apt(interface)
        self.show_result_button.configure(state="normal", fg_color="green")
        self.main_button_1.configure(state="normal")

    def scan_apt_pcap(self,pcap_file):
        print("starting Apt scan using pcap csv file")
        self.percentage,self.flowlist = apt.predict_apt_file(pcap_file)
        self.show_result_button.configure(state="normal", fg_color="green")
        self.main_button_1.configure(state="normal")
        print("Finished prediction")

    def setlog(self):
        sys.stdout = self.logger

    def display_result(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.focus()
            # create window if its None or destroyed
        else:
            self.toplevel_window.focus()
        table_label = customtkinter.CTkLabel(self.toplevel_window, text="Detected APTs:",
                                             font=customtkinter.CTkFont(family="Arial", size=15,
                                                                        weight="bold"))
        table_label.grid(row=0, column=0, padx=20, pady=0, sticky="sw")
        self.toplevel_window.cols = ['Source Ip','Destination Ip','Source Port', 'Destination Port']
        self.toplevel_window.tree = ttk.Treeview(self.toplevel_window)
        self.sb = customtkinter.CTkScrollbar(self.toplevel_window)
        self.sb.grid(row=1, column=3,pady=10 ,sticky="ns")
        self.toplevel_window.tree.config(yscrollcommand=self.sb.set)
        self.sb.configure(command=self.toplevel_window.tree.yview)
        self.toplevel_window.tree.grid(row=1, column=0,rowspan=2, columnspan=3, padx=(20,0), pady=(0, 20))
        self.toplevel_window.tree["columns"] = self.toplevel_window.cols
        for i in self.toplevel_window.cols:
            self.toplevel_window.tree.column(i, anchor="w", minwidth=50)
            self.toplevel_window.tree.heading(i, text=i, anchor='w')

        for index, row in reversed(list(enumerate(self.flowlist))):
            self.toplevel_window.tree.insert("", 0, text=str(index+1), values=row)

        percentage_label = customtkinter.CTkLabel(self.toplevel_window, text="Percentage of APTs:",
                                            font=customtkinter.CTkFont(family="Arial", size=15,
                                                                       weight="bold"))
        percentage_label.grid(row=0, column=4, padx=20, pady=0, sticky="sw")
        percentage_box = customtkinter.CTkButton(
            self.toplevel_window, text=str(self.percentage)[:5]+"%",
            compound="top", width=100, height=100, state="disabled", fg_color="#2E6770",
            font=customtkinter.CTkFont(family="Arial", size=20,
                                       weight="bold")
        )
        percentage_box.grid(row=1, column=4, padx=20, pady=10, sticky="NSEW")


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minsize(width=970, height=550)
        self.title("APT scan result")
