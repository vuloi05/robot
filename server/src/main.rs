//! Restaurant Fleet Server (Stage 1 Skeleton)
//! Các module sẽ triển khai ở Giai đoạn 4:
//!   - `mqtt_gateway`: Kết nối rumqttc <-> Mosquitto (robot/+/telemetry, event, cmd, table/+/call, dock/+/status)
//!   - `dispatcher`: Hàng đợi ưu tiên (Priority Queue) & chọn robot khả dụng
//!   - `ws`: Broadcast realtime telemetry & biểu cảm Robot Face tới React Web
//!   - `db`: SQLx migrations & CRUD cho bàn ăn, waypoints, lịch sử nhiệm vụ

mod models;

// Khai báo trước các crate đã khóa phiên bản cho Giai đoạn 4 (mqtt_gateway, db, dispatcher)
use chrono as _;
use rumqttc as _;
use sqlx as _;
use uuid as _;

use axum::{routing::get, Json, Router};
use serde::Serialize;
use std::net::SocketAddr;
use tower_http::{cors::CorsLayer, trace::TraceLayer};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[derive(Serialize)]
struct HealthResponse {
    status: &'static str,
    service: &'static str,
    schema_version: u32,
}

#[derive(Serialize)]
struct InfoResponse {
    service: &'static str,
    version: &'static str,
    schema_version: u32,
    mqtt_topics: Vec<&'static str>,
}

async fn health_handler() -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok",
        service: "restaurant_fleet_server",
        schema_version: models::SCHEMA_VERSION,
    })
}

async fn info_handler() -> Json<InfoResponse> {
    Json(InfoResponse {
        service: "restaurant_fleet_server",
        version: env!("CARGO_PKG_VERSION"),
        schema_version: models::SCHEMA_VERSION,
        mqtt_topics: vec![
            "robot/+/status",
            "robot/+/telemetry",
            "robot/+/cmd",
            "robot/+/cmd_ack",
            "robot/+/event",
            "robot/+/supervisor",
            "table/+/call",
            "table/+/led",
            "dock/+/status",
        ],
    })
}

#[tokio::main]
async fn main() {
    let _ = dotenvy::dotenv();

    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,restaurant_fleet_server=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let host = std::env::var("SERVER_HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port: u16 = std::env::var("SERVER_PORT")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(8080);

    let app = Router::new()
        .route("/health", get(health_handler))
        .route("/api/v1/info", get(info_handler))
        .layer(CorsLayer::permissive())
        .layer(TraceLayer::new_for_http());

    let addr: SocketAddr = format!("{host}:{port}")
        .parse()
        .expect("Invalid SERVER_HOST or SERVER_PORT");

    tracing::info!("restaurant_fleet_server listening on http://{addr}");
    let listener = tokio::net::TcpListener::bind(addr)
        .await
        .expect("Failed to bind TCP listener");

    axum::serve(listener, app)
        .await
        .expect("Axum server exited unexpectedly");
}
