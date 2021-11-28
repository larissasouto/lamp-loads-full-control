from pymodbus.client.sync import ModbusTcpClient
import gpiozero
import time

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

# initial states Load 1
prevRTAC_C1 = 0
nextRTAC_C1 = 0
prevManual_S1 = 0
nextManual_S1 = 0
prevFlipFlop_L1 = 0
nextFlipFlop_L1 = 0

# initial states Load 2
prevRTAC_C2 = 0
nextRTAC_C2 = 0
prevManual_S2 = 0
nextManual_S2 = 0
prevFlipFlop_L2 = 0
nextFlipFlop_L2 = 0

# initial states Load 3
prevRTAC_C3 = 0
nextRTAC_C3 = 0
prevManual_S3 = 0
nextManual_S3 = 0
prevFlipFlop_L3 = 0
nextFlipFlop_L3 = 0

# initial states Load 4
prevRTAC_C4 = 0
nextRTAC_C4 = 0
prevManual_S4 = 0
nextManual_S4 = 0
prevFlipFlop_L4 = 0
nextFlipFlop_L4 = 0

# initial states Load 5
prevRTAC_C5 = 0
nextRTAC_C5 = 0
prevManual_S5 = 0
nextManual_S5 = 0
prevFlipFlop_L5 = 0
nextFlipFlop_L5 = 0

# initial states Load 6
prevRTAC_C6 = 0
nextRTAC_C6 = 0
prevManual_S6 = 0
nextManual_S6 = 0
prevFlipFlop_L6 = 0
nextFlipFlop_L6 = 0

# initial states Load 7
prevRTAC_C7 = 0
nextRTAC_C7 = 0
prevManual_S7 = 0
nextManual_S7 = 0
prevFlipFlop_L7 = 0
nextFlipFlop_L7 = 0

# LOGIC FUNCTIONS
""" Pset control mode """

def pset_mode(value):
    print("PSET CONTROL MODE")
    pset_power = value.registers[0]

    if pset_power < 828:
        relay1.on() # inverted logic
        relay2.on()
        relay3.on()
        relay4.on()
        relay5.on()
        relay6.on()
        relay7.on()

        client.write_coils(9, [1] * 7, unit=UNIT)  # RTAC loads state (OFF = 1)

    if (pset_power >= 828) and (pset_power < 1656):
        relay1.off()
        relay2.on()
        relay3.on()
        relay4.on()
        relay5.on()
        relay6.on()
        relay7.on()

        client.write_coil(9, 0, unit=UNIT)  # RTAC loads state (ON = 0)
        client.write_coils(10, [1] * 6, unit=UNIT)  # RTAC loads state (OFF = 1)

    if (pset_power >= 1656) and (pset_power < 2484):
        relay1.off()
        relay2.off()
        relay3.on()
        relay4.on()
        relay5.on()
        relay6.on()
        relay7.on()

        client.write_coils(9, [0] * 2, unit=UNIT)  # RTAC loads state (ON = 0)
        client.write_coils(11, [1] * 5, unit=UNIT)  # RTAC loads state (OFF = 1)

    if (pset_power >= 2484) and (pset_power < 3312):
        print("S1 ON\nS2 ON\nS3 ON\nS4 OFF\nS5 OFF\nS6 OFF\nS7 OFF\n")
        relay1.off()
        relay2.off()
        relay3.off()
        relay4.on()
        relay5.on()
        relay6.on()
        relay7.on()

        client.write_coils(9, [0] * 3, unit=UNIT)  # RTAC loads state (ON = 0)
        client.write_coils(12, [1] * 4, unit=UNIT)  # RTAC loads state (OFF = 1)

    if (pset_power >= 3312) and (pset_power < 4140):
        relay1.off()
        relay2.off()
        relay3.off()
        relay4.off()
        relay5.on()
        relay6.on()
        relay7.on()

        client.write_coils(9, [0] * 4, unit=UNIT)  # RTAC loads state (ON = 0)
        client.write_coils(13, [1] * 3, unit=UNIT)  # RTAC loads state (OFF = 1)

    if (pset_power >= 4140) and (pset_power < 4968):
        relay1.off()
        relay2.off()
        relay3.off()
        relay4.off()
        relay5.off()
        relay6.on()
        relay7.on()

        client.write_coils(9, [0] * 5, unit=UNIT)  # RTAC loads state (ON = 0)
        client.write_coils(14, [1] * 2, unit=UNIT)  # RTAC loads state (OFF = 1)

    if (pset_power >= 4968) and (pset_power < 5796):
        relay1.off()
        relay2.off()
        relay3.off()
        relay4.off()
        relay5.off()
        relay6.off()
        relay7.on()

        client.write_coils(9, [0] * 6, unit=UNIT)  # RTAC loads state (ON = 0)
        client.write_coil(15, 1, unit=UNIT)  # RTAC loads state (OFF = 1)

    if pset_power >= 5796:
        relay1.off()
        relay2.off()
        relay3.off()
        relay4.off()
        relay5.off()
        relay6.off()
        relay7.off()

        client.write_coils(9, [0] * 7, unit=UNIT)  # RTAC loads state (ON = 0)

    print(f'S1 {relay1.value}\nS2 {relay2.value}\nS3 {relay3.value}\nS4 {relay4.value}\nS5 {relay5.value}\nS6 {relay6.value}\nS7 {relay7.value}\n')


def risingEdgeDetector(prevState, nextState):
    if prevState < nextState:
        return 1
    return 0


def fallingEdgeDetector(prevState, nextState):
    if prevState > nextState:
        return 1
    return 0


def srFlipFlop(s, r, prevFlipFlop, nextFlipFlop):
    # SR flip-flop truth table implementation
    if s == 0 and r == 0:
        nextFlipFlop = prevFlipFlop
    elif s == 0 and r == 1:
        nextFlipFlop = 0
    elif s == 1 and r == 0:
        nextFlipFlop = 1
    else:
        nextFlipFlop = prevFlipFlop

    return nextFlipFlop


def orLogic(RTAC, manual):
    if RTAC == 0 and manual == 1:
        return 1
    if RTAC == 1 and manual == 0:
        return 1
    return 0


""" RTAC control mode """


def rtac_mode(values, load):
    # initial states Load 1
    global prevRTAC_C1, nextRTAC_C1, prevManual_S1, nextManual_S1

    # initial states Load 2
    global prevRTAC_C2, nextRTAC_C2, prevManual_S2, nextManual_S2

    # initial states Load 3
    global prevRTAC_C3, nextRTAC_C3, prevManual_S3, nextManual_S3

    # initial states Load 4
    global prevRTAC_C4, nextRTAC_C4, prevManual_S4, nextManual_S4

    # initial states Load 5
    global prevRTAC_C5, nextRTAC_C5, prevManual_S5, nextManual_S5

    # initial states Load 6
    global prevRTAC_C6, nextRTAC_C6, prevManual_S6, nextManual_S6

    # initial states Load 7
    global prevRTAC_C7, nextRTAC_C7, prevManual_S7, nextManual_S7

    # manual commands
    manual = client.read_coils(16, 22, unit=UNIT)

    if load == 1:
        prevRTAC_C1 = nextRTAC_C1
        nextRTAC_C1 = values.bits[0]  # coil 2 - S1 cmd

        prevManual_S1 = nextManual_S1
        nextManual_S1 = manual.bits[0]  # coil 16 - S1 manual cmd

        risingEdgeRTAC = risingEdgeDetector(prevRTAC_C1, nextRTAC_C1)
        risingEdgeManual = risingEdgeDetector(prevManual_S1, nextManual_S1)

        fallingEdgeRTAC = fallingEdgeDetector(prevRTAC_C1, nextRTAC_C1)
        fallingEdgeManual = fallingEdgeDetector(prevManual_S1, nextManual_S1)

        # OR Logic
        s = orLogic(risingEdgeRTAC, risingEdgeManual)
        r = orLogic(fallingEdgeRTAC, fallingEdgeManual)

        global prevFlipFlop_L1, nextFlipFlop_L1
        prevFlipFlop_L1 = nextFlipFlop_L1

        loadState = srFlipFlop(s, r, prevFlipFlop_L1, nextFlipFlop_L1)
        nextFlipFlop_L1 = loadState

        if loadState == 0:
            relay1.on()  # load OFF
        else:
            relay1.off()  # load ON

        client.write_coil(9, loadState, unit=UNIT)
        return loadState

    if load == 2:
        prevRTAC_C2 = nextRTAC_C2
        nextRTAC_C2 = values.bits[1]  # coil 3 - S2 cmd

        prevManual_S2 = nextManual_S2
        nextManual_S2 = manual.bits[1]  # coil 17 - S2 manual cmd

        risingEdgeRTAC = risingEdgeDetector(prevRTAC_C2, nextRTAC_C2)
        risingEdgeManual = risingEdgeDetector(prevManual_S2, nextManual_S2)

        fallingEdgeRTAC = fallingEdgeDetector(prevRTAC_C2, nextRTAC_C2)
        fallingEdgeManual = fallingEdgeDetector(prevManual_S2, nextManual_S2)

        # OR Logic
        s = orLogic(risingEdgeRTAC, risingEdgeManual)
        r = orLogic(fallingEdgeRTAC, fallingEdgeManual)

        global prevFlipFlop_L2, nextFlipFlop_L2
        prevFlipFlop_L2 = nextFlipFlop_L2

        loadState = srFlipFlop(s, r, prevFlipFlop_L2, nextFlipFlop_L2)
        nextFlipFlop_L2 = loadState

        if loadState == 0:
            relay2.on()  # load OFF
        else:
            relay2.off()  # load ON

        client.write_coil(10, loadState, unit=UNIT)
        return loadState

    if load == 3:
        prevRTAC_C3 = nextRTAC_C3
        nextRTAC_C3 = values.bits[2]  # coil 4 - S3 cmd

        prevManual_S3 = nextManual_S3
        nextManual_S3 = manual.bits[2]  # coil 18 - S3 manual cmd

        risingEdgeRTAC = risingEdgeDetector(prevRTAC_C3, nextRTAC_C3)
        risingEdgeManual = risingEdgeDetector(prevManual_S3, nextManual_S3)

        fallingEdgeRTAC = fallingEdgeDetector(prevRTAC_C3, nextRTAC_C3)
        fallingEdgeManual = fallingEdgeDetector(prevManual_S3, nextManual_S3)

        # OR Logic
        s = orLogic(risingEdgeRTAC, risingEdgeManual)
        r = orLogic(fallingEdgeRTAC, fallingEdgeManual)

        global prevFlipFlop_L3, nextFlipFlop_L3
        prevFlipFlop_L3 = nextFlipFlop_L3

        loadState = srFlipFlop(s, r, prevFlipFlop_L3, nextFlipFlop_L3)
        nextFlipFlop_L3 = loadState

        if loadState == 0:
            relay3.on()  # load OFF
        else:
            relay3.off()  # load ON

        client.write_coil(11, loadState, unit=UNIT)
        return loadState

    if load == 4:
        prevRTAC_C4 = nextRTAC_C4
        nextRTAC_C4 = values.bits[3]  # coil 5 - S4 cmd

        prevManual_S4 = nextManual_S4
        nextManual_S4 = manual.bits[3]  # coil 19 - S4 manual cmd

        risingEdgeRTAC = risingEdgeDetector(prevRTAC_C4, nextRTAC_C4)
        risingEdgeManual = risingEdgeDetector(prevManual_S4, nextManual_S4)

        fallingEdgeRTAC = fallingEdgeDetector(prevRTAC_C4, nextRTAC_C4)
        fallingEdgeManual = fallingEdgeDetector(prevManual_S4, nextManual_S4)

        # OR Logic
        s = orLogic(risingEdgeRTAC, risingEdgeManual)
        r = orLogic(fallingEdgeRTAC, fallingEdgeManual)

        global prevFlipFlop_L4, nextFlipFlop_L4
        prevFlipFlop_L4 = nextFlipFlop_L4

        loadState = srFlipFlop(s, r, prevFlipFlop_L4, nextFlipFlop_L4)
        nextFlipFlop_L4 = loadState

        if loadState == 0:
            relay4.on()  # load OFF
        else:
            relay4.off()  # load ON

        client.write_coil(12, loadState, unit=UNIT)
        return loadState

    if load == 5:
        prevRTAC_C5 = nextRTAC_C5
        nextRTAC_C5 = values.bits[4]  # coil 6 - S5 cmd

        prevManual_S5 = nextManual_S5
        nextManual_S5 = manual.bits[4]  # coil 20 - S5 manual cmd

        risingEdgeRTAC = risingEdgeDetector(prevRTAC_C5, nextRTAC_C5)
        risingEdgeManual = risingEdgeDetector(prevManual_S5, nextManual_S5)

        fallingEdgeRTAC = fallingEdgeDetector(prevRTAC_C5, nextRTAC_C5)
        fallingEdgeManual = fallingEdgeDetector(prevManual_S5, nextManual_S5)

        # OR Logic
        s = orLogic(risingEdgeRTAC, risingEdgeManual)
        r = orLogic(fallingEdgeRTAC, fallingEdgeManual)

        global prevFlipFlop_L5, nextFlipFlop_L5
        prevFlipFlop_L5 = nextFlipFlop_L5

        loadState = srFlipFlop(s, r, prevFlipFlop_L5, nextFlipFlop_L5)
        nextFlipFlop_L5 = loadState

        if loadState == 0:
            relay5.on()  # load OFF
        else:
            relay5.off()  # load ON

        client.write_coil(13, loadState, unit=UNIT)
        return loadState

    if load == 6:
        prevRTAC_C6 = nextRTAC_C6
        nextRTAC_C6 = values.bits[5]  # coil 7 - S6 cmd

        prevManual_S6 = nextManual_S6
        nextManual_S6 = manual.bits[5]  # coil 21 - S6 manual cmd

        risingEdgeRTAC = risingEdgeDetector(prevRTAC_C6, nextRTAC_C6)
        risingEdgeManual = risingEdgeDetector(prevManual_S6, nextManual_S6)

        fallingEdgeRTAC = fallingEdgeDetector(prevRTAC_C6, nextRTAC_C6)
        fallingEdgeManual = fallingEdgeDetector(prevManual_S6, nextManual_S6)

        # OR Logic
        s = orLogic(risingEdgeRTAC, risingEdgeManual)
        r = orLogic(fallingEdgeRTAC, fallingEdgeManual)

        global prevFlipFlop_L6, nextFlipFlop_L6
        prevFlipFlop_L6 = nextFlipFlop_L6

        loadState = srFlipFlop(s, r, prevFlipFlop_L6, nextFlipFlop_L6)
        nextFlipFlop_L6 = loadState

        if loadState == 0:
            relay6.on()  # load OFF
        else:
            relay6.off()  # load ON

        client.write_coil(14, loadState, unit=UNIT)
        return loadState

    if load == 7:
        prevRTAC_C7 = nextRTAC_C7
        nextRTAC_C7 = values.bits[6]  # coil 8 - S7 cmd

        prevManual_S7 = nextManual_S7
        nextManual_S7 = manual.bits[6]  # coil 22 - S7 manual cmd

        risingEdgeRTAC = risingEdgeDetector(prevRTAC_C7, nextRTAC_C7)
        risingEdgeManual = risingEdgeDetector(prevManual_S7, nextManual_S7)

        fallingEdgeRTAC = fallingEdgeDetector(prevRTAC_C7, nextRTAC_C7)
        fallingEdgeManual = fallingEdgeDetector(prevManual_S7, nextManual_S7)

        # OR Logic
        s = orLogic(risingEdgeRTAC, risingEdgeManual)
        r = orLogic(fallingEdgeRTAC, fallingEdgeManual)

        global prevFlipFlop_L7, nextFlipFlop_L7
        prevFlipFlop_L7 = nextFlipFlop_L7

        loadState = srFlipFlop(s, r, prevFlipFlop_L7, nextFlipFlop_L7)
        nextFlipFlop_L7 = loadState

        if loadState == 0:
            relay7.on()  # load OFF
        else:
            relay7.off()  # load ON

        client.write_coil(15, loadState, unit=UNIT)
        return loadState


def getValues():
    # code here
    control_mode = client.read_coils(1, 1, unit=UNIT)

    if control_mode.bits[0] == False:
        print("RTAC CONTROL MODE")
        values = client.read_coils(2, 9, unit=UNIT)
        #  Load 1
        loadState = rtac_mode(values, 1)
        if loadState == 0:
            print("SWITCH 1: OFF")
        else:
            print("SWITCH 1 = ON")
        #  Load 2
        loadState = rtac_mode(values, 2)
        if loadState == 0:
            print("SWITCH 2: OFF")
        else:
            print("SWITCH 2 = ON")
        #  Load 3
        loadState = rtac_mode(values, 3)
        if loadState == 0:
            print("SWITCH 3: OFF")
        else:
            print("SWITCH 3 = ON")
        #  Load 4
        loadState = rtac_mode(values, 4)
        if loadState == 0:
            print("SWITCH 4: OFF")
        else:
            print("SWITCH 4 = ON")
        #  Load 5
        loadState = rtac_mode(values, 5)
        if loadState == 0:
            print("SWITCH 5: OFF")
        else:
            print("SWITCH 5 = ON")
        #  Load 6
        loadState = rtac_mode(values, 6)
        if loadState == 0:
            print("SWITCH 6: OFF")
        else:
            print("SWITCH 6 = ON")
        #  Load 7
        loadState = rtac_mode(values, 7)
        if loadState == 0:
            print("SWITCH 7: OFF")
        else:
            print("SWITCH 7 : ON")

    else:
        power_value = client.read_holding_registers(0, 1, unit=UNIT)
        pset_mode(power_value)
    time.sleep(5)  # wait 5 seconds


while True:
    getValues()