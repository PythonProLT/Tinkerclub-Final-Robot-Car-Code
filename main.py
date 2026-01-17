def on_received_number(receivedNumber):
    Forward(250, 25, 25)
radio.on_received_number(on_received_number)

def Forward(Time_ms: number, Left_Speed: number, Right_Speed: number):
    wuKong.set_all_motor(Left_Speed, Right_Speed)
    basic.pause(Time_ms)
    wuKong.stop_all_motor()

def on_forever():
    pass
basic.forever(on_forever)
