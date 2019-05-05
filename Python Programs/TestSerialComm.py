import serial
ser = serial.Serial(‘/dev/ttyAMA0’, 9600)

while True:
    ser.open()
    while ser.inWaiting():
        receivedMessage = ser.readline()
        print(receivedMessage + "\n")
        ser.write("message received")

    

