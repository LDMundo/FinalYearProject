/**************************************
 * Robotic Rotavator Test Code        *
 * By: Lloyd Mundo                    *
 * Last Modified: 07 Mar. 2019        *
 **************************************/

/* Global Variables are declared here */
const int echoPin = 13;   // echo pin of ultrasonic sensor
const int trigPin = 4;    // trigger pin of ultrasonic sensor
long duration;            // duraion of the echo pulse
int distance;             // distance of the object detected
 
/* Function prototypes declarations */
void forward( int ms );     
void reverse( int ms );
void stopMotor( int ms );
void rotor();
int objDistance();

/* Set up function to define ports and run once*/
void setup() {
  /* Ultrasonic Sensor */
  pinMode( 4, OUTPUT );
  pinMode( 13, INPUT );

  /* Wheel Motor */ 
  pinMode( 12, OUTPUT );  //HIGH for forward
  pinMode( 11, OUTPUT );  //HIGH for reverse
  pinMode( 10, OUTPUT );  //HIGH for forward
  pinMode(  9, OUTPUT );  //HIGH for reverse

  /* Rotor Motor */
  pinMode( 8, OUTPUT ); //HIGH for reverse
  pinMode( 7, OUTPUT ); //HIGH for forward
  pinMode( 6, OUTPUT ); //HIGH for reverse
  pinMode( 5, OUTPUT ); //HIGH for forward

  Serial.begin(9600);
}


/* Main Program */
void loop() 
{
  rotor();
  if(objDistance() < 6)
  {
    reverse( 50 );  // reverse
  }
  else
  {
    forward( 50 );  // forward
  }
  /*forward( 1000 );  // forward for 1s
  stopMotor( 50 );  // stop for 50ms
  reverse( 2000 );  // reverse for 2s
  stopMotor( 50 );  // stop for 50ms
  */
  delay(50); //50ms delay
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

/********************************
 * Function to turn rotor ON    *
 * No arguments or retun values *
 *******************************/
void rotor()
{
  digitalWrite(8, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, HIGH);
  digitalWrite(5, HIGH);
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
