import { Link, Route, Routes, useParams } from "react-router-dom";
import {
  Bot,
  ChefHat,
  ConciergeBell,
  LayoutDashboard,
  QrCode,
  Smile,
} from "lucide-react";

interface RoleCard {
  path: string;
  title: string;
  subtitle: string;
  icon: typeof ChefHat;
}

const ROLE_CARDS: RoleCard[] = [
  {
    path: "/kitchen",
    title: "Bếp (Kitchen)",
    subtitle: "Gán món theo Khay 1 / Khay 2 và gọi robot đi giao đa bàn",
    icon: ChefHat,
  },
  {
    path: "/reception",
    title: "Lễ tân (Reception)",
    subtitle: "Gọi robot ra quầy đón và dẫn khách đến bàn trống",
    icon: ConciergeBell,
  },
  {
    path: "/table/table_01",
    title: "Nhân viên / QR Bàn",
    subtitle: "Gọi robot thu dọn bát đĩa hoặc gọi hỗ trợ tại bàn",
    icon: QrCode,
  },
  {
    path: "/admin",
    title: "Admin Map Live",
    subtitle: "Bản đồ 2D realtime, vị trí robot, pin, hàng đợi & E-Stop",
    icon: LayoutDashboard,
  },
  {
    path: "/robot-face",
    title: "Robot Face Kiosk",
    subtitle: "Màn hình cảm ứng 7 inch trên thân robot: biểu cảm & xác nhận",
    icon: Smile,
  },
];

function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-12">
      <div className="mb-10 flex items-center gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
          <Bot className="h-7 w-7" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            Hệ Thống Điều Phối Robot Phục Vụ Nhà Hàng
          </h1>
          <p className="text-sm text-slate-400">
            Giai đoạn 1 Skeleton — ROS 2 Jazzy + Mosquitto MQTT + Rust Axum + React
          </p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {ROLE_CARDS.map((card) => {
          const Icon = card.icon;
          return (
            <Link
              key={card.path}
              to={card.path}
              className="group rounded-2xl border border-slate-800 bg-slate-900/70 p-5 transition hover:border-emerald-500/60 hover:bg-slate-900"
            >
              <Icon className="mb-3 h-7 w-7 text-emerald-400 transition group-hover:scale-105" />
              <h2 className="text-lg font-semibold text-slate-100">{card.title}</h2>
              <p className="mt-1 text-sm text-slate-400">{card.subtitle}</p>
              <span className="mt-4 inline-block text-xs font-mono text-emerald-400">
                {card.path} →
              </span>
            </Link>
          );
        })}
      </div>
    </main>
  );
}

function StagePlaceholder({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center px-6">
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8">
        <p className="text-xs font-semibold uppercase tracking-wider text-emerald-400">
          Stage 4 Target UI
        </p>
        <h1 className="mt-2 text-2xl font-bold">{title}</h1>
        <p className="mt-3 text-slate-300">{description}</p>
        <Link
          to="/"
          className="mt-6 inline-block rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-700"
        >
          ← Quay lại chọn giao diện
        </Link>
      </div>
    </main>
  );
}

function TablePage() {
  const { tableId } = useParams();
  return (
    <StagePlaceholder
      title={`Bàn ${tableId ?? "table_01"} — Gọi Thu Dọn & Hỗ Trợ`}
      description="Giao diện QR tại bàn kết nối trực tiếp tới Rust Backend (và đồng bộ LED nút ESP32 tại bàn qua MQTT table/{id}/led)."
    />
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route
        path="/kitchen"
        element={
          <StagePlaceholder
            title="Bảng Điều Khiển Bếp (/kitchen)"
            description="Sẽ hoàn thiện ở Giai đoạn 4: chọn bàn cho Khay 1 / Khay 2, tối ưu thứ tự bàn và theo dõi trạng thái giao món."
          />
        }
      />
      <Route
        path="/reception"
        element={
          <StagePlaceholder
            title="Bảng Điều Khiển Lễ Tân (/reception)"
            description="Sẽ hoàn thiện ở Giai đoạn 4: xem bàn trống, gọi robot ra quầy lễ tân đón khách và dẫn khách tốc độ chậm."
          />
        }
      />
      <Route path="/table/:tableId" element={<TablePage />} />
      <Route
        path="/admin"
        element={
          <StagePlaceholder
            title="Admin Map Live Dashboard (/admin)"
            description="Sẽ hoàn thiện ở Giai đoạn 4: hiển thị OccupancyGrid 2D, vị trí robot realtime, % pin, hàng đợi ưu tiên và nút E-Stop."
          />
        }
      />
      <Route
        path="/robot-face"
        element={
          <StagePlaceholder
            title="Robot Face Kiosk 7-inch (/robot-face)"
            description="Sẽ hoàn thiện ở Giai đoạn 4: khuôn mặt biểu cảm động theo RobotState và nút chạm xác nhận đã nhận món."
          />
        }
      />
    </Routes>
  );
}
