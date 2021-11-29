from pymodbus.client.sync import ModbusTcpClient
import gpiozero
import time
from operator import itemgetter
import numpy as np

# server connection
server_ip_address = '127.0.0.1'
server_port = 10502

client = ModbusTcpClient(server_ip_address, server_port)

print("[+]Info : Connection : " + str(client.connect()))

UNIT = 2

""" 
Rpi pin definition
PIN | GPIO
29     5
31     6
33     13
36     16
35     19
38     20
40     21
"""

relay1 = gpiozero.OutputDevice(5, initial_value=True)
relay2 = gpiozero.OutputDevice(6, initial_value=True)
relay3 = gpiozero.OutputDevice(13, initial_value=True)
relay4 = gpiozero.OutputDevice(16, initial_value=True)
relay5 = gpiozero.OutputDevice(19, initial_value=True)
relay6 = gpiozero.OutputDevice(20, initial_value=True)
relay7 = gpiozero.OutputDevice(21, initial_value=True)

# initial Loads states
status = client.read_coils(9, 15, unit=UNIT)
memCMD = [status.bits[0], status.bits[1], status.bits[2], status.bits[3],
          status.bits[4], status.bits[5], status.bits[6]]
# default priority array
Ysort = [0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125]

memYGr = [0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125]


# LOGIC FUNCTIONS
def manual_command(values):
    # Load 1 - manual CMD
    load_1_State = values.bits[0]
    if load_1_State:  # True
        relay1.off()  # load ON
    else:
        relay1.on()  # load OFF

    client.write_coil(9, load_1_State, unit=UNIT)

    # Load 2 - manual CMD
    load_2_State = values.bits[1]
    if load_2_State:  # True
        relay2.off()  # load ON
    else:
        relay2.on()  # load OFF

    client.write_coil(10, load_2_State, unit=UNIT)

    # Load 3 - manual CMD
    load_3_State = values.bits[2]
    if load_3_State:  # True
        relay3.off()  # load ON
    else:
        relay3.on()  # load OFF

    client.write_coil(11, load_3_State, unit=UNIT)

    # Load 4 - manual CMD
    load_4_State = values.bits[3]
    if load_4_State:  # True
        relay4.off()  # load ON
    else:
        relay4.on()  # load OFF

    client.write_coil(12, load_4_State, unit=UNIT)

    # Load 5 - manual CMD
    load_5_State = values.bits[4]
    if load_5_State:  # True
        relay5.off()  # load ON
    else:
        relay5.on()  # load OFF

    client.write_coil(13, load_5_State, unit=UNIT)

    # Load 6 - manual CMD
    load_6_State = values.bits[5]
    if load_6_State:  # True
        relay6.off()  # load ON
    else:
        relay6.on()  # load OFF

    client.write_coil(14, load_6_State, unit=UNIT)

    # Load 7 - manual CMD
    load_7_State = values.bits[6]
    if load_7_State:  # True
        relay7.off()  # load ON
    else:
        relay7.on()  # load OFF

    client.write_coil(15, load_7_State, unit=UNIT)


def calculate_priority(values):
    global memCMD, memYGr
    ord = [1, 2, 3, 4, 5, 6, 7]
    endCMD = [values.bits[0], values.bits[1], values.bits[2], values.bits[3],
              values.bits[4], values.bits[5], values.bits[6]]

    aux = np.array([ord, memCMD, memYGr, endCMD, memYGr])
    aux = np.transpose(aux)

    aux = sorted(aux, key=itemgetter(2), reverse=True)
    aux = sorted(aux, key=itemgetter(1))
    aux = sorted(aux, key=itemgetter(3), reverse=True)

    aux = np.transpose(aux)

    for i in range(0, 6):
        aux[4:i] = Ysort

    aux = np.transpose(aux)

    aux = sorted(aux, key=itemgetter(0))
    aux = np.transpose(aux)

    YGr = aux[4]
    print(YGr)
    
    client.write_register(1, int(YGr[0]*1000), unit=UNIT)
    client.write_register(2, int(YGr[1]*1000), unit=UNIT)
    client.write_register(3, int(YGr[2]*1000), unit=UNIT)
    client.write_register(4, int(YGr[3]*1000), unit=UNIT)
    client.write_register(5, int(YGr[4]*1000), unit=UNIT)
    client.write_register(6, int(YGr[5]*1000), unit=UNIT)
    client.write_register(7, int(YGr[6]*1000), unit=UNIT)

    memCMD = endCMD
    memYGr = YGr

    time.sleep(10)
    return YGr


def pset_mode(value, ranking):
    print("PSET CONTROL MODE")
    pset_power = value.registers[0]

    state = client.read_coils(9, 16, unit=UNIT)

    # each load group has 828 Watts
    actual_state = [state.bits[0], state.bits[1], state.bits[2], state.bits[3],
                    state.bits[4], state.bits[5], state.bits[6]]
    power_consumption = actual_state.count(True) * 828
    print(actual_state)

    base_value = 0.125
    aux = 0

    while pset_power < power_consumption:
        _ranking = np.where(ranking == base_value + aux)
        minor_priority = _ranking[0]

        if actual_state[minor_priority[0]]:
            load_manual_coil = minor_priority[0] + 16
            print("switch: ", minor_priority[0] + 1)
            load_state_coil = minor_priority[0] + 9

            relay = "relay" + str(minor_priority[0] + 1)
            if relay == "relay1":
                relay1.on()  # load OFF
            if relay == "relay2":
                relay2.on()  # load OFF
            if relay == "relay3":
                relay3.on()  # load OFF
            if relay == "relay4":
                relay4.on()  # load OFF
            if relay == "relay5":
                relay5.on()  # load OFF
            if relay == "relay6":
                relay6.on()  # load OFF
            if relay == "relay7":
                relay7.on()  # load OFF

            client.write_coil(load_state_coil, 0, unit=UNIT)
            client.write_coil(load_manual_coil, 0, unit=UNIT)
            time.sleep(10)

            # each load group has 828 Watts
            state = client.read_coils(9, 16, unit=UNIT)
            actual_state = [state.bits[0], state.bits[1], state.bits[2], state.bits[3],
                            state.bits[4], state.bits[5], state.bits[6]]
            power_consumption = actual_state.count(True) * 828
            print("power consumption: ", power_consumption)

        else:
            aux += base_value


def getValues():
    # manual commands
    manual = client.read_coils(16, 22, unit=UNIT)

    manual_command(manual)
    ranking = calculate_priority(manual)

    power_value = client.read_holding_registers(0, 1, unit=UNIT)

    pset_mode(power_value, ranking)

    time.sleep(5)  # wait 5 seconds


while True:
    getValues()
