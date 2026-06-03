# main.py
# 空氣品質分析主程式（月平均值格式）
import sys
from parser     import parse_air_quality_file
from analyzer   import (summarize_records, print_summary,
                        find_worst_months_pm25, find_worst_months_pm10,
                        seasonal_average)
from visualizer import (plot_monthly_trend, plot_pm25_bar,
                        plot_pm10_bar, plot_seasonal_bar)

# ── 可調整參數 ────────────────────────────────────────────
INPUT_FILE    = "data/air_quality.csv"
OUTPUT_FOLDER = "figures"
TOP_N         = 3    # 顯示最差前幾個月
# ─────────────────────────────────────────────────────────

def main():
    # ── 讀取資料 ─────────────────────────────────────────
    try:
        records, site = parse_air_quality_file(INPUT_FILE)
    except FileNotFoundError as e:
        print(e)
        print("請將 CSV 放到 data/air_quality.csv 後重新執行")
        sys.exit(1)
    except Exception as e:
        print(f"資料讀取失敗：{e}")
        sys.exit(1)

    if not records:
        print("沒有有效資料，程式結束")
        return

    # ── 統計分析 ─────────────────────────────────────────
    summary = summarize_records(records)
    print_summary(summary, site)

    # PM2.5 最差月份
    worst_pm25 = find_worst_months_pm25(records, top_n=TOP_N)
    print(f"\nPM2.5 最高 Top {TOP_N} 月份：")
    for i, r in enumerate(worst_pm25, 1):
        print(f"  {i}. {r['date']}  PM2.5：{r['pm25']:.1f} μg/m³")

    # PM10 最差月份
    worst_pm10 = find_worst_months_pm10(records, top_n=TOP_N)
    print(f"\nPM10 最高 Top {TOP_N} 月份：")
    for i, r in enumerate(worst_pm10, 1):
        print(f"  {i}. {r['date']}  PM10：{r['pm10']:.1f} μg/m³")

    # 四季分析
    seasonal = seasonal_average(records)
    print("\n四季平均：")
    for season, data in seasonal.items():
        pm25 = f"{data['avg_pm25']:.1f}" if data["avg_pm25"] is not None else "N/A"
        pm10 = f"{data['avg_pm10']:.1f}" if data["avg_pm10"] is not None else "N/A"
        print(f"  {season}：PM2.5={pm25}  PM10={pm10}")

    # ── 畫圖輸出 ─────────────────────────────────────────
    print("\n開始繪圖...")
    try:
        plot_monthly_trend(records, site)
    except Exception as e:
        print(f"圖 1 失敗：{e}")

    try:
        plot_pm25_bar(records, site)
    except Exception as e:
        print(f"圖 2 失敗：{e}")

    try:
        plot_pm10_bar(records, site)
    except Exception as e:
        print(f"圖 3 失敗：{e}")

    try:
        plot_seasonal_bar(seasonal, site)
    except Exception as e:
        print(f"圖 4 失敗：{e}")

    print("\n所有分析完成，圖片已輸出至 figures/")


if __name__ == "__main__":
    main()