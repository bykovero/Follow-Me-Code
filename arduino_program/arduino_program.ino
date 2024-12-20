//PIN BELEGUNG
int left_forward = 9;
int left_backward = 8;
int right_forward = 6;
int right_backward = 7;

int left_speed = 10;
int right_speed = 11;

int led = 3;

//SPEED VARIABLEN
int max_speed = 100;
int min_speed = 60;

int turn_speed_aussen = 80;
int turn_speed_innen = 60;

//SERIAL VARIABLEN
String serialInString = "";


void setup() {
  Serial.begin(9600);

  //FESTLEGUNG DER PINMODES
  pinMode(left_forward, OUTPUT);
  pinMode(left_backward, OUTPUT);
  pinMode(right_forward, OUTPUT);
  pinMode(right_backward, OUTPUT);

  pinMode(left_speed, OUTPUT);
  pinMode(right_speed, OUTPUT);

}

void stop(){
  analogWrite(led, 0);
  Serial.println("Stop!");
  
  digitalWrite(left_forward, LOW);
  digitalWrite(left_backward, LOW);
  digitalWrite(right_forward, LOW);
  digitalWrite(right_backward, LOW);
}

void drive_forward(int speed) {
  analogWrite(led, 50);
  Serial.println("Driving forwards!");
  analogWrite(left_speed, speed);
  analogWrite(right_speed, speed);

  digitalWrite(left_forward, HIGH);
  digitalWrite(left_backward, LOW);
  digitalWrite(right_forward, HIGH);
  digitalWrite(right_backward, LOW);
}

void turn_right(int speed_aussen, int speed_innen){
  analogWrite(led, 50);
  Serial.println("Driving Right!");

  //Calculate indivudual speeds based on degree

  //Drive
  analogWrite(left_speed, speed_aussen);
  analogWrite(right_speed, speed_innen);

  digitalWrite(left_forward, HIGH);
  digitalWrite(left_backward, LOW);
  digitalWrite(right_forward, HIGH);
  digitalWrite(right_backward, LOW);
}

void turn_left(int speed_aussen, int speed_innen){
  analogWrite(led, 50);
  Serial.println("Driving Left!");
  analogWrite(left_speed, speed_innen);
  analogWrite(right_speed, speed_aussen);

  digitalWrite(left_forward, HIGH);
  digitalWrite(left_backward, LOW);
  digitalWrite(right_forward, HIGH);
  digitalWrite(right_backward, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println("I am working!");
  //Serial.println("Hallo!");

  while (Serial.available() > 0) {
    char inChar = Serial.read();
    char left;
    char right;
    char forward;
    String speed = "";

    if (isDigit(inChar)){
      serialInString += (char(inChar));
    }
    
    if (inChar == '\n'){
      left = serialInString[0];
      right = serialInString[1];
      forward = serialInString[2];
      
      for (int i = 3; i < serialInString.length(); i++){
        speed += serialInString[i];
      }

      serialInString = "";
    }

    /*Serial.println(left);
    Serial.println(right);
    Serial.println(forward);
    Serial.println(speed);*/

    if (left == '1'){
      turn_left(turn_speed_aussen, turn_speed_innen);
    }

    else if (right == '1'){
      turn_right(turn_speed_aussen, turn_speed_innen);
    }

    else if (forward == '1'){
      drive_forward(speed.toInt()); 
    }
    
    else if (forward == '0'){
      stop();
    }
    
    left = 0;
    right = 0;
    forward = 0;
  }
}
