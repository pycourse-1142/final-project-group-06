# visualizer.py
# 統計圖繪製模組，輸出 PNG 至 figures/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 中文字型（Windows / Mac / Linux 通用）
plt.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei", "Noto Sans CJK TC", "PingFang TC", "sans-serif"
]
plt.rcParams["axes.unicode_minus"] = False

FIGURES_DIR = "figures"


def ensure_output_folder(folder=FIGURES_DIR):
    """建立輸出資料夾（若不存在）。"""
    if not os.path.exists(folder):
        os.makedirs(folder)


def _save(fig, filename):
    ensure_output_folder()
    path = os.path.join(FIGURES_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"已儲存：{path}")
    return path


# ── 圖 1：PM2.5 / PM10 月趨勢折線圖 ──────────────────────
def plot_monthly_trend(records, site, filename="fig1_monthly_trend.png"):
    """PM2.5 與 PM10 每月趨勢折線圖。"""

    dates = [r["date"] for r in records]
    pm25s = [r["pm25"] for r in records]
    pm10s = [r["pm10"] for r in records]

    fig, ax = plt.subplots(figsize=(12, 5))

    # 畫 PM2.5
    if any(v is not None for v in pm25s):
        ax.plot(dates, pm25s, marker="o", color="#4E79A7",
                linewidth=2, label="PM2.5 (μg/m³)", zorder=3)

    # 畫 PM10
    if any(v is not None for v in pm10s):
        ax.plot(dates, pm10s, marker="s", color="#F28E2B",
                linewidth=2, label="PM10 (μg/m³)", zorder=3)

    # WHO PM2.5 年平均標準線（5 μg/m³）
    ax.axhline(5, color="#4E79A7", linestyle="--", linewidth=1, alpha=0.5)
    ax.text(dates[-1], 5.5, "WHO PM2.5 標準 5", color="#4E79A7",
            fontsize=8, ha="right")

    ax.set_title(f"{site} 測站 PM2.5 / PM10 月平均趨勢", fontsize=14, fontweight="bold")
    ax.set_xlabel("月份")
    ax.set_ylabel("濃度 (μg/m³)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()

    return _save(fig, filename)


# ── 圖 2：PM2.5 月份長條圖（最差月份標紅）─────────────────
def plot_pm25_bar(records, site, filename="fig2_pm25_bar.png"):
    """PM2.5 各月長條圖，最高月份標紅。"""

    valid = [(r["date"], r["pm25"]) for r in records if r["pm25"] is not None]
    if not valid:
        print("PM2.5 無資料，跳過圖 2")
        return

    dates, values = zip(*valid)
    max_val = max(values)
    colors  = ["#E15759" if v == max_val else "#4E79A7" for v in values]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(dates, values, color=colors, edgecolor="white", linewidth=0.5)

    # 數值標籤
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9)

    # WHO 年平均標準線
    ax.axhline(5, color="gray", linestyle="--", linewidth=1, alpha=0.7)
    ax.text(dates[-1], 5.3, "WHO 標準 5", color="gray", fontsize=8, ha="right")

    ax.set_title(f"{site} 測站 PM2.5 月平均（紅色為最高月份）",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("月份")
    ax.set_ylabel("PM2.5 (μg/m³)")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()

    return _save(fig, filename)


# ── 圖 3：PM10 月份長條圖 ──────────────────────────────────
def plot_pm10_bar(records, site, filename="fig3_pm10_bar.png"):
    """PM10 各月長條圖，最高月份標紅。"""

    valid = [(r["date"], r["pm10"]) for r in records if r["pm10"] is not None]
    if not valid:
        print("PM10 無資料，跳過圖 3")
        return

    dates, values = zip(*valid)
    max_val = max(values)
    colors  = ["#E15759" if v == max_val else "#F28E2B" for v in values]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(dates, values, color=colors, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9)

    ax.set_title(f"{site} 測站 PM10 月平均（紅色為最高月份）",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("月份")
    ax.set_ylabel("PM10 (μg/m³)")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()

    return _save(fig, filename)


# ── 圖 4：四季平均雷達圖 ───────────────────────────────────
def plot_seasonal_bar(seasonal_data, site, filename="fig4_seasonal.png"):
    """四季平均 PM2.5 / PM10 分組長條圖。"""

    seasons = ["春", "夏", "秋", "冬"]
    pm25_vals = [seasonal_data[s]["avg_pm25"] or 0 for s in seasons]
    pm10_vals = [seasonal_data[s]["avg_pm10"] or 0 for s in seasons]

    x = range(len(seasons))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width/2 for i in x], pm25_vals, width,
           label="PM2.5", color="#4E79A7", edgecolor="white")
    ax.bar([i + width/2 for i in x], pm10_vals, width,
           label="PM10",  color="#F28E2B", edgecolor="white")

    ax.set_title(f"{site} 測站四季平均 PM2.5 / PM10",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(seasons, fontsize=12)
    ax.set_ylabel("濃度 (μg/m³)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    fig.tight_layout()

    return _save(fig, filename)