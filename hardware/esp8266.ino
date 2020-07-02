#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#define DUP 1
#define MAX_LEN 512
const int LED = 2; // GPIO2

char ssid[16] = "";
char password[32] = "";

const char* ssid_ptr = ssid;
const char* password_ptr = password;

const char* host = "www.csie.ntu.edu.tw";
const int httpsPort = 443; 

// Use web browser to view and copy
// SHA1 fingerprint of the certificate
const char fingerprint[] PROGMEM = "17 e2 8e 36 b4 5b 64 dd 19 71 32 e4 d9 50 9b fa 57 62 f5 a8";
char dat = 0;
char mess[MAX_LEN] = "";
String url = "/~b06902041/index.php";
String data, line;

bool CheckMessage(const char *message) {
  while (!Serial.available())
    delay(5);
  int r = 0;
  while (strncmp(mess, message, strlen(message)) && r < 30) {
    dat = Serial.read();
    for (int i = 0; i < MAX_LEN; i++)
      mess[i] = 0;
    for (int i = 0; i < MAX_LEN && dat != '\n'; i++) {
      mess[i] = dat;
      dat = Serial.read();
    }
    r++;
  }
  if (!strncmp(mess, message, strlen(message))) {
    return true;
  }
  return false;
}

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  //Ask for Wifi
  while (!(Serial.available())) {
    Serial.println("What is ssid?");
    digitalWrite(LED, HIGH);
    delay(5);
    digitalWrite(LED, LOW);
    delay(5);
  }
  dat = Serial.read();
  for (int i = 0; i < 16 && dat != '\n'; i++) {
    if (!isSpace(dat))
      ssid[i] = dat;
    dat = Serial.read();
  }
  while (!(Serial.available())) {
    Serial.println("What is password?");
    digitalWrite(LED, HIGH);
    delay(5);
    digitalWrite(LED, LOW);
    delay(5);
  }
  dat = Serial.read();
  for (int i = 0; i < 16 && dat != '\n'; i++) {
    if (!isSpace(dat))
      password[i] = dat;
    dat = Serial.read();
  }

  // Connecting
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid_ptr, password_ptr);
  while (WiFi.status() != WL_CONNECTED) {
    delay(5);
  }

  // Check WiFi connection with arduino
  for (int i = 0; i < DUP; i++)
    Serial.println("WiFi connected");

}

void loop() {

  // Use WiFiClientSecure class to create TLS connection
  WiFiClientSecure client;
  client.setFingerprint(fingerprint);

  int r = 0;
  /*
    // Check data is ready
    while (!CheckMessage("data ready") && r < 30)
    r++;
    if (r == 30) {
    client.flush();
    client.stop();
    return;
    }
    /**/
  r = 0;
  for (int i = 0; i < MAX_LEN; i++)
    mess[i] = 0;
  while (!Serial.available()) {
    digitalWrite(LED, HIGH);
    delay(5);
    digitalWrite(LED, LOW);
    delay(5);
  }
  dat = Serial.read();
  for (int i = 0; i < MAX_LEN-1 && dat != '\n'; i++) {
    if (!isSpace(dat))
      mess[i] = dat;
    dat = Serial.read();
  }
  while (!client.connect(host, httpsPort)) {
    digitalWrite(LED, HIGH);
    delay(5);
    digitalWrite(LED, LOW);
  }
  /*
  // Check HTTPS connection with arduino
  for (int i = 0; i < DUP; i++) {
    Serial.println("connection ready");
    Serial.flush();
  }


  // Check data end with arduino
  /*
    for (int i = 0; i < DUP; i++)
    Serial.println("data end");
  */

  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Content-Type: application/x-www-form-urlencoded" + "\r\n" +
               "Content-Length: " + String(strlen(mess)) + "\r\n\r\n" +
               String(mess) + "\r\n" +
               "Connection: close\r\n\r\n");
  /*
    while (client.connected()) {
    line = client.readStringUntil('\n');
    if (line == "\r") {
      break;
    }
    }

    // Check message sent with arduino
    /*
    String line;
    if (client.available()) {
    line = client.readStringUntil('.'); // Read "Hi, welcome back"
    if (line.equals("Hi, welcome back")) {
      for (int i = 0; i < DUP; i++) {
        Serial.println("Message sent");
        Serial.flush();
      }
    }
    else {
      for (int i = 0; i < DUP; i++) {
        Serial.println("Message didnt sent");
        Serial.flush();
      }
    }
    } else {
    for (int i = 0; i < DUP; i++) {
      Serial.println("Message unavailable");
      Serial.flush();
    }/*
    }
    /**/
  client.stop();
}
