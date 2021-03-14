#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <DHT.h>
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>


//CONNECT WIFI, ganti wifi anda di sini
char ssid[] = "muiren";     // your network SSID (name)  
char password[] = "muirenoleander"; // your network key
char ip_address[]="192.168.1.6";
char nama[]="front";
char id_arduino[]="48C4D907E4604B10AC65";
String control_page="http://"+String(ip_address)+":5000/api_control/"+String(id_arduino);
String raspi_input= "http://"+String(ip_address)+":5000/input";






WiFiClientSecure client;


int led1=14;
int stat = 0;
int led2=13;
int relay=5;
int buzzer=12;
float h=0;
float t=0;
int sm=0;
int Relay = 0;
int limit=0;


int smval=0;
int val=0;
bool Start = false;
String perintah;
String status_perintah;
String curr_perintah;

  
  int readSuhu(){
    smval = analogRead(sm);
    Serial.println(smval);
    return smval;
  }

  //Relay control for timing 
  void relay1(int Relay){
    if(Relay==1){
    digitalWrite(relay,HIGH);
    delay(1000);
    digitalWrite(relay,LOW);
    }
    else if(Relay==0) 
    digitalWrite(relay,LOW); 
  }

  void relay2(int Relay){
    if(Relay==1){
    digitalWrite(relay,HIGH);
    }
    else if(Relay==0) 
    digitalWrite(relay,LOW); 
  }

  //GET control
  void get_control(){
    HTTPClient http;
    http.useHTTP10(true);
    http.begin(control_page);
    http.addHeader("Content-Type", "application/json");
    http.GET();
    //Test
//    String json=http.getString();
//    Serial.println(json);
    //Parsing
//  StaticJsonDocument<256> doc;
    DynamicJsonDocument doc(2048); 
    deserializeJson(doc, http.getStream());   
    //Read result parsing
    perintah=doc["perintah"].as<String>();
    status_perintah=doc["status"].as<String>();
    http.end();
  }

  //upload data to raspberry server local
  void post_sensor(){
    HTTPClient http;    //Declare object of class HTTPClient
    //Sensor
    smval = readSuhu();
    val= map(smval,1023,465,0,100);
    if(val<0)val=0;
    else if (val>100)val=100;
    h = dht.readHumidity();
    t = dht.readTemperature();
    //Post Data
    String postData;
    postData = "suhu=" + String(t) + "&lembap=" + String(h) + "&sm=" + String(val) + "&relay=" + String(Relay)+ "&id_arduino="+String(id_arduino);
    http.begin(raspi_input);              //Specify request destination
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header
    int httpCode = http.POST(postData);   //Send the request
    String payload = http.getString();    //Get the response payload
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
    http.end();  //Close connection
    Serial.println("Post berhasil");
    Serial.println("Suhu: " + String(t) +", Kelembapan: " + String(h) +", SM: "+ String(val) + ", relay: "+ String(Relay)+ ", id: "+ String(id_arduino)); 
  }
  
void post_control(){
    HTTPClient http;    //Declare object of class HTTPClient
    //Post Data
    String postData;
//     
    postData = "perintah=" + curr_perintah + "&status=" + status_perintah+ "&nama=" + String(nama);
    http.begin(control_page);              //Specify request destination
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header
    int httpCode = http.POST(postData);   //Send the request
    String payload = http.getString();    //Get the response payload
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
    http.end();  //Close connection
    Serial.println("Post control berhasil");
  }

/*
   -baca perintah baru
   -jika perintah sekarang & baru berbeda maka :
    - perintah sekarang = baru
    - status = 0
    - lakukan perintah / ubah mode
      -0 default
        jika <40 stat=0 & siram , else stat=1 & berhenti
      -1 terjadwal
        ambil timestamp, masuk range = siram
      -2 nyala
        relay pompa = 1
      -3 mati
        relay pompa = 0
    - status perintah = 1
    - keluar
  -jika perintah sama
    -mode yg aktif jalan(asumsi mode akan selalu jalan dilakukan pengecekan terus)
  */

void mode_control(String a){
  if(a=="0"){ //Mode default, otomatis menyiram bila lembap tanah < 40%
    if (val < 40.00 && limit==3) {
        digitalWrite(buzzer,HIGH);
        delay(500);
        digitalWrite(buzzer,LOW);
        delay(500);
        digitalWrite(buzzer,HIGH);
        delay(500);
        digitalWrite(buzzer,LOW);
        relay1(1);
        Relay = 1;
        if (stat == 1){
          stat = 0;
        }
    }else if(val >= 40.00 && stat == 0 && limit==3) {
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        delay(50);
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        relay1(0);
        Relay = 0;
        stat = 1;
    }
    Serial.println("Mode 0");
  }else if(a=="1"){//mode terjadwal, sesuai timestamp pagi&sore nyiram
    Serial.println("Mode 1");
  }else if(a=="2"){//mode menyala
    relay2(1);
    Relay=1;
    Serial.println("Mode 2");
  }else if(a=="3"){//mode mati
    relay2(0);
    Relay=0;
    Serial.println("Mode 3");
  }
}

void cek_control(){
  /*
   * bila belum ada node, return error, tapi di sini perintah jadi 0???
  */
  Serial.println("perintah :"+perintah);
  Serial.println("status :"+status_perintah);
  get_control();
  Serial.println("perintah :"+perintah);
  Serial.println("status :"+status_perintah);
  Serial.println("curr_perintah:"+curr_perintah);
  if(curr_perintah!=perintah){
    Serial.println("Baca perintah baru!");
    curr_perintah=perintah;
    status_perintah="1";
    post_control();
    Serial.println("Perintah tersimpan");
    //Eksekusi perintah    
  }
}


//-------------------SETUP MULAI------------------
  void setup() {
    Serial.begin(9600);
    dht.begin();
    // Set WiFi to station mode and disconnect from an AP if it was Previously
    // connected
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(10);
    pinMode(buzzer,OUTPUT);
    pinMode(relay,OUTPUT);
    pinMode(led1,OUTPUT);
    pinMode(led2,OUTPUT);
    Serial.print("Connecting Wifi: ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");//if not connected printing .........
      digitalWrite(led1,HIGH);
      delay(50);
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(led1,LOW);
    client.setInsecure();
    
  }

//----------------LOOP MULAI-----------------
  void loop(){
    if(WiFi.status()!= WL_CONNECTED){
        delay(1);
        digitalWrite(led1,HIGH);
        WiFi.begin(ssid, password);
        return;
    }
//Periksa perintah baru atau tidak------
    cek_control();
//Baca sensor------
    smval = readSuhu();
    val= map(smval,1023,465,0,100);
    if(val<0)val=0;
    else if (val>100)val=100;
//Aksi pompa-----
    mode_control(curr_perintah);
//Loop-control-----
    delay(1000);
    limit++;
    Serial.println(limit);
    if(limit==100){
      post_sensor();//upload data to raspberry only happen once in 4 loop
      limit=0;
    }
  }
