#!/usr/bin/env python3
"""
MEME币热度监控
监测链上异动：价格飙升、成交量暴增、换手率异常
数据源：Binance公共API（无需Key）
"""
import json, os, sys, time, subprocess, platform, csv
import urllib.request
from datetime import datetime
from collections import deque

# ── 微信推送 ──
SKILL_DIR = os.environ.get("SKILL_DIR", r"C:\Users\user\.workbuddy\skills\alarm-memo-assistant-pro")
SEND_WECHAT = os.path.join(SKILL_DIR, "scripts", "send_wechat.py")
PYTHON_EXE = r"C:\Users\user\.workbuddy\binaries\python\versions\3.13.12\python.exe"

def wechat(msg):
    try:
        env = os.environ.copy()
        env["SKILL_DIR"] = SKILL_DIR
        subprocess.run([PYTHON_EXE, SEND_WECHAT, "send", msg],
            capture_output=True, text=True, encoding="utf-8", timeout=15, env=env)
    except:
        pass

PROXY = "http://127.0.0.1:6864"
handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(handler)

BASE = r"C:\Users\user\WorkBuddy\Claw\乌龙指研究"
LOG_DIR = os.path.join(BASE, "results")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_CSV = os.path.join(LOG_DIR, "meme_heat_log.csv")
ALERT_LOG = os.path.join(LOG_DIR, "meme_alerts.json")

# 监控的MEME币（成交量降序）
MEME_COINS = [
    "DOGE", "PEPE", "WIF", "BONK", "PENGU", "SHIB",
    "FLOKI", "BOME", "MEW", "POPCAT", "NEIRO", "BABYDOGE",
]

# 上次价格缓存：symbol -> {price, vol_24h, time}
price_cache = {}
alerts = []

def fetch_all():
    """获取所有MEME币的24h行情"""
    result = []
    try:
        # 批量获取24h ticker
        req = urllib.request.Request(
            'https://api.binance.com/api/v3/ticker/24hr',
            headers={'User-Agent': 'Mozilla/5.0'})
        resp = opener.open(req, timeout=10)
        all_tickers = json.loads(resp.read().decode())
        
        for t in all_tickers:
            sym = t['symbol'].replace('USDT', '')
            if sym in MEME_COINS:
                result.append({
                    'name': sym,
                    'price': float(t['lastPrice']),
                    'chg_pct': float(t['priceChangePercent']),
                    'high': float(t['highPrice']),
                    'low': float(t['lowPrice']),
                    'vol_24h': float(t['quoteVolume']),
                    'vol_original': float(t['volume']),  # 原始币量
                })
    except:
        pass
    return result

def detect_signals(data):
    """检测异动信号"""
    signals = []
    now = datetime.now()
    
    for d in data:
        name = d['name']
        price = d['price']
        chg = d['chg_pct']
        vol_usdt = d['vol_24h']
        
        # 信号1：涨跌幅异常（单日>15%）
        if abs(chg) > 15:
            direction = "暴涨" if chg > 0 else "暴跌"
            signals.append({
                'name': name, 'price': round(price, 8), 'chg': round(chg, 2),
                'vol': f"{vol_usdt/1e6:.1f}M", 'type': f'{direction}>15%',
                'severity': '🔥' if abs(chg) > 25 else '⚠️',
                'time': now.strftime('%H:%M:%S'),
            })
        
        # 信号2：价格相比缓存变化>5%（短时监控）
        if name in price_cache:
            prev = price_cache[name]
            if prev > 0 and abs(price - prev) / prev > 0.05:
                short_chg = (price - prev) / prev * 100
                direction = "急涨" if short_chg > 0 else "急跌"
                signals.append({
                    'name': name, 'price': round(price, 8), 'chg': round(short_chg, 2),
                    'vol': f"{vol_usdt/1e6:.1f}M", 'type': f'{direction}',
                    'severity': '⚡',
                    'time': now.strftime('%H:%M:%S'),
                })
        
        # 信号3：成交量异常（24h成交额>5亿USDT，排除DOGE/SHIB等常态高量币）
        if vol_usdt > 500_000_000 and name not in ('DOGE', 'SHIB'):
            signals.append({
                'name': name, 'price': round(price, 8), 'chg': round(chg, 2),
                'vol': f"{vol_usdt/1e6:.1f}M", 'type': '高活跃度',
                'severity': '📊',
                'time': now.strftime('%H:%M:%S'),
            })
        
        # 更新缓存
        price_cache[name] = price
    
    return signals

def main():
    args = sys.argv[1:]
    interval = 60  # 每60秒扫一次
    
    print("=" * 60)
    print(" MEME币热度监控")
    print("=" * 60)
    print(f" 监控: {', '.join(MEME_COINS)}")
    print(f" 轮询: 每{interval}秒")
    print(f" 数据源: Binance API")
    print()
    
    # 写CSV表头
    if not os.path.exists(LOG_CSV):
        with open(LOG_CSV, "w", newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(["time","name","price","chg_24h_pct","vol_24h_usdt","high","low","signal"])
    
    start = time.time()
    print(f" 启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        while True:
            t0 = time.time()
            elapsed = time.time() - start
            
            data = fetch_all()
            sigs = detect_signals(data)
            
            for s in sigs:
                alerts.append(s)
                msg = (f"{s['severity']}【MEME异动】{s['name']}\n"
                       f"价格: ${s['price']}\n"
                       f"变化: {s['chg']:+.2f}%\n"
                       f"成交: {s['vol']}\n"
                       f"类型: {s['type']}")
                print(f"\n{msg}")
                wechat(msg)
            
            # 记录CSV
            now_str = datetime.now().strftime('%H:%M:%S')
            for d in data:
                has_signal = 'Y' if any(s['name'] == d['name'] for s in sigs) else ''
                with open(LOG_CSV, "a", newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    w.writerow([now_str, d['name'], round(d['price'],8),
                                round(d['chg_pct'],2), round(d['vol_24h'],0),
                                round(d['high'],8), round(d['low'],8), has_signal])
            
            now_s = datetime.now().strftime('%H:%M:%S')
            status = ', '.join([f"{d['name']}:{d['chg_pct']:+.1f}%" for d in data[:5]])
            print(f"\r[{elapsed:6.0f}s] {now_s} | {status} | 总信号{len(alerts)}", end="")
            
            time.sleep(max(0, interval - (time.time() - t0)))
            
    except KeyboardInterrupt:
        print(f"\n\n 用户中断")

if __name__ == "__main__":
    main()
