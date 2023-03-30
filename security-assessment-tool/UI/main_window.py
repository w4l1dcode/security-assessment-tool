import customtkinter
from tkinter import PhotoImage
import os
from PIL import Image
import re
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import phishingframe
import APTframe
import networkframe
import malwareframe


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("light")
        self.title("Sentinel Shield")
        # self.maxsize(width=700, height=450)
        self.minsize(width=970, height=550)
        self.resizable(False, False)
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.phishing_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "phishing.png")),
            dark_image=Image.open(
                os.path.join(image_path, "phishing_dark.png")), size=(24, 24))

        self.vuln_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "vulnerability.png")),
                                                 dark_image=Image.open(
                                                     os.path.join(image_path, "vulnerability_dark.png")), size=(24, 24))

        self.malware_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "malware.png")),
                                                    dark_image=Image.open(
                                                        os.path.join(image_path, "malware_dark.png")), size=(24, 24))
        self.APT_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "APT.png")),
                                                dark_image=Image.open(
                                                    os.path.join(image_path, "APT_dark.png")), size=(24, 24))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "sentinel_logo.png")),
                                                 size=(135, 80))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(24, 24))
        self.icon = PhotoImage(file=str(os.path.join(image_path,"sentinel_logo.png")))
        self.after(201,lambda: self.iconbitmap(os.path.join(image_path,"sentinel_icon.ico")))
        self.help_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "help_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "help_light.png")),
                                                 size=(24, 24))

        self.help_image1 = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "help_light.png")),
                                                  size=(50, 50))
        self.phishing_image1 = customtkinter.CTkImage(
            dark_image=Image.open(
                os.path.join(image_path, "phishing_dark.png")), size=(50, 50))

        self.vuln_image1 = customtkinter.CTkImage(
            dark_image=Image.open(
                os.path.join(image_path, "vulnerability_dark.png")), size=(50, 50))

        self.malware_image1 = customtkinter.CTkImage(
            dark_image=Image.open(
                os.path.join(image_path, "malware_dark.png")), size=(50, 50))

        self.APT_image1 = customtkinter.CTkImage(
            dark_image=Image.open(
                os.path.join(image_path, "APT_dark.png")), size=(50, 50))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, width=300)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid()
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" ",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=0, pady=0)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
                                                   text="Home", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=50,
                                                      border_spacing=10, text="Vulnerability scan",
                                                      font=customtkinter.CTkFont(size=15, weight="bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.vuln_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=50,
                                                      border_spacing=10, text="APT detection",
                                                      font=customtkinter.CTkFont(size=15, weight="bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.APT_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=50,
                                                      border_spacing=10, text="Malware detection",
                                                      font=customtkinter.CTkFont(size=15, weight="bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.malware_image, anchor="w",
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=50,
                                                      border_spacing=10, text="Phishing detection",
                                                      font=customtkinter.CTkFont(size=15, weight="bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.phishing_image, anchor="w",
                                                      command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")
        self.frame_6_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=50,
                                                      border_spacing=10, text="Help page",
                                                      font=customtkinter.CTkFont(size=15, weight="bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.help_image, anchor="w",
                                                      command=self.frame_6_button_event)
        self.frame_6_button.grid(row=6, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)
        # self.home_frame.grid_rowconfigure(, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.grid_columnconfigure(2, weight=1)

        self.home_frame_label = customtkinter.CTkLabel(self.home_frame, text="Home page",
                                                       font=customtkinter.CTkFont(family="Arial", size=30), )
        self.home_frame_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="w")
        self.home_label = customtkinter.CTkLabel(self.home_frame,
                                                 text="Sentinel shield is a tool that uses AI to help network and IT personel"
                                                      " with evaluating and finding problems in their local network. \n\n"
                                                      "The vulnerability scan checks for vulnerabilities in the software"
                                                      " and hardware of a network using the CVE databases of known vulnerabilities.\n\n The APT (advanced persistent threat)"
                                                      " scan will use AI to look at captured network trafic for anamolous"
                                                      " behaviour like nmap scans or sql injection attacks.\n\n Malware analysis"
                                                      " uses AI to check if a folder contains executable files that resemble certain kinds of malware.\n\n Lastly "
                                                      "we have phishing detection that also uses AI to determine if urls found in "
                                                      "mails or in a csv file are at risk of being phishing attacks. ",
                                                 font=customtkinter.CTkFont(family="Arial", size=15, weight="bold"),
                                                 wraplength=700,justify="left",compound="left")
        self.home_label.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="nw")
        # home buttons:
        button_info = [
            ("Vulnerability scan", self.frame_2_button_event, self.vuln_image1),
            ("APT detection", self.frame_3_button_event, self.APT_image1),
            ("Malware detection", self.frame_4_button_event, self.malware_image1),
            ("Phishing detection", self.frame_5_button_event, self.phishing_image1),
            ("Help page", self.frame_6_button_event, self.help_image1)
        ]

        for i, (text, command, image) in enumerate(button_info):
            f = customtkinter.CTkFrame(self.home_frame, width=200, height=200)
            f.rowconfigure(0, weight=1)
            f.columnconfigure(0, weight=1)
            f.grid_propagate(False)
            button = customtkinter.CTkButton(
                f, text=text, image=image,
                compound="top", command=command, fg_color="#2E6770",
                font=customtkinter.CTkFont(family="Arial", size=20),
            )
            f.grid(row=i // 3 + 2, column=i % 3, padx=(10, 5), pady=10)
            button.grid(sticky="NWSE")

        # create second frame
        self.second_frame = networkframe.NetworkFrame(self, corner_radius=0, fg_color="transparent")
        # create third frame
        self.third_frame = APTframe.APTFrame(self, corner_radius=0, fg_color="transparent")
        # create fourth frame
        self.fourth_frame = malwareframe.MalwareFrame(self, corner_radius=0, fg_color="transparent")
        # create fifth frame
        self.fifth_frame = phishingframe.PhishingFrame(self, corner_radius=0, fg_color="transparent")
        # create sixth frame
        self.sixth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.sixth_frame_label = customtkinter.CTkLabel(self.sixth_frame, text="Help",
                                                        font=customtkinter.CTkFont(family="Arial", size=30), )
        self.sixth_frame_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="w")
        self.home_label = customtkinter.CTkLabel(self.sixth_frame,
                                                 text="Network scan:\nTo scan network for vulnerabilities give a host "
                                                      "ip adress in cidr notation and a range of ports to scan or leave "
                                                      "empty for full scann. once the scan is complete click on show "
                                                      "results to view the dashboard.\n\n"
                                                      "APT detection:\nTo scan for APT's you can either do a live scan "
                                                      "on an interface or switch over to csv file to upload a previous "
                                                      "CICflowmeter csv file. If you select live interface then the scan "
                                                      "will run for 30 minutes and then make a prediction.\n\n"
                                                      "Malware scan:\nTo scan for malware on your system you give the tool "
                                                      "a directory. the tool will look for executables in the directory "
                                                      "to make a prediction.\n\n"
                                                      "Phishing scan:\nTo detect phishing attacks there are two options, "
                                                      "one is collecting emails using your email-address, an app password "
                                                      "that can be generated in gmail or outlook and the inbox to scan in. "
                                                      "the second option is to give the tool a csv file that has a column "
                                                      "\'url\' with suspected phishing urls.",
                                                 font=customtkinter.CTkFont(family="Arial", size=15, weight="bold"),
                                                 wraplength=700, justify="left", compound="left")
        self.home_label.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="nw")
        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.second_frame.setlog()
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
            self.third_frame.setlog()
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
            self.fourth_frame.setlog()
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
            self.fifth_frame.setlog()
        else:
            self.fifth_frame.grid_forget()
        if name == "frame_6":
            self.sixth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sixth_frame.grid_forget()

    def home_button_event(self):
        sys.stdout = sys.__stdout__
        self.select_frame_by_name("home")
        sys.stderr = sys.__stderr__

    def frame_2_button_event(self):
        sys.stdout = sys.__stdout__
        self.select_frame_by_name("frame_2")
        sys.stderr = sys.__stderr__

    def frame_3_button_event(self):
        sys.stdout = sys.__stdout__
        self.select_frame_by_name("frame_3")
        sys.stderr = sys.__stderr__

    def frame_4_button_event(self):
        sys.stdout = sys.__stdout__
        self.select_frame_by_name("frame_4")
        sys.stderr = sys.__stderr__

    def frame_5_button_event(self):
        sys.stdout = sys.__stdout__
        self.select_frame_by_name("frame_5")
        sys.stderr = sys.__stderr__

    def frame_6_button_event(self):
        sys.stdout = sys.__stdout__
        self.select_frame_by_name("frame_6")
        sys.stderr = sys.__stderr__

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
