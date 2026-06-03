# render.py — ④ HTML 대시보드 생성

from datetime import datetime
from storage import load_data

OUTPUT_FILE = "index.html"


def render_dashboard(processed_data):
    """가공된 데이터로 HTML 대시보드 파일 생성"""
    history  = load_data()
    cards    = _build_cards(processed_data)
    chart    = _build_chart(history)
    updated  = datetime.today().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>금융 대시보드</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, sans-serif; background: #f5f5f5; padding: 32px; }}
    h1 {{ font-size: 22px; margin-bottom: 4px; }}
    .sub {{ color: #999; font-size: 13px; margin-bottom: 28px; }}
    .cards {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 32px; }}
    .card {{ background: white; border-radius: 12px; padding: 20px; min-width: 180px;
             box-shadow: 0 1px 6px rgba(0,0,0,0.07); }}
    .card-name  {{ font-size: 13px; color: #999; margin-bottom: 8px; }}
    .card-price {{ font-size: 22px; font-weight: 600; margin-bottom: 4px; }}
    .card-change {{ font-size: 14px; }}
    .green {{ color: #16a34a; }}
    .red   {{ color: #dc2626; }}
    .gray  {{ color: #999; }}
    .box   {{ background: white; border-radius: 12px; padding: 24px;
              box-shadow: 0 1px 6px rgba(0,0,0,0.07); }}
    .box h2 {{ font-size: 15px; color: #666; margin-bottom: 16px; }}
  </style>
</head>
<body>
  <h1>📈 금융 대시보드</h1>
  <p class="sub">마지막 업데이트: {updated}</p>

  <div class="cards">
{cards}
  </div>

  <div class="box">
    <h2>히스토리</h2>
    {chart}
  </div>
</body>
</html>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[완료] {OUTPUT_FILE} 생성됨 — 브라우저로 열어보세요!")


def _build_cards(processed_data):
    """종목별 카드 HTML 조각 생성"""
    cards = []
    for name, info in processed_data.items():
        cards.append(f"""    <div class="card">
      <div class="card-name">{name}</div>
      <div class="card-price">{info['price_str']}</div>
      <div class="card-change {info['color']}">{info['change_str']}</div>
    </div>""")
    return "\n".join(cards)


def _build_chart(history):
    """히스토리로 차트 생성 — 데이터가 2일치 미만이면 안내 메시지"""
    dates = set(row["date"] for row in history)
    if len(dates) < 2:
        return '<p style="color:#bbb; font-size:14px; padding: 8px 0;">데이터가 쌓이면 차트가 표시돼요. 내일 다시 실행해보세요 :)</p>'

    import plotly.graph_objects as go

    names = list(set(row["name"] for row in history))
    fig   = go.Figure()

    for name in names:
        rows = sorted([r for r in history if r["name"] == name], key=lambda r: r["date"])
        fig.add_trace(go.Scatter(
            x    = [r["date"]        for r in rows],
            y    = [float(r["price"]) for r in rows],
            name = name,
            mode = "lines+markers",
        ))

    fig.update_layout(height=320, margin=dict(l=0, r=0, t=8, b=0),
                      plot_bgcolor="white", paper_bgcolor="white")
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


if __name__ == "__main__":
    from fetch import fetch_data
    from process import process_data

    raw       = fetch_data()
    processed = process_data(raw)
    render_dashboard(processed)