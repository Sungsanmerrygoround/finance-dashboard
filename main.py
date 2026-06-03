# main.py — 네 단계를 순서대로 실행

from fetch   import fetch_data
from process import process_data
from storage import save_data
from render  import render_dashboard

def main():
    print("① 데이터 가져오는 중...")
    raw = fetch_data()

    print("② 가공 중...")
    processed = process_data(raw)

    print("③ 저장 중...")
    save_data(processed)

    print("④ 대시보드 생성 중...")
    render_dashboard(processed)

    print("\n✅ 완료! dashboard.html을 열어보세요.")

if __name__ == "__main__":
    main()