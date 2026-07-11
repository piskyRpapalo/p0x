#include <Arduino.h>
#include <Wire.h>
#include <math.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
#include <Adafruit_ADXL345_U.h>
#include <RTClib.h>

// Grove I2C del M5 Atom Lite/Matrix
static const int PIN_SDA = 26;
static const int PIN_SCL = 32;

Adafruit_BME680 bme;
Adafruit_ADXL345_Unified adxl = Adafruit_ADXL345_Unified(12345);
RTC_DS3231 ds3231;
RTC_PCF8563 pcf8563;

bool   bme_ok  = false; uint8_t bme_addr  = 0;
bool   adxl_ok = false; uint8_t adxl_addr = 0;
bool   rtc_ok  = false; uint8_t rtc_addr  = 0;
int    rtc_type = 0; // 1 = DS3231, 2 = PCF8563

static bool i2c_present(uint8_t addr) {
  Wire.beginTransmission(addr);
  return (Wire.endTransmission() == 0);
}

static void printNum(float v, int dec) {
  if (isnan(v)) Serial.print("null");
  else          Serial.print(v, dec);
}

void setup() {
  Serial.begin(115200);
  delay(300);
  Wire.begin(PIN_SDA, PIN_SCL);
  delay(50);

  // --- I2C scan: una sola linea JSON ---
  Serial.print("{\"event\":\"i2c_scan\",\"found\":[");
  bool first = true;
  for (uint8_t a = 0x01; a <= 0x7F; a++) {
    if (i2c_present(a)) {
      if (!first) Serial.print(",");
      first = false;
      Serial.print("\"0x");
      if (a < 0x10) Serial.print("0");
      Serial.print(a, HEX);
      Serial.print("\"");
    }
  }
  Serial.println("]}");

  // --- BME680 @ 0x76 / 0x77 ---
  if (i2c_present(0x76) && bme.begin(0x76)) { bme_ok = true; bme_addr = 0x76; }
  else if (i2c_present(0x77) && bme.begin(0x77)) { bme_ok = true; bme_addr = 0x77; }
  if (bme_ok) {
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150); // 320 C por 150 ms
  }

  // --- ADXL345 @ 0x53 / 0x1D ---
  if (i2c_present(0x53) && adxl.begin(0x53)) { adxl_ok = true; adxl_addr = 0x53; }
  else if (i2c_present(0x1D) && adxl.begin(0x1D)) { adxl_ok = true; adxl_addr = 0x1D; }
  if (adxl_ok) adxl.setRange(ADXL345_RANGE_2_G);

  // --- RTC: DS3231 @ 0x68 o PCF8563 @ 0x51 ---
  if (i2c_present(0x68) && ds3231.begin()) { rtc_ok = true; rtc_addr = 0x68; rtc_type = 1; }
  else if (i2c_present(0x51) && pcf8563.begin()) { rtc_ok = true; rtc_addr = 0x51; rtc_type = 2; }
}

// --- Comando serial (P0X #30): "T<epoch_unix>\n" fija el RTC ---------------
// El epoch se envía ya en hora local de Lisboa (el DS3231 guarda hora de pared).
// Única escritura admitida; cualquier otra línea se ignora.
static void handleSerial() {
  if (!Serial.available()) return;
  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() < 2 || line[0] != 'T') return;
  uint32_t epoch = (uint32_t) strtoul(line.c_str() + 1, nullptr, 10);
  if (epoch < 1600000000UL) {   // sanidad: nada anterior a 2020
    Serial.println("{\"event\":\"rtc_set\",\"ok\":false,\"motivo\":\"epoch invalido\"}");
    return;
  }
  if (!rtc_ok) {
    Serial.println("{\"event\":\"rtc_set\",\"ok\":false,\"motivo\":\"sin rtc\"}");
    return;
  }
  if (rtc_type == 1) ds3231.adjust(DateTime(epoch));
  else               pcf8563.adjust(DateTime(epoch));
  DateTime now = (rtc_type == 1) ? ds3231.now() : pcf8563.now();
  char buf[64];
  snprintf(buf, sizeof(buf),
           "{\"event\":\"rtc_set\",\"ok\":true,\"rtc\":\"%04d-%02d-%02dT%02d:%02d:%02d\"}",
           now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());
  Serial.println(buf);
}

void loop() {
  unsigned long ts = millis();

  float temp = NAN, hum = NAN, pres = NAN;
  long  gas  = -1;
  if (bme_ok && bme.performReading()) {
    temp = bme.temperature;
    hum  = bme.humidity;
    pres = bme.pressure / 100.0f;      // hPa
    gas  = (long)bme.gas_resistance;   // ohm
  }

  float ax = NAN, ay = NAN, az = NAN;
  if (adxl_ok) {
    sensors_event_t e;
    adxl.getEvent(&e);
    ax = e.acceleration.x / 9.80665f;  // g
    ay = e.acceleration.y / 9.80665f;
    az = e.acceleration.z / 9.80665f;
  }

  Serial.print("{\"ts_ms\":");        Serial.print(ts);
  Serial.print(",\"temp_c\":");        printNum(temp, 2);
  Serial.print(",\"humidity\":");      printNum(hum, 2);
  Serial.print(",\"pressure_hpa\":");  printNum(pres, 2);
  Serial.print(",\"gas_ohm\":");       if (gas < 0) Serial.print("null"); else Serial.print(gas);
  Serial.print(",\"accel_g\":{\"x\":");printNum(ax, 3);
  Serial.print(",\"y\":");             printNum(ay, 3);
  Serial.print(",\"z\":");             printNum(az, 3);
  Serial.print("}");

  Serial.print(",\"rtc\":");
  if (rtc_ok) {
    DateTime now = (rtc_type == 1) ? ds3231.now() : pcf8563.now();
    char buf[26];
    snprintf(buf, sizeof(buf), "\"%04d-%02d-%02dT%02d:%02d:%02d\"",
             now.year(), now.month(), now.day(),
             now.hour(), now.minute(), now.second());
    Serial.print(buf);
  } else {
    Serial.print("null");
  }

  Serial.print(",\"sensors\":{\"bme680\":"); Serial.print(bme_ok  ? "true" : "false");
  Serial.print(",\"adxl345\":");             Serial.print(adxl_ok ? "true" : "false");
  Serial.print(",\"rtc\":");                 Serial.print(rtc_ok  ? "true" : "false");
  Serial.println("}}");

  // 5s entre telemetrías, pero atendiendo el serial cada 100ms (rtc_set #30)
  for (int i = 0; i < 50; i++) { handleSerial(); delay(100); }
}
