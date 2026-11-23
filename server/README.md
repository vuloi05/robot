# Restaurant Fleet Server (Rust — Axum + rumqttc + sqlx)

Backend IoT Gateway & điều phối nhiệm vụ trung tâm cho hệ thống robot phục vụ nhà hàng (Tầng 5).

## Kiến trúc dự kiến (hoàn thiện ở GĐ 4)
- **Axum + Tokio:** REST API & WebSocket realtime tới `web_app/`.
- **rumqttc:** Giao tiếp Pub/Sub với Mosquitto Broker (`robot/+/...`, `table/+/...`, `dock/+/...`).
- **sqlx (SQLite/PostgreSQL):** Lưu waypoints, bàn ăn, hàng đợi nhiệm vụ ưu tiên và nhật ký đo đạc.

## Chạy thử ở Giai đoạn 1
```bash
cp ../infra/.env.example .env
cargo run
```

Kiểm tra endpoint:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/info
```
