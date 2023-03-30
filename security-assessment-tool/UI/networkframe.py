import customtkinter
import threading
import re
from matplotlib.figure import Figure
import sys
import PrintLogger
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Vulnerability_Scanning.report as report
import pandas as pd
from tkinter import ttk


class NetworkFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="Phishing detection", **kwargs):

        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(3, weight=1)
        # self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        # self.grid_columnconfigure((4, 5, 6), weight=0)
        self.second_frame_label = customtkinter.CTkLabel(self, text="Vulnerability scan",
                                                         font=customtkinter.CTkFont(family="Arial", size=30))
        self.second_frame_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="w")

        self.second_frame_entry_label = customtkinter.CTkLabel(self, text="Host Ip adress",
                                                               font=customtkinter.CTkFont(family="Arial", size=15,
                                                                                          weight="bold"))
        self.second_frame_entry_label.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=0, sticky="sw")

        self.second_frame_entry1 = customtkinter.CTkEntry(self,
                                                          placeholder_text="example: 192.156.23.0/24")
        self.second_frame_entry1.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=0, sticky="nw")

        self.second_frame_entry_label = customtkinter.CTkLabel(self, text="Ports",
                                                               font=customtkinter.CTkFont(family="Arial", size=15,
                                                                                          weight="bold"))
        self.second_frame_entry_label.grid(row=1, column=2, columnspan=2, padx=(20, 0), pady=0, sticky="sw")

        self.second_frame_entry2 = customtkinter.CTkEntry(self, placeholder_text="example: 1-1024")
        self.second_frame_entry2.grid(row=2, column=2, columnspan=2, padx=(20, 0), pady=0, sticky="nw")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="green", hover_color="#1F9F3A",
                                                     border_width=0,
                                                     text_color=("white", "#DCE4EE"), text="Start scan",
                                                     corner_radius=8,
                                                     command=self.start_scan_button_event)
        self.main_button_1.grid(row=2, column=4, padx=(20, 0), pady=0, sticky="new")

        self.scrolloutput = customtkinter.CTkTextbox(self, width=550, state="disabled")
        self.scrolloutput.grid(row=3, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        self.show_result_button = customtkinter.CTkButton(self, fg_color="gray", border_width=2,
                                                          text_color=("white", "#DCE4EE"), text="Show result",
                                                          corner_radius=8, state="DISABLED")
        self.show_result_button.grid(row=3, column=7, padx=20, pady=20, sticky="s")
        self.logger = PrintLogger.PrintLogger(self.scrolloutput)
        self.toplevel_window = None

    def validate_input_scan(self, ip, ports):
        if not ip and not ports:
            print("please provide a host address and port or port range")
            return False
        if not ip and ports:
            print("please provide a host address")
            return False
        if ip and not ports:
            print("please provide a port or port range")
            return False
        ip_regex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$'
        if not re.match(ip_regex, ip):
            print("host address doesn't match")
            return False

        # Validate ports
        port_regex = r'^\d+(-\d+)?$'
        if not re.match(port_regex, ports):
            print("ports isn't valid")
            return False

        # Check port range if applicable
        if '-' in ports:
            port_range = ports.split('-')
            if int(port_range[0]) > int(port_range[1]):
                print("port range is not correct")
                return False

        return True

    def start_scan_button_event(self):
        self.logger.clear()
        ip = self.second_frame_entry1.get()
        ports = self.second_frame_entry2.get()
        # if self.validate_input_scan(ip, ports):
        print("starting scan on " + ip)
        self.main_button_1.configure(state="disabled")
        detectionthread = threading.Thread(target=self.scan_network, args=[ip])
        detectionthread.start()
        # lib.network.run_nmap_scan(ip,ports)

    def scan_network(self, ip):
        num_vulnerabilities, severity_counts, cve_ids, overall_risk_score, endpoints = report.analyze_network(
            ip)
        print("Vulnerability scan finished, click on \"show results\" to view dashboard")
        self.show_result_button.configure(state="normal", fg_color="green")
        self.show_result_button.configure(command=lambda: self.display_result(num_vulnerabilities, severity_counts, cve_ids, overall_risk_score, endpoints))
        self.main_button_1.configure(state="normal")

    def display_result(self, num_vulnerabilities, severity_counts, cve_ids, overall_risk_score, endpoints):
        dataframe = pd.read_csv("Vulnerability_Scanning/CVE_data.csv", header=0)
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.df = dataframe
            self.toplevel_window.focus()
            # create window if its None or destroyed
        else:
            self.toplevel_window.focus()
            self.toplevel_window.df = dataframe
        print("output of dataframe")
        table_label = customtkinter.CTkLabel(self.toplevel_window, text="vulnerabilities",
                                             font=customtkinter.CTkFont(family="Arial", size=15,
                                                                        weight="bold"))
        table_label.grid(row=0, column=0, padx=20, pady=0, sticky="sw")
        self.toplevel_window.cols = list(dataframe.columns)
        self.toplevel_window.tree = ttk.Treeview(self.toplevel_window)
        self.toplevel_window.tree.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 20))
        self.toplevel_window.tree["columns"] = self.toplevel_window.cols
        for i in self.toplevel_window.cols:
            self.toplevel_window.tree.column(i, anchor="w",minwidth=50)
            self.toplevel_window.tree.heading(i, text=i, anchor='w')

        for index, row in reversed(list(self.toplevel_window.df.iterrows())):
            self.toplevel_window.tree.insert("", 0, text=index, values=list(row))
        fig = Figure(figsize=(6, 4))

        # Pie chart
        labels = list(severity_counts.keys())
        values = list(severity_counts.values())
        ax1 = fig.add_subplot(121)
        ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title("Vulnerability distribution")

        hosts = list(endpoints.keys())
        endpoints_per_host = [len(endpoints[host]) for host in hosts]
        ax2 = fig.add_subplot(122)
        ax2.bar(np.arange(len(hosts)), endpoints_per_host)

        ax2.set_xticks(np.arange(len(hosts)), hosts, fontsize=6)
        ax2.set_ylabel('Number of Endpoints Tested')
        ax2.set_title('Endpoints Tested per Host')
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=self.toplevel_window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row=3, column=0,rowspan=2, columnspan=3, padx=20, pady=(0, 20), sticky="nsew")
        # pie_label = customtkinter.CTkLabel(self.toplevel_window, text="Endpoints",
        #                                    font=customtkinter.CTkFont(family="Arial", size=15,
        #                                                               weight="bold"))
        # pie_label.grid(row=2, column=1, padx=20, pady=0, sticky="sw")
        risk_label = customtkinter.CTkLabel(self.toplevel_window, text="Risk score:",
                                            font=customtkinter.CTkFont(family="Arial", size=15,
                                                                       weight="bold"))
        risk_label.grid(row=5, column=0, padx=20, pady=0, sticky="sw")

        risk_box = customtkinter.CTkButton(
            self.toplevel_window, text=str(overall_risk_score)[:3],
            compound="top", width=100, height=100, state="disabled", fg_color="#2E6770", font=customtkinter.CTkFont(family="Arial", size=20,
                                                                       weight="bold")
        )
        risk_box.grid(row=6, column=0, padx=20, pady=10, sticky="NSEW")

        table_label = customtkinter.CTkLabel(self.toplevel_window,
                                             text="Number of vulnerabilities:"
                                             , font=customtkinter.CTkFont(family="Arial", size=15,
                                                                          weight="bold"))
        table_label.grid(row=5, column=1, padx=20, pady=0, sticky="sw")

        risk_box = customtkinter.CTkButton(
            self.toplevel_window, text=str(num_vulnerabilities),
            compound="top", width=100, height=100, state="disabled", fg_color="#2E6770",font=customtkinter.CTkFont(family="Arial", size=20,
                                                                       weight="bold")
        )
        risk_box.grid(row=6, column=1, padx=20, pady=10, sticky="NSEW")

    def setlog(self):
        sys.stdout = self.logger


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataframe = None
        self.minsize(width=970, height=550)
        self.title("Vulnerability scan result")
        self.df = None
        self.grid_rowconfigure(6,weight=1)
