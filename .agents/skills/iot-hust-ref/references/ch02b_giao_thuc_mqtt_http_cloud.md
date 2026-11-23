# Chương 2 (Phần B): Giao thức IoT (HTTP, MQTT, AMQP) & Cloud Platform

- **PDF gốc:** `docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf` (*IT4735 IoT và Ứng dụng*, SoICT - HUST, 2025)
- **Phạm vi slide:** 92–190
- **Các mục lớn:** 2.3 Giao thức ứng dụng IoT: HTTP, MQTT, AMQP (92–178); 2.4 IoT Cloud Platform (179–190)
- **Ứng dụng vào dự án Robot Nhà Hàng:** Cốt lõi cho tầng MQTT Broker (Pub/Sub, QoS 0/1/2, Retain, LWT) và so sánh lý thuyết MQTT vs HTTP trong luận văn.

---

### [Slide 92]

2.3. Một số giao thức cho ứng dụng IoT

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 92 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 93]

Một số giao thức cho ứng dụng IoT
•
•
•

HTTP, HTTPS
MQTT (Message Queue Telemetry Transport)
AMQP (Avanced Message Queue Protocol)

https://www.postscapes.com/internet-of-things-technologies/

---

### [Slide 94]

2.3.1. Trao đổi dữ liệu dùng HTTP
HTTP = HyperText Transfer Procol

---

### [Slide 95]

Ví dụ 1: Trao đổi dữ liệu sử dụng http với ThingSpeak server
▪ Viết 1 chương trình java gửi dữ liệu đến ThingSpeak server
▪ a) Dữ liệu được đóng gói trong url (url-encoded)
▪ GET https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5&field1=20&field2=33

95

---

### [Slide 96]

Ví dụ 1.a): Gửi dữ liệu trong url-encoded
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
public class App {
public static void main(String[] args) {
try {
// URL của API
String url =
"https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5&field1=21&field2=79";
// Tạo đối tượng URL
URL obj = new URL(url);
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
// Thiết lập phương thức GET
con.setRequestMethod("GET");
// Kiểm tra mã phản hồi
int responseCode = con.getResponseCode();
System.out.println("Response Code: " + responseCode);
96

---

### [Slide 97]

Ví dụ 1.a): Gửi dữ liệu trong url-encoded
// Đọc phản hồi từ server
BufferedReader in = new BufferedReader(new
InputStreamReader(con.getInputStream()));
String inputLine;
StringBuilder response = new StringBuilder();
while ((inputLine = in.readLine()) != null) {
response.append(inputLine);
}
in.close();
// In kết quả phản hồi
System.out.println("Response: " + response.toString());

} catch (Exception e) {
e.printStackTrace();
}
}
}
97

---

### [Slide 98]

Ví dụ 1.a): Gửi dữ liệu trong url-encoded

98

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 98 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 99]

Ví dụ 1.a): Gửi dữ liệu trong url-encoded

99

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 99 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 100]

Ví dụ 1.a): Gửi dữ liệu trong url-encoded

100

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 100 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 101]

Ví dụ 1.a): Gửi dữ liệu trong url-encoded

101

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 101 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 102]

Ví dụ 1.a): Gửi dữ liệu trong url-encoded

102

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 102 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 103]

Ví dụ 1: Trao đổi dữ liệu sử dụng http với ThingSpeak server
▪ Viết 1 chương trình java gửi dữ liệu đến ThingSpeak server
▪ b) Gửi dữ liệu được đóng gói trong request body (json data)
▪ POST
https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5
▪ Ví dụ: request body. { "field1": 20, "field2": 33 }

103

---

### [Slide 104]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
public class App {
public static void main(String[] args) {
try {
// URL với API key
URL url = new
URL("https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5");
// Mở kết nối
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
// Thiết lập phương thức POST và định dạng JSON
conn.setRequestMethod("POST");
conn.setRequestProperty("Content-Type", "application/json");
conn.setDoOutput(true);
104

---

### [Slide 105]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body
// Nội dung JSON cần gửi
String jsonData = "{\"field1\": 20, \"field2\": 33}";
// Gửi dữ liệu JSON vào body request
try (OutputStream os = conn.getOutputStream()) {
byte[] input = jsonData.getBytes("utf-8");
os.write(input, 0, input.length);
}
// Lấy mã phản hồi
int responseCode = conn.getResponseCode();
System.out.println("Response Code: " + responseCode);
if (responseCode == HttpURLConnection.HTTP_OK) {
System.out.println("Gửi dữ liệu thành công lên ThingSpeak.");
} else {
System.out.println("Gửi dữ liệu thất bại.");
}
conn.disconnect();
} catch (Exception e) {
e.printStackTrace();
}
}

}
105

---

### [Slide 106]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body

106

---

### [Slide 107]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body

107

---

### [Slide 108]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body

108

---

### [Slide 109]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body

109

---

### [Slide 110]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body

110

---

### [Slide 111]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body

111

---

### [Slide 112]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body

112

---

### [Slide 113]

Ví dụ 1.b): Gửi dữ liệu json đóng gói trong request body
▪ Bổ sung: Đọc nội dung phản hồi từ server (http response)

113

---

### [Slide 114]

Gửi dữ liệu http bằng chương trình python
import requests
import json
# URL của ThingSpeak kèm theo API key
url = "https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5"
# Dữ liệu JSON cần gửi
data = {
"field1": 20,
"field2": 33
}
# Gửi POST request
response = requests.post(url, json=data)
# In mã phản hồi và nội dung phản hồi
print("Response Code:", response.status_code)
print("Response Body:", response.text)
# Kiểm tra kết quả
if response.status_code == 200:
print("Gửi dữ liệu thành công.")
else:
print("Gửi dữ liệu thất bại.")
114

---

### [Slide 115]

Gửi dữ liệu http bằng chương trình python

115

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 115 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 116]

Ví dụ 2: Hệ thống Smart Locker giao tiếp dữ liệu sử dụng http

Server back-end
& Web front-end

Application on
Android device
controller

Lockers
Controller
(ATmega2560)

Locker
RFID tag
reader
Hệ thống Smart Locker

---

### [Slide 117]

Ví dụ 2: Hệ thống Smart Locker giao tiếp dữ liệu sử dụng http (1)
• Sử dụng thư viện HttpURLConnection trên Java thực hiện một http request tới http
REST api
• Bước 1: Tạo một kết nối http connection, thiết lập các thuộc tính cho request
public String requestUserInfor(String devId, String qrDevId, String qrCode, int
timeout){
String result = "";
try {
String urlApi =
"https://203.171.20.94:8080/api/AccessControl/GetUserInfor";
URL url = new URL(urlApi);
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("POST");
conn.setConnectTimeout(timeout);
conn.setReadTimeout(timeout);
conn.setRequestProperty("Content-Type", "application/json; charset=utf-8");

---

### [Slide 118]

Ví dụ 2: Hệ thống Smart Locker giao tiếp dữ liệu sử dụng http (2)
▪ Bước 2: Ghi dữ liệu cần gửi vào luồng output stream của request. Dữ liệu có
thể được đóng gói bằng JSON
...
OutputStream os = conn.getOutputStream();
BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
JSONObject jsonObj = new JSONObject();
try {
jsonObj.accumulate("deviceId", devId);
jsonObj.accumulate("qrCodeId", qrDevId);
jsonObj.accumulate("qrCodeValue", qrCode);
} catch (JSONException e) {
e.printStackTrace();
}
writer.write(jsonObj.toString());
writer.flush();
writer.close();
os.close();
conn.connect();
118

---

### [Slide 119]

Ví dụ 2: Hệ thống Smart Locker giao tiếp dữ liệu sử dụng http (3)
▪ Bước 3: Nhận phản hồi http response từ server. Kiểm tra mã trả về và đọc dữ
liệu từ luồng input stream của http response
...
StringBuffer sb = new StringBuffer();
if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
InputStream in = conn.getInputStream();
int chr;
while ((chr = in.read()) != -1) {
sb.append((char) chr);
}
in.close();
} else {
sb.append(conn.getResponseCode());
}
result = sb.toString();
conn.disconnect();

}
catch(IOException e){
e.printStackTrace();
}
return result;
}

119

---

### [Slide 120]

Sử dụng công cụ Postman

120

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 120 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 121]

Http Response code
▪ 200: OK
▪ 201: Created
▪ 204: No Content
▪ 401: Unauthorized
▪ 403: Forbidden
▪ 404: Not Found
▪ 408: Request Timeout
▪ 500: Internal Server Error
▪ 502: Bad Gateway
▪ 503: Service Unavailable
121

---

### [Slide 122]

Bài tập 1. Trao đổi dữ liệu qua HTTP
Yêu cầu. Viết chương trình (bằng ngôn ngữ tùy ý: C#, Java, python) thực hiện
a) Gửi dữ liệu gồm 2 trường field1, field2 lên Thinkspeak qua API theo 2 cách:

Cách 1. Các trường field1, field2 được đóng gói trong url (urlencoded)
GET https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5&field1=20&field2
=33

Cách 2. Các trường field1, field2 được đóng gói trong body request bằng json.
POST https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5
Ví dụ: body request.
{
"field1": 20,
"field2": 33
}
122

---

### [Slide 123]

Bài tập 1. Trao đổi dữ liệu qua HTTP
Yêu cầu. Viết chương trình (bằng ngôn ngữ tùy ý: C#, Java, python) thực hiện
b) Lấy dữ liệu về từ Thingspeak API

GET https://api.thingspeak.com/channels/1529099/feeds.json?results=2
Parsing dữ liệu gửi về để lấy ra 2 trường field1 (temperature) và field2 (humidity) và hiển thị ra màn hình.

123

---

### [Slide 124]

2.3.2. Trao đổi dữ liệu dùng MQTT
▪ The Messaging and Data Exchange Protocol of the IoT
▪ MQTT (Message Queuing Telemetry Transport):
▪ Giao thức truyền thông điệp (message) theo mô hình publish/subscribe
(xuất bản – theo dõi)
▪ Sử dụng băng thông thấp, độ tin cậy cao và có khả năng hoạt động trong
điều kiện đường truyền không ổn định.

124

---

### [Slide 125]

Giao thức MQTT
▪ Kiến trúc mức cao của MQTT gồm 2 thành phần chính:
▪ Broker
▪ Clients

125

---

### [Slide 126]

Giao thức MQTT
▪ Publish/Subscribe:
▪ Trong một hệ thống sử dụng giao thức MQTT, nhiều node trạm (gọi là mqtt
client – gọi tắt là client) kết nối tới một MQTT server (gọi là broker).
▪ Mỗi client sẽ đăng ký một vài kênh (topic), ví dụ như
“/client1/channel1”, “/client1/channel2”. Quá trình đăng ký này gọi là
“subscribe”. Mỗi client sẽ nhận được dữ liệu khi bất kỳ trạm nào khác gửi
dữ liệu vào kênh đã đăng ký.
▪ Khi một client gửi dữ liệu tới kênh đó, gọi là “publish”.

126

---

### [Slide 127]

Giao thức MQTT

https://www.hivemq.com/mqtt-essentials/

---

### [Slide 128]

Giao thức MQTT
▪ QoS (Quality of Service):
▪ Có 3 tùy chọn QoS khi “publish” và “subscribe”:
▪ QoS0 Broker/client sẽ gửi dữ liệu đúng 1 lần, quá trình gửi được
xác nhận bởi chỉ giao thức TCP/IP, (“fire and forget”).
▪ QoS1 Broker/client sẽ gửi dữ liệu với ít nhất 1 lần xác nhận từ đầu
kia, nghĩa là có thể có nhiều hơn 1 lần xác nhận đã nhận được dữ
liệu.
▪ QoS2 Broker/client đảm bảo khi gửi dữ liệu thì phía nhận chỉ nhận
được đúng 1 lần, quá trình này phải trải qua 4 bước bắt tay

128

---

### [Slide 129]

Giao thức MQTT
▪ Sử dụng công cụ client: MQTTBox
▪ https://www.hivemq.com/mqtt-toolbox/
▪ Publish/Subscribe (gửi/nhận) dữ liệu

129

---

### [Slide 130]

Công cụ mqtt client: MQTTBox

130

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 130 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 131]

Thư viện MQTT client
▪ Thư viện mqtt client cho các nền tảng khác nhau:
▪ https://www.hivemq.com/mqtt-client-library-encyclopedia/

131

---

### [Slide 132]

Ví dụ:
▪ Chương trình Java thực hiện publish/subscribe (gửi/nhận) dữ liệu sử dụng thư
viện Paho MQTT Client
▪ Thư viện Paho Mqtt Client
▪ https://eclipse.dev/paho/downloads/

▪ Using the Paho Java Client:
▪ Using Maven dependency
▪ Hoặc add thư viện .jar (Build Path >> Add External Archives):
Download file thư viện: org.eclipse.paho.client.mqttv3-1.1.1.jar

132

---

### [Slide 133]

Chương trình MQTT Example
package mqttDemo;
import org.eclipse.paho.client.mqttv3.*;

public class MqttExample {
private static final String BROKER = "tcp://broker.emqx.io:1883";
private static final String TOPIC = “test/topic";
private static final String CLIENT_ID = "JavaClientExample";
public static void main(String[] args) {
try {
MqttClient client = new MqttClient(BROKER, CLIENT_ID, null);

// Tạo options
MqttConnectOptions options = new MqttConnectOptions();
options.setCleanSession(true);

133

---

### [Slide 134]

Chương trình MQTT Example
client.setCallback(new MqttCallback() {
@Override
public void connectionLost(Throwable cause) {
System.out.println("Kết nối bị mất: " + cause.getMessage());
}
@Override
public void messageArrived(String topic, MqttMessage message) throws
Exception {
System.out.println("Nhận tin nhắn từ topic '" + topic + "': " + new
String(message.getPayload()));
}

@Override
public void deliveryComplete(IMqttDeliveryToken token) {
System.out.println("Gửi thành công!");
}
});
134

---

### [Slide 135]

Chương trình MQTT Example
// Kết nối đến broker
client.connect(options);
System.out.println("Đã kết nối đến broker: " + BROKER);

// Đăng ký nhận tin từ topic
client.subscribe(TOPIC);
System.out.println("Đăng ký topic: " + TOPIC);
// Gửi dữ liệu đến topic
String content = "Xin chào từ Java MQTT!";
MqttMessage message = new MqttMessage(content.getBytes());
message.setQos(1);
client.publish(TOPIC, message);

} catch (MqttException e) {
e.printStackTrace();
}
}
}

135

---

### [Slide 136]

Chương trình MQTT Example

136

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 136 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 137]

Chương trình MQTT Example

137

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 137 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 138]

Chương trình MQTT Example

138

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 138 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 139]

Chương trình MQTT Example

139

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 139 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 140]

Chương trình MQTT Example

140

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 140 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 141]

Chương trình MQTT Example

141

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 141 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 142]

Chương trình MQTT Example

142

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 142 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 143]

Chương trình MQTT Example – Hàm callback()

143

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 143 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 144]

Chương trình MQTT Example – Hàm callback()

144

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 144 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 145]

Chương trình MQTT Example – Hàm callback()

145

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 145 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 146]

Chương trình MQTT Example – Hàm callback()

146

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 146 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 147]

Chương trình MQTT Example – Hàm callback()

147

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 147 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 148]

Chương trình MQTT Example – Dữ liệu json
▪ Cải tiến: Gửi dữ liệu json

148

---

### [Slide 149]

Chương trình MQTT Example – Dữ liệu json
▪ Cải tiến: Nhận dữ liệu json và bóc tách dữ liệu

149

---

### [Slide 150]

Chương trình MQTT Example – Dữ liệu json
▪ Sử dụng thư viện java json

150

---

### [Slide 151]

Chương trình MQTT Example - Reconnect
▪ Tự động kết nối lại

151

---

### [Slide 152]

Bài tập 2
▪ Viết một chương trình mqtt client thực hiện:
▪ Gửi (publish) dữ liệu lên mqtt broker
▪ Nhận (subscribe) dữ liệu từ mqtt broker
▪ Đóng gói dữ liệu bằng JSON. Ví dụ:
{
"DeviceName": "my-mqtt-client",
"temperature":30,
"humidity":60
}

▪ Dùng MQTTBox để minh họa gửi nhận
▪ Ví dụ dùng mqtt broker: tcp://broker.hivemq.com:1883
152

---

### [Slide 153]

2.3.3. Giao thức AMQP
▪ AMQP (Advanced Message Queue Protocol): Giao thức truyền nhận
dùng hàng đợi thông điệp
▪ RabbitMQ: Một broker sử dụng giao thức AMQP
▪ RabbitMQ broker đóng vai trò trung gian lưu trữ cũng như điều phối
thông điệp (message) giữa bên gửi (producer) và bên nhận
(consumer)

153

---

### [Slide 154]

Giao thức AMQP
▪ RabbitMQ:
▪ Luồng gửi nhận message qua RabbitMQ

154

---

### [Slide 155]

Giao thức AMQP
▪ RabbitMQ:
▪ 4 loại Exchange: direct, topic, fanout, headers

155

---

### [Slide 156]

Giao thức AMQP
▪ Cài đặt RabbitMQ broker (server)
▪ https://www.rabbitmq.com/download.html
▪ https://www.rabbitmq.com/install-windows.html

▪ Quản trị RabbitMQ broker bằng công cụ:
▪ https://www.rabbitmq.com/management.html

▪ RabbitMQ tutorials:
▪ https://www.rabbitmq.com/getstarted.html

156

---

### [Slide 157]

Tutorial 1
▪ Viết chương trình gửi nhận dữ liệu qua RabbitMQ
▪ Cài đặt, sử dụng một RabbitMQ broker
▪ Chương trình Producer gửi dữ liệu (message)
▪ Chương trình Consumer nhận dữ liệu
• Sử dụng default exchange (type: direct)

157

---

### [Slide 158]

Tutorial 1
▪ Tham khảo:
▪ Chương trình java https://www.rabbitmq.com/tutorials/tutorial-one-java.html
▪ Chương trình python https://www.rabbitmq.com/tutorials/tutorial-one-python

158

---

### [Slide 159]

Tutorial 1. Producer
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.nio.charset.StandardCharsets;

Sender.java

public class send {
private final static String QUEUE_NAME = “ktmt";
public static void main(String[] argv) throws Exception {
ConnectionFactory factory = new ConnectionFactory();
factory.setHost(“localhost");
factory.setUsername(“guest");
factory.setPassword(“guest");
try (Connection connection = factory.newConnection();
Channel channel = connection.createChannel()) {
channel.queueDeclare(QUEUE_NAME, false, false, false, null);
String message = "Hello World! Publish message to broker";
channel.basicPublish("", QUEUE_NAME, null,
message.getBytes(StandardCharsets.UTF_8));
System.out.println(" [x] Sent '" + message + "'");
}
}
}
159

---

### [Slide 160]

Tutorial 1. Consumer
import com.rabbitmq.client.Channel;
Recv.java
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;
public class Receive {
private final static String QUEUE_NAME = "ktmt";
public static void main(String[] argv) throws Exception {
ConnectionFactory factory = new ConnectionFactory();
factory.setHost("localhost");
factory.setUsername("guest");
factory.setPassword("guest");
Connection connection = factory.newConnection();
Channel channel = connection.createChannel();
channel.queueDeclare(QUEUE_NAME, false, false, false, null);
System.out.println(" [*] Waiting for messages. To exit press CTRL+C");
DeliverCallback deliverCallback = (consumerTag, delivery) -> {
String message = new String(delivery.getBody(), "UTF-8");
System.out.println(" [x] Received '" + message + "'");
};
channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag-> { });
}
}
160

---

### [Slide 161]

Sử dụng CloudAMQP
▪ Sử dụng RabbitMQ broker trên CouldAMQP (miễn phí)
▪ Truy cập trang https://www.cloudamqp.com/
▪ Đăng ký tài khoản (Sign Up)
▪ Tạo instance miễn phí (Create New Instance)

161

---

### [Slide 162]

Sử dụng CloudAMQP
▪ Sau khi tạo xong instance thành công, lấy thông tin truy cập broker

162

---

### [Slide 163]

Sử dụng CloudAMQP
▪ Thiết lập thông tin kết nối broker trong chương trình (Java)

ConnectionFactory factory = new ConnectionFactory();
//Set CloudAMQP credentials
factory.setUsername("cohushpn");
factory.setPassword("m_PtS6PB02IfLhaAa7LPDr0yAHZhcIF_");
factory.setVirtualHost("cohushpn");
factory.setHost("armadillo.rmq.cloudamqp.com");
factory.setPort(5671); //AMQPs
factory.useSslProtocol();

163

---

### [Slide 164]

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

Producer.java

public class Producer {
private static final String QUEUE_NAME = "testQueue";
public static void main(String[] args) throws Exception {
ConnectionFactory factory = new ConnectionFactory();
//Thông tin từ CloudAMQP
factory.setHost("armadillo.rmq.cloudamqp.com");
factory.setUsername("cohushpn");
factory.setPassword("m_PtS6PB02IfLhaAa7LPDr0yAHZhcIF_");
factory.setVirtualHost("cohushpn");
factory.setPort(5671); // Sử dụng AMQPS
factory.useSslProtocol(); // SSL an toàn
try (Connection connection = factory.newConnection();
Channel channel = connection.createChannel()) {
channel.queueDeclare(QUEUE_NAME, true, false, false, null);
String message = "Xin chào từ Producer!";
channel.basicPublish("", QUEUE_NAME, null, message.getBytes("UTF-8"));
System.out.println(" [x] Đã gửi: '" + message + "'");
}
}
}
164

---

### [Slide 165]

import com.rabbitmq.client.*;
public class Consumer {
Consumer.java
private static final String QUEUE_NAME = "testQueue";
public static void main(String[] args) throws Exception {
ConnectionFactory factory = new ConnectionFactory();
// Thông tin từ CloudAMQP
factory.setHost("armadillo.rmq.cloudamqp.com");
factory.setUsername("cohushpn");
factory.setPassword("m_PtS6PB02IfLhaAa7LPDr0yAHZhcIF_");
factory.setVirtualHost("cohushpn");
factory.setPort(5671); // Sử dụng AMQPS
factory.useSslProtocol(); // SSL an toàn
Connection connection = factory.newConnection();
Channel channel = connection.createChannel();
channel.queueDeclare(QUEUE_NAME, true, false, false, null);
System.out.println(" [*] Đang chờ tin nhắn. Nhấn Ctrl+C để thoát.");
DeliverCallback deliverCallback = (consumerTag, delivery) -> {
String message = new String(delivery.getBody(), "UTF-8");
System.out.println(" [x] Nhận được: '" + message + "'");
};
channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> {});
}
}
165

---

### [Slide 166]

Các bước chính trong Producer

166

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 166 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 167]

Các bước chính trong Producer

167

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 167 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 168]

Các bước chính trong Producer

168

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 168 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 169]

Các bước chính trong Producer

169

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 169 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 170]

Các bước chính trong Consumer

170

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 170 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 171]

Các bước chính trong Consumer

171

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 171 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 172]

Tóm tắt quy trình Producer - Consumer

172

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 172 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 173]

Tutorial 3
▪ Cải tiến Tutorial 1: một Producer gửi message đến tất cả các
consumer
▪ Sử dụng exchange type = “fanout” (broadcast)
channel.exchangeDeclare(EXCHANGE_NAME, "fanout");

https://www.rabbitmq.com/tutorials/tutorial-three-java.html
173

---

### [Slide 174]

Producer gửi broadcast đến tất cả consumer

174

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 174 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 175]

Consumer bind với queue để nhận

175

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 175 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 176]

Tutorial 4
▪ Routing (định tuyến) thông điệp
▪ Chọn thông điệp muốn nhận (Receiving messages selectively)
Producer

channel.exchangeDeclare(EXCHANGE_NAME, "direct");
channel.basicPublish(EXCHANGE_NAME, “black”, null, message.getBytes());
Consumer
channel.queueBind(queueName, EXCHANGE_NAME, “black”);

https://www.rabbitmq.com/tutorials/tutorial-four-java.html
176

---

### [Slide 177]

Tutorial 5
▪ Sử dụng exchange type = “topic”
▪ routing_key must be a list of words, delimited by dots.
▪ *(star) can substitute for exactly one word.
▪ #(hash) can substitute for zero or more words.
Producer

channel.basicPublish(EXCHANGE_NAME, routingKey, null, message.getBytes("UTF-8"));

Consumer

channel.queueBind(queueName, EXCHANGE_NAME, bindingKey);

https://www.rabbitmq.com/tutorials/tutorial-five-java.html
177

---

### [Slide 178]

Bài tập 3
▪ Viết một chương trình gửi/nhận dữ liệu qua RabbitMQ broker:
▪ Gửi (publish) dữ liệu lên RabbitMQ broker (cài đặt hoặc dùng CloudAMQP)
▪ Nhận (subscribe) dữ liệu từ RabbitMQ broker
▪ Đóng gói dữ liệu bằng JSON. Ví dụ:
{
"DeviceName": “sender-1",
"temperature":30,
"humidity":60

}

178

---

### [Slide 179]

2.4. Nền tảng IoT Cloud Platform
▪ Các kiến trúc IoT phải có khả năng mở rộng (scaling) qui mô kết nối các thiết
bị, thu thập dữ liệu (data gathering), xử lý (data processing) và lưu trữ dữ
liệu (data storage)
▪ Khả năng thực hiện các công việc trên nhanh chóng trong khi vẫn thực hiện
phân tích dữ liệu theo thời gian thực (real-time data insights)
▪ Gửi lượng lớn dữ liệu lên cloud làm chậm quá trình xử lý, đòi hỏi thêm băng
thông cho truyền nhận dữ liệu

179

---

### [Slide 180]

IoT Cloud Platform
▪ Giải pháp tính toán phân tán (distributed computing) ~ fog or edge
computing trở nên phổ biến
▪ Edge computing (tính toán cận biên): việc xử lý tính toán thực hiện trên các
nodes trong mạng là các thiết bị IoT (IoT devices) nằm ở biên “edge” của
mạng
▪ Giải pháp dẫn đến nhu cầu cho thiết bị IoT có khả năng: xử lý, phân tích dữ
liệu cục bộ (cleaning, processing, analyzing data locally). Chỉ gửi dữ liệu đã
xử lý trước đến cloud

180

---

### [Slide 181]

IoT Cloud Platform

181

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 181 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 182]

IoT Cloud Platforms
▪ Một số nền tảng dịch vụ IoT Cloud:
▪ ThingsBoard
▪ AWS IoT
▪ Google Cloud IoT
▪ Microsoft Azure IoT
▪ IBM Watson IoT

https://www.postscapes.com/internet-of-things-technologies/

182

---

### [Slide 183]

Google Cloud IoT Architecture
Be capable of doing data import, process, storage, and analysis for hundreds of millions of events per hour
from devices all over the world

---

### [Slide 184]

Google Cloud IoT
▪ Kiến trúc Google Cloud IoT chia làm 4 thành phần:
▪ data gathering (thu thập dữ liệu trên thiết bị)
▪ data ingest (tiếp nhận dữ liệu trên Cloud)
▪ data processing (xử lý dữ liệu)
▪ data analysis (phân tích dữ liệu)

184

---

### [Slide 185]

Google Cloud IoT
▪ Data Gathering (Thu thập dữ liệu trên thiết bị):
▪ Xảy ra trên các thiết bị (devices) và cảm biến (sensors)
▪ Cảm biến (sensors) thu thập (gather) dữ liệu từ môi trường,
gửi lên cloud hoặc trực tiếp hoặc gián tiếp thông qua thiết bị
trung gian
▪ Thiết bị (devices) chuẩn bị dữ liệu truyền lên cloud. Tùy thuộc
loại mạng kết nối, quá trình chuẩn bị bao gồm: làm sạch dữ
liệu, tiền xử lý, phân tích hoặc có thể sử dụng cả machine
learning

185

---

### [Slide 186]

Google Cloud IoT
▪ Cloud IoT Edge:

186

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 186 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 187]

Google Cloud IoT
▪ Cloud IoT Edge:
▪ Trong kiến trúc Goolge Cloud IoT, giai đoạn thu thập dữ liệu có thể thực
hiện trên Cloud IoT Edge.
▪ Thành phần này là một nhóm các thiết bị có khả năng thực hiện các
phân tích thời gian thực và ML (machine learning). Cho phép mở rộng
các xử lý dữ liệu và ML thực hiện trên các thiết bị (edge devices).
▪ Cloud IoT Edge có thể sử dụng Android Things OS, Linux-based OS.
▪ Gồm 2 thành phần: Edge IoT Core và Edge ML

187

---

### [Slide 188]

Google Cloud IoT
▪ Ingest and Process data (Tiếp nhận và xử lý dữ liệu):

188

---

### [Slide 189]

Google Cloud IoT
▪ Data Analytics and ML (Phân tích dữ liệu và Học máy):
▪ Có thể thực hiện trên Edge hoặc Cloud.
▪ Google's Cloud IoT Core Data Analytics and ML are fully integrated with IoT data.

189

---

### [Slide 190]

Nội dung
▪ Chương 1. Tổng quan về IoT
▪ Chương 2. Các công nghệ IoT
▪ Chương 3. Lập trình ứng dụng IoT
▪ Chương 4. An toàn và Bảo mật IoT
▪ Chương 5. Thiết kế và xây dựng hệ thống IoT

190
