const int nextButton = 2;
const int prevButton = 7;

const int potPin = A0;
const int ledPin = 9;

int currentPlanet = 0;

bool lastNextState = HIGH;
bool lastPrevState = HIGH;

const char* planets[] = {
  "Mercury",
  "Venus",
  "Earth",
  "Mars",
  "Jupiter",
  "Saturn",
  "Uranus",
  "Neptune"
};

void sendData() {
  Serial.println(planets[currentPlanet]);
}

void setup() {

  pinMode(nextButton, INPUT_PULLUP);
  pinMode(prevButton, INPUT_PULLUP);

  pinMode(ledPin, OUTPUT);

  Serial.begin(9600);

  delay(1000);

  sendData();
}

void loop() {

  bool nextState = digitalRead(nextButton);
  bool prevState = digitalRead(prevButton);

  // NEXT PLANET
  if (nextState == LOW && lastNextState == HIGH) {

    currentPlanet++;

    if (currentPlanet >= 8)
      currentPlanet = 0;

    sendData();

    delay(200);
  }

  // PREVIOUS PLANET
  if (prevState == LOW && lastPrevState == HIGH) {

    currentPlanet--;

    if (currentPlanet < 0)
      currentPlanet = 7;

    sendData();

    delay(200);
  }

  lastNextState = nextState;
  lastPrevState = prevState;

  // BRIGHTNESS CONTROL

  int potValue = analogRead(potPin);

  int brightness = map(
    potValue,
    0,
    1023,
    0,
    255
  );

  analogWrite(ledPin, brightness);

  delay(20);
}