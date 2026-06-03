# process.py — ② 데이터 가공하기

def process_data(raw_data):
    """fetch_data()의 결과를 화면에 표시하기 좋은 형태로 가공"""
    result = {}

    for name, info in raw_data.items():
        pct = info["change_pct"]

        # 등락 방향과 색상 결정
        if pct > 0:
            direction = "▲"
            color = "green"
        elif pct < 0:
            direction = "▼"
            color = "red"
        else:
            direction = "—"
            color = "gray"

        result[name] = {
            **info,                              # fetch에서 온 데이터 그대로 유지
            "direction":  direction,
            "color":      color,
            "price_str":  f"{info['price']:,.2f}",        # 예: 1,517.37
            "change_str": f"{direction} {abs(pct):.2f}%", # 예: ▲ 0.40%
        }

    return result


if __name__ == "__main__":
    from fetch import fetch_data

    raw       = fetch_data()
    processed = process_data(raw)

    for name, info in processed.items():
        print(f"{name:10}  {info['price_str']:>15}  {info['change_str']}")