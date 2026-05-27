# parser.py
# 讀取環境部「月平均值查詢」格式 CSV
# 格式：測項, 日期, 平均值, 單位, 備註（Big5 編碼）
import csv
import os


# 從標題列抽出測站名稱
# 例如「月平均值查詢-基隆」→「基隆」
def _extract_site(header_row):
    text = header_row[0] if header_row else ""
    if "-" in text:
        return text.split("-")[-1].strip()
    return "未知測站"


def parse_air_quality_file(filepath):
    """
    讀取月平均值 CSV，回傳整理後的 records。

    每筆 record：
        {
            "site":  測站名稱,
            "date":  "2025/01",
            "pm25":  float 或 None,
            "pm10":  float 或 None,
        }
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到檔案：{filepath}")

    # 讀取原始列
    raw = []
    for enc in ["big5", "cp950", "utf-8-sig"]:
        try:
            with open(filepath, encoding=enc) as f:
                raw = list(csv.reader(f))
            break
        except UnicodeDecodeError:
            continue

    if not raw:
        raise ValueError("無法解析檔案編碼")

    # 第一列是站名標題
    site = _extract_site(raw[0])

    # 收集 PM2.5 / PM10 各月數值
    # 用 dict[date] = {"pm25": ..., "pm10": ...} 合併
    monthly = {}

    invalid = {"", "#", "*", "x", "X", "-", "NR", "NA", "ND"}

    for row in raw[3:]:   # 前三列是標題，跳過
        if len(row) < 3:
            continue

        item  = row[0].strip()
        date  = row[1].strip()
        value = row[2].strip()

        # 只取 PM2.5 / PM10
        if item not in ("PM2.5", "PM10"):
            continue

        if date not in monthly:
            monthly[date] = {"pm25": None, "pm10": None}

        if value in invalid:
            continue

        try:
            v = float(value)
        except ValueError:
            continue

        # 過濾異常值
        if item == "PM2.5" and 0 <= v <= 500:
            monthly[date]["pm25"] = v
        elif item == "PM10" and 0 <= v <= 600:
            monthly[date]["pm10"] = v

    # 組成 records，依日期排序
    records = []
    for date in sorted(monthly.keys()):
        entry = monthly[date]
        # PM2.5 / PM10 至少要有一個有效值
        if entry["pm25"] is None and entry["pm10"] is None:
            continue
        records.append({
            "site":  site,
            "date":  date,
            "pm25":  entry["pm25"],
            "pm10":  entry["pm10"],
        })

    print(f"測站：{site}，解析完成：{len(records)} 個月份")
    return records, site