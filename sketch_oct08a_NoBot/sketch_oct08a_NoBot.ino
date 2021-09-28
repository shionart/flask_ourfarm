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
char ssid[] = "kamar_aal";     // your network SSID (name)  
char password[] = "ASuryani"; // your network key
char ip_address[]="192.168.1.50";
char nama[]="front";
char id_arduino[]="48C4D907E4604B10AC65";
char id_user[]="fpC1dDVM36WpxPkD56pMEOSM8zI2";
String control_page="http://"+String(ip_address)+":5000/api_control/"+String(id_arduino);
String raspi_input= "http://"+String(ip_address)+":5000/input";

WiFiClientSecure client;
int led3=2; //cadangan
int led1=14; //PIN LED INDIKATOR WIFI
int stat = 0; //
int led2=15; //PIN RELAY LED KE LDR
int relay=5; //PIN RELAY PUMP
int buzzer=12; //PIN BUZZER
float h=0; //var humidity di udara
float t=0; //var temperature di udara
int sm=0; // PIN ANALOG SOIL MOISTURE
int Relay = 0; //VAR RELAY 0 mati, 1 nyala
int limit=0; //VAR COUNTER
int ldr = 13;
int ldrvalue=0;

int smval=0;
int val=0;
bool Start = false;
String perintah; //Var untuk perintah dari rasp
String status_perintah="1"; //status perintah eksekusi
String curr_perintah="0"; //perintah yg dijalankan arduino
int status_connect=1;

  
  int readSM(){
    smval = analogRead(sm);
    Serial.println(smval);
    return smval;
  }

  //Relay control for timing 
  void relay1(int rly){
    if(rly==1){
    digitalWrite(relay,LOW);
    delay(1000);
    digitalWrite(relay,HIGH);
    }
    else if(rly==0){ 
    digitalWrite(relay,HIGH); 
    }
    Relay=rly;
  }

  void relay2(int rly){
    if(rly==1){
    digitalWrite(relay,LOW);
    }
    else if(rly==0) {
    digitalWrite(relay,HIGH); 
    }
    Relay=rly;
  }

  //GET control
  void get_control(){
    HTTPClient http;
    http.useHTTP10(true);
    http.begin(control_page);
//    Serial.println(control_page);
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
//    smval = readSM();
//    val= map(smval,1023,165,0,100);
//    if(val<0)val=0;
//    else if (val>100)val=100;
//    h = dht.readHumidity();
//    t = dht.readTemperature();
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
    Serial.println("Post selesai");
    Serial.println("Suhu: " + String(t) +", Kelembapan: " + String(h) +", SM: "+ String(val)+"|"+String(smval)+ ", relay: "+ String(Relay)+ ", id: "+ String(id_arduino)); 
  }
  
void post_control(){
    HTTPClient http;    //Declare object of class HTTPClient
    //Post Data
    String postData;
//     
    postData = "id_user="+String(id_user)+"&perintah=" + curr_perintah + "&status=" + status_perintah+ "&nama=" + String(nama);
    http.begin(control_page);              //Specify request destination
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header
    int httpCode = http.POST(postData);   //Send the request
    String payload = http.getString();    //Get the response payload
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
    http.end();  //Close connection
    Serial.println("Post control selesai");
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
    digitalWrite(relay,HIGH); 
    if (limit==100){
       if (val < 30.00) {
          digitalWrite(buzzer,HIGH);
          delay(500);
          digitalWrite(buzzer,LOW);
          delay(500);
          digitalWrite(buzzer,HIGH);
          delay(500);
          digitalWrite(buzzer,LOW);
          relay1(1);
          if (stat == 1){
            stat = 0;
          }
      }else if(val >= 40.00 && stat == 0) {
          digitalWrite(buzzer,HIGH);
          delay(50);
          digitalWrite(buzzer,LOW);
          delay(50);
          digitalWrite(buzzer,HIGH);
          delay(50);
          digitalWrite(buzzer,LOW);
          relay1(0);
          stat = 1;
      }
    }
    
    Serial.println("Mode 0");
  }else if(a=="1"){//mode terjadwal, sesuai timestamp pagi&sore nyiram
    Serial.println("Mode 1");
  }else if(a=="2"){//mode menyala
    relay2(1);
    Serial.println("Mode 2");
  }else if(a=="3"){//mode mati
    relay2(0);
    Serial.println("Mode 3");
  }
}
boolean handler = false;
void cek_control(){
  /*
   * bila belum ada node, return error, tapi di sini perintah jadi 0???
  */
//  Serial.println("perintah :"+perintah);
//  Serial.println("status :"+status_perintah);
  if(perintah=="null" || handler){
    perintah="0";
    status_perintah="1";
    handler=true;
    if(limit % 10 ==0){
//      get_control();
      handler=false;}
  }else{
    get_control();  
    Serial.println("perintah :"+perintah);
    Serial.println("status :"+status_perintah);
    Serial.println("curr_perintah:"+curr_perintah);
    if(perintah=="5"){
        perintah="0";
        post_control();
    } 
    if(status_perintah=="0" || perintah!= curr_perintah){
      Serial.println("Baca perintah baru!");
      curr_perintah=perintah;
      status_perintah="1";
      post_control();
      Serial.println("Perintah tersimpan");
      //Eksekusi perintah    
    }
  }
}

void lampu(){
  ldrvalue = digitalRead(ldr);
    Serial.println(ldrvalue);
  if(ldrvalue==0){
    digitalWrite(led2, LOW);
    }
   else{
    digitalWrite(led2, HIGH);
    }
  }

void data_sensor(){
   smval = readSM();
    //val= map(smval,1023,165,0,100); // sm biasa
    val = smval/10; //sm robotdyn
    if(val<0)val=0;
    else if (val>100)val=100;
    h = dht.readHumidity();
    t = dht.readTemperature();
  }

//-------------------SETUP MULAI------------------
  void setup() {
    Serial.begin(9600);
    digitalWrite(relay, HIGH);
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
    pinMode(ldr,INPUT);
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
    lampu();
//Periksa perintah baru atau tidak------
    cek_control();
//Baca sensor------
//    smval = readSM();
//    val= map(smval,1023,165,0,100);
//    if(val<0)val=0;
//    else if (val>100)val=100;
    Serial.println( "Lembap Udara "+String(dht.readHumidity())+
    " Suhu "+String(dht.readTemperature()));
//Aksi pompa-----
    
//Loop-control-----
    delay(1000);
    limit++;
    Serial.println(limit);
    if(limit==100){
      data_sensor();
      mode_control(curr_perintah);
      post_sensor();//upload data to raspberry only happen once in 100 loop
      limit=0;
      digitalWrite(buzzer,HIGH);
      delay(200);
      digitalWrite(buzzer,LOW);
    }else{
      mode_control(curr_perintah);
      }
    
  }
