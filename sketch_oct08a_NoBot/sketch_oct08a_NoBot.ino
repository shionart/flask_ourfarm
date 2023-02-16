//http://arduino.esp8266.com/stable/package_esp8266com_index.json - versi di bawah 3
#include <ESP8266WiFi.h> 
#include <WiFiClientSecure.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

//DHT sensor library - adafruit
#include <DHT.h> 
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

//Arduinojson library - benchon
#include <ArduinoJson.h> 


/**
CONNECT WIFI, ganti wifi anda di sini
 ssid - nama wifi, bisa dari web pusat
 password - password wifi, bisa dari web pusat
 ip_address - ip address dari raspy/web apps local, bisa dari web pusat
 nama - nama nodes/arduino, bisa dari web pusat
 id_arduino - id unik arduino, bisa dari web pusat
*/
char ssid[] = "samlekom";
char password[] = "dragonica025";
char ip_address[]="192.168.137.147";
char nama[]="front";
char id_arduino[]="6f39b26f5345407b94f8";
char id_user[]="fpC1dDVM36WpxPkD56pMEOSM8zI2";
//url daftar device, sync control
String control_page="http://"+String(ip_address)+":5000/api_control/"+String(id_arduino); 
//url input data  sensor
String raspi_input= "http://"+String(ip_address)+":5000/input"; 

WiFiClientSecure client;
int led3=2;       //cadangan
int led1=14;      //PIN LED INDIKATOR WIFI
int led2=15;      //PIN RELAY LED controlled by ldr
int relay=5;      //PIN RELAY PUMP
int buzzer=12;    //PIN BUZZER
int sm=0;         //PIN ANALOG SOIL MOISTURE
int ldr = 13;     //PIN LDR output
float h=0;        //VAR humidity di udara
float t=0;        //VAR temperature di udara
int Relay = 0;    //VAR RELAY 0 mati, 1 nyala
int limit=0;      //VAR COUNTER
int stat = 0;     //
int ldrvalue=0;   //VAR LDR
int smval=0;      //VAR SM
int val=0;        //VAR relay kayanya sih
float temph=0;
float tempt=0;
bool Start = false;
String status_perintah="1"; //status perintah eksekusi, 1 berarti executed
String curr_perintah="0";   //perintah yg dijalankan arduino, mode ada 0 1 2 3
int batas_bawah=40;
int batas_atas=50;
int jeda=12;
int status_connect=1;       //terkoneksi
boolean handler = false;    //VAR handler gagal fetch/post
unsigned long previousMillis = 0;
unsigned long sejam = 3600000;
unsigned long semenit = 60000;
int readSM(){
  smval = analogRead(sm);
  Serial.println("Nilai mentah sm : ");
  Serial.println(smval);
  return smval;
}

//Relay control for timing 
void relay1(int rly){
  if(rly==1){
  digitalWrite(relay,LOW);
  delay(2000);
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
  http.addHeader("Content-Type", "application/json");
  int status_code = http.GET();
  Serial.println("get control status code :"+String(status_code) );
  if (status_code ==200){
    DynamicJsonDocument doc(2048); 
    deserializeJson(doc, http.getStream());   
  //Read result parsing
    if(doc["perintah"].as<String>()!="5"){
      Serial.println("Refreshing control");
      curr_perintah=doc["perintah"].as<String>();
      batas_bawah=doc["batas_bawah"].as<int>();
      batas_atas=doc["batas_atas"].as<int>();
      jeda=doc["jeda"].as<int>();
    }
    if(doc["status"].as<String>()=="0"){
      Serial.println("Baca perintah baru!");
      post_control();
      Serial.println("Perintah tersimpan");
    }  
  }
  else{
    Serial.println("Get control gagal");
    handler=true; 
  }
  http.end();
}

//upload data to raspberry server local
void post_sensor(){
  HTTPClient http;                        //Declare object of class HTTPClient
  String postData;
  postData = "suhu=" + String(t) + "&lembap=" 
    + String(h) + "&sm=" + String(smval) + "&relay=" 
    + String(Relay)+ "&id_arduino="+String(id_arduino);
  http.begin(raspi_input);                //Specify request destination
  http.addHeader("Content-Type", 
    "application/x-www-form-urlencoded"); //Specify content-type header
  int httpCode = http.POST(postData);     //Send the request
  String payload = http.getString();      //Get the response payload
  Serial.println(httpCode);               //Print HTTP return code
  Serial.println(payload);                //Print request response payload
  http.end();                             //Close connection
  Serial.println("Post selesai");
  Serial.println("Suhu: " + String(t) +", Kelembapan: " + String(h) +", SM: "+String(smval)
    + ", relay: "+ String(Relay)+ ", id: "+ String(id_arduino)); 
}
  
void post_control(){
    HTTPClient http;    //Declare object of class HTTPClient
    //Post Data
    String postData;
    postData = "id_user="+String(id_user)+"&perintah=" 
      + curr_perintah + "&status=" 
      + status_perintah+ "&nama=" + String(nama);
    http.begin(control_page);               //Specify request destination
    http.addHeader("Content-Type", 
      "application/x-www-form-urlencoded"); //Specify content-type header
    int httpCode = http.POST(postData);     //Send the request
    String payload = http.getString();      //Get the response payload
    Serial.println(httpCode);               //Print HTTP return code
    Serial.println(payload);                //Print request response payload
    http.end();                             //Close connection
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
    digitalWrite(relay,HIGH); //TODO ini cek defaultnya apa, kalo bisa kondisi dicolok ya mati.
    if (limit==100){
       if (smval < batas_bawah) {
          Serial.println("sudah lewat batas batah, menyalakan pompa...");
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
      }else if(smval >= batas_atas && stat == 0) {
          Serial.println("sudah lewat batas atas, mematikan pompa...");
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
  }else if(a=="1"){           //mode terjadwal, sesuai timestamp pagi&sore nyiram
    Serial.println("Mode 1");
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= (jeda*sejam)) {
      previousMillis=currentMillis;
      Serial.println("Masuk waktu interval, melakukan penyiraman....");
      Serial.println(previousMillis);
      relay1(1);
    }
    
  }else if(a=="2"){           //mode menyala
    relay2(1);
    Serial.println("Mode 2");
  }else if(a=="3"){           //mode mati
    relay2(0);
    Serial.println("Mode 3");
  }
}

void cek_control(){
  if(handler){                      //tidak ada koneksi
    Serial.println("tidak ada koneksi, akan retry setiap 5x loop");
    handler=true;
    if(limit % 10 ==0){             //lakukan pengecekan koneksi setiap 10 loop
      handler=false;
    }
  }else{
    get_control();  
    Serial.println("curr_perintah: "+curr_perintah+ "| batas_bawah: "+batas_bawah
    +"| batas_atas: "+batas_atas+"| jeda: "+jeda);
  }
}

void lampu(){                   //ldr control led
    ldrvalue = digitalRead(ldr);
    Serial.println("ldr value : ");
    Serial.println(ldrvalue);
  if(ldrvalue==0){
    digitalWrite(led2, LOW);
    }
   else{
    digitalWrite(led2, HIGH);
    }
  }

void data_sensor(){                     //fetch data from sensor
   smval = readSM();
    //val= map(smval,1023,165,0,100);   // sm biasa
    smval = smval/10;                     //sm robotdyn
    Serial.println("smval setelah dibagi 10 : ");
    Serial.print(smval);
    if(smval<0)smval=0;
    else if (smval>100)smval=100;
    if(!isnan(temph)) h=temph;
    if(!isnan(tempt)) t=tempt;
  }

//-------------------SETUP MULAI------------------
  void setup() {
    Serial.begin(9600);
    digitalWrite(relay, HIGH);
    dht.begin();
    WiFi.mode(WIFI_STA);              // Set WiFi to station mode and disconnect from an AP if it was Previously connected
    WiFi.disconnect();
    delay(10);
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(buzzer,OUTPUT);
    pinMode(relay,OUTPUT);
    pinMode(led1,OUTPUT);
    pinMode(led2,OUTPUT);
    pinMode(ldr,INPUT);
    Serial.print("Connecting Wifi: ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");               //if not connected printing .........
      digitalWrite(LED_BUILTIN,LOW);
      digitalWrite(buzzer,HIGH);
      delay(50);
      digitalWrite(buzzer,LOW);
      digitalWrite(LED_BUILTIN,HIGH);
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
    cek_control();              //Periksa perintah baru atau tidak------   
//Baca sensor------
//    smval = readSM();
//    val= map(smval,1023,165,0,100);
//    if(val<0)val=0;
//    else if (val>100)val=100;
    temph=dht.readHumidity();
    tempt=dht.readTemperature();
    Serial.println( "Lembap Udara "+String(temph)+
    " Suhu "+String(tempt));
    if(!isnan(temph)) h=temph;
    if(!isnan(tempt)) t=tempt;
    delay(1000);
    if(limit==100 || limit==0){
      data_sensor();
      mode_control(curr_perintah);//lakukan perintah dulu di sini biar ngasih tau status relay nya sebelum dipost
      post_sensor();            //upload data to raspberry only happen once in 100 loop
      limit=1;
      digitalWrite(buzzer,HIGH);
      delay(200);
      digitalWrite(buzzer,LOW);
      h=0;
      t=0;
    }else{
      mode_control(curr_perintah);
      }
    Serial.println(limit);
    limit++;
  }
