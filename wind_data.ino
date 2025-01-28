void setup() {
  Serial.begin(9600);
  analogReference(INTERNAL);
}

void loop() {
  int wind_speed = analogRead(A0);
  Serial.println(wind_speed);
}
