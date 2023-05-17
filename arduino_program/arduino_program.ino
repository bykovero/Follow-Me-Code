//PIN BELEGUNG
int left_forward = 9
int left_backward = 8
int right_forward = 6
int right_backward = 7

int left_speed = 10
int right_speed = 11

int max_speed = 100
int min_speed = 50

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

void drive_forwards(speed) {
  Serial.println("Driving forwards!");
  analogWrite(left_speed, speed);
  analogWrite(right_speed, speed);

  digitalWrite(left_forward, HIGH);
  digitalWrite(left_backward, LOW);
  digitalWrite(right_forward, HIGH);
  digitalWrite(right_backward, LOW);
  
  delay(1000);
}

void drive_right(speed, degree){
  Serial.println("Driving Right!");

  //Calculate indivudual speeds based on degree

  //Drive

}

void drive_left(speed, degree){
  Serial.println("Driving Left!");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("I am working!");
}
