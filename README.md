<br />
<div align="center">
<img src="images/logo.png" alt="" height="150">
<h3 align="center">The Lab project 2023 - Security assessment tool</h3>
</div>

<p>Authors:</p>
<ul>
    <li>Walid Loutfi</li>
    <li>Jonas Hendrix</li>
    <li>Lars de Loenen</li>
</ul>

<!-- ABOUT THE PROJECT -->

## About this project
This security assessment tool is designed to assist you in identifying and evaluating possible security vulnerabilities in your system. With this tool, you can perform vulnerability scanning, advanced persistent threat detection, malware analysis, and phishing detection to ensure that your system is secure and protected against potential security breaches. By utilizing the advanced features of this tool, you can proactively identify security weaknesses and take appropriate measures to mitigate the risks, ensuring the safety of your systems and sensitive data. We have also written an article on Medium that explains the features of this tool and how it can be used to improve your system's security. You can find the article [here](https://medium.com/@walid.loutfi/stop-cyber-threats-in-their-tracks-with-our-ai-powered-security-assessment-tool-74bb059fc66a).


### Built With
* [Python](https://docs.python.org/3/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
* Python 3.x

* pip (Python package manager)

* nmap
    * Installation on windows:
        1. Download the Nmap installer from the official website [here](https://nmap.org/download.html#windows).
        2. Run the installer and follow the on-screen instructions to install Nmap.
        3. Add the Nmap installation directory to your system's PATH environment variable:
            * Right-click on "This PC" or "My Computer" and select "Properties".
            * Click on "Advanced system settings" and then click on the "Environment Variables" button.
            * Under "System Variables", scroll down and select "Path" then click "Edit".
            * Add the path to the Nmap installation directory (e.g. C:\Program Files (x86)\Nmap) to the list of paths.
            * Click "OK" to save the changes.
            * Open a command prompt or PowerShell window and type "nmap" to verify that Nmap is installed and accessible.
        
    * Installation on linux:
        1. Open a terminal window.
        2. Run the following command to install nmap:
        ```python
        sudo apt-get install nmap
        ````
        3. Type "nmap" to verify that Nmap is installed and accessible.

* To install the required Python packages, navigate to the project directory and run the     following command:
  ```python
  pip3 install -r requirements.txt
  ```

### Installation

1. Clone the repository with the following command:
   ```console
   git clone https://github.com/walid-loutfi/security-assessment-tool.git
   ```
   
2. Navigate to the project directory "security-assessment-tool" and run the file 'security_assessment_tool.py' via an IDE or by running:
   ```python
    python3 security_assessment_tool.py
   ```

<!-- LICENSE -->
## LICENSE
This project is licensed under the MIT License - see the LICENSE file for details.