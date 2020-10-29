#define START_PIN 4
#define STOP_PIN 8
#define START_CHAR '#'
#define STOP_CHAR '$'
#define LED 13

char recievedChar;
bool wasCharSet;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(START_PIN, OUTPUT);
  pinMode(STOP_PIN, OUTPUT);
  pinMode(LED, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0) {
    recievedChar = Serial.read();
    wasCharSet = true;
  }

  if(recievedChar == START_CHAR) {
    triggerStart();
  } else if (recievedChar == STOP_CHAR) {
    triggerStop();
  }
  
}

void triggerStart() {
  if(wasCharSet) {
    digitalWrite(START_PIN,HIGH);
    digitalWrite(LED,HIGH);
    delay(100);
    digitalWrite(START_PIN,LOW);
  }
  wasCharSet = false;
}

void triggerStop() {
  if(wasCharSet) {
    digitalWrite(STOP_PIN,HIGH);
    digitalWrite(LED,LOW);
    delay(100);
    digitalWrite(STOP_PIN,LOW);
  }
  wasCharSet = false;
}

