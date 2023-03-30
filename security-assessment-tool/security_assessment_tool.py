import sys
sys.path.append('UI')
sys.path.append('APT_Detection')
sys.path.append('Malware_Analysis')
sys.path.append('Phishing_Detection')
import UI.main_window as mw


if __name__ == '__main__':
    app = mw.App()
    app.mainloop()