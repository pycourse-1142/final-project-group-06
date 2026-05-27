# analyzer.py
# 統計分析模組（配合月平均值格式）


def calculate_average(values):
    """計算平均值（自動過濾 None）。"""
    valid = [v for v in values if v is not None]
    if not valid:
        return None
    return sum(valid) / len(valid)


def summarize_records(records):
    """整體統計摘要。"""
    if not records:
        return {}

    pm25s = [r["pm25"] for r in records if r["pm25"] is not None]
    pm10s = [r["pm10"] for r in records if r["pm10"] is not None]

    summary = {
        "total_months": len(records),
    }

    if pm25s:
        summary["avg_pm25"] = sum(pm25s) / len(pm25s)
        summary["max_pm25"] = max(pm25s)
        summary["min_pm25"] = min(pm25s)

    if pm10s:
        summary["avg_pm10"] = sum(pm10s) / len(pm10s)
        summary["max_pm10"] = max(pm10s)
        summary["min_pm10"] = min(pm10s)

    return summary


def find_worst_months_pm25(records, top_n=3):
    """PM2.5 最高的前 N 個月。"""
    valid = [r for r in records if r["pm25"] is not None]
    sorted_r = sorted(valid, key=lambda x: x["pm25"], reverse=True)
    return sorted_r[:top_n]


def find_worst_months_pm10(records, top_n=3):
    """PM10 最高的前 N 個月。"""
    valid = [r for r in records if r["pm10"] is not None]
    sorted_r = sorted(valid, key=lambda x: x["pm10"], reverse=True)
    return sorted_r[:top_n]


def seasonal_average(records):
    """
    計算四季平均（PM2.5 / PM10）。
    春：3-5月  夏：6-8月  秋：9-11月  冬：12-2月
    """
    season_map = {
        "01": "冬", "02": "冬", "03": "春",
        "04": "春", "05": "春", "06": "夏",
        "07": "夏", "08": "夏", "09": "秋",
        "10": "秋", "11": "秋", "12": "冬",
    }

    seasonal = {"春": {"pm25": [], "pm10": []},
                "夏": {"pm25": [], "pm10": []},
                "秋": {"pm25": [], "pm10": []},
                "冬": {"pm25": [], "pm10": []}}

    for r in records:
        month = r["date"].split("/")[-1]   # "2025/01" → "01"
        season = season_map.get(month, "")
        if not season:
            continue
        if r["pm25"] is not None:
            seasonal[season]["pm25"].append(r["pm25"])
        if r["pm10"] is not None:
            seasonal[season]["pm10"].append(r["pm10"])

    result = {}
    for season, data in seasonal.items():
        result[season] = {
            "avg_pm25": calculate_average(data["pm25"]),
            "avg_pm10": calculate_average(data["pm10"]),
        }
    return result


def print_summary(summary, site):
    """印出統計摘要。"""
    print(f"\n===== {site} 空氣品質統計摘要 =====")
    print(f"資料月份數：{summary.get('total_months', 0)}")
    if "avg_pm25" in summary:
        print(f"PM2.5  平均：{summary['avg_pm25']:.2f} μg/m³  "
              f"最高：{summary['max_pm25']:.2f}  最低：{summary['min_pm25']:.2f}")
    if "avg_pm10" in summary:
        print(f"PM10   平均：{summary['avg_pm10']:.2f} μg/m³  "
              f"最高：{summary['max_pm10']:.2f}  最低：{summary['min_pm10']:.2f}")
    print("=" * 38)