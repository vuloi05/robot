# Chương 2 (Phần A): Cảm biến, Thiết bị & Chuẩn truyền thông

- **PDF gốc:** `docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf` (*IT4735 IoT và Ứng dụng*, SoICT - HUST, 2025)
- **Phạm vi slide:** 61–91
- **Các mục lớn:** 2.1 Cảm biến và thiết bị IoT (62–81); 2.2 Một số chuẩn truyền thông (82–91)
- **Ứng dụng vào dự án Robot Nhà Hàng:** Phân loại cảm biến/cơ cấu chấp hành và so sánh các chuẩn truyền thông không dây (Wi-Fi, BLE, Zigbee, LoRa) cho ESP32 IoT.

---

### [Slide 61]

Chương 2. Các công nghệ IoT
▪ 2.1. Cảm biến và thiết bị
▪ 2.2. Một số chuẩn truyền thông cho IoT
▪ 2.3. Các giao thức cho ứng dụng IoT
▪ 2.4. Nền tảng đám mây IoT

61

---

### [Slide 62]

2.1. Cảm biến và thiết bị IoT
▪ Cảm biến và thiết bị:
▪ Các cảm biến và thiết bị IoT thường được gọi đơn giản là thiết bị (devices) với
ngầm định bao gồm cả các cảm biến được ghép nối
▪ Trong nhiều tình huống, khi đề cập “thiết bị” có thể được hiểu là bao gồm cả
thiết bị và cảm biến

62

---

### [Slide 63]

Cảm biến và thiết bị IoT
▪ Cảm biến quan sát các thay đổi xung quanh và gửi thông tin về các thay
đổi đó đến thiết bị
▪ Các thiết bị thu thập dữ liệu từ các cảm biến và gửi tới cloud/server

63

---

### [Slide 64]

Cảm biến và thiết bị IoT
▪ Các thiết bị có thể hạn chế về tài nguyên tính toán (CPU, bộ nhớ hạn chế,
…)
▪ Các thiết bị có thể giao tiếp truyền thông riêng mà không kết nối trực tiếp
với cloud platform, ví dụ thông qua Bluetooth Low Energy (BLE)
▪ Các thiết bị có thể lưu trữ, xử lý và phân tích dữ liệu trước khi gửi lên
cloud

64

---

### [Slide 65]

Phân loại cảm biến (Types of Sensors)
▪ Theo yêu cầu về nguồn cấp

▪ Theo loại tín hiệu

▪ Theo loại thiết bị đo

65

---

### [Slide 66]

Lựa chọn cảm biến
• Lựa chọn cảm biến cần cân nhắc đến tầm quan trọng của các yếu tố
và mức độ ưu tiên trong thiết kế tổng thể.
• Durability (Tính lâu bền):
– Tính lâu bên phải được cân nhắc đến dựa trên môi trường hoạt động của
sensor.
– Đảm bảo thiết bị hoạt động lâu bền trong khoảng thời gian đáng kể không
phải tốn chi phí sửa chữa thay thế.
– Ví dụ: cảm biến nhiệt kháng nước dùng cho trạm thời tiết

66

---

### [Slide 67]

Lựa chọn cảm biến
• Accuracy (Độ chính xác):
– Cần độ chính xác đáp ứng đủ nhu cầu (độ chính xác cao đi kèm giá thành
đắt)
– Ví dụ: Đo nhiệt độ nhà kho có thể chấp nhận độ chính xác +/-2 độ. Đo
nhiệt độ hệ thống thiết bị y tế cần độ chính xác +/-0.2 độ

67

---

### [Slide 68]

Lựa chọn cảm biến
• Versatility (Tính linh hoạt):
– Cảm biến có thể vận hành với các biến động của môi trường xung quanh
– Ví dụ: cảm biến cho trạm thời tiết có thể hoạt động trong điều kiện mùa
hè, mùa đông. Không khả thi với loại cảm biến chỉ hoạt động trong môi
trường trong nhà.

68

---

### [Slide 69]

Lựa chọn cảm biến
• Power Consumption (Tiêu thụ điện năng):
– Tùy theo tình huống, có thể đòi hỏi các thiết bị tiêu thụ ít điện năng, sử
dụng các đặc tính tiết kiệm năng lượng
– Ví dụ: cảm biến hoặc thiết bị sử dụng pin năng lượng mặt trời cần thiết
kế chế độ ngủ (sleep mode) tiết kiệm năng lượng, thức dậy (wake-up)
khi cần thu thập và truyền dữ liệu

69

---

### [Slide 70]

Lựa chọn cảm biến
• Cân nhắc môi trường đặc biệt:
– Ví dụ: Cảm biến trong giám sát chất lượng nước trong nuôi thủy sản
đòi hỏi sensor đặt trong môi trường nước (pH, DO, TDS, …) khác với các
cảm biến dựa trên lấy mẫu phân tích.

70

---

### [Slide 71]

Lựa chọn cảm biến
• Cost (Chi phí):
– Các mạng IoT thường bao gồm hàng trăm, ngàn thiết bị và cảm biến.
– Thiết kế cần cân nhắc đến chi phí lắp đặt, bảo trì, thay thế, etc.

71

---

### [Slide 72]

Devices – Thiết bị IoT
▪ Một “Thing” trong “Internet of Things” là một đơn vị xử lý mà có khả năng
kết nối vào internet để trao đổi dữ liệu với cloud.
▪ Các thiết bị thường được gọi là "smart devices" or "connected devices."
▪ Thiết bị giao tiếp với 2 loại dữ liệu: telemetry (dữ liệu thu thập) và state
(trạng thái của thiết bị).

72

---

### [Slide 73]

Các loại thông tin
▪ Mỗi thiết bị có thể cung cấp hoặc sử dụng một vài loại thông tin phục vụ
cho mỗi loại hệ thống backend khác nhau.
▪ Device metadata: Metadata chứa các thông tin mô tả về thiết bị (thường ít
thay đổi). Ví dụ:
▪ Identifier (ID) – Định danh thiết bị
▪ Class or type: Lớp/loại thiết bị
▪ Model
▪ Revision
▪ Date manufactured
▪ Hardware serial number
73

---

### [Slide 74]

Các loại thông tin
▪ Telemetry:
▪ Dữ liệu được thu thập bởi thiết bị qua các cảm biến được gọi là telemetry.
▪ Là dữ liệu chỉ đọc (từ môi trường xung quanh)

74

---

### [Slide 75]

Các loại thông tin
▪ State information:
▪ Thông tin trạng thái: Mô tả trạng thái hiện thời của thiết bị. Có thể
đọc/ghi, cập nhật (nhưng ít thường xuyên)

75

---

### [Slide 76]

Lệnh thực thi trên thiết bị (Device Commands)
▪ Commands: Là các hành động được được thực hiện bởi thiết bị.
▪ Ví dụ:
▪ Quay 360 độ sang phải.
▪ Tắt/bật đèn
▪ Tăng tần suất truyền dữ liệu

76

---

### [Slide 77]

Định nghĩa thiết bị
▪ Trong hệ thống IoT, định nghĩa thiết bị có thể thay đổi phụ thuộc vào nhu
cầu của dự án.
▪ Mỗi thiết bị có thể được cân nhắc như một thực thể tách biệt, hoặc một
thiết bị có thể chịu trách nhiệm với một nhóm cảm biến.

77

---

### [Slide 78]

Định nghĩa Thiết bị – Ví dụ
▪ Giám sát nhiệt độ phòng khách sạn
▪ Giải pháp 1: Mỗi phòng có 3 cảm biến: one near the floor, one near the bed,
and one near the ceiling.

78

---

### [Slide 79]

Định nghĩa Thiết bị – Ví dụ
▪ Giải pháp 1: dữ liệu được gửi đến cloud như là 3 thiết bị khác nhau, mỗi cái
gửi một thông tin nhiệt độ đến cloud.
▪ {deviceID: "dh28dslkja", "location": "floor", "room": 128, "temp": 22 }
▪ {deviceID: "8d3kiuhs8a", "location": "ceiling", "room": 128, "temp": 24 }
▪ {deviceID: "kd8s8hh3o", "location": "bedside", "room": 128, "temp": 23 }

79

---

### [Slide 80]

Định nghĩa Thiết bị – Ví dụ
▪ Giải pháp 2: mỗi phòng sử dụng 1 thiết bị chịu trách nhiệm gửi dữ liệu từ 3
cảm biến.

80

---

### [Slide 81]

Định nghĩa Thiết bị – Ví dụ
▪ Giải pháp 2: dữ liệu được gửi đến cloud bằng 1 thiết bị với 3 cảm biến. Có
thể bổ sung thêm xử lý tính nhiệt độ trung bình trên thiết bị.
▪ {deviceID: "dh28dslkja", "room": 128, "temp_floor": 22, "temp_ceiling": 24,
"temp_bedside": 23, "average_temp": 23 }

▪ Việc lựa chọn giải pháp nào phụ thuộc vào ý định sử dụng thông tin ở thời
điểm hiện tại và cả tiềm năng trong tương lai.

81

---

### [Slide 82]

2.2. Một số chuẩn truyền thông
▪ Communication standards:
▪ NFC and RFID
▪ Bluetooth
▪ WiFi
▪ GSM, GPRS, 2G/3G/4G, LTE
▪ ZigBee
▪ 6LoWPAN
▪ Thread

82

---

### [Slide 83]

Một số chuẩn truyền thông trong IoT

https://www.youtube.com/watch?v=MAA9JpGraoU
Frequency: 120–150 kHz (LF), 13.56 MHz (HF), 433 MHz (UHF), 865-868 MHz (Europe)902-928 MHz
(North America) UHF, 2450-5800 MHz (microwave), 3.1–10 GHz (microwave)
Range: 10cm to 200m
Examples: Road tolls, Building Access, Inventory

83

---

### [Slide 84]

Một số chuẩn truyền thông trong IoT
▪ NFC (Near-Field Communications)

Frequency: 13.56 MHz
Range: < 0.2 m
Examples: Smart Wallets/Cards, Action Tags, Access Control

84

---

### [Slide 85]

Một số chuẩn truyền thông trong IoT
▪ Bluetooth

Frequency: 2.4GHz
Range: 1-100m
Examples: Hands-free headsets, key dongles, fitness trackers
85

---

### [Slide 86]

Một số chuẩn truyền thông trong IoT
▪ WiFi

Frequency: 2.4 GHz, 3.6 GHz and 4.9/5.0 GHz bands.
Range: Common range is up to 100m but can be extended.
Applications: Routers, Tablets, etc
More: https://www.postscapes.com/internet-of-things-technologies/

86

---

### [Slide 87]

Một số chuẩn truyền thông trong IoT
▪ GSM (Global System for Mobile communications)

Frequency: Europe: 900MHz & 1.8GHz, US: 1.9GHz & 850MHz, Full List can be
found here.
Data Rate: 9.6 kbps
Examples: Cell phones, M2M, smart meter, asset tracking
More: https://www.postscapes.com/internet-of-things-technologies/

87

---

### [Slide 88]

Một số chuẩn truyền thông trong IoT
▪ ZigBee

▪ Standard: ZigBee 3.0 based on IEEE802.15.4
▪ Frequency: 2.4GHz
▪ Range: 10-100m
▪ Data Rates: 250kbps

88

---

### [Slide 89]

Một số chuẩn truyền thông trong IoT
▪ 6LoWPAN
▪ IPv6 protocol over low-power wireless PANs (sử dụng giao thức IPv6 trong các
mạng PAN không dây công suất thấp)

89

---

### [Slide 90]

Một số chuẩn truyền thông trong IoT
▪ Thread: Giao thức IP mới dựa trên nền tảng IPv6 được thiết kế riêng cho mảng
tự động hóa trong nhà thông minh, các tòa nhà.
▪ Ra mắt vào giữa năm 2014 bởi Theard Group, giao thức Thread dựa trên các tiêu
chuẩn khác nhau, bao gồm IEEE802.15.4, IPv6 và 6LoWPAN, và cung cấp một giải
pháp dựa trên nền tảng IP cho các ứng dụng IoT
▪ Tiêu chuẩn: Theard, dựa trên IEEE802.15.4 và 6LowPAN.
▪ Tần số: 2.4GHz (ISM).
▪ Tham khảo: https://smarthomekit.vn/thread-protocol/

90

---

### [Slide 91]

Một số chuẩn truyền thông trong IoT
▪ Thread:

91

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 91 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]
