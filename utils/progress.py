import time


class ProgressTracker:
    def __init__(self, total_bytes: int):
        self.total = max(total_bytes, 1)
        self.current = 0
        self.start_time = time.time()

    def update(self, downloaded: int):
        self.current = downloaded

    @property
    def percent(self) -> float:
        return (self.current / self.total) * 100

    @property
    def speed(self) -> float:
        elapsed = max(time.time() - self.start_time, 0.001)
        return self.current / elapsed

    @property
    def eta(self) -> int:
        if self.speed <= 0:
            return 0

        remaining = self.total - self.current
        return int(remaining / self.speed)

    @staticmethod
    def human_size(size: int) -> str:
        value = float(size)

        for unit in ("B", "KB", "MB", "GB", "TB"):
            if value < 1024:
                return f"{value:.2f} {unit}"
            value /= 1024

        return f"{value:.2f} PB"

    @staticmethod
    def progress_bar(percent: float, length: int = 10) -> str:
        filled = int((percent / 100) * length)
        return "█" * filled + "░" * (length - filled)

    def text(self) -> str:
        return (
            "📥 Downloading...\n\n"
            f"{self.progress_bar(self.percent)} {self.percent:.1f}%\n\n"
            f"📦 {self.human_size(self.current)} / "
            f"{self.human_size(self.total)}\n\n"
            f"🚀 {self.human_size(int(self.speed))}/s\n"
            f"⏱ ETA: {self.eta}s"
        )
