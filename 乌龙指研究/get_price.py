"""
第3课：我的第一个行情抓取脚本
—— 从多个源抓比特币价格（国内可用版）
"""

import urllib.request
import json
import time

def fetch_price(name, url, parser):
    """尝试从一个源抓价格，失败就返回None"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        price = parser(data)
        print(f"  ✅ {name}: ${price:,.2f}")
        return price
    except Exception as e:
        print(f"  ❌ {name}: 连不上 ({str(e)[:40]})")
        return None

print("📡 正在查询比特币价格...")
print("=" * 55)

# ===== 同时尝试多个数据源 =====
prices = []

# 源1：CoinGecko（国内能打开）
p1 = fetch_price("CoinGecko", 
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
    lambda d: d["bitcoin"]["usd"])
if p1: prices.append(("CoinGecko", p1))

# 源2：币安（用国内访问的镜像或直连）
p2 = fetch_price("币安(Binance)",
    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
    lambda d: float(d["price"]))
if p2: prices.append(("币安", p2))

# 源3：OKX
p3 = fetch_price("OKX",
    "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
    lambda d: float(d["data"][0]["last"]))
if p3: prices.append(("OKX", p3))

# ===== 显示结果 =====
print("=" * 55)

if len(prices) >= 2:
    # 用第一个作为基准算价差
    ref_name, ref_price = prices[0]
    print(f"\n📊 以 {ref_name} 为基准：")
    for name, price in prices[1:]:
        diff = price - ref_price
        diff_pct = diff / ref_price * 10000
        print(f"   {name} vs {ref_name}: {diff:+,.2f} ({diff_pct:+.2f} bps)")

elif len(prices) == 1:
    name, price = prices[0]
    print(f"\n💰 只连上了一个源：{name} = ${price:,.2f}")
    print("   一个源也能用，后面学到多源对比就有意思了！")
else:
    print("\n⚠️  所有源都连不上，可能是因为：")
    print("   1. 开了VPN/代理（试试关掉）")
    print("   2. 公司/学校网络限制了外网")
    print("   3. DNS解析问题")

# ===== 时间戳 =====
t = time.localtime()
print(f"\n🕐 查询时间: {t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}")
print("=" * 55)
