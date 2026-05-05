#!/usr/bin/env python3
"""
双策略监控：币安OKX价差套利 + 可转债乌龙指
自动切换代理状态，两种策略互不干扰

用法:
  python dual_monitor.py                      # 双策略全开
  python dual_monitor.py --crypto-only        # 仅币安套利
  python dual_monitor.py --cb-only            # 仅可转债
"""
import json, os, sys, time, subprocess, platform, csv
import urllib.request
from datetime import datetime
from collections import deque

# ── 微信推送 ──
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

# ── 代理/VPN控制 ──
WMSXWDA_DIR = r"C:\Program Files (x86)\wmsxwda"

def vpn_stop():
    """停VPN进程（关代理）"""
    subprocess.run(["taskkill", "/f", "/im", "AtlasCore_amd64.exe"], capture_output=True, timeout=5)
    subprocess.run(["taskkill", "/f", "/im", "wmsxwda.exe"], capture_output=True, timeout=5)
    time.sleep(1)

def vpn_start():
    """启动VPN"""
    exe = os.path.join(WMSXWDA_DIR, "wmsxwda.exe")
    if os.path.exists(exe):
        subprocess.Popen([exe], shell=True)
    time.sleep(3)

def set_proxy(on=True):
    val = "1" if on else "0"
    try:
        subprocess.run([
            "powershell", "-Command",
            f"Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' -Name ProxyEnable -Value {val}"
        ], capture_output=True, timeout=5)
        time.sleep(0.5)
    except:
        pass

# ── 币安/OKX 价差套利 ──
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
OKX_URL = "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"
SPREAD_THRESHOLD = 0.0045  # 0.45%
FEE_BPS = 40  # 0.4% total

crypto_trades = []
last_spread_log = 0

def fetch_crypto():
    """通过VPN获取币安OKX价格"""
    handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
    opener = urllib.request.build_opener(handler)

    req_b = urllib.request.Request(BINANCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    req_o = urllib.request.Request(OKX_URL, headers={"User-Agent": "Mozilla/5.0"})

    for attempt in range(3):
        try:
            rb = json.loads(opener.open(req_b, timeout=10).read().decode())
            ro = json.loads(opener.open(req_o, timeout=10).read().decode())
            pb = float(rb["price"])
            po = float(ro["data"][0]["last"])
            spread_bps = (pb - po) / po * 10000
            return pb, po, round(spread_bps, 1)
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
                continue
            return None, None, None

# ── 可转债乌龙指 ──
cb_price_cache = {}
cb_alerts = []

def fetch_cb():
    """临时停VPN获取可转债数据"""
    vpn_stop()
    try:
        url = 'https://push2.eastmoney.com/api/qt/clist/get'
        params = ('pn=1&pz=500&po=1&np=1'
                  '&fields=f12,f14,f2,f3,f6'
                  '&fid=f2&fs=b:MK0354')
        full_url = f"{url}?{params}"
        req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        items = data['data']['diff']
        result = []
        for item in items:
            code = str(item.get('f12', ''))
            name = item.get('f14', '')
            price = item.get('f2', 0)
            chg = item.get('f3', 0)
            vol = item.get('f6', 0)
            if price and price > 10000:
                price = price / 1000
            result.append({
                'code': code, 'name': name,
                'price': round(price, 2) if price else 0,
                'chg_pct': round(chg, 2) if chg else 0,
                'volume': vol or 0,
            })
        return result
    except Exception as e:
        return []
    finally:
        vpn_start()


def detect_cb_fatfinger(bonds):
    """检测可转债乌龙指"""
    signals = []
    now = datetime.now()
    for b in bonds:
        code = b['code']
        price = b['price']
        name = b['name']
        if price <= 0:
            continue
        if code in cb_price_cache:
            prev = cb_price_cache[code]
            if prev['price'] > 0:
                change = abs(price - prev['price']) / prev['price']
                if change > 0.08 and price > 50:
                    direction = "上涨" if price > prev['price'] else "下跌"
                    signals.append({
                        'code': code, 'name': name,
                        'prev': prev['price'], 'price': price,
                        'change': round((price - prev['price']) / prev['price'] * 100, 2),
                        'direction': direction,
                    })
        cb_price_cache[code] = {'name': name, 'price': price}
    return signals


def print_header():
    print("=" * 70)
    print(" 双策略监控 | 币安OKX价差套利 + 可转债乌龙指")
    print("=" * 70)
    print(f" 价差阈值: {SPREAD_THRESHOLD*100:.2f}% | 乌龙指阈值: 8%")
    print(f" 代理: crypto走VPN | 可转债临时断代理")
    print()


# ═══════════════════════════════════════════
#  主循环
# ═══════════════════════════════════════════
def main():
    args = sys.argv[1:]
    crypto_only = "--crypto-only" in args
    cb_only = "--cb-only" in args

    print_header()
    start_time = time.time()
    crypto_cycle = 0
    cb_cycle = 0
    total_signals = {"crypto": 0, "cb": 0}

    # 可转债预热
    if not crypto_only:
        print(" 可转债预热...")
        bonds = fetch_cb()
        if bonds:
            for b in bonds:
                cb_price_cache[b['code']] = {'name': b['name'], 'price': b['price']}
            print(f" 已缓存 {len(bonds)} 只可转债")
        print()

    print(f" 监控启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")

    try:
        while True:
            now = datetime.now().strftime('%H:%M:%S')
            elapsed = time.time() - start_time
            status_parts = []

            # ── Crypto价差（每30s） ──
            if not cb_only:
                crypto_cycle += 1
                pb, po, spread = fetch_crypto()
                if pb is not None:
                    is_signal = abs(spread) > SPREAD_THRESHOLD * 10000
                    if is_signal:
                        total_signals["crypto"] += 1
                        direction = "空币安多OKX" if pb > po else "多币安空OKX"
                        msg = (f"【价差套利信号】\n"
                               f"币安: ${pb:,.2f}\nOKX: ${po:,.2f}\n"
                               f"价差: {spread:+.1f}bps\n方向: {direction}")
                        print(f"\n>>> {msg}")
                        wechat(msg)
                    status_parts.append(f"C:${pb:,.0f}/${po:,.0f} {spread:+.1f}bps{'!!' if is_signal else ''}")
                else:
                    status_parts.append("C:连接失败")

            # ── 可转债乌龙指（每60s） ──
            if not crypto_only and crypto_cycle % 2 == 0:
                cb_cycle += 1
                bonds = fetch_cb()
                signals = detect_cb_fatfinger(bonds)
                for s in signals:
                    total_signals["cb"] += 1
                    msg = (f"【可转债乌龙指】\n"
                           f"{s['name']}({s['code']})\n"
                           f"${s['prev']}→${s['price']}\n"
                           f"变化: {s['change']:+.2f}%")
                    print(f"\n>>> {msg}")
                    wechat(msg)
                if bonds:
                    status_parts.append(f"CB:{len(bonds)}只 {len(signals)}信号")
                else:
                    status_parts.append("CB:获取失败")

            # 状态行
            s = " | ".join(status_parts) if status_parts else "等待..."
            print(f"\r[{elapsed:6.0f}s] {now} {s} ", end="")
            time.sleep(30)

    except KeyboardInterrupt:
        print(f"\n\n 用户中断")

    print(f"\n 运行 {time.time()-start_time:.0f}s")
    print(f" 信号统计: 价差{total_signals['crypto']} 乌龙指{total_signals['cb']}")


if __name__ == "__main__":
    main()
