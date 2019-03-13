/**************************************
 * Robotic Rotavator Test Code        *
 * By: Lloyd Mundo                    *
 * Last Modified: 11 Mar. 2019        *
 **************************************/

/* Global Variables are declared here */
const int echoPin = 13;     // echo pin of ultrasonic sensor
const int trigPin = 4;      // trigger pin of ultrasonic sensor
long duration;              // duraion of the echo pulse
int distance;               // distance of the object detected
const byte leftSwitch = 3;  // interrupt pin for left limit switch
const byte rightSwitch = 2; // interrupt pin for right limit switch
volatile bool bumpedOnLeft = 0;
volatile bool bumpedOnRight = 0;
 
/* Function prototypes declarations */
void forward( int ms );     
void reverse( int ms );
void stopMotor( int ms );
void turnLeft( int ms );
void turnRight( int ms );
void rotorOn();
void rotorOff();
int objDistance();

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
  pinMode(leftSwitch, INPUT_PULLUP);
  pinMode(rightSwitch, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(leftSwitch), leftBump, HIGH);
  attachInterrupt(digitalPinToInterrupt(rightSwitch), rightBump, HIGH);

  Serial.begin(9600);
}


/* Main Program */
void loop() 
{
  rotorOn();
  
  if(objDistance() < 7)
  {
    turnLeft(1000);  
    if(objDistance() < 7)
    {
      turnRight(2000); 
    }
  }
  else if(bumpedOnLeft == 1)
  {
    rotorOff();
    reverse(1500);
    turnRight(1000);
    bumpedOnLeft = 0;
  }
  else if(bumpedOnRight == 1)
  {
    rotorOff();
    reverse(1500);
    turnLeft(1000);
    bumpedOnRight = 0; 
  }
  else
  {
    forward( 50 );  // forward
  }
    
  delay(50); //50ms delay
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
void forward(int ms)
{
  digitalWrite(12, HIGH);
  digitalWrite(10, HIGH);
  digitalWrite(11, LOW);
  digitalWrite(9, LOW);
  delay(ms);
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
void stopMotor(int ms)
{
  digitalWrite(12, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
  digitalWrite(9, LOW);
  delay(ms);
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
int objDistance()
{
  digitalWrite(trigPin, HIGH);          // output high on trigger pin
  delayMicroseconds(10);                // high for 10us delay
  digitalWrite(trigPin, LOW);           // pull it low after
  duration = pulseIn(echoPin, HIGH);    // measure duration of a 'high' on the eco pin
  distance = duration/58;               // distance in cm (from datasheet)
  return distance;                      
}
