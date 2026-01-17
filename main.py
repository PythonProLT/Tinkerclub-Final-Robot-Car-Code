# status: 0 = ready
# 
# 1 = busy
def Forward(Time_ms: number, Left_Speed: number, Right_Speed: number):
    global status
    wuKong.set_all_motor(Left_Speed, Right_Speed)
    basic.pause(Time_ms)
    wuKong.stop_all_motor()
    status = 0

def on_button_pressed_ab():
    global failSafeIndex, failSafeEngaged
    failSafeIndex = len(robotMovements) - 1
    while len(robotMovements) > 0:
        if robotMovements[failSafeIndex] == "FORWARD":
            Forward(250, 25, 25)
            robotMovements.pop()
            failSafeIndex += -1
        elif robotMovements[failSafeIndex] == "LEFT":
            Forward(1500, -200, 0)
            robotMovements.pop()
            failSafeIndex += -1
        elif robotMovements[failSafeIndex] == "RIGHT":
            Forward(1500, 0, -200)
            robotMovements.pop()
            failSafeIndex += -1
    failSafeEngaged = 1
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_received_string(receivedString):
    global status, failSafeEngagable, lastConfirmation
    serial.write_line(receivedString)
    if receivedString == "Forward":
        status = 1
        robotMovements.append("FORWARD")
        Forward(400, -25, -25)
    elif receivedString == "Left":
        status = 1
        robotMovements.append("LEFT")
        Forward(660, 140, 0)
    elif receivedString == "Right":
        status = 1
        robotMovements.append("RIGHT")
        Forward(648, 0, 140)
    elif receivedString == "Fail Safe Unengagable":
        failSafeEngagable = 0
    elif receivedString == "Fail Safe Engagable":
        failSafeEngagable = 1
    elif receivedString == "Here?":
        lastConfirmation = input.running_time()
radio.on_received_string(on_received_string)

failSafeEngagable = 0
failSafeIndex = 0
robotMovements: List[str] = []
failSafeEngaged = 0
lastConfirmation = 0
status = 0
radio.set_group(1)
status = 0
lastConfirmation = input.running_time()
failSafeEngaged = 0
robotMovements = ["START"]

def on_forever():
    global failSafeIndex, failSafeEngaged
    if input.running_time() - lastConfirmation > 5000 and failSafeEngaged == 0 and failSafeEngagable == 1:
        failSafeIndex = len(robotMovements) - 1
        while len(robotMovements) > 0:
            if robotMovements[failSafeIndex] == "FORWARD":
                Forward(400, 25, 25)
                robotMovements.pop()
                failSafeIndex += -1
            elif robotMovements[failSafeIndex] == "LEFT":
                Forward(660, -140, 0)
                robotMovements.pop()
                failSafeIndex += -1
            elif robotMovements[failSafeIndex] == "RIGHT":
                Forward(648, 0, -140)
                robotMovements.pop()
                failSafeIndex += -1
        failSafeEngaged = 1
basic.forever(on_forever)

def on_forever2():
    if status == 0:
        radio.send_string("Ready")
        serial.write_line("Sent: Ready")
        basic.pause(1000)
    else:
        radio.send_string("Busy")
        serial.write_line("Sent: Busy")
        basic.pause(1000)
basic.forever(on_forever2)
