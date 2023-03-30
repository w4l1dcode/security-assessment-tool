import Phishing_Detection.assessment_engine.assessment as phish
import customtkinter
import threading
import sys
import PrintLogger
import tkinter
from tkinter import ttk
import pandas as pd
import concurrent.futures
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import textwrap

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataframe = None
        self.minsize(width=970, height=550)
        self.title("Phishing scan result")
        self.df = None


class PhishingFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="Phishing detection", **kwargs):
        super().__init__(*args, **kwargs)
        self.url_csv = ''
        self.grid_rowconfigure(3, weight=1)
        self.fifth_frame_label = customtkinter.CTkLabel(self, text="Phishing detection",
                                                        font=customtkinter.CTkFont(family="Arial", size=30), )
        self.fifth_frame_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="w")

        self.tabview = customtkinter.CTkTabview(self, height=100)
        self.tabview.grid(row=1, column=0, columnspan=7, padx=(20, 0), pady=0, sticky="nw")
        self.tabview.add("email")
        self.tabview.add("file")
        # Email tab view
        self.username_label = customtkinter.CTkLabel(self.tabview.tab("email"), text="Username",
                                                     font=customtkinter.CTkFont(family="Arial", size=15, weight="bold"))
        self.username_label.grid(row=1, column=0, columnspan=2, padx=20, pady=0, sticky="sw")

        self.username_entry = customtkinter.CTkEntry(self.tabview.tab("email"),
                                                     placeholder_text="name@gmail.com")
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=0, sticky="nw")

        self.password_label = customtkinter.CTkLabel(self.tabview.tab("email"), text="app password",
                                                     font=customtkinter.CTkFont(family="Arial", size=15, weight="bold"))
        self.password_label.grid(row=1, column=2, columnspan=2, padx=(20, 0), pady=(0, 0), sticky="sw")

        self.password_entry = customtkinter.CTkEntry(self.tabview.tab("email"), placeholder_text="diiwazblxakjnads")
        self.password_entry.grid(row=2, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.inbox_label = customtkinter.CTkLabel(self.tabview.tab("email"), text="inbox",
                                                  font=customtkinter.CTkFont(family="Arial", size=15, weight="bold"))
        self.inbox_label.grid(row=1, column=3, columnspan=2, padx=(20, 0), pady=(0, 0), sticky="sw")

        self.inbox_entry = customtkinter.CTkEntry(self.tabview.tab("email"), placeholder_text="[Gmail]/Spam")
        self.inbox_entry.grid(row=2, column=3, padx=(20, 0), pady=(0, 0), sticky="nsw")

        self.start_scan_button = customtkinter.CTkButton(master=self.tabview.tab("email"), fg_color="green",
                                                         hover_color="#1F9F3A",
                                                         border_width=0,
                                                         text_color=("white", "#DCE4EE"), text="Start scan",
                                                         corner_radius=8, command=self.scan_phishing_button_event)
        self.start_scan_button.grid(row=2, column=5, padx=(20, 0), pady=0, sticky="nsw")

        # File view
        self.chosedirbutton = customtkinter.CTkButton(master=self.tabview.tab("file"), fg_color="#2E6770",
                                                      border_width=0,
                                                      text_color=("white", "#DCE4EE"), text="Select file",
                                                      corner_radius=10,
                                                      command=self.choose_file)
        self.chosedirbutton.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.label_file = customtkinter.CTkLabel(self.tabview.tab("file"), text="Chosen file",
                                                 font=customtkinter.CTkFont(family="Arial", size=15,
                                                                            weight="bold"))
        self.label_file.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("file"), fg_color="green",
                                                     hover_color="#1F9F3A",
                                                     border_width=0,
                                                     text_color=("white", "#DCE4EE"), text="Start scan",
                                                     corner_radius=8,
                                                     command=self.scan_phishing_file_button_event)
        self.main_button_1.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        # Lower half of screen
        self.scrolloutput = customtkinter.CTkTextbox(self, width=550, state="disabled")
        self.scrolloutput.grid(row=3, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        self.show_result_button = customtkinter.CTkButton(self, fg_color="gray", border_width=2,
                                                          text_color=("white", "#DCE4EE"), text="Show result",
                                                          corner_radius=8, state="DISABLED")
        self.show_result_button.grid(row=3, column=6, padx=20, pady=20, sticky="s")
        self.logger = PrintLogger.PrintLogger(self.scrolloutput)
        self.toplevel_window = None

    def choose_file(self):
        self.url_csv = filedialog.askopenfilename(initialdir="/",
                                                  title="Select a csv file",
                                                  filetypes=(("comma seperated value", "*.csv"),))
        # Change label contents
        self.label_file.configure(self.tabview.tab("file"), text="Selected file:\n" + "\n".join(textwrap.wrap(self.url_csv, width=50)))

    def get_values(self):
        entries = [self.username_entry, self.password_entry, self.inbox_entry]
        count = 0
        for entry in entries:
            if not entry.get():
                count += 1
                print("input needed")
                entry.configure(border_color="red")
            else:
                entry.configure(border_color='')
        if count != 0:
            # return False
            result = []
            # for entry in entries:
            #     result.append(entry.get())
            return result
        else:
            result = []
            for entry in entries:
                result.append(entry.get())
            return result

    def scan_file(self, filename):
        '''
        Use CSV file with header that at least contains "url" to predict if it is a phishing url or not
        :param filename:
        :return:
        '''
        phish.predict_phishing_file(filename)
        self.show_result_button.configure(state="normal", fg_color="green")
        self.show_result_button.configure(command=self.display_result)
        self.main_button_1.configure(state="normal")

    def scan_mail(self, username='lars.de.loenen@gmail.com', password='diiwazblxakjnads', mailbox='[Gmail]/Spam'):
        phish.predict_phishing(username, password, mailbox)
        self.show_result_button.configure(state="normal", fg_color="green")
        self.show_result_button.configure(command=self.display_result)
        self.main_button_1.configure(state="normal")

    def display_result(self):
        dataframe = pd.read_csv("Phishing_detection/assessment_engine/predicted_result.csv", header=0)
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.df = dataframe
            self.toplevel_window.focus()
            # create window if its None or destroyed
        else:
            self.toplevel_window.focus()
            self.toplevel_window.df = dataframe
        print("output of dataframe")
        # Table of the output
        table_label = customtkinter.CTkLabel(self.toplevel_window, text="Prediction",
                                             font=customtkinter.CTkFont(family="Arial", size=15,
                                                                        weight="bold"))
        table_label.grid(row=0, column=0, padx=20, pady=0, sticky="sw")
        self.toplevel_window.cols = list(dataframe.columns)
        self.toplevel_window.tree = ttk.Treeview(self.toplevel_window)
        self.toplevel_window.tree.grid(row=1, column=0, columnspan=2, padx=20, pady=(0,20))
        self.toplevel_window.tree["columns"] = self.toplevel_window.cols
        for i in self.toplevel_window.cols:
            self.toplevel_window.tree.column(i, anchor="w")
            self.toplevel_window.tree.heading(i, text=i, anchor='w')

        for index, row in reversed(list(self.toplevel_window.df.iterrows())):
            self.toplevel_window.tree.insert("", 0, text=index, values=list(row))
        # Pie Chart
        pie_label = customtkinter.CTkLabel(self.toplevel_window, text="Result Distribution",
                                           font=customtkinter.CTkFont(family="Arial", size=15,
                                                                      weight="bold"))
        pie_label.grid(row=2, column=0, padx=20, pady=0, sticky="sw")
        value_counts = self.toplevel_window.df['result'].value_counts()
        labels = value_counts.index.tolist()
        sizes = value_counts.values.tolist()
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=self.toplevel_window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row=3, column=0, padx=20, pady=(0,20),sticky="nw")
        # TODO add another chart or something

    def scan_phishing_button_event(self):

        self.logger.clear()

        inputs = self.get_values()
        if not inputs:
            return

        print("Starting phishing scan")

        # Run prediction and display in seperate thread so the mainloop doesn't freeze
        detectionthread = threading.Thread(target=self.scan_mail,args=inputs)
        detectionthread.start()
        self.main_button_1.configure(state="disabled")

    def scan_phishing_file_button_event(self):
        if not self.url_csv:
            print("please select a file")
            return
        print("Starting phishing scan using file: " + self.url_csv)
        detectionthread = threading.Thread(target=self.scan_file, args=[self.url_csv])
        detectionthread.start()
        self.main_button_1.configure(state="disabled")

    def setlog(self):
        sys.stdout = self.logger
