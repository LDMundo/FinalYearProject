void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
}

void forward();
void motorStop();
void reverse();

void loop() {
  // put your main code here, to run repeatedly:
  forward();
  delay(2000);
  motorStop();
  delay(1000);
  reverse();
  delay(1500);
  motorStop();
  delay(500);
  
}

void forward(){
  digitalWrite(12, HIGH);
  digitalWrite(10, HIGH);
}

void reverse(){
  digitalWrite(11, HIGH);
  digitalWrite(9, HIGH);
}

void motorStop(){
  digitalWrite(12, LOW);
  digitalWrite(10, LOW);  
  digitalWrite(11, LOW);
  digitalWrite(9, LOW);
}
