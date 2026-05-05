"""
第6课：价差监控器
—— 每10秒扫描一次，发现价差过大就报警
"""

import urllib.request
import json
import time

def get_price(name, url, parser):
    """从指定API抓价格"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        return parser(data)
    except:
        return None

# 设置报警阈值（bps）
ALERT_THRESHOLD = 10   # 价差超过10个基点就报警
CHECK_INTERVAL = 10    # 每10秒查一次

print("🚀 价差监控器已启动")
print(f"📊 报警阈值: {ALERT_THRESHOLD} bps")
print(f"⏱  扫描间隔: {CHECK_INTERVAL} 秒")
print("=" * 55)
print("按 Ctrl+C 停止监控")
print("=" * 55)

round_num = 0

while True:
    round_num += 1
    
    # 抓三个源的价格
    cg = get_price("CoinGecko",
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
        lambda d: d["bitcoin"]["usd"])
    
    ba = get_price("币安",
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        lambda d: float(d["price"]))
    
    ok = get_price("OKX",
        "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
        lambda d: float(d["data"][0]["last"]))

    t = time.localtime()
    ts = f"{t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"

    print(f"\n[{ts}] 第 {round_num} 轮扫描")

    if ba and ok:
        diff = ba - ok
        diff_pct = diff / ((ba + ok) / 2) * 10000
        status = "⚠️ 警报！" if abs(diff_pct) > ALERT_THRESHOLD else "✅ 正常"
        print(f"  币安 vs OKX: {diff:+,.2f} ({diff_pct:+.2f} bps) {status}")
    
    if ba and cg:
        diff = ba - cg
        diff_pct = diff / ((ba + cg) / 2) * 10000
        status = "⚠️ 警报！" if abs(diff_pct) > ALERT_THRESHOLD else "✅ 正常"
        print(f"  币安 vs CoinGecko: {diff:+,.2f} ({diff_pct:+.2f} bps) {status}")

    # 等一会再查下一次
    time.sleep(CHECK_INTERVAL)
