# Chương 1: Tổng quan về IoT

- **PDF gốc:** `docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf` (*IT4735 IoT và Ứng dụng*, SoICT - HUST, 2025)
- **Phạm vi slide:** 1–60
- **Các mục lớn:** Giới thiệu môn học (1–4); 1.1 Tổng quan (6–18); 1.2 Kiến trúc (19–22); 1.3 Công nghệ (23–35); 1.4 Ứng dụng (36–52); 1.5 Thách thức (53–60)
- **Ứng dụng vào dự án Robot Nhà Hàng:** Khái niệm hệ thống IoT, mô hình kiến trúc phân lớp (Edge/Gateway/Cloud) dùng chuẩn cho chương Thiết kế hệ thống trong luận văn.

---

### [Slide 1]

IT4735

IoT VÀ ỨNG DỤNG
(IoT and Applications)
Phạm Ngọc Hưng, Nguyễn Đình Thuận, Đặng Tuấn Linh
Faculty of Computer Engineering
School of Information and Communication Technology (SoICT)

Hanoi University of Science and Technology
E-mail: [hungpn, thuannd, linhdt]@soict.hust.edu.vn
1

---

### [Slide 2]

Giới thiệu học phần
▪ IT4735 IoT và Ứng dụng (IoT and Applications)
▪ Credits: 2 (2-1-0-4)
▪ Đánh giá:
▪ Quá trình: 50%, Bài tập tuần, Bài tập Project
▪ Cuối kỳ: 50%,
• Bài tập Project, báo cáo, thuyết trình, vấn đáp (50%)
• Thi trắc nghiệm (50%)

2

---

### [Slide 3]

Mục tiêu
▪ Kiến thức tổng quan về IoT
▪ Kiến trúc, mô hình phân lớp, các thành phần của hệ thống IoT
▪ Các công nghệ IoT: thiết bị và cảm biến, một số chuẩn truyền
thông IoT, các giao thức truyền thông cho ứng dụng IoT, nền tảng
đám mây
▪ Lập trình cho thiết bị, hệ thống IoT
▪ Bảo mật trong IoT
▪ Vận dụng kỹ năng thiết kế và xây dựng một hệ thống ứng dụng
IoT

3

---

### [Slide 4]

Nội dung
▪ Chương 1. Tổng quan về IoT
▪ Chương 2. Các công nghệ IoT
▪ Chương 3. Lập trình ứng dụng IoT
▪ Chương 4. An toàn và Bảo mật IoT
▪ Chương 5. Thiết kế và xây dựng hệ thống IoT

4

---

### [Slide 5]

Chương 1. Tổng quan về IoT
▪ 1.1. Tổng quan về IoT
▪ 1.2. Kiến trúc tổng quan hệ thống IoT
▪ 1.3. Tổng quan về các công nghệ trong IoT
▪ 1.4. Các ứng dụng IoT
▪ 1.5. Các vấn đề thách thức của IoT

5

---

### [Slide 6]

1.1. Tổng quan về IoT
▪ What is the Internet of Things (IoT) ?
▪ IoT is the network of things, with clear element identifcation, embedded with software
intelligence, sensors, and ubiquitous connectivity to the Internet
▪ (Book: Internet of Things From Hype to Reality)
▪ Components:
•
•
•
•

Sensors: to collect information.
Identifiers: to identify the source of data (e.g., sensors, devices).
Software: to analyze data.
Internet connectivity: to communicate and notify.

▪ “Things” = “anything”, “everything”
▪ Home appliances, building, car, people, animals,
trees, plants, ...
IoE = Internet of Everything (by Cisco)
6

---

### [Slide 7]

Tổng quan về IoT

7

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 7 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 8]

Tổng quan về IoT
▪ How does IoT works ?
▪ IoT devices: smart devices (that use embedded systems such as
processors, sensors and communication hardware) to collect, send and
act on data they acquire from their environments.
▪ IoT devices share the sensor data they collect by connecting to an IoT
gateway, which acts as a central hub where IoT devices can send data.
▪ Before the data is shared, it can also be sent to an edge device where
that data is analyzed locally. Analyzing data locally reduces the volume of
data sent to the cloud, which minimizes bandwidth consumption.

8

---

### [Slide 9]

Tổng quan về IoT
▪ How does IoT works ?
▪ Sometimes, IoT devices communicate with other related devices and act
on the information they get from one another.
▪ The devices do most of the work without human intervention, although
people can interact with the devices -- for example, to set them up, give
them instructions or access the data.
▪ The connectivity, networking and communication protocols used with these
web-enabled devices largely depend on the specific IoT applications
deployed.
▪ IoT can also use artificial intelligence and machine learning to aid in
making data collection processes easier and more dynamic.

9

---

### [Slide 10]

Tổng quan về IoT
▪ An example of IoT smart home solution

10

---

### [Slide 11]

Tổng quan về IoT
▪ Why is IoT important ?
▪ IoT helps people live and work smarter.
• For example: IoT-embedded devices -- such as cars, smartwatches or thermostats -improve people lives.

▪ IoT is essential to business:
• Real-time supervising of products/objects/system
• Delivering insights into everything from the performance of machines to supply chain
and logistics operations.

▪ IoT enables machines to complete tedious tasks without human intervention.
• automate processes, reduce labor costs, cut down on waste and improve service
delivery.
• less expensive to manufacture and deliver goods,
• transparency into customer transactions.

11

---

### [Slide 12]

Tiến hóa của IoT
▪ The field of IoT has grown tremendously
▪ 1999: Kevin Ashton (Auto-ID Center, MIT) first mentioned the
internet of things in a presentation about RFID

(Source: IHS)

12

---

### [Slide 13]

Tiến hóa của IoT
▪ IoT has evolved from the convergence of:
▪ Wireless technology
▪ Microelectromechanical systems
▪ Microservices
▪ Internet

▪ M2M (machine to machine) communication, evolved to next level
▪ 2010: broder consumer use (smart phones, smart TV)
▪ 2020: cellular IoT (2G/3G/4G/5G. LoRaWAN, LTE)
▪ 2023: billions of internet-connected devices
▪ Digital twins: virtual representation of a real-world entity or process

13

---

### [Slide 14]

Tiến hóa của IoT

1. Pre-Internet: https://en.wikipedia.org/wiki/History_of_the_telephone
2. Internet of content (WWW, 1989, Tim Berners-Lee)
https://en.wikipedia.org/wiki/History_of_the_World_Wide_Web
3. Internet of services (Web 2.0, Yahoo, Amazon, … ~2000, dotcom companies)
4. Internet of people (smart phones, social networks, iPhone1 2007)
Internet of Things named 1999

https://iot-analytics.com/internet-of-things-definition/

14

---

### [Slide 15]

Tiến hóa của IoT

15

Idea: Move from Internet of People → Internet of Things

• Internet xuất hiện ở khắp nơi trên thế
giới
• Ban đầu là để kết nối con người – con
người

❖ Internet of Things kết nối mọi thứ
(“things”) sử dụng các phương tiện
hạ tầng đã có.

---

### [Slide 16]

Tiến hóa của IoT
IoT: Human connecting with Things

ECG sensor

Internet
Motion sensor

Motion sensor
Motion sensor

16

---

### [Slide 17]

Tiến hóa của IoT
IoT: Things connecting with Things

- Complex and heterogeneous
resources and networks
17

---

### [Slide 18]

4th IR and IoT
▪ The Fourth Industrial Revolution and IoT
▪ 1st IR: transformed society with the introduction of machines and mechanized production.
▪ 2nd IR: introduced electricity, which led to mass production.
▪ 3rd IR: has been called the dawn of the information age.
▪ 4th IR: as "the fusion of technologies that is blurring the lines between the physical, digital, and
biological spheres.“ (by Klaus Schwab)

▪ IoT is being called a major driver of the Fourth Industrial Revolution. Why?

18

---

### [Slide 19]

1.2. Kiến trúc tổng quan hệ thống IoT

(1)

(2)

(3)

19

---

### [Slide 20]

Kiến trúc phân tầng của hệ thống IoT (1)

20

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 20 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 21]

Kiến trúc phân tầng của hệ thống IoT (2)

IoT Layered Architecture (Source: ITU-T)
21

---

### [Slide 22]

Bốn “trụ cột” nền tảng của IoT
▪ Connections: Khả năng kết nối (mới) của các thiết bị và thông tin
▪ Collection: Khả năng thu thập dữ liệu (lớn) từ việc gia tăng kết nối các thiết bị và
thông tin
▪ Computation: Khả năng tính toán cho phép chuyển đổi từ các dữ liệu đã thu thập vào
các tính năng mới
▪ Creation: Khả năng sáng tạo độc đáo của các tương tác, các mô hình kinh doanh, và
các giải pháp mới

22

---

### [Slide 23]

1.3. Tổng quan về các công nghệ trong IoT
▪ Phần cứng (Hardware)

▪ Truyền thông (Communication)
▪ Các giao thức (Protocols)
▪ Phân tích dữ liệu (Data Analytic)

▪ Nền tảng đám mây (Cloud Platforms)

23

---

### [Slide 24]

1.3.1. Phần cứng IoT (Hardware)
Các máy tính nhúng (Embedded Computers):
- Vi điều khiển: 8-bit, 32-bit, không dùng hệ điều hành
- Vi điều khiển có dùng hệ điều hành đơn giản (ví dụ: FreeRTOS)
- Bộ xử lý 32-bit, 64-bit, hiệu năng cao, có hệ điều hành (Raspbian, Embedded
Linux, Ubuntu, Embedded Windows, …)
- Các kiến trúc: AVR, Microchip, ARM, Intel, …

Arduino Uno

ESP32

Raspberry Pi

Intel Galileo
24

---

### [Slide 25]

Các cảm biến (Sensors)
▪ Cảm biến có thể coi là thành phần quan trọng nhất trong thiết bị IoT
▪ Đầu ra là tương tự hoặc đầu ra là số

▪ Các module cảm biến là các thiết bị thường bao gồm:
▪ Thành phần cung cấp, quản lý năng lượng (energy/power modules)
▪ Thành phần cảm biến (sensing modules)
▪ Thành phần quản lý giao tiếp

▪ Thành phần quản lý giao tiếp thông qua xử lý tín hiệu (RF modules)
▪ WiFi, ZigBee, Bluetooth, radio transceiver, …

25

---

### [Slide 26]

Các cảm biến (Sensors)
▪ Có nhiều loại cảm biến:

26

---

### [Slide 27]

Các cảm biến (Sensors)

27

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 27 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 28]

Các cảm biến (Laboratory type)

28

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 28 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 29]

Wearables IoT
▪ Head – Helmets, glasses
▪ Neck – Jewelry, collars
▪ Arm – Watches, wristbands, rings
▪ Torso – Clothing, backpacks
▪ Feet – Socks, shoes

29

---

### [Slide 30]

Wearables IoT

▪

https://www.sportswearable.net/fitness-and-sports-wearables-world-wide-marketanalysis-forecasts-and-trends-through-2019-2025/

30

---

### [Slide 31]

1.3.2. Truyền thông trong IoT (Communications)

31

---

### [Slide 32]

Truyền thông trong IoT
▪ Một số chuẩn truyền thông (communication standards) phổ biến
cho IoT:
▪ NFC and RFID
▪ Bluetooth
▪ WiFi
▪ GSM, 3G/4G/LTE, LTE-A

32

---

### [Slide 33]

Truyền thông trong IoT
▪ Một số giao thức (protocols) phổ biến cho truyền nhận dữ liệu trong
IoT:
▪ HTTP (HyperText Transfer Protocol)
▪ MQTT (Message Queue Telemetry Transport)
▪ AMQP (Advanced Message Queue Protocol)
▪ CoAP (Constrained Application Protocol)
▪ XMPP (Extensible Messaging and Presence Protocol)

https://www.postscapes.com/internet-of-things-technologies/

33

---

### [Slide 34]

1.3.3. Phân tích dữ liệu trong IoT (Data Analytic)

34

---

### [Slide 35]

1.3.4. IoT Cloud Platforms
▪ Một số nền tảng IoT Cloud
▪ AWS IoT
▪ Google Cloud IoT
▪ Azure IoT
▪ IBM BlueMix

https://www.postscapes.com/internet-of-things-technologies/

35

---

### [Slide 36]

1.4. Các1.4.
ứngCác
dụng
của
IoT của IoT
ứng
dụng

36

---

### [Slide 37]

Các ứng dụng của IoT

37

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 37 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 38]

Top Industrial IoT Applications
▪ Healthcare
▪ Smart Retail
▪ Smart Building/Smart Home
▪ Smart Agriculture
▪ Smart Utilities (Power Energy, Water)

38

---

### [Slide 39]

Healthcare
▪ One of the fastest sectors adopting the IoT
▪ A lot of sensors for tracking patients

39

---

### [Slide 40]

Smart Retail

https://www.smartofthings.co.th/2018/08/27/smart-retail-solution/
40

---

### [Slide 41]

Smart Retail

Amazon Go store

41

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 41 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 42]

Smart Retail: Shopping

42

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 42 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 43]

Smart Building

43

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 43 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 44]

Smart Home

44

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 44 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 45]

Smart Agriculture

https://www.smartofthings.co.th/2018/08/27/smart-agriculture-solution/

45

---

### [Slide 46]

Smart Utilities

Electrical power, Water Supplying

https://www.smartofthings.co.th/2018/08/27/smart-utilities-solution/
46

---

### [Slide 47]

Transportation

47

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 47 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 48]

IoT – Manufacturing Applications
▪ Intelligent Product Enhancements
▪ Dynamic Response to Market Demands
▪ Lower Costs, Optimized Resource Use, Waste Reduction
▪ Improved Facility Safety
▪ Product Safety

48

---

### [Slide 49]

Một số sản phẩm thương mại ứng dụng IoT

49

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 49 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 50]

Một số sản phẩm thương mại ứng dụng IoT

50

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 50 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 51]

Một số sản phẩm thương mại ứng dụng IoT

51

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 51 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 52]

Thảo luận - Discussion
▪ What everyday activity can be changed by IoT?
▪ What existing process can be changed by IoT? Will this change lead to
the greater good of society? Or to the individual?

52

---

### [Slide 53]

1.5. Các vấn đề thách thức của IoT
▪

Rất nhiều chuẩn công nghệ khác nhau:
• Thuận lợi + Khó khăn ?

▪

Thách thức với các chính phủ trong vấn đề quản trị đổi mới quá nhanh của
công nghệ:
• Ví dụ Uber, Grab

▪

Vấn đề về quyền riêng tư (Privacy) và bảo mật (security)
• Ví dụ: Facebook

▪

Thiếu vắng cơ quan quản lý, điều hành chung
• Vấn đề chung của dịch vụ Internet

▪

Dễ bị tấn công trên Internet:
• Ví dụ IP cameras
53

---

### [Slide 54]

Các thách thức kỹ thuật (Challenges) …
▪ Connectivity - Vấn đề kết nối:
▪ Hiện tại, IoT dựa trên mô hình server/client để xác thực, kết nối các
thiết bị trong mạng. Mô hình này đã có thể làm việc với hàng trăm,
ngàn thiết bị. Vấn đề khó khăn khi số lượng thiết bị lên tới hàng
triệu, tỷ trong mạng
▪ Nếu không cân nhắc đến thiết kế thông lượng mạng thích hợp, vấn
đề tắc nghẽn (bottlenecks) có thể xảy ra trong quá trình trao đổi dữ
liệu tại server.
▪ Các tác vụ có thể chuyển sang thực hiện trên các thiết bị (off-loading
tasks to the edge)
▪ Xu hướng: Các mạng IoT sẽ cần các thiết bị có khả năng thực hiện
phân tích xử lý dữ liệu trên thiết bị (edge computing)
54

---

### [Slide 55]

Các thách thức kỹ thuật (Challenges) …
▪ Brownfield deployment (legacy infrastructure) – Vấn đề triển
khai trên các hạ tầng cũ đã có:
▪ Các thiết bị IoT, các hạ tầng mạng đã có, các công nghệ mới được kết
hợp với nhau (brownfield deployment)
▪ Các công ty đối mặt với vấn đề tích hợp các thiết bị công nghệ mới
với hạ tầng mạng đã tồn tại

55

---

### [Slide 56]

Các thách thức kỹ thuật (Challenges) …
▪ Dealing with non-standard communication protocols:
- Vấn đề với các giao thức truyền thông phi chuẩn
▪ Có nhiều giao thức truyền thông khác nhau được đề xuất, phát triển.

56

---

### [Slide 57]

Các thách thức kỹ thuật (Challenges) …
▪ IT/OT convergence – Sự hội tụ của IT và OT
▪ Sự tích hợp/hội tụ của IT (Information Technology) và OT
(Operational Technology – Công nghệ vận hành) trong các ứng dụng
công nghiệp của Internet of Things (IIoT). Ví dụ về IT, OT trong nhà
máy điện
▪ IT: trung tâm dữ liệu (data-centric), OT: giám sát sự kiện (monitor
events); IoT làm mờ sự phân biệt này thông qua việc giám sát các
thiết bị đồng thời tạo ra một lượng lớn dữ liệu
▪ Các doanh nghiệp vận hành công nghiệp sẽ cần điều chỉnh qui trình
để thích ứng với các thiết bị IIoT và dữ liệu

57

---

### [Slide 58]

Các thách thức kỹ thuật (Challenges) …
▪ Get actionable intelligence from data – Khai thác khả năng thông
minh từ dữ liệu:
▪ Giá trị của dữ liệu gia tăng khi khả năng khai thác thông minh từ dữ liệu gia tăng
▪ Phân tích IoT sẽ cần làm việc với các dữ liệu chưa được cấu trúc, lượng dữ liệu
lớn theo thời gian thực và cả với các dữ liệu ngoại biệt

58

---

### [Slide 59]

Thảo luận - Discussion
▪ Industry Transformations
▪ IoT will cause the most transformation in non-technology-based industries.

▪ Give an example of a non-technology-based industry and explain how IoT
will transform it.

59

---

### [Slide 60]

Nội dung
▪ Chương 1. Tổng quan về IoT
▪ Chương 2. Các công nghệ IoT
▪ Chương 3. Lập trình ứng dụng IoT
▪ Chương 4. An toàn và Bảo mật IoT
▪ Chương 5. Thiết kế và xây dựng hệ thống IoT

60
