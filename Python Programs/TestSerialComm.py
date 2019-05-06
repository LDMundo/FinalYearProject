import serial
ser = serial.Serial(
        port='/dev/serial0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.3
)


while True:
    while ser.inWaiting():
        response = ser.read(8)
        print('message received: ' + response.decode('utf-8'))
        ser.write('received'.encode('utf-8'))
    
