#include <ESP8266WiFi.h>
#include <DHT.h>
DHT dht(5, DHT11); //Pin, Jenis DHT


const int pinSensor = A0;
int pinPIR = 4; 
int statusPIR = 0;  

const char* ssid = "Owa";               // Nama WIFI kamu
const char* password = "mamasuka";                  // Password Wifi
const char* host = "192.168.1.5";                 // Link website / Ip Server

void setup(){
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
 
 dht.begin();

 
}

void loop(){
  WiFiClient client;

  Serial.printf("\n[Connecting to %s ... ", host);
  if (client.connect(host, 80)) {
    Serial.println("connected]");
    Serial.println("[Sending a request]");

  
 //DHT11
 int kelembaban = dht.readHumidity();
 int suhu = dht.readTemperature();
 Serial.print("kelembaban: ");
 Serial.print(kelembaban);
 Serial.print(" ");
 Serial.print("suhu: ");
 Serial.println(suhu);

 //Cahaya
 int cahaya;
 cahaya = analogRead(pinSensor);
  Serial.print("kecerahan : ");
  Serial.println(cahaya);

 //gerak
 int gerak;
  statusPIR = digitalRead(pinPIR);
  if (statusPIR ==HIGH) {            //jika sensor membaca gerakan maka relay akan aktif
  
  Serial.println("ADA GERAKAN");
  gerak = 1;
  delay(100); //Diberikan waktu tunda 10 detik
  }
  else {
    gerak = 0;
  Serial.println("TIDAK ADA GERAKAN");
  }
  Serial.println(gerak);

  Serial.print("GET lcs/wemos/sensor?temp=");
  Serial.print(suhu);
  Serial.print("&humid=");
  Serial.print(kelembaban);
  Serial.print("&cahaya=");
  Serial.print(cahaya);
  Serial.print("&gerak=");
  Serial.print(gerak);      
      client.print(String("GET /") + "lcs/wemos/sensor?temp=" + suhu + "&humid=" + kelembaban + "&cahaya=" + cahaya + "&gerak=" + gerak + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n"
                );
    }

  
  else
  {
    Serial.println("connection failed!]");
    client.stop();
  }
  

 delay(500000);
}
