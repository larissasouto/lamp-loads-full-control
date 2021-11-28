from pymodbus.client.sync import ModbusTcpClient
import subprocess
import os
import signal
import time
import sys

# server connection
server_ip_address = '127.0.0.1'
server_port = 10502

client = ModbusTcpClient(server_ip_address, server_port)

print("Info : Connection : " + str(client.connect()))

UNIT = 3

control_type_mem = client.read_coils(23, 1, unit=UNIT)

# first call
if control_type_mem.bits[0]:
    p_dr = subprocess.Popen("python3 demand_response.py", shell=True, preexec_fn=os.setsid)
        
else:
    p_rtac = subprocess.Popen("python3 RTAC_control.py", shell=True, preexec_fn=os.setsid)

def main():
    global control_type_mem, p_dr, p_rtac
    
    control_type = client.read_coils(23, 1, unit=UNIT)
    control_state = client.read_coils(0, 1, unit=UNIT)

    if control_type.bits[0] != control_type_mem.bits[0]:
        if control_type.bits[0]:
            os.killpg(os.getpgid(p_rtac.pid), signal.SIGTERM)
            p_dr = subprocess.Popen("python3 demand-response.py", shell=True, preexec_fn=os.setsid)
                
        else:
            os.killpg(os.getpgid(p_dr.pid), signal.SIGTERM)
            p_rtac = subprocess.Popen("python3 lamp_loads.py", shell=True, preexec_fn=os.setsid)
        
        control_type_mem = control_type
        
    #  turn control ON/OFF
    if not control_state.bits[0]:
        print("Your control is OFF!")
        if "p_dr" in globals():
            os.killpg(os.getpgid(p_dr.pid), signal.SIGTERM)
        if "p_rtac" in globals():
            os.killpg(os.getpgid(p_rtac.pid), signal.SIGTERM)
        

def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    if "p_dr" in globals():
        os.killpg(os.getpgid(p_dr.pid), signal.SIGINT)
    if "p_rtac" in globals():
        os.killpg(os.getpgid(p_rtac.pid), signal.SIGINT)
        
    sys.exit(0)
        

while True:
    main()
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(5)
    
    

