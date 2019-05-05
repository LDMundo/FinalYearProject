
String messageReceived;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write("Arduino Message");
  if(Serial.available() > 0)
  {
    messageReceived = Serial.read();
    Serial.println(messageReceived);
  }
  else
    Serial.println("error\n");

  delay(2000);
}
