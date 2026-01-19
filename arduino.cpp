#include <WiFiS3.h>

// -------- WiFi credentials --------
const char* ssid = "WIFI_NAME";
const char* password = "WIFI_PASSWORD";

// -------- Sensor --------
const int tempPin = A0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("Starting WiFi...");

  // Connect to WiFi
  int status = WiFi.begin(ssid, password);

  while (status != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
    status = WiFi.status();
  }

  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  int rawValue = analogRead(tempPin);

  // Convert ADC value to voltage
  float voltage = rawValue * (5.0 / 1023.0);

  // Convert voltage to temperature (LM35)
  float temperatureC = voltage * 100.0;

  Serial.print("Temperature: ");
  Serial.print(temperatureC);
  Serial.println(" °C");

  delay(2000);
}
