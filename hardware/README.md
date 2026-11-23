# Thiết Kế Phần Cứng, Cơ Khí & Danh Mục Linh Kiện (BOM)

Mô hình robot thực tế cỡ nhỏ/vừa: kích thước bao khoảng **38 × 38 cm**, chiều cao **65–75 cm**, 2 tầng khay phục vụ (tải trọng 3–8 kg).

## Nguyên Tắc Cơ Khí & An Toàn Bắt Buộc

1. **Kết cấu khung lắp ghép dễ gia công:** Nhôm định hình `2020` + tấm Mica/Nhôm cắt Laser/CNC + chi tiết gá cảm biến/vỏ màn hình in 3D.
2. **Cấu hình Differential Drive chuẩn:** 2 bánh chủ động cao su D=85–100 mm đặt đúng trục tâm ngang của thân xe + 2 bánh đa hướng (caster) trước và sau để xoay tại chỗ `0` bán kính (tránh quét đuôi vào chân bàn).
3. **Hạ thấp trọng tâm:** Pin LiFePO4/Li-ion, động cơ và board STM32 đặt sát tầng đáy (`z < 12 cm`) để robot không bị nghiêng lắc khi phanh với khay nước ở tầng trên.
4. **Khe quét LiDAR 2D thoáng 360°:** Đặt LiDAR ở độ cao `~18–22 cm` với trụ chống bố trí gọn ngoài góc mù hoặc tối ưu đường kính trụ để giữ vùng quét trước/hai bên thông thoáng.
5. **Chống điểm mù mặt bàn:** Cấu hình Nav2 `footprint` bao trọn kích thước khay lớn nhất ở tầng trên (`~40 × 40 cm`), kết hợp 3 cảm biến ToF `VL53L0X` gắn ở tầng khay nối về ESP32 tầng trên.
6. **An toàn điện:** Nguồn Pin → Cầu chì tổng → Công tắc chính → **Nút E-Stop cứng** cắt nguồn nhánh động cơ; nhánh Raspberry Pi 5 dùng mạch Buck `5V / 5A` riêng biệt để không bị sụt áp reset Pi khi động cơ khởi động; cực tiếp điểm sạc ngoài qua **diode chống ngược dòng (Ideal Diode / Schottky)**.

Xem danh mục linh kiện chi tiết và mức độ ưu tiên đặt mua trong [bom.csv](bom.csv).
