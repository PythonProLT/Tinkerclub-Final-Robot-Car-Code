// status: 0 = ready
// 
// 1 = busy
function Forward (Time_ms: number, Left_Speed: number, Right_Speed: number) {
    wuKong.setAllMotor(Left_Speed, Right_Speed)
    basic.pause(Time_ms)
    wuKong.stopAllMotor()
    status = 0
}
input.onButtonPressed(Button.AB, function () {
    failSafeIndex = robotMovements.length - 1
    while (robotMovements.length > 0) {
        if (robotMovements[failSafeIndex] == "FORWARD") {
            Forward(250, 25, 25)
            robotMovements.pop()
            failSafeIndex += -1
        } else if (robotMovements[failSafeIndex] == "LEFT") {
            Forward(1500, -200, 0)
            robotMovements.pop()
            failSafeIndex += -1
        } else if (robotMovements[failSafeIndex] == "RIGHT") {
            Forward(1500, 0, -200)
            robotMovements.pop()
            failSafeIndex += -1
        }
    }
    failSafeEngaged = 1
})
radio.onReceivedString(function (receivedString) {
    serial.writeLine(receivedString)
    if (receivedString == "Forward") {
        status = 1
        robotMovements.push("FORWARD")
        Forward(400, -25, -25)
    } else if (receivedString == "Left") {
        status = 1
        robotMovements.push("LEFT")
        Forward(660, 140, 0)
    } else if (receivedString == "Right") {
        status = 1
        robotMovements.push("RIGHT")
        Forward(648, 0, 140)
    } else if (receivedString == "Fail Safe Unengagable") {
        failSafeEngagable = 0
    } else if (receivedString == "Fail Safe Engagable") {
        failSafeEngagable = 1
    } else if (receivedString == "Here?") {
        lastConfirmation = input.runningTime()
    }
})
let failSafeEngagable = 0
let failSafeIndex = 0
let robotMovements: string[] = []
let failSafeEngaged = 0
let lastConfirmation = 0
let status = 0
radio.setGroup(1)
status = 0
lastConfirmation = input.runningTime()
failSafeEngaged = 0
robotMovements = ["START"]
basic.forever(function () {
    if (input.runningTime() - lastConfirmation > 5000 && failSafeEngaged == 0 && failSafeEngagable == 1) {
        failSafeIndex = robotMovements.length - 1
        while (robotMovements.length > 0) {
            if (robotMovements[failSafeIndex] == "FORWARD") {
                Forward(400, 25, 25)
                robotMovements.pop()
                failSafeIndex += -1
            } else if (robotMovements[failSafeIndex] == "LEFT") {
                Forward(660, -140, 0)
                robotMovements.pop()
                failSafeIndex += -1
            } else if (robotMovements[failSafeIndex] == "RIGHT") {
                Forward(648, 0, -140)
                robotMovements.pop()
                failSafeIndex += -1
            }
        }
        failSafeEngaged = 1
    }
})
basic.forever(function () {
    if (status == 0) {
        radio.sendString("Ready")
        serial.writeLine("Sent: Ready")
        basic.pause(1000)
    } else {
        radio.sendString("Busy")
        serial.writeLine("Sent: Busy")
        basic.pause(1000)
    }
})
