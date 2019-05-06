import serial
import time
#opens the serial communication
ser = serial.Serial(
        port='/dev/serial0',            #port
        baudrate=9600,                  #baud rate is the same as arduino
        parity=serial.PARITY_NONE,      #no parity
        stopbits=serial.STOPBITS_ONE,   #defining stop bit as 1
        bytesize=serial.EIGHTBITS,      #size of incoming byte
        timeout=0.3                     #timeout
)


while True:
    while ser.inWaiting():              #wait when the number of byte is >1
        response = ser.read(5)          #read 5 bytes of data
        print('message received: ' + response.decode('utf-8'))  # decode and print received message
        time.sleep(2)                       #delay test
        ser.write('rpi'.encode('utf-8'))    #encode and send reply to arduino
        ser.flush()                         #waits until transmission is completed
    
