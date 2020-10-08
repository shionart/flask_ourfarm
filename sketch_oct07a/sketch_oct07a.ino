#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <DHT.h>
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

//CONNECT WIFI, ganti wifi anda di sini
char ssid[] = "muiren";     // your network SSID (name)  
char password[] = "muirenoleander"; // your network key
const char* raspi_input = "http://192.168.137.1:5000/input";
const char* control_page="control/1";
const char* id_arduino="1";





#define BOTtoken "900269469:AAH1iXjLyX8hbfPro69lvJ3cmZhwLiN2W2I"  // your Bot Token (Get from Botfather)
#define idChat "732393843"
//973721551
//-415977731
//732393843
WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);
String control;
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
int Bot_mtbs = 1; //mean time between scan messages
long Bot_lasttime;   //last time messages' scan has been done
bool Start = false;

//command on telegram
void handleNewMessages(int numNewMessages) {
    Serial.println("handleNewMessages");
    Serial.println(String(numNewMessages));
    for (int i=0; i<numNewMessages; i++) {
      String chat_id = String(bot.messages[i].chat_id);
      String text = bot.messages[i].text;
      String from_name = bot.messages[i].from_name;
      if (from_name == "") from_name = "Guest";
      if (text == "/on") {
        bot.sendChatAction(chat_id, "typing");
        String welcome = "Relay dinyalakan";
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        delay(50);
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        relay1(1);
        bot.sendMessage(chat_id, welcome);
      }
      if (text == "/off") {
        bot.sendChatAction(chat_id, "typing");
        String welcome = "Relay dimatikan";
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        delay(50);
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
         delay(50);
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        relay1(0);
        bot.sendMessage(chat_id, welcome);
      }
      if (text == "/sensor") {
        smval = readSuhu();
        bot.sendChatAction(chat_id, "typing");
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        awal:
         h = dht.readHumidity();
         t = dht.readTemperature();
          if (isnan(h) || isnan(t)) {
            Serial.println("Failed to read from DHT sensor!");
            delay(10);
            goto awal;
          }
        val= map(smval,1023,465,0,100);
        if(val<0)val=0;
        else if (val>100)val=100;
        String welcome = "Data sensor untuk " + from_name + " \U0001F4C3\n\nSoil moisture : ";
        welcome += val;
        welcome += "%\nSuhu : ";
        welcome += t;
        welcome += "C\nKelembapan : ";
        welcome += h;
        welcome += "%\nRelay dalam kondisi ";
        boolean a=digitalRead(relay);
        if(a)welcome += "mati";
        else welcome += "menyala";
        bot.sendMessage(chat_id, welcome);
      }
    }
  }
  
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


  //upload data to raspberry server local
  void post(){
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
    //NGROK SERVER LOCAL HARAP DIGANTI SETIAP BOOT UP SERVER
    http.begin(raspi_input);              //Specify request destination
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header
    int httpCode = http.POST(postData);   //Send the request
    String payload = http.getString();    //Get the response payload
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
    http.end();  //Close connection
    Serial.println("Post berhasil");
    Serial.println("Suhu: " + String(t) +", Kelembapan: " + String(h) +", SM: "+ String(val) + ", relay: "+ String(Relay)); 
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
    if (WiFi.status() != WL_CONNECTED) {
        delay(1);
        digitalWrite(led1,HIGH);
        WiFi.begin(ssid, password);
        return;
    }   
    if (millis() > Bot_lasttime + Bot_mtbs){
      int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
      digitalWrite(led2,HIGH);
      delay(10);
      digitalWrite(led2,LOW);
      Serial.println(numNewMessages);
      while(numNewMessages >= 1) {
        Serial.println("got response");
        handleNewMessages(numNewMessages);
        numNewMessages = bot.getUpdates(bot.last_message_received + 1);
      }
      Bot_lasttime = millis();
    }
    Serial.println("Selesai cek repsonse bot input");
    smval = readSuhu();
    val= map(smval,1023,465,0,100);
    if(val<0)val=0;
    else if (val>100)val=100;
    Serial.println("Notif mositure bot");
    if (val < 40.00 && limit==3) {
      String welcome = "Perhatian, tanah kering! \U0001F525";
      welcome += "\n\nSoil Moisture : ";
      welcome += val;
      welcome += "%\nRelay dinyalakan ";
        digitalWrite(buzzer,HIGH);
        delay(500);
        digitalWrite(buzzer,LOW);
        delay(500);
        digitalWrite(buzzer,HIGH);
        delay(500);
        digitalWrite(buzzer,LOW);
        relay1(1);
        Relay = 1;
        Serial.println("Mengirim pesan bot");
        bot.sendMessage(idChat, welcome);
        if (stat == 1){
          stat = 0;
        }
    }else if(val >= 40.00 && stat == 0 && limit==3) {
      String welcome = "Kondisi tanah sudah kembali normal \U00002705";
      welcome += "\n\nSoil Moisture : ";
      welcome += val;
      welcome += "%\nRelay dimatikan ";
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        delay(50);
        digitalWrite(buzzer,HIGH);
        delay(50);
        digitalWrite(buzzer,LOW);
        relay1(0);
        Relay = 0;
        Serial.println("Mengirim pesan bot");
        bot.sendMessage(idChat, welcome);
        stat = 1;
    }
    Serial.println("Notif selesai");
//    delay(100);
    limit++;
    Serial.println(limit);
    if(limit==4){
      post();//upload data to raspberry only happen once in 4 loop
      limit=0;
    }
  }
