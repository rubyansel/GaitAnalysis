#include <SoftwareSerial.h>
const char Name[8] = "right";
const char Password[16] = "righttt";
#define MAX_LEN 64
#define MES_NUM 4

#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

MPU6050 accelgyro;
//MPU6050 accelgyro(0x69); // <-- use for AD0 high

int16_t ax[MES_NUM], ay[MES_NUM], az[MES_NUM];
int16_t gx[MES_NUM], gy[MES_NUM], gz[MES_NUM];
#define CYCLE_TIME 100

#define OUTPUT_READABLE_ACCELGYRO

#define LED_PIN 13
bool blinkState = false;

SoftwareSerial espSerial(8, 9); // RX, TX

const char ssid[8] = "TsaiYun"; // Robot313AP
const char pwd[16] = "rubyansel"; // robot313

char data[MAX_LEN] = "";
char result[MAX_LEN] = "";
char dat = 0;
int count = 0;

void print_ag() {
  Serial.print("trim=1234567890123456789012345678901234567890123456789012345678901234567890123456789012345"); // 100 char
  espSerial.print("trim=1234567890123456789012345678901234567890123456789012345678901234567890123456789012345");
  Serial.print("123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"); // 100 char
  espSerial.print("123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890");
  Serial.print("&name="); // 6 char
  espSerial.print("&name=");
  Serial.print(Name); // 4-5 char
  espSerial.print(Name);
  Serial.print("&password="); // 10 char
  espSerial.print("&password=");
  Serial.print(Password); // 7-8 char
  espSerial.print(Password);
  for (int i = 0; i < MES_NUM; i++) {
    Serial.print("&ax"); // 3 char
    espSerial.print("&ax");
    Serial.print(i); // 1 char
    espSerial.print(i);
    Serial.print("="); // 1 char
    espSerial.print("=");
    Serial.print(ax[i]); // 6 char
    espSerial.print(ax[i]);
    Serial.print("&ay");
    espSerial.print("&ay");
    Serial.print(i);
    espSerial.print(i);
    Serial.print("=");
    espSerial.print("=");
    Serial.print(ay[i]);
    espSerial.print(ay[i]);
    Serial.print("&az");
    espSerial.print("&az");
    Serial.print(i);
    espSerial.print(i);
    Serial.print("=");
    espSerial.print("=");
    Serial.print(az[i]);
    espSerial.print(az[i]);
    Serial.print("&gx");
    espSerial.print("&gx");
    Serial.print(i);
    espSerial.print(i);
    Serial.print("=");
    espSerial.print("=");
    Serial.print(gx[i]);
    espSerial.print(gx[i]);
    Serial.print("&gy");
    espSerial.print("&gy");
    Serial.print(i);
    espSerial.print(i);
    Serial.print("=");
    espSerial.print("=");
    Serial.print(gy[i]);
    espSerial.print(gy[i]);
    Serial.print("&gz");
    espSerial.print("&gz");
    Serial.print(i);
    espSerial.print(i);
    Serial.print("=");
    espSerial.print("=");
    Serial.print(gz[i]);
    espSerial.print(gz[i]);
    Serial.flush();
    espSerial.flush();
  }
  Serial.println();
  espSerial.println();
  Serial.flush();
  espSerial.flush();
}

void setup() {
  Serial.begin(9600);
  Serial.println("Print to Serial Monitor");
  espSerial.begin(115200);
  Serial.println("esp ready");

  // Ready for asking wifi
  while (!espSerial.available())
    delay(5);
  Serial.println("esp available");

  while (strncmp(data, "What is ssid?", 13)) {
    dat = espSerial.read();
    for (int i = 0; i < MAX_LEN; i++)
      data[i] = 0;
    for (int i = 0; i < MAX_LEN && dat != '\n'; i++) {
      data[i] = dat;
      dat = espSerial.read();
    }
    Serial.println(data);
    delay(5);
  }
  espSerial.println(ssid);
  Serial.println("ssid sent");
  while (!(espSerial.available()))
    delay(5);
  while (strncmp(data, "What is password?", 17)) {
    dat = espSerial.read();
    for (int i = 0; i < MAX_LEN; i++)
      data[i] = 0;
    for (int i = 0; i < MAX_LEN && dat != '\n'; i++) {
      data[i] = dat;
      dat = espSerial.read();
    }
    Serial.println(data);
    delay(5);
  }
  espSerial.println(pwd);
  Serial.println("password sent");
  while (!(espSerial.available()))
    delay(5);
  while (strncmp(data, "WiFi", 4)) {
    dat = espSerial.read();
    for (int i = 0; i < MAX_LEN; i++)
      data[i] = 0;
    for (int i = 0; i < MAX_LEN && dat != '\n'; i++) {
      data[i] = dat;
      dat = espSerial.read();
    }
    Serial.println(data);
    delay(5);
  }
  /**/

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif

  // initialize device
  Serial.println("Initializing I2C devices...");
  accelgyro.initialize();

  // verify connection
  Serial.println("Testing device connections...");
  while (!accelgyro.testConnection()) {
    Serial.println("MPU6050 connection failed");
    delay(5);
  }
  Serial.println("MPU6050 connection successful");

  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  /*
    if (espSerial.available()) {
    Serial.write(espSerial.read());
    }
    if (Serial.available()) {
    espSerial.write(Serial.read());
    }
  */
  for (int cnt = 0; cnt < MES_NUM; cnt++) {
    int32_t ax_tot = 0;
    int32_t ay_tot = 0;
    int32_t az_tot = 0;
    int32_t gx_tot = 0;
    int32_t gy_tot = 0;
    int32_t gz_tot = 0;
    for (int i = 0; i < CYCLE_TIME; i++) {
      accelgyro.getMotion6(&ax[cnt], &ay[cnt], &az[cnt], &gx[cnt], &gy[cnt], &gz[cnt]);
      ax_tot += ax[cnt];
      ay_tot += ay[cnt];
      az_tot += az[cnt];
      gx_tot += gx[cnt];
      gy_tot += gy[cnt];
      gz_tot += gz[cnt];
    }
    ax[cnt] = ax_tot / CYCLE_TIME;
    ay[cnt] = ay_tot / CYCLE_TIME;
    az[cnt] = az_tot / CYCLE_TIME;
    gx[cnt] = gx_tot / CYCLE_TIME;
    gy[cnt] = gy_tot / CYCLE_TIME;
    gz[cnt] = gz_tot / CYCLE_TIME;
    /*
      #ifdef OUTPUT_READABLE_ACCELGYRO
      // display tab-separated accel/gyro x/y/z values
      Serial.print("a/g:\t");
      Serial.print(ax); Serial.print("\t");
      Serial.print(ay); Serial.print("\t");
      Serial.print(az); Serial.print("\t");
      Serial.print(gx); Serial.print("\t");
      Serial.print(gy); Serial.print("\t");
      Serial.println(gz);
      #endif

      #ifdef OUTPUT_BINARY_ACCELGYRO
      Serial.write((uint8_t)(ax >> 8)); Serial.write((uint8_t)(ax & 0xFF));
      Serial.write((uint8_t)(ay >> 8)); Serial.write((uint8_t)(ay & 0xFF));
      Serial.write((uint8_t)(az >> 8)); Serial.write((uint8_t)(az & 0xFF));
      Serial.write((uint8_t)(gx >> 8)); Serial.write((uint8_t)(gx & 0xFF));
      Serial.write((uint8_t)(gy >> 8)); Serial.write((uint8_t)(gy & 0xFF));
      Serial.write((uint8_t)(gz >> 8)); Serial.write((uint8_t)(gz & 0xFF));
      #endif
    */
    // blink LED to indicate activity
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);
  }

  print_ag();
}
