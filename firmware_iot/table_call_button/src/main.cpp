#include <Arduino.h>

// Stage 1 Skeleton: ESP32 Table Call Button (GĐ 4 triển khai Wi-Fi + PubSubClient MQTT)
// Topics:
//   Publish  : table/{table_id}/call
//   Subscribe: table/{table_id}/led

static const char *TABLE_ID = "table_01";

void setup() {
  Serial.begin(115200);
  Serial.printf("Table Call Button skeleton initialized for %s\n", TABLE_ID);
}

void loop() {
  delay(1000);
}
