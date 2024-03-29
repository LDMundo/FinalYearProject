/**************************************
 * Robotic Rotavator Test Code        *
 * By: Lloyd Mundo                    *
 * Last Modified: 20 May 2019         *
 **************************************/

/* Global Variables are declared here */
const int echoPin = 13;           // echo pin of ultrasonic sensor
const int trigPin = 4;            // trigger pin of ultrasonic sensor
long duration = 0;                // duraion of the echo pulse
float distance = 0;               // distance of the object detected
const byte leftSwitch = 3;        // interrupt pin for left limit switch
const byte rightSwitch = 2;       // interrupt pin for right limit switch
volatile bool bumpedOnLeft = 0;   // flag for when left bumper is hit
volatile bool bumpedOnRight = 0;  // flag for when right bumper is hit
bool forwardState = 0;            // 1 if forward, 0 for stopped
unsigned long previousMillis = 0; // store the last time forwardState is updated
unsigned long currentMillis = 0;  // current running time of forwardState
unsigned long serialMillis = 0;   // store the time when a message is sent to the pi
unsigned long afterSerialMillis = 0;  // current running time after sending a request to pi
const long interval = 1500;       // interval to stop and forward the motor (wheels)
String reply = "";                // holds the reply from raspbery pi
 
/* Function prototypes declarations */
void forward();     
void reverse( int ms );
void stopMotor();
void turnLeft( int ms );
void turnRight( int ms );
void rotorOn();
void rotorReverse();
void rotorOff();
float objDistance();

/* Set up function to define ports and run once*/
void setup()
{
  /* Ultrasonic Sensor */
  pinMode( trigPin, OUTPUT );
  pinMode( echoPin, INPUT );

  /* Wheel Motors */ 
  pinMode( 12, OUTPUT );  //HIGH for forward
  pinMode( 11, OUTPUT );  //HIGH for reverse
  pinMode( 10, OUTPUT );  //HIGH for forward
  pinMode(  9, OUTPUT );  //HIGH for reverse

  /* Rotor Motors */
  pinMode( 8, OUTPUT ); //HIGH for reverse
  pinMode( 7, OUTPUT ); //HIGH for forward
  pinMode( 6, OUTPUT ); //HIGH for reverse
  pinMode( 5, OUTPUT ); //HIGH for forward

  /* Interrupts */
  pinMode(leftSwitch, INPUT);
  pinMode(rightSwitch, INPUT);
  attachInterrupt(digitalPinToInterrupt(leftSwitch), leftBump, HIGH);
  attachInterrupt(digitalPinToInterrupt(rightSwitch), rightBump, HIGH);
  
  Serial.begin(9600);
  delay(1000); // 1 second delay before robot starts
}


/* Main Program */
void loop() 
{
  rotorOn();
  currentMillis = millis();
  if(currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis;
    if(forwardState == 0){
      forwardState = 1;
      forward();
    }
    else{
      forwardState = 0;
      stopMotor();
    }
  }
  /*
  Serial.write("req");
  serialMillis = millis();
  while(!Serial.available())
  {
    afterSerialMillis = millis();
    // if elapsed time after sending a message is greater than or equal 1s
    if((afterSerialMillis - serialMillis) >= 400) 
      break;
  }
  reply = Serial.readString();
  if(reply == "turnRight")
  {
    turnRight(800);
  }
  else if(reply == "turnLeft")
  {
    turnLeft(800);
  }
  else if(reply == "reverse")
  {
    rotorReverse();
    reverse(1500);
    rotorOn();
    turnRight(1000);
  }
  else if(reply == "noObject"){}
  reply = ""; //flush reply
  */
  if(bumpedOnLeft == 1){
    rotorReverse();
    reverse(1000);
    rotorOn();
    turnRight(1000);
    bumpedOnLeft = 0;
  }
  else if(bumpedOnRight == 1){
    rotorReverse();
    reverse(1500);
    rotorOn();
    turnLeft(1000);
    bumpedOnRight = 0;
  }
  else if(objDistance() < 10){
    rotorReverse();
    reverse(1500);
    rotorOn();
    turnLeft(1000);
  }
}

/****************************************************
 * Interrupt Service Routine for left limit switch  *
 ***************************************************/
void leftBump()
{
  bumpedOnLeft = 1;
}

/****************************************************
 * Interrupt Service Routine for right limit switch *
 ***************************************************/
void rightBump()
{  
  bumpedOnRight = 1;
}

/**********************************
 * Function to move robot forward *
 * Arguments: delay in ms         *
 *********************************/
void forward()
{
  digitalWrite(12, HIGH);
  digitalWrite(10, HIGH);
  digitalWrite(11, LOW);
  digitalWrite(9, LOW);
}

/******************************************
 * Function to move the robot in reverse  *
 * Arguments: delay in ms                 *
 *****************************************/
void reverse(int ms)
{
  digitalWrite(12, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, HIGH);
  digitalWrite(9, HIGH);
  delay(ms);
}

/******************************
 * Function to stop the robot *
 * Arguments: delay in ms     *
 *****************************/
void stopMotor()
{
  digitalWrite(12, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
  digitalWrite(9, LOW);
}

/******************************************
 * Function to turn robot to left         *
 * Arguments: delay in ms                 *
 *****************************************/
void turnLeft(int ms)
{
  digitalWrite(12, HIGH);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
  digitalWrite(9, HIGH);
  delay(ms);
}

/******************************************
 * Function to turn robot to right        *
 * Arguments: delay in ms                 *
 *****************************************/
void turnRight(int ms)
{
  digitalWrite(12, LOW);
  digitalWrite(10, HIGH);
  digitalWrite(11, HIGH);
  digitalWrite(9, LOW);
  delay(ms);
}

/********************************
 * Function to turn rotor ON    *
 * No arguments or retun values *
 *******************************/
void rotorOn()
{
  digitalWrite(8, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, HIGH);
  digitalWrite(5, HIGH);
}

/********************************
 * Function to reverse rotor    *
 * No arguments or retun values *
 *******************************/
void rotorReverse()
{
  digitalWrite(8, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);
  digitalWrite(5, LOW);
}

/********************************
 * Function to turn rotor OFF   *
 * No arguments or retun values *
 *******************************/
void rotorOff()
{
  digitalWrite(8, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  digitalWrite(5, LOW);
}

/*********************************************************
 * Function to determine the distance of object detected *
 * Returns: object distance                              *
 ********************************************************/
float objDistance()
{
  digitalWrite(trigPin, HIGH);          // output high on trigger pin
  delayMicroseconds(10);                // high for 10us delay
  digitalWrite(trigPin, LOW);           // pull it low after
  duration = pulseIn(echoPin, HIGH);    // measure duration of a 'high' on the eco pin
  distance = duration/58;               // distance in cm (from datasheet)
  return distance;                      
}
