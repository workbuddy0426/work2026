#!/usr/bin/env python3
"""
可转债乌龙指实时监控
检测可转债瞬间大幅偏离（乌龙指），自动微信通知
数据源：新浪财经API（无需VPN）

用法:
  python cb_fat_finger_monitor.py                    # 每120秒扫一次
  python cb_fat_finger_monitor.py --interval 60      # 每60秒
"""
import json, os, sys, time, subprocess, platform, csv
import urllib.request
from datetime import datetime

SKILL_DIR = os.environ.get("SKILL_DIR", r"C:\Users\user\.workbuddy\skills\alarm-memo-assistant-pro")
SEND_WECHAT = os.path.join(SKILL_DIR, "scripts", "send_wechat.py")
PYTHON_EXE = r"C:\Users\user\.workbuddy\binaries\python\versions\3.13.12\python.exe"
CONFIG = {"push_enabled": True}

def wechat(msg):
    try:
        env = os.environ.copy()
        env["SKILL_DIR"] = SKILL_DIR
        py = "python" if platform.system() != "Windows" else PYTHON_EXE
        subprocess.run([py, SEND_WECHAT, "send", msg],
            capture_output=True, text=True, encoding="utf-8", timeout=15, env=env)
    except:
        pass

CB_LIST = "data/cb_list_20260428.csv"
BATCH = 50
cache = {}
alerts = []

def load_codes():
    codes = []
    with open(CB_LIST, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            codes.append((row['代码'].strip(), row['名称'].strip()))
    return codes

def fetch_all(codes):
    """新浪财经批量查询"""
    result = {}
    for i in range(0, len(codes), BATCH):
        batch = codes[i:i+BATCH]
        # 根据代码前两位判断交易所 sz=深市 sh=沪市
        prefixes = []
        for c in batch:
            code = c[0]
            if code.startswith('11'):
                prefixes.append(f'sh{code}')
            else:
                prefixes.append(f'sz{code}')
        query = ','.join(prefixes)
        req = urllib.request.Request(
            f'https://hq.sinajs.cn/list={query}',
            headers={'Referer': 'https://finance.sina.com.cn'}
        )
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            for line in resp.read().decode('gbk').strip().split('\n'):
                if 'hq_str' not in line:
                    continue
                parts = line.split(',')
                # parts[0]: var hq_str_sz123456="名称
                name = parts[0].split('=')[-1].strip('"').strip('"')
                price = float(parts[3]) if parts[3] else 0
                if price > 0:
                    result[name] = {
                        'price': price,
                        'open': float(parts[1]) if parts[1] else 0,
                        'high': float(parts[4]) if parts[4] else 0,
                        'low': float(parts[5]) if parts[5] else 0,
                        'volume': int(parts[8]) if parts[8] else 0,
                    }
        except:
            continue
    return result

def detect(codes, data):
    signals = []
    now = datetime.now().strftime('%H:%M:%S')
    for name, d in data.items():
        price = d['price']
        if name in cache:
            prev = cache[name]
            if prev > 0:
                chg = abs(price - prev) / prev
                if chg > 0.08 and price > 50:
                    direction = "上涨" if price > prev else "下跌"
                    signals.append({
                        'name': name, 'prev': round(prev, 2),
                        'price': round(price, 2),
                        'chg': round((price - prev) / prev * 100, 2),
                        'direction': direction, 'time': now,
                    })
        cache[name] = price
    return signals

# ── 数据日志（积累真实历史数据用于回测）──
DATA_LOG = "results/cb_price_log.csv"

def log_prices(data):
    """记录每次扫描的全市场价格（压缩格式：timestamp|count|json_data）"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 只记录价格，减少体积
    prices = {name: round(d['price'], 2) for name, d in data.items()}
    import json
    line = f"{now}|{len(prices)}|{json.dumps(prices, ensure_ascii=False)}\n"
    try:
        with open(DATA_LOG, "a", encoding="utf-8") as f:
            f.write(line)
    except:
        pass

# ── 交易时段判断 ──
MARKET_OPEN = {}

# 中国法定节假日（A股休市）
HOLIDAYS = {
    (2026, 5, 1), (2026, 5, 2), (2026, 5, 3), (2026, 5, 4), (2026, 5, 5),  # 五一
    (2026, 6, 12), (2026, 6, 13), (2026, 6, 14),  # 端午
    (2026, 10, 1), (2026, 10, 2), (2026, 10, 3), (2026, 10, 4), (2026, 10, 5), (2026, 10, 6), (2026, 10, 7),  # 国庆
}

def is_holiday(d):
    return (d.year, d.month, d.day) in HOLIDAYS

def market_is_open():
    """判断A股可转债是否在交易时段"""
    now = datetime.now()
    # 节假日休市
    if is_holiday(now):
        return False
    # 周末休市
    if now.weekday() >= 5:
        return False
    h, m = now.hour, now.minute
    # 上午 9:30-11:30, 下午 13:00-15:00
    if (h == 9 and m >= 30) or (h == 10) or (h == 11 and m <= 30):
        return True
    if (h == 13) or (h == 14) or (h == 15 and m == 0):
        return True
    return False

def main():
    args = sys.argv[1:]
    interval = 120
    for i, a in enumerate(args):
        if a == "--interval" and i+1 < len(args):
            try: interval = int(args[i+1])
            except: pass

    print("=" * 70)
    print(" 可转债乌龙指实时监控（新浪数据源）")
    print("=" * 70)
    print(f" 轮询: 每{interval}秒 | 触发: 间隔波动>8% | 数据源: 新浪财经")
    print(f" 数据日志: results/cb_price_log.csv（自动积累历史数据）")
    codes = load_codes()
    print(f" 监控: {len(codes)}只可转债")

    print("\n 预热缓存...")
    data = fetch_all(codes)
    for name, d in data.items():
        cache[name] = d['price']
    print(f" 已缓存 {len(cache)} 只")

    print(f"\n{'='*70}")
    print(f" 监控启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")

    start = time.time()
    try:
        while True:
            t0 = time.time()

            # 交易时段检查
            if not market_is_open():
                now_s = datetime.now().strftime('%H:%M:%S')
                elapsed = time.time() - start
                # 每30秒打印一次休市状态
                if int(elapsed) % 30 == 0:
                    now = datetime.now()
                    if is_holiday(now):
                        reason = "节假日休市"
                    elif now.weekday() >= 5:
                        reason = "周末休市"
                    else:
                        reason = "非交易时段"
                    print(f"[{elapsed:6.0f}s] {now_s} {reason}（交易日9:30-15:00运行）", flush=True)
                time.sleep(30)
                continue

            data = fetch_all(codes)
            signals = detect(codes, data)
            log_prices(data)  # 记录数据到日志
            elapsed = time.time() - start

            for s in signals:
                alerts.append(s)
                msg = (f"【可转债乌龙指】\n{s['name']}\n"
                       f"${s['prev']}→${s['price']}\n"
                       f"变化: {s['chg']:+.2f}% ({s['direction']})\n"
                       f"时间: {s['time']}")
                print(f"\n>>> {msg}")
                if CONFIG["push_enabled"]:
                    wechat(msg)

            now_s = datetime.now().strftime('%H:%M:%S')
            print(f"[{elapsed:6.0f}s] {now_s} {len(data)}只 | 信号{len(alerts)}", flush=True)
            time.sleep(max(0, interval - (time.time() - t0)))

    except KeyboardInterrupt:
        print(f"\n\n 用户中断")
    print(f" 运行 {time.time()-start:.0f}s, 检测 {len(alerts)} 个信号")


if __name__ == "__main__":
    main()
