# main.py
# ==================================================
# 空氣品質分析主程式
# 功能：
# 1. 讀取空氣品質 CSV 檔案
# 2. 執行統計分析
# 3. 顯示分析結果
# 4. 產生圖表並輸出成 PNG
# ==================================================

# 匯入 sys 模組
# 用於程式異常時結束程式
import sys

# 從 parser.py 匯入資料解析函式
# 功能：讀取 CSV 並整理成 records 格式
from parser import parse_air_quality_file

# 從 analyzer.py 匯入統計分析相關函式
from analyzer import (
    summarize_records,       # 整體統計摘要
    print_summary,           # 印出統計結果
    find_worst_months_pm25,  # 找出 PM2.5 最差月份
    find_worst_months_pm10,  # 找出 PM10 最差月份
    seasonal_average         # 計算四季平均
)

# 從 visualizer.py 匯入繪圖函式
from visualizer import (
    plot_monthly_trend,  # 月趨勢折線圖
    plot_pm25_bar,       # PM2.5 長條圖
    plot_pm10_bar,       # PM10 長條圖
    plot_seasonal_bar    # 四季比較圖
)

# ==================================================
# 可調整參數區
# ==================================================

# 輸入檔案位置
INPUT_FILE = "data/air_quality.csv"

# 圖片輸出資料夾
OUTPUT_FOLDER = "figures"

# 顯示污染最嚴重前幾個月份
TOP_N = 3

# ==================================================
# 主程式
# ==================================================
def main():

    # ==============================================
    # 讀取資料
    # ==============================================

    try:
        # 呼叫 parser.py 解析資料
        #
        # records:
        # [
        #   {
        #     "site":"基隆",
        #     "date":"2025/01",
        #     "pm25":18.2,
        #     "pm10":35.6
        #   }
        # ]
        #
        # site:
        # "基隆"
        records, site = parse_air_quality_file(INPUT_FILE)

    # 找不到檔案
    except FileNotFoundError as e:

        # 顯示錯誤訊息
        print(e)

        # 提示使用者放置資料檔案
        print("請將 CSV 放到 data/air_quality.csv 後重新執行")

        # 結束程式
        sys.exit(1)

    # 其他例外錯誤
    except Exception as e:

        # 顯示錯誤原因
        print(f"資料讀取失敗：{e}")

        # 結束程式
        sys.exit(1)

    # 若 records 為空
    if not records:

        # 表示沒有成功解析出資料
        print("沒有有效資料，程式結束")

        # 結束函式
        return

    # ==============================================
    # 統計分析
    # ==============================================

    # 計算整體統計摘要
    #
    # summary 範例：
    # {
    #   "total_months":12,
    #   "avg_pm25":15.3,
    #   "max_pm25":32.1,
    #   "min_pm25":7.2,
    #   ...
    # }
    summary = summarize_records(records)

    # 印出統計結果
    print_summary(summary, site)

    # ==============================================
    # PM2.5 最差月份分析
    # ==============================================

    # 取得 PM2.5 最高前 TOP_N 名月份
    worst_pm25 = find_worst_months_pm25(
        records,
        top_n=TOP_N
    )

    # 顯示標題
    print(f"\nPM2.5 最高 Top {TOP_N} 月份：")

    # enumerate(...,1)
    # 讓排名從 1 開始
    for i, r in enumerate(worst_pm25, 1):

        # r 為單筆月份資料
        # 顯示排名、日期、PM2.5 值
        print(
            f"  {i}. "
            f"{r['date']}  "
            f"PM2.5：{r['pm25']:.1f} μg/m³"
        )

    # ==============================================
    # PM10 最差月份分析
    # ==============================================

    # 取得 PM10 最高前 TOP_N 名月份
    worst_pm10 = find_worst_months_pm10(
        records,
        top_n=TOP_N
    )

    # 顯示標題
    print(f"\nPM10 最高 Top {TOP_N} 月份：")

    # 顯示排名結果
    for i, r in enumerate(worst_pm10, 1):

        print(
            f"  {i}. "
            f"{r['date']}  "
            f"PM10：{r['pm10']:.1f} μg/m³"
        )

    # ==============================================
    # 四季平均分析
    # ==============================================

    # 計算春夏秋冬平均值
    seasonal = seasonal_average(records)

    # 顯示標題
    print("\n四季平均：")

    # seasonal.items()
    # 逐一取得季節與對應資料
    for season, data in seasonal.items():

        # 若有資料則顯示數值
        if data["avg_pm25"] is not None:
            pm25 = f"{data['avg_pm25']:.1f}"
        else:
            pm25 = "N/A"

        # 若有資料則顯示數值
        if data["avg_pm10"] is not None:
            pm10 = f"{data['avg_pm10']:.1f}"
        else:
            pm10 = "N/A"

        # 顯示結果
        print(
            f"  {season}："
            f"PM2.5={pm25}  "
            f"PM10={pm10}"
        )

    # ==============================================
    # 開始繪圖
    # ==============================================

    print("\n開始繪圖...")

    # ----------------------------------------------
    # 圖1：PM2.5 / PM10 趨勢折線圖
    # ----------------------------------------------
    try:

        # 呼叫繪圖函式
        plot_monthly_trend(records, site)

    except Exception as e:

        # 若失敗顯示原因
        print(f"圖 1 失敗：{e}")

    # ----------------------------------------------
    # 圖2：PM2.5 長條圖
    # ----------------------------------------------
    try:

        plot_pm25_bar(records, site)

    except Exception as e:

        print(f"圖 2 失敗：{e}")

    # ----------------------------------------------
    # 圖3：PM10 長條圖
    # ----------------------------------------------
    try:

        plot_pm10_bar(records, site)

    except Exception as e:

        print(f"圖 3 失敗：{e}")

    # ----------------------------------------------
    # 圖4：四季比較圖
    # ----------------------------------------------
    try:

        plot_seasonal_bar(
            seasonal,
            site
        )

    except Exception as e:

        print(f"圖 4 失敗：{e}")

    # ==============================================
    # 全部完成
    # ==============================================

    print("\n所有分析完成，圖片已輸出至 figures/")


# ==================================================
# Python 程式入口點
# ==================================================
#
# 當直接執行：
# python main.py
#
# __name__ 會等於 "__main__"
#
# 因此會執行 main()
#
# 若被其他程式 import：
# 不會自動執行 main()
#
# ==================================================
if __name__ == "__main__":
    main()