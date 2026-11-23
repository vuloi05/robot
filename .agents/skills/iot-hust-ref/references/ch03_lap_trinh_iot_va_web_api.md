# Chương 3: Lập trình thiết bị IoT, Web API & Platform

- **PDF gốc:** `docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf` (*IT4735 IoT và Ứng dụng*, SoICT - HUST, 2025)
- **Phạm vi slide:** 191–291
- **Các mục lớn:** 3.1 Lập trình thiết bị IoT (192–240); 3.2 Xây dựng Web API (241–277); 3.3 Lập trình với IoT Platform (278–291)
- **Ứng dụng vào dự án Robot Nhà Hàng:** Nguyên lý tương tác phần cứng & thiết kế REST/WebSocket API. Lưu ý: code mẫu Java/ThingSpeak chỉ dùng tham khảo khái niệm, dự án code bằng Rust/ESP32.

---

### [Slide 191]

Chương 3. Lập trình ứng dụng IoT
▪ 3.1. Lập trình cho thiết bị IoT (ESP32)
▪ 3.2. Xây dựng Web API (IoT Server)
▪ 3.3. Khai thác dịch vụ IoT Cloud Platform

191

---

### [Slide 192]

3.1. Lập trình cho thiết bị IoT
▪ Các thiết bị dùng vi điều khiển hiệu năng thấp
▪ Kiến trúc 8 bit, hiệu năng thấp, không dùng hệ điều hành
▪ Lập trình firmware, giao tiếp vào ra cơ bản GPIO, ghép nối các ngoại vi
(sensor, actuator) theo các chuẩn truyền thông phổ biến UART, SPI, I2C
▪ Ví dụ: ATmega, PIC, AVR, Arduino

192

---

### [Slide 193]

Lập trình với thiết bị IoT
▪ Các thiết bị dùng Vi xử lý 32 bit, hiệu năng trung bình
▪ Có thể dùng hệ điều hành đơn giản (FreeRTOS, TinyOS, uCLinux, …)
▪ Giao tiếp vào ra cơ bản GPIO, ghép nối các ngoại vi theo các chuẩn truyền
thông phổ biến UART, SPI, I2C
▪ Có thêm khả năng kết nối Wi-Fi, Bluetooth, GSM module,
▪ Ví dụ: ESP8266, ESP32, Arduino Uno WiFi

193

---

### [Slide 194]

Lập trình với thiết bị IoT
▪ Các thiết bị dùng Vi xử lý 32/64 bit, hiệu năng cao
▪ Dùng hệ điều hành (Embedded Linux, Raspbian, Windows Embedded,
Android, Ubuntu, …)
▪ Kết nối Wi-Fi, Ethernet, …
▪ Các giao tiếp ngoại vi qua cơ chế driver trên hệ điều hành
▪ Có thể sử dụng các thư viện trên hệ điều hành (Java, Python, .Net
Framework, OpenCV, …)
▪ Ví dụ: Raspberry Pi

194

---

### [Slide 195]

Lập trình cho thiết bị IoT (ESP32)
▪ Lập trình cho ESP32
▪ https://esp32.vn/index.html
▪ https://randomnerdtutorials.com/projects-esp32/

195

---

### [Slide 196]

Lập trình thiết bị ESP32
▪ A. Môi trường lập trình Arduino IDE
▪ B. Kết nối WiFi cho ESP32
▪ C. Giao tiếp HTTP với ESP32
▪ D. Giao tiếp MQTT với ESP32
▪ E. Lập trình multi-tasks với FreeRTOS

196

---

### [Slide 197]

Môi trường lập trình Arduino IDE
▪ Arduino IDE: Công cụ phát triển phần mềm cho vi điều khiển, máy tính nhúng
▪ https://www.arduino.cc/
▪ Ví dụ: Arduino Uno dùng Vi điều khiển ATmega328
In circuit Serial
programming

Digital output
~: PWM.
0,1: Serial port.

Atmel
MicroController

USB
port

Power input

Power Supply

Analog input.

197

---

### [Slide 198]

Lập trình Arduino
▪ Cài đặt Arduino IDE
▪ https://www.arduino.cc/en/guide/windows

▪ Cấu trúc code
void setup()
{
//Used to indicate the initial values of system on starting.
}
void loop()
{
Contains the statements that will run whenever the system
is powered after setup.
}

198

---

### [Slide 199]

Lập trình Arduino
▪ Program used to code and upload it to
arduino boards (using PC)
▪ Editor (for code edit)
▪ Sketch (piece of program)

199

---

### [Slide 200]

Lập trình Arduino
▪ Tài liệu: Arduino References
▪ http://arduino.cc/en/Reference/HomePage

200

---

### [Slide 201]

Ví dụ 1: Giao tiếp GPIO - Output
▪ LED on/off trên pin 2
void setup() {
// initialize digital pin 2 as an output.
pinMode(2, OUTPUT);
}
void loop() {
digitalWrite(2, HIGH);
delay(1000);
digitalWrite(2, LOW);
delay(1000);
}

// turn the LED on
// wait for a second
// turn the LED off
// wait for a second

201

---

### [Slide 202]

Ví dụ 1: Giao tiếp GPIO - Input
▪ Đọc trạng thái nút bấm trên pin 2, turn on/off trên pin 13
const int buttonPin = 2; // the number of the pushbutton pin
const int ledPin = 13;
// the number of the LED pin
int buttonState = 0;
void setup() {
pinMode(ledPin, OUTPUT);
pinMode(buttonPin, INPUT);
}
void loop() {
// read the state of the pushbutton value:
buttonState = digitalRead(buttonPin);
if (buttonState == HIGH) {
digitalWrite(ledPin, HIGH);
} else {
digitalWrite(ledPin, LOW);
}
delay(100);
}
202

---

### [Slide 203]

Ví dụ 2: Giao tiếp UART
▪ Sử dụng thư viện Serial của Arduino
▪ https://www.arduino.cc/reference/en/language/functions/communication/serial/

int incomingByte = 0;
void setup() {
// opens serial port, sets data rate to 9600 bps
Serial.begin(9600);
}
void loop() {
// send data only when you receive data:
if (Serial.available() > 0) {
// read the incoming byte:
incomingByte = Serial.read();
// say what you got:
Serial.print("I received: ");
Serial.println(incomingByte, DEC);
}
}
203

---

### [Slide 204]

Giao tiếp Serial
void setup() {
// put your setup code here, to run once:
pinMode(2, OUTPUT); //Cau hinh pin 2 la output
Serial.begin(9600);
}
void loop() {
// put your main code here, to run repeatedly:
if(Serial.available() > 0){
int c = Serial.read();
if(c == '0'){
digitalWrite(2, 0);
}
else if(c == '1'){
digitalWrite(2, 1);
}
Serial.print("Toi nhan duoc: ");
Serial.println(c);
}
}
204

---

### [Slide 205]

Ví dụ 3: Giao tiếp I2C
▪ Sử dụng thư viện Wire
▪ https://www.arduino.cc/en/Reference/Wire

▪ Giao tiếp SRFxx Sonic Range Finder
▪ https://www.arduino.cc/en/Tutorial/LibraryExamples/SFRRangerReader

205

---

### [Slide 206]

Thiết lập Arduino IDE cho ESP32
3) Chọn Tools > Board > Boards Manager…

206

---

### [Slide 207]

Thiết lập Arduino IDE cho ESP32
▪ Kết nối bo mạch ESP32 với máy tính
▪ Chọn Board trong Tools > Board menu (ví dụ DOIT ESP32 DEVKIT V1 )

207

---

### [Slide 208]

Kết nối với thiết bị

208

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 208 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 209]

Nạp chương trình cho thiết bị
▪ Upload the Blink Program. This program should blink the LED at an
interval of 1 second.
int LED_BUILTIN = 2;
void setup() {
pinMode (LED_BUILTIN, OUTPUT);
}
void loop() {
digitalWrite(LED_BUILTIN,HIGH);
delay(1000);
digitalWrite(LED_BUILTIN,LOW);
delay(1000);
}

209

---

### [Slide 210]

B. Kết nối Wi-Fi cho ESP32
Ví dụ 1: File > Examples > WiFi (ESP32) > WiFiClientBasic
#include <WiFi.h>
const char* ssid = "yourNetworkName";
const char* password = "yourNetworkPass";

void setup() {
Serial.begin(115200);
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
delay(500);
Serial.println("Connecting to WiFi..");
}
Serial.println("Connected to the WiFi network");
}
void loop() {
}
Ví dụ 2: File > Examples > WiFi (ESP32) > WiFiClient
210

---

### [Slide 211]

Ví dụ kết nối Wi-Fi
▪ Kết quả: Ghi log ra Serial port

211

---

### [Slide 212]

C. Giao tiếp HTTP với ESP32
▪ HTTP request methods: GET vs. POST
▪ HTTP GET:
▪ Sử dụng để request dữ liệu/tài nguyên (get values from APIs)
▪ Dữ liệu được gửi trong URL của GET request
▪ Ví dụ:
GET /update-sensor?temperature=value1
▪ Hoặc get JSON object:
GET /get-sensor

212

---

### [Slide 213]

Giao tiếp HTTP với ESP32
▪ HTTP POST:
▪ Gửi dữ liệu đến server để create/update tài nguyên
▪ Dữ liệu được gửi trong body của POST request
▪ Ví dụ:
POST /update-sensor HTTP/1.1 Host: example.com
api_key=api&sensor_name=name&temperature=value1&humidity=value2&pressure=value3
Content-Type: application/x-www-form-urlencoded

▪ Hoặc gửi JSON object:
POST /update-sensor HTTP/1.1 Host: example.com {api_key: "api",
sensor_name: "name", temperature: value1, humidity: value2, pressure: value3}
Content-Type: application/json

213

---

### [Slide 214]

ESP32 HTTP GET
▪ ESP 32 gửi dữ liệu lên server dùng http get request

https://randomnerdtutorials.com/esp32-http-get-post-arduino/

214

---

### [Slide 215]

ESP32 HTTP GET – Code minh họa
Part 1. Connect WiFi
#include <WiFi.h>
#include <HTTPClient.h>
const char* ssid = "HungiPhone";
const char* password = "hung1234";
String serverName = "https://postman-echo.com/get";
void setup()
{
Serial.begin(115200);
delay(10);
// We start by connecting to a WiFi network
WiFi.begin(ssid, password);
Serial.print("Wait for WiFi... ");
while (WiFi.status() != WL_CONNECTED) {
Serial.println("Connecting to WiFi ...");
delay(1000);
}
Serial.println("WiFi connected");
Serial.println("IP address: ");
Serial.println(WiFi.localIP());
delay(500);
}
215

---

### [Slide 216]

ESP32 HTTP GET – Code minh họa
void loop()
{
Part 2. Send http GET request
if (WiFi.status() == WL_CONNECTED) {
HTTPClient http;
String serverPath = serverName + "?temp1=24.7&temp2=30";
// Your Domain name with URL path or IP address with path
http.begin(serverPath.c_str()); // Send HTTP GET request
int httpResponseCode = http.GET();
if (httpResponseCode > 0) {
Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
String payload = http.getString();
Serial.println(payload);
}
else {
Serial.print("Error code: "); Serial.println(httpResponseCode);
}
http.end();
}
else {
Serial.println("WiFi Disconnected");
}
delay(3000);
}
216

---

### [Slide 217]

ESP32 HTTP GET – Mô phỏng trên Wokwi

217

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 217 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 218]

#include <WiFi.h>
#include <HTTPClient.h>
String serverName = "https://postman-echo.com/get";
void setup() {
//setup for serial communication
Serial.begin(9600);
Serial.print("Connecting to WiFi");
//setup for WiFi connection
WiFi.begin("Wokwi-GUEST", "", 6);
while (WiFi.status() != WL_CONNECTED) {
delay(100);
Serial.print(".");
}
Serial.println("WiFi Connected!");
}
void loop() {
if (WiFi.status() == WL_CONNECTED) {
HTTPClient http;
String serverPath = serverName + "?temp=24.7&humid=30";
http.begin(serverPath.c_str()); // Send HTTP GET request
int httpResponseCode = http.GET();
if (httpResponseCode > 0) {
Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
String payload = http.getString();
Serial.println(payload);
}
else {
Serial.print("Error code: "); Serial.println(httpResponseCode);
}
http.end();
}
else {
Serial.println("WiFi Disconnected");
}
delay(3000);
}

218

---

### [Slide 219]

ESP32 HTTP Get

219

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 219 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 220]

ESP32 HTTP Get

220

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 220 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 221]

ESP32 HTTP Get

221

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 221 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 222]

ESP32 HTTP Get

222

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 222 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 223]

ESP32 HTTP Get

223

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 223 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 224]

ESP32 HTTP Get

224

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 224 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 225]

ESP32 HTTP POST
▪ Gửi dữ liệu dùng:
▪ URL encoded (đóng gói trong URL)
▪ JSON object (đóng gói trong request body)
▪ Plain text

Tham khảo code: https://randomnerdtutorials.com/esp32-http-get-post-arduino/

225

---

### [Slide 226]

ESP32 HTTP POST
▪ POST dữ liệu với URL encoded
POST /update-sensor HTTP/1.1 Host: 192.168.1.106:1880
api_key=tPmAT5Ab3j7F9&sensor=BME280&value1=24.25&value2=49.54&value3=1005.14 ContentType: application/x-www-form-urlencoded
// Your Domain name with URL path or IP address with path
http.begin(serverName);
// Specify content-type header
http.addHeader("Content-Type", "application/x-www-form-urlencoded");
// Data to send with HTTP POST
String httpRequestData =
"api_key=tPmAT5Ab3j7F9&sensor=BME280&value1=24.25&value2=49.54&value3=1005.14";
// Send HTTP POST request
int httpResponseCode = http.POST(httpRequestData);

226

---

### [Slide 227]

ESP32 HTTP POST
▪ Post JSON object
POST /update-sensor HTTP/1.1 Host: example.com {api_key: "tPmAT5Ab3j7F9", sensor_name: "BME280",
temperature: 24.25; humidity: 49.54; pressure: 1005.14} Content-Type: application/json
http.addHeader("Content-Type", "application/json");
int httpResponseCode =
http.POST("{\"api_key\":\"tPmAT5Ab3j7F9\",\"sensor\":\"BME280\",\"value1\":\"24.25\",\"value2\":\"49
.54\",\"value3\":\"1005.14\"}");

▪ Post Plain Text
http.addHeader("Content-Type", "text/plain");
int httpResponseCode = http.POST("Hello, World!");

227

---

### [Slide 228]

Ví dụ: HTTP post url-encoded
#include <WiFi.h>
#include <HTTPClient.h>
String serverName = "https://postman-echo.com/post";
void setup() {
//setup for serial communication
//setup for WiFi connection
}
void loop() {
if (WiFi.status() == WL_CONNECTED) {
HTTPClient http;
float x = 30.5;
float y = 78;
http.begin(serverName);
http.addHeader("Content-Type", "application/x-www-form-urlencoded");
String httpRequestData = "field1=" + String(x) + "&field2=" + String(y);
Serial.println(httpRequestData);
int httpResponseCode = http.POST(httpRequestData);
if (httpResponseCode > 0) {
Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
String payload = http.getString();
Serial.println(payload);
}
else {
Serial.print("Error code: "); Serial.println(httpResponseCode);
}
http.end();
}
else {
Serial.println("WiFi Disconnected");
}
delay(3000);
}

228

---

### [Slide 229]

Ví dụ: HTTP post json object
void loop() {
if (WiFi.status() == WL_CONNECTED) {
HTTPClient http;
float x = 30.5;
float y = 78;
int motion = 1;
http.begin(serverName);
http.addHeader("Content-Type", "application/json");
String httpRequestData = "{\"value1\": 24.25,\"value2\": 49.54, \"motion\":1 }";
//String httpRequestData = "{\"temperature\": " + String(x) +",\"humidity\": " + String(y) +
",\"motion\": " + String(motion) + "}";
Serial.println(httpRequestData);
int httpResponseCode = http.POST(httpRequestData);
if (httpResponseCode > 0) {
Serial.print("HTTP Response code: "); Serial.println(httpResponseCode);
String payload = http.getString();
Serial.println(payload);
}
else { Serial.print("Error code: "); Serial.println(httpResponseCode); }
http.end();
}
else { Serial.println("WiFi Disconnected");}
delay(3000);
}
229

---

### [Slide 230]

Sử dụng thư viện Arduino JSON
▪ Sketch > Include Library > Manage Libraries
▪ Add thư viện trên Arduino Library Manager

230

---

### [Slide 231]

Sử dụng thư viện Arduino JSON
▪ https://arduinojson.org/v6/example/string/

231

---

### [Slide 232]

Bài tập
▪ Bài 5. Lập trình ESP32 gửi dữ liệu HTTP

232

---

### [Slide 233]

ESP32 Web server
▪ Xây dựng một web server đơn giản trên ESP32, điều khiển GPIO
▪ Ví dụ:
▪ https://randomnerdtutorials.com/esp32-web-server-arduino-ide/

233

---

### [Slide 234]

ESP32 Web server

234

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 234 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 235]

D. Giao tiếp MQTT với ESP32
▪ Sử dụng thư viện mqtt PubSubClient cho Arduino
▪ https://www.arduinolibraries.info/libraries/pub-sub-client
▪ https://github.com/knolleary/pubsubclient

235

---

### [Slide 236]

Giao tiếp MQTT với ESP32/ESP8266
▪ Tham khảo mã nguồn:
▪ https://github.com/knolleary/pubsubclient/blob/master/examples/mqtt_esp8266/mqtt_esp8
266.ino
#include <ESP8266WiFi.h>
//Hoặc #include <WiFi.h>
#include <PubSubClient.h>
WiFiClient espClient;
PubSubClient client(espClient);
const char* mqtt_server = "broker.mqtt-dashboard.com";
void setup_wifi() { …}
void callback(char* topic, byte* payload, unsigned int length) { …}
void reconnect() { …}
void setup() {
Serial.begin(115200);
setup_wifi();
client.setServer(mqtt_server, 1883);
client.setCallback(callback);
}
void loop() { … }
236

---

### [Slide 237]

E. Lập trình multi-task với FreeRTOS
▪ FreeRTOS multi-tasking

237

---

### [Slide 238]

Lập trình multi-task với FreeRTOS
▪ Create a task

xTaskCreate(
BlinkLED, // Function that should be called
“Blink LED", // Name of the task (for debugging)
1024, // Stack size (bytes)
NULL, // Parameter to pass
1, // Task priority
NULL// Task handle );

238

---

### [Slide 239]

Lập trình multi-task với FreeRTOS
▪ Hàm xử lý của task
void BlinkLED(void * parameter){

for(;;){ // infinite loop
// Turn the LED on
digitalWrite(led1, HIGH);
// Pause the task for 500ms
vTaskDelay(500 / portTICK_PERIOD_MS);
// Turn the LED off
digitalWrite(led1, LOW);
// Pause the task again for 500ms
vTaskDelay(500 / portTICK_PERIOD_MS);
}
}
239

---

### [Slide 240]

Programming multi-task with FreeRTOS
void BlinkLED( void *pvParameters );
void setup(){
//Create the task 1 to run BlinkLED
xTaskCreate(
BlinkLED,
// Function that should be called
"Blink LED",
// Name of the task (for debugging)
1024,
// Stack size (bytes)
NULL,
// Parameter to pass
1,
// Task priority
NULL
// Task handle
);
}
void BlinkLED( void *pvParameters ){//The function for Task 1
for(;;){ // infinite loop
digitalWrite(led1, HIGH);
vTaskDelay(500 / portTICK_PERIOD_MS);
digitalWrite(led1, LOW);
vTaskDelay(500 / portTICK_PERIOD_MS);
Serial.println("LED is blinking ...");
}
}
240

---

### [Slide 241]

3.2. Xây dựng Web API
3.2.1. Công nghệ .Net Core, Entity Framework
3.2.2. Công nghệ NodeJS, MongoDB

241

---

### [Slide 242]

3.2.1. Xây dựng Web API với .NET Core
▪ Sử dụng công nghệ ASP.NET Core và Entity Framework để xây dựng
Web API cho ứng dụng IoT

242

---

### [Slide 243]

RESTful API
▪ REST = REpresentational State Transfer: Các trạng thái tài nguyên
được truyền tải qua HTTP
▪ Tiêu chuẩn dùng trong thiết kế Web API

243

---

### [Slide 244]

RESTful API
▪ Dựa trên giao thức HTTP. Sử dụng các phương thức http
• GET: Lấy về (READ) một tài nguyên cụ thể (by Id) hoặc một danh sách tài
nguyên (Resource).
• POST: Tạo mới (CREATE) một tài nguyên.
• PUT: Cập nhật (UPDATE) thông tin cho 1 tài nguyên (by Id).
• DELETE: Xóa (DELETE) 1 tài nguyên (by Id).

244

---

### [Slide 245]

Tạo Web API project
▪ Open File/New/Project in Visual Studio

https://medium.com/net-core/how-to-build-a-restful-api-with-asp-net-core-fb7dd8d3e5e3

245

---

### [Slide 246]

Tạo Web API project
▪ Chọn .NET Core, ASP.NET Core 2.2, API Project

246

---

### [Slide 247]

Tạo Web API project
▪ Project WebAPIDemo

247

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 247 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 248]

Tạo Web API project
▪ MVC (Model-View-Controller) được thêm trong Startup.cs

248

---

### [Slide 249]

Routing and URL paths
▪ Run app (Ctrl + F5), sử dụng IIS Express (MS webserver)
▪ Kết quả demo trên trình duyệt

249

---

### [Slide 250]

Routing and URL paths
▪ URL mặc định https://localhost:{port}/api/values được thiết lập trong thuộc
tính launchUrl trong file Properties\launchSettings.json
▪ Values nhận được trên trình duyệt được mặc định trong phương thức Get của
ValuesController

250

---

### [Slide 251]

Tạo một model
▪ Xây dựng data model class (Model trong kiến trúc MVC)
▪ In Solution Explorer, right-click the project. Select Add > New Folder and
name the folder Models.
▪ Then right-click the Models folder and select Add->Class. Name the
class SensorData.cs and click Add.

251

---

### [Slide 252]

Tạo một model
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;
namespace WebAPIDemo.Models
{
public class SensorData
{
public int Id { get; set; }
[Required] //Data Annotation
[StringLength(60, MinimumLength = 3)]
public string Name { get; set; }
public float Value { get; set; }
[DataType(DataType.Date)]
public DateTime ReceiveTime { get; set; }
}
}
252

---

### [Slide 253]

Tạo một controller
▪ Tạo một controller (thành phần Controller trong mô hình MVC), gắn với
SensorData model
▪ Sử dụng Entity Framework Core (EF Core) để làm việc với database

253

---

### [Slide 254]

Tạo một controller

254

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 254 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 255]

Tạo một controller
▪ Công cụ scaffolding của .NET Core hỗ trợ tự động sinh code
▪ The automatic creation of the database context and CRUD (Create,
Read, Update, and Delete) action methods is known as scaffolding.

255

---

### [Slide 256]

Controller Class
▪ Ví dụ SensorDatasController class với các methods:
▪ GetSensorData (GET method)
▪ PostSensorData (POST method)
▪ PutSensorData (PUT method)
▪ DeleteSensorData (DELETE method)

▪ Controller class kế thừa từ ControllerBase
public class SensorDatasController : ControllerBase

256

---

### [Slide 257]

Thêm controller

SensorDatasController.cs

257

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 257 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 258]

EF Core Database Context
▪ Data\WebAPIDemoContext.cs
▪ WebAPIDemoContext kết nối với các chức năng của EF Core (Create,
Read, Update, Delete, etc.) cho SensorData model
▪ WebAPIDemoContext kế thừa từ
Microsoft.EntityFrameworkCore.DbContext.

258

---

### [Slide 259]

EF Core Database Context
▪ In Entity Framework terminology, an entity set typically
corresponds to a database table and an entity corresponds to a
row in the table.
▪ ASP.NET Core configuration system reads the connection string
from the appsettings.json file:

259

---

### [Slide 260]

EF Core Database Context
▪ Đăng ký DB Context (WebAPIDemoContext) trong Startup.cs

Inject the database context (WebAPIDemoContext) into the controller:

260

---

### [Slide 261]

Tạo database sử dụng Migrations
▪ Sử dụng Entity Framework code first
▪ Công cụ Migrations tạo (create) database tương ứng với data model
được xây dựng (code first) và cập nhật (update) database schema khi
có thay đổi của data model
▪ Chạy các lệnh của công cụ Migrations:
▪ Mở Tools -> NuGet Package Manager > Package Manager Console (PMC), thực hiện
command:
▪ Add-Migration Initial (Tạo database)
▪ Update-Database (Cập nhật database schema)

261

---

### [Slide 262]

Tạo database sử dụng Migrations
▪ Migration files được sinh tự động trong Migration folder

262

---

### [Slide 263]

Tạo database sử dụng Migrations
▪ Chạy lệnh Update-Database (trong PMC)
▪ Phương thức Up trong file Migrations/{time-stamp}_Initial.cs sẽ được thực
thi và tạo database
▪ Mở SQL Server Object Explorer

263

---

### [Slide 264]

Tạo database
▪ Thêm dữ liệu vào bảng SensorData
▪ Mở SQL Server Object Explorer, chuột phải vào bảng SensorData, chọn
View Data để thêm bản ghi

264

---

### [Slide 265]

GET method
▪ GetSensorData(): trả về tất cả bản ghi trong SensorData database
▪ GetSensorData(int id): trả về bản ghi Id tương ứng
▪ [HttpGet] phương thức xử lý khi có HTTP GET request

265

---

### [Slide 266]

GET method
▪ GET endpoints:
▪ GET /api/SensorData
▪ GET /api/SensorData/{id}

▪ Gọi HTTP GET request từ trình duyệt:
▪ https://localhost:{port}/api/SensorDatas
▪ https://localhost:{port}/api/SensorDatas/2

▪ Kiểu giá trị trả về ActionResult<T> type
▪ .NET Core tự động serializes object thành JSON và ghi vào body của gói tin
response
▪ Respone code: 200 (nếu không có unhandled exceptions), nếu có sẽ trả về
mã lỗi 5xx
266

---

### [Slide 267]

GET method
▪ Kiểm thử trên trình duyệt

267

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 267 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 268]

GET method
▪ URL mặc định: Cấu hình launchUrl trong file launchsettings.json

268

---

### [Slide 269]

POST method
▪ Hàm PostSensorData tạo một bản ghi mới trong database
▪ Dữ liệu (bản ghi) được gửi trong body của HTTP POST request
▪ Hàm CreatedAtAction:
▪ Trả về mã HTTP 201 nếu thành công

269

---

### [Slide 270]

Kiểm thử dùng Postman
▪ GET method: get all resource

270

---

### [Slide 271]

Kiểm thử dùng Postman
▪ GET method: get 1 resource by Id

271

---

### [Slide 272]

Kiểm thử dùng Postman
▪ POST method

272

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 272 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 273]

PUT method
▪ Phương thức PutSensorData() cập nhật một bản ghi

273

---

### [Slide 274]

PUT method
▪ Mã trả về: HTTP 204 (No Content)

274

---

### [Slide 275]

DELETE method
▪ Xóa một bản ghi (by Id)

275

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 275 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 276]

DELETE method
▪ Xóa một bản ghi (by Id)
▪ Mã trả về HTTP OK 200 (xóa thành công)

276

---

### [Slide 277]

3.2.2. Công nghệ NodeJS, MongoDB
•

https://viblo.asia/p/xay-dung-restful-api-don-gian-voi-nodejs-1Je5EdewlnL
https://viblo.asia/p/tao-rest-api-voi-spring-boot-mysql-jpa-repository-Eb85oJykl2G

---

### [Slide 278]

3.3. Lập trình với IoT Platform
▪ Các dịch vụ:
▪ Tiếp nhận dữ liệu (Collecting, Ingesting data)
▪ Lưu trữ dữ liệu (Cloud Storage, Database)
▪ Trình bày dữ liệu (Data Representation),
▪ Theo dõi giám sát, điều khiển (Dashboard)

▪ Thingsboard - open-source IoT platform for data collection,
processing, visualization, and device management
▪

https://thingsboard.io/

278

---

### [Slide 279]

Case study: Hệ thống kiểm soát vào ra
▪ Kiến trúc hệ thống: Khai thác ThingsBoard IoT platform

MQTT
Broker
publish/subscribe

Sensors
IoT Device
Actuators

DashBoard
(Administration)

http request

Server
(IoT cloud platform)

http response

User App

ThingsBoard IoT Platform

279

---

### [Slide 280]

3.3.1. Đăng ký thiết bị
▪ Device Provisioning: Thiết bị thực hiện đăng ký qua MQTT API

280

---

### [Slide 281]

Đăng ký thiết bị
▪ Device Provisioning: Thiết bị thực hiện đăng ký qua MQTT API

https://thingsboard.io/docs/user-guide/device-provisioning/

281

---

### [Slide 282]

Đăng ký thiết bị
▪ Step 1. Thiết bị kết nối tới ThingsBoard MQTT broker, sử dụng
username = “provision”
▪ Step 2. Thiết bị gửi provision request lên server bằng cách publish lên
topic /provision/request
{
"deviceName": "DEVICE_NAME",
"provisionDeviceKey": "PUT_PROVISION_KEY_HERE",
"provisionDeviceSecret": "PUT_PROVISION_SECRET_HERE"
}

282

---

### [Slide 283]

Đăng ký thiết bị
▪ provisionDeviceKey và provisionDeviceSecret được tạo trên
ThingsBoard tương ứng với Tenant (dự án)

283

---

### [Slide 284]

Đăng ký thiết bị
▪ Step 3. Thiết bị nhận phản hồi của server bằng cách subscribe topic
/provision/response
{
"status":"SUCCESS",
"credentialsType":"ACCESS_TOKEN",
"credentialsValue":"sLzc0gDAZPkGMzFVTyUY"
}

Kết quả: Thiết bị nhận được ACCESS_TOKEN sẽ dùng để xác thực cho
các yêu cầu giao tiếp tiếp theo
284

---

### [Slide 285]

Đăng ký thiết bị
▪ Bài tập 1. Viết chương trình (java, python) thực hiện đăng ký một
thiết bị (IoT device) với ThingsBoard IoT platform
▪ https://thingsboard.io/docs/user-guide/device-provisioning/

285

---

### [Slide 286]

3.3.2. Gửi dữ liệu từ thiết bị IoT lên server (ThingsBoard)
▪ (1) Gửi dữ liệu bằng MQTT API
▪ Thiết bị thực hiện gửi dữ liệu thông qua MQTT Device API
▪ Tài liệu: https://thingsboard.io/docs/reference/mqtt-api/

▪ (2) Gửi dữ liệu bằng HTTP API
▪ Thiết bị thực hiện gửi dữ liệu thông qua HTTP Device API
▪ Tài liệu: https://thingsboard.io/docs/reference/http-api/

286

---

### [Slide 287]

Gửi dữ liệu bằng MQTT API
▪ Thiết bị kết nối với ThingsBoard MQTT broker
▪ Sử dụng username = $ACCESS_TOKEN

▪ Thiết bị gửi dữ liệu (telemetry data) lên server bằng cách publish gói
dữ liệu lên topic
▪ v1/devices/me/telemetry

▪ Dữ liệu được đóng gói bằng json data
▪ Ví dụ:
{"ts":1451649600512, "values":{"key1":"value1", "key2":"value2"}}

287

---

### [Slide 288]

Gửi dữ liệu bằng MQTT API
▪ Bài tập 2. Viết chương trình (Java, python) thực hiện gửi dữ liệu
(json) từ thiết bị lên ThingsBoard server sử dụng MQTT

288

---

### [Slide 289]

Gửi dữ liệu bằng HTTP API
▪ Telemetry upload API:
▪ Thiết bị gửi POST request đến url:
▪ http(s)://$THINGSBOARD_HOST_NAME/api/v1/$ACCESS_TOKEN/telemetry

▪ $ACCESS_TOKEN của thiết bị thực hiện gửi

289

---

### [Slide 290]

Gửi dữ liệu bằng HTTP API
▪ Bài tập 3. Viết chương trình (Java, python) thực hiện gửi dữ liệu từ
thiết bị lên ThingsBoard server qua HTTP API

290

---

### [Slide 291]

Nội dung
▪ Chương 1. Tổng quan về IoT
▪ Chương 2. Các công nghệ IoT
▪ Chương 3. Lập trình ứng dụng IoT
▪ Chương 4. An toàn và Bảo mật IoT
▪ Chương 5. Thiết kế và xây dựng hệ thống IoT

291
