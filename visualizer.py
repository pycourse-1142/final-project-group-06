# visualizer.py
# ==================================================
# 視覺化模組
#
# 功能：
# 1. 建立輸出資料夾
# 2. 繪製 PM2.5 / PM10 月趨勢圖
# 3. 繪製 PM2.5 長條圖
# 4. 繪製 PM10 長條圖
# 5. 繪製四季平均比較圖
# 6. 輸出 PNG 圖片
#
# 使用套件：
# matplotlib
# ==================================================

# 作業系統模組
# 用於建立資料夾與組合檔案路徑
import os

# matplotlib 主模組
import matplotlib

# 使用 Agg 後端
# 適合產生圖片，不需要開啟視窗
# 在伺服器或 VS Code 執行較穩定
matplotlib.use("Agg")

# pyplot 繪圖模組
import matplotlib.pyplot as plt

# ==================================================
# 中文字型設定
# 避免中文顯示成方框
# ==================================================
plt.rcParams["font.sans-serif"] = [

    # Windows 常見字型
    "Microsoft JhengHei",

    # Linux 常見中文字型
    "Noto Sans CJK TC",

    # MacOS 常見中文字型
    "PingFang TC",

    # 預設字型
    "sans-serif"
]

# 避免負號變成亂碼
plt.rcParams["axes.unicode_minus"] = False

# ==================================================
# 圖片輸出資料夾
# ==================================================
FIGURES_DIR = "figures"


# ==================================================
# 建立輸出資料夾
#
# 若 figures 不存在
# 則自動建立
# ==================================================
def ensure_output_folder(folder=FIGURES_DIR):

    # 檢查資料夾是否存在
    if not os.path.exists(folder):

        # 建立資料夾
        os.makedirs(folder)


# ==================================================
# 統一圖片儲存函式
#
# 參數：
# fig      → matplotlib 圖形物件
# filename → 檔名
#
# 回傳：
# 圖片完整路徑
# ==================================================
def _save(fig, filename):

    # 確保輸出資料夾存在
    ensure_output_folder()

    # 組合完整路徑
    #
    # figures + fig1.png
    # ->
    # figures/fig1.png
    #
    path = os.path.join(
        FIGURES_DIR,
        filename
    )

    # 儲存圖片
    fig.savefig(

        path,

        # 解析度
        dpi=150,

        # 自動調整邊界
        bbox_inches="tight"
    )

    # 關閉圖表
    # 釋放記憶體
    plt.close(fig)

    # 顯示儲存訊息
    print(f"已儲存：{path}")

    # 回傳路徑
    return path


# ==================================================
# 圖1：PM2.5 / PM10 月趨勢折線圖
#
# 顯示：
# 每月 PM2.5
# 每月 PM10
#
# 並加入 WHO PM2.5 標準線
# ==================================================
def plot_monthly_trend(
    records,
    site,
    filename="fig1_monthly_trend.png"
):

    # ==============================================
    # 取得所有日期
    # ==============================================
    dates = [

        r["date"]

        for r in records
    ]

    # ==============================================
    # 取得 PM2.5 數值
    # ==============================================
    pm25s = [

        r["pm25"]

        for r in records
    ]

    # ==============================================
    # 取得 PM10 數值
    # ==============================================
    pm10s = [

        r["pm10"]

        for r in records
    ]

    # 建立圖表
    fig, ax = plt.subplots(

        figsize=(12, 5)
    )

    # ==============================================
    # 畫 PM2.5 折線
    # ==============================================
    if any(v is not None for v in pm25s):

        ax.plot(

            dates,
            pm25s,

            # 圓形標記
            marker="o",

            # 顏色
            color="#4E79A7",

            # 線寬
            linewidth=2,

            # 圖例名稱
            label="PM2.5 (μg/m³)",

            # 顯示層級
            zorder=3
        )

    # ==============================================
    # 畫 PM10 折線
    # ==============================================
    if any(v is not None for v in pm10s):

        ax.plot(

            dates,
            pm10s,

            # 方形標記
            marker="s",

            color="#F28E2B",

            linewidth=2,

            label="PM10 (μg/m³)",

            zorder=3
        )

    # ==============================================
    # WHO PM2.5 標準線
    #
    # 年平均：
    # 5 μg/m³
    # ==============================================
    ax.axhline(

        5,

        color="#4E79A7",

        linestyle="--",

        linewidth=1,

        alpha=0.5
    )

    # 標準線文字
    ax.text(

        dates[-1],

        5.5,

        "WHO PM2.5 標準 5",

        color="#4E79A7",

        fontsize=8,

        ha="right"
    )

    # 圖表標題
    ax.set_title(

        f"{site} 測站 PM2.5 / PM10 月平均趨勢",

        fontsize=14,

        fontweight="bold"
    )

    # X軸名稱
    ax.set_xlabel("月份")

    # Y軸名稱
    ax.set_ylabel("濃度 (μg/m³)")

    # 顯示圖例
    ax.legend()

    # 顯示格線
    ax.grid(

        axis="y",

        alpha=0.3,

        linestyle="--"
    )

    # X軸文字旋轉
    plt.xticks(

        rotation=30,

        ha="right"
    )

    # 自動調整版面
    fig.tight_layout()

    # 儲存圖片
    return _save(fig, filename)


# ==================================================
# 圖2：PM2.5 長條圖
#
# 最高月份標示紅色
# ==================================================
def plot_pm25_bar(
    records,
    site,
    filename="fig2_pm25_bar.png"
):

    # 只保留有效 PM2.5 資料
    valid = [

        (r["date"], r["pm25"])

        for r in records

        if r["pm25"] is not None
    ]

    # 沒資料直接離開
    if not valid:

        print("PM2.5 無資料，跳過圖 2")

        return

    # 拆成日期與數值
    dates, values = zip(*valid)

    # 找出最大值
    max_val = max(values)

    # 顏色設定
    colors = [

        "#E15759" if v == max_val

        else "#4E79A7"

        for v in values
    ]

    # 建立圖表
    fig, ax = plt.subplots(

        figsize=(12, 5)
    )

    # 畫長條圖
    bars = ax.bar(

        dates,

        values,

        color=colors,

        edgecolor="white",

        linewidth=0.5
    )

    # ==============================================
    # 顯示數值標籤
    # ==============================================
    for bar, val in zip(bars, values):

        ax.text(

            bar.get_x() + bar.get_width()/2,

            bar.get_height() + 0.2,

            f"{val:.1f}",

            ha="center",

            va="bottom",

            fontsize=9
        )

    # WHO 標準線
    ax.axhline(

        5,

        color="gray",

        linestyle="--",

        linewidth=1,

        alpha=0.7
    )

    ax.text(

        dates[-1],

        5.3,

        "WHO 標準 5",

        color="gray",

        fontsize=8,

        ha="right"
    )

    ax.set_title(
        f"{site} 測站 PM2.5 月平均（紅色為最高月份）",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("月份")
    ax.set_ylabel("PM2.5 (μg/m³)")

    ax.grid(axis="y", alpha=0.3, linestyle="--")

    plt.xticks(rotation=30, ha="right")

    fig.tight_layout()

    return _save(fig, filename)


# ==================================================
# 圖3：PM10 長條圖
#
# 與 PM2.5 邏輯相同
# 差別只有資料來源改為 PM10
# ==================================================
def plot_pm10_bar(
    records,
    site,
    filename="fig3_pm10_bar.png"
):

    valid = [
        (r["date"], r["pm10"])
        for r in records
        if r["pm10"] is not None
    ]

    if not valid:
        print("PM10 無資料，跳過圖 3")
        return

    dates, values = zip(*valid)

    max_val = max(values)

    colors = [
        "#E15759" if v == max_val
        else "#F28E2B"
        for v in values
    ]

    fig, ax = plt.subplots(figsize=(12, 5))

    bars = ax.bar(
        dates,
        values,
        color=colors,
        edgecolor="white",
        linewidth=0.5
    )

    for bar, val in zip(bars, values):

        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.2,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    ax.set_title(
        f"{site} 測站 PM10 月平均（紅色為最高月份）",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("月份")
    ax.set_ylabel("PM10 (μg/m³)")

    ax.grid(axis="y", alpha=0.3, linestyle="--")

    plt.xticks(rotation=30, ha="right")

    fig.tight_layout()

    return _save(fig, filename)


# ==================================================
# 圖4：四季平均比較圖
#
# 春 夏 秋 冬
#
# PM2.5
# PM10
#
# 分組長條圖比較
# ==================================================
def plot_seasonal_bar(
    seasonal_data,
    site,
    filename="fig4_seasonal.png"
):

    # 季節順序
    seasons = ["春", "夏", "秋", "冬"]

    # PM2.5 四季平均
    pm25_vals = [
        seasonal_data[s]["avg_pm25"] or 0
        for s in seasons
    ]

    # PM10 四季平均
    pm10_vals = [
        seasonal_data[s]["avg_pm10"] or 0
        for s in seasons
    ]

    # X軸位置
    x = range(len(seasons))

    # 長條寬度
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))

    # PM2.5 長條
    ax.bar(
        [i - width/2 for i in x],
        pm25_vals,
        width,
        label="PM2.5",
        color="#4E79A7",
        edgecolor="white"
    )

    # PM10 長條
    ax.bar(
        [i + width/2 for i in x],
        pm10_vals,
        width,
        label="PM10",
        color="#F28E2B",
        edgecolor="white"
    )

    ax.set_title(
        f"{site} 測站四季平均 PM2.5 / PM10",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(seasons)

    ax.set_ylabel("濃度 (μg/m³)")

    ax.legend()

    ax.grid(
        axis="y",
        alpha=0.3,
        linestyle="--"
    )

    fig.tight_layout()

    return _save(fig, filename)