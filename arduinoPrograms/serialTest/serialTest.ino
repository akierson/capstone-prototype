String incomingData;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2, OUTPUT);
}
int count = 0;
void loop() {
  // put your main code here, to run repeatedly:
  // Add buffer
  if(Serial.available() > 0){
    char inc = Serial.read();
    if (inc == '1') {
      digitalWrite(2, HIGH);
    } if (inc == '0') {
      digitalWrite(2, LOW);
    }
  }
}
