#include <HTTPClient.h>
#include <WiFi.h>
const char* SSID="ODISEA 2.4G.";
const char* PSSWRD="Green2050";
String user="";
String pass="";
String EFF1="1";
String EFF2="0";
String EFF3="0";
String OnHour="23:15:40";
String Offhour="23:35:40";
String ID="1342000";
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);


  WiFi.begin(SSID, PSSWRD);

  Serial.print("Conectando...");
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(500);
    Serial.print(".");
  }

  Serial.print("Conectado con éxito, mi IP es: ");
  Serial.println(WiFi.localIP());

}

void loop() {
if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status

    HTTPClient http;
    String datos_a_enviar = "id=" + ID;
    http.begin("http://192.168.5.102:8000/On");        //Indicamos el destino
    http.addHeader("Content-Type", "application/json"); //Preparamos el header text/plain si solo vamos a enviar texto plano sin un paradigma llave:valor.
    //http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    String Data="{\"id\":\""+ID+"\",\"EFF1\":\""+EFF1+"\",\"EFF2\":\""+EFF2+"\",\"EFF3\":\""+EFF3+"\",\"OnHour\":\""+OnHour+"\",\"Offhour\":\""+Offhour+"\"}";
    Serial.println(Data);
    //+"\",\"EFF1\":\""+EFF1+"\",\"EFF2\":\""+EFF2+"\",\"EFF3\":\""+EFF3+"\",\"OnHour\":\""+OnHour+"\",\"Offhour\":\""+Offhour"    
    int codigo_respuesta = http.POST(Data); 
    //int codigo2=http.POST("{\"EFF1\":\"1\"}");  //Enviamos el post pasándole, los datos que queremos enviar. (esta función nos devuelve un código que guardamos en un int)
    //int codigo_respuesta = http.POST("{\"id\":\"1234512\"}");
    //int codigo_respuesta = http.POST(datos_a_enviar);   //Enviamos el post pasándole, los datos que queremos enviar. (esta función nos devuelve un código que guardamos en un int)

    if(codigo_respuesta>0){
      Serial.println("Código HTTP ► " + String(codigo_respuesta));   //Print return code

      if(codigo_respuesta == 200){
        String cuerpo_respuesta = http.getString();
        Serial.println("El servidor respondió ▼ ");
        Serial.println(cuerpo_respuesta);

      }

    }else{

     Serial.print("Error enviando POST, código: ");
     Serial.println(codigo_respuesta);

    }

    http.end();  //libero recursos

  }else{

     Serial.println("Error en la conexión WIFI");

  }

   delay(2000);
}

