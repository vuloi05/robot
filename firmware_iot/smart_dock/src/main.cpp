#include <Arduino.h>

// Stage 1 Skeleton: ESP32 Smart Dock (GĐ 5 triển khai INA219 + PubSubClient MQTT)
// Topic:
//   Publish: dock/{dock_id}/status (QoS 1, Retain, LWT)

static const char *DOCK_ID = "dock_01";

void setup() {
  Serial.begin(115200);
  Serial.printf("Smart Dock skeleton initialized for %s\n", DOCK_ID);
}

void loop() {
  delay(1000);
}
