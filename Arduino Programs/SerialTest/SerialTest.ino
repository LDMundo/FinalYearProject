String messageReceived;
void setup() {
  pinMode(LED_BUILTIN, OUTPUT); //built in LED
  Serial.begin(9600);   //baud rate
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write("Hello");  //writes Hello into serial buffer
  while(Serial.available() == 0); //waits for data in buffer
  messageReceived = Serial.readString();  // reads the buffer and decodes it to string
  if (messageReceived == "rpi") //check if the reply from pi is rpi
  {
    digitalWrite(LED_BUILTIN,!digitalRead(LED_BUILTIN));  //turn ON/OFF the LED
  }
  messageReceived = ""; //flushes the reply
  delay(1000); //One second delay
}
