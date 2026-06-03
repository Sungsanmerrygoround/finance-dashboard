# storage.py — ③ 저장하기

import csv
import os
from datetime import datetime

DATA_FILE = "data/history.csv"
FIELDNAMES = ["date", "name", "ticker", "price", "change", "change_pct"]


def save_data(processed_data):
    """가공된 데이터를 CSV에 날짜별로 누적 저장"""
    os.makedirs("data", exist_ok=True)  # data 폴더 없으면 자동 생성

    today = datetime.today().strftime("%Y-%m-%d")

    if _already_saved(today):
        print(f"[건너뜀] {today} 데이터가 이미 있어요.")
        return

    file_exists = os.path.exists(DATA_FILE)

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()  # 파일 처음 만들 때만 헤더 한 번 씀

        for name, info in processed_data.items():
            writer.writerow({
                "date":       today,
                "name":       name,
                "ticker":     info["ticker"],
                "price":      info["price"],
                "change":     info["change"],
                "change_pct": info["change_pct"],
            })

    print(f"[저장 완료] {today} — {len(processed_data)}개 항목 → {DATA_FILE}")


def load_data():
    """저장된 전체 히스토리를 읽어서 반환"""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _already_saved(date):
    """해당 날짜 데이터가 이미 저장됐는지 확인 (중복 방지)"""
    for row in load_data():
        if row["date"] == date:
            return True
    return False


if __name__ == "__main__":
    from fetch import fetch_data
    from process import process_data

    raw       = fetch_data()
    processed = process_data(raw)
    save_data(processed)

    print("\n--- 저장된 전체 기록 ---")
    for row in load_data():
        print(row)