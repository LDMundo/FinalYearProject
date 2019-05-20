String messageReceived;
unsigned long serialMillis = 0;   // store the time when a message is sent to the pi
unsigned long afterSerialMillis = 0;  // current running time after sending a request to pi
void setup() {
  pinMode(LED_BUILTIN, OUTPUT); //built in LED
  Serial.begin(9600);   //baud rate
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write("request");  //writes Hello into serial buffer
  serialMillis = millis();
  while(!Serial.available())
  {
    afterSerialMillis = millis();
    // if elapsed time after sending a message is greater than or equal 500ms
    if((afterSerialMillis - serialMillis) >= 500) 
      break;
  }
  messageReceived = Serial.readString();  // reads the buffer and decodes it to string
  if (messageReceived == "rpi") //check if the reply from pi is rpi
  {
    digitalWrite(LED_BUILTIN,!digitalRead(LED_BUILTIN));  //turn ON/OFF the LED
  }
  messageReceived = ""; //flushes the reply
  delay(1000); //One second delay
}
