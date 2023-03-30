import subprocess


def execute_cicflowmeter(interface):
    subprocess.call([f"cicflowmeter -i \"{interface}\" -c flows.csv"], shell=True)