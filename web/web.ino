#include <ESP8266WiFi.h>

#define LED1 1
#define LED2 3
#define LED3 5
#define LED4 4
#define LED5 0
#define LED6 2
#define LED7 14
#define LED8 16
#define LED9 13
#define LED10 12

const char* ssid = "Owa";               // Nama WIFI kamu
const char* password = "mamasuka";                  // Password Wifi
const char* host = "192.168.1.8";                 // Link website / Ip Server

bool Parsing = false;
String dataPHP, data[11];

void setup()
{
  Serial.begin(9600);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  pinMode(LED6, OUTPUT);
  pinMode(LED7, OUTPUT);
  pinMode(LED8, OUTPUT);
  pinMode(LED9, OUTPUT);
  pinMode(LED10, OUTPUT);
}

void loop()
{
  WiFiClient client;

  Serial.printf("\n[Connecting to %s ... ", host);
  if (client.connect(host, 80)) {
    Serial.println("connected]");
    Serial.println("[Sending a request]");

    String url = "lcs/wemos/lampu"; // Lokasi File Baca Data
    client.print(String("GET /") + url + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n"
                );

    Serial.println("[Response:]");
    while (client.connected())
    {
        dataPHP = client.readStringUntil('\n');
        int q = 0;
        Serial.print("Data Masuk : ");
        //Serial.print(dataPHP);
        Serial.println();

        data[q] = "";
        for (int i = 0; i < dataPHP.length(); i++) {
          if (dataPHP[i] == '#') {
            q++;
            data[q] = "";
          }
          else {
            data[q] = data[q] + dataPHP[i];
          }
        }

        if (data[1].toInt() == 1)
        {
          digitalWrite(LED1, LOW);
        } 
        if (data[1].toInt() == 0)
        {
          digitalWrite(LED1, HIGH);
        }
        Serial.println(data[1].toInt());
        

        Serial.println(data[2].toInt());
        if (data[2].toInt() == 1)
        {
          digitalWrite(LED2, LOW);
        } 
        if (data[2].toInt() == 0)
        {
          digitalWrite(LED2, HIGH);
        }

        Serial.println(data[3].toInt());
        if (data[3].toInt() == 1)
        {
          digitalWrite(LED3, LOW);
        } 
        if (data[3].toInt() == 0)
        {
          digitalWrite(LED3, HIGH);
        }

        Serial.println(data[4].toInt());
        if (data[4].toInt() == 1)
        {
          digitalWrite(LED4, LOW);
        } 
        if (data[4].toInt() == 0)
        {
          digitalWrite(LED4, HIGH);
        }

        Serial.println(data[5].toInt());
        if (data[5].toInt() == 1)
        {
          digitalWrite(LED5, LOW);
        } 
        if (data[5].toInt() == 0)
        {
          digitalWrite(LED5, HIGH);
        }

        Serial.println(data[6].toInt());
        if (data[6].toInt() == 1)
        {
          digitalWrite(LED6, LOW);
        } 
        if (data[6].toInt() == 0)
        {
          digitalWrite(LED6, HIGH);
        }

        Serial.println(data[7].toInt());
        if (data[7].toInt() == 1)
        {
          digitalWrite(LED7, LOW);
        } 
        if (data[7].toInt() == 0)
        {
          digitalWrite(LED7, HIGH);
        }

        Serial.println(data[8].toInt());
        if (data[8].toInt() == 1)
        {
          digitalWrite(LED8, LOW);
        } 
        if (data[8].toInt() == 0)
        {
          digitalWrite(LED8, HIGH);
        }

        Serial.println(data[9].toInt());
        if (data[9].toInt() == 1)
        {
          digitalWrite(LED9, LOW);
        } 
        if (data[9].toInt() == 0)
        {
          digitalWrite(LED9, HIGH);
        }

        Serial.println(data[10].toInt());
        if (data[10].toInt() == 1)
        {
          digitalWrite(LED10, LOW);
        } 
        if (data[10].toInt() == 0)
        {
          digitalWrite(LED10, HIGH);
        }
        
        Parsing = false;
        dataPHP = "";
      
    }
    client.stop();
    Serial.println("\n[Disconnected]");
  }
  else
  {
    Serial.println("connection failed!]");
    client.stop();
  }
  delay(1000);
}
