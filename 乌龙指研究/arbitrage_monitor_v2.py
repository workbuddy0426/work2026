#!/usr/bin/env python3
"""
跨交易所价差套利监控 V2 - 多币种
同时监控 Binance vs OKX 的 BTC/ETH/WIF 价差
"""
import json, os, sys, time, subprocess, platform, csv
import urllib.request
from datetime import datetime

SKILL_DIR = os.environ.get("SKILL_DIR", r"C:\Users\user\.workbuddy\skills\alarm-memo-assistant-pro")
SEND_WECHAT = os.path.join(SKILL_DIR, "scripts", "send_wechat.py")
PYTHON_EXE = r"C:\Users\user\.workbuddy\binaries\python\versions\3.13.12\python.exe"
PROXY = "http://127.0.0.1:6864"

def wechat(msg):
    try:
        env = os.environ.copy()
        env["SKILL_DIR"] = SKILL_DIR
        py = "python" if platform.system() != "Windows" else PYTHON_EXE
        subprocess.run([py, SEND_WECHAT, "send", msg],
            capture_output=True, text=True, encoding="utf-8", timeout=15, env=env)
    except:
        pass

# ─── 配置：监控的币种 ───
SYMBOLS = [
    {"name": "BTC", "binance": "BTCUSDT", "okx": "BTC-USDT", "threshold": 0.0045, "active": True},
    {"name": "ETH", "binance": "ETHUSDT", "okx": "ETH-USDT", "threshold": 0.0045, "active": True},
]

LOG_DIR = "results"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_CSV = os.path.join(LOG_DIR, "arbitrage_log_v2.csv")
TRADE_FILE = os.path.join(LOG_DIR, "arbitrage_trades_v2.json")
TRADE_SIZE = 2500  # 每笔交易投入USDT

# 写入CSV表头
if not os.path.exists(LOG_CSV):
    with open(LOG_CSV, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["time","symbol","binance","okx","spread_bps","elapsed"])

trades_log = []
position = None  # 当前持仓 {symbol, direction, entry_spread, entry_time}

def fetch_price(binance_pair, okx_pair, retries=3):
    """获取双所价格"""
    handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
    opener = urllib.request.build_opener(handler)
    
    for _ in range(retries):
        try:
            req = urllib.request.Request(
                f'https://api.binance.com/api/v3/ticker/price?symbol={binance_pair}',
                headers={'User-Agent': 'Mozilla/5.0'})
            pb = float(json.loads(opener.open(req, timeout=8).read().decode())['price'])
            
            req = urllib.request.Request(
                f'https://www.okx.com/api/v5/market/ticker?instId={okx_pair}',
                headers={'User-Agent': 'Mozilla/5.0'})
            po = float(json.loads(opener.open(req, timeout=8).read().decode())['data'][0]['last'])
            
            return pb, po
        except:
            time.sleep(2)
    return None, None

def main():
    global position, trades_log
    args = sys.argv[1:]
    interval = 15
    
    print("=" * 70)
    print(" 多币种价差套利监控 V2")
    print("=" * 70)
    print(f" 代理: {PROXY}")
    print(f" 轮询: 每{interval}秒")
    print(f" 监控:")
    for s in SYMBOLS:
        print(f"    {s['name']} {'✅' if s['active'] else '❌'} 阈值{s['threshold']*100:.2f}%")
    
    # 预热
    print("\n 测试连接...")
    for s in SYMBOLS:
        if not s['active']: continue
        pb, po = fetch_price(s['binance'], s['okx'])
        if pb:
            spread = (pb - po) / po * 10000
            print(f"  {s['name']}: Binance ${pb:.2f}  OKX ${po:.2f}  价差:{spread:+.1f}bps")
    print()
    
    start_time = time.time()
    print(f" 监控启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    try:
        while True:
            t0 = time.time()
            elapsed = time.time() - start_time
            now_str = datetime.now().strftime('%H:%M:%S')
            status_parts = []
            
            for s in SYMBOLS:
                if not s['active']: continue
                
                pb, po = fetch_price(s['binance'], s['okx'])
                if not pb:
                    status_parts.append(f"{s['name']}:连接失败")
                    continue
                
                spread_bps = (pb - po) / po * 10000
                is_signal = abs(spread_bps) > s['threshold'] * 10000
                
                # 记录CSV
                with open(LOG_CSV, "a", newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    w.writerow([now_str, s['name'], f"{pb:.6f}", f"{po:.6f}", f"{spread_bps:.1f}", f"{elapsed:.0f}"])
                
                # 检查是否已有持仓
                if is_signal and not position:
                    direction = "做多币安做空OKX" if pb > po else "做空币安做多OKX"
                    position = {"symbol": s['name'], "direction": direction, "entry_spread": spread_bps, "entry_time": now_str}
                    msg = (f"【价差信号】{s['name']}\n"
                           f"币安: ${pb:.2f}\nOKX: ${po:.2f}\n"
                           f"价差: {spread_bps:+.1f}bps\n方向: {direction}")
                    print(f"\n>>> {msg}")
                    wechat(msg)
                
                # 持仓检查：价差回到2bps以内平仓
                if position and position['symbol'] == s['name']:
                    if abs(spread_bps) < 2:
                        spread_diff = abs(position['entry_spread'] - spread_bps)
                        pnl = round(TRADE_SIZE * spread_diff / 10000, 2)
                        reason = "价差收敛"
                        trade = {
                            "symbol": s['name'], "side": position['direction'],
                            "entry_time": position['entry_time'], "exit_time": now_str,
                            "entry_spread": round(position['entry_spread'], 1),
                            "exit_spread": round(spread_bps, 1),
                            "pnl": round(pnl, 2),
                            "reason": reason,
                        }
                        trades_log.append(trade)
                        with open(TRADE_FILE, "w", encoding='utf-8') as f:
                            json.dump(trades_log, f, ensure_ascii=False, indent=2)
                        msg = (f"【平仓】{s['name']}\n"
                               f"入场价差:{position['entry_spread']:+.1f}bps\n"
                               f"出场价差:{spread_bps:+.1f}bps\n"
                               f"盈亏: ${pnl:.2f}\n原因: {reason}")
                        print(f"\n>>> {msg}")
                        wechat(msg)
                        position = None
                
                # 状态显示
                flag = " **持仓**" if (position and position['symbol'] == s['name']) else (" **信号**" if is_signal else "")
                status_parts.append(f"{s['name']}:${pb:.0f} {spread_bps:+.1f}bps{flag}")
            
            print(f"\r[{elapsed:6.0f}s] {now_str} | {' | '.join(status_parts)}", end="")
            time.sleep(max(0, interval - (time.time() - t0)))
            
    except KeyboardInterrupt:
        print(f"\n\n 用户中断")

if __name__ == "__main__":
    main()
