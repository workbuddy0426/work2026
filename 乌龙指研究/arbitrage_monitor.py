#!/usr/bin/env python3
"""
跨交易所价差套利实时监控
监控 Binance vs OKX 的 BTC/USDT 价差
检测到套利机会时自动微信通知 + 模拟交易

用法:
  python arbitrage_monitor.py                    # 默认模式(30秒轮询)
  python arbitrage_monitor.py --interval 10      # 10秒轮询
  python arbitrage_monitor.py --threshold 0.003  # 0.3%价差触发
  python arbitrage_monitor.py --paper            # 启用模拟交易
"""
import json, os, sys, time, subprocess, platform
import urllib.request
from datetime import datetime
from collections import deque

# ============================================================
# 微信推送
# ============================================================
SKILL_DIR = os.environ.get("SKILL_DIR", r"C:\Users\user\.workbuddy\skills\alarm-memo-assistant-pro")
SEND_WECHAT = os.path.join(SKILL_DIR, "scripts", "send_wechat.py")
PYTHON_EXE = r"C:\Users\user\.workbuddy\binaries\python\versions\3.13.12\python.exe"

def wechat_send(msg):
    try:
        env = os.environ.copy()
        env["SKILL_DIR"] = SKILL_DIR
        py = "python" if platform.system() != "Windows" else PYTHON_EXE
        subprocess.run([py, SEND_WECHAT, "send", msg],
            capture_output=True, text=True, encoding="utf-8", timeout=15, env=env)
    except:
        pass

# ============================================================
# 配置
# ============================================================
CONFIG = {
    "proxy": "http://127.0.0.1:6864",      # VPN代理
    "poll_interval": 30,                     # 轮询秒数
    "spread_threshold": 0.003,              # 0.3% 价差触发
    "exit_ratio": 0.3,                      # 收敛到峰值30%退出
    "fee": 0.001,                           # 0.1%/边
    "paper_enabled": False,                 # --paper开启
    "capital": 10000.0,
    "trade_pct": 0.5,                       # 50%资金开一组
}

LOG_FILE = "results/arbitrage_log.csv"
TRADE_FILE = "results/arbitrage_trades.json"

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
OKX_URL = "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"


def fetch_price(url, proxy=None, retries=3):
    """获取交易所价格，返回(price, elapsed)，失败自动重试"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(retries):
        try:
            if proxy:
                handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
                opener = urllib.request.build_opener(handler)
            else:
                opener = urllib.request.build_opener()
            start = time.time()
            resp = opener.open(req, timeout=10)
            data = json.loads(resp.read().decode())
            elapsed = time.time() - start
            return float(data["price"] if "price" in data else data["data"][0]["last"]), elapsed
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(3)
                continue
            raise
    raise RuntimeError(f"Failed after {retries} retries")


class ArbitrageTrader:
    """套利模拟交易"""
    def __init__(self):
        self.capital = CONFIG["capital"]
        self.trade_size = self.capital * CONFIG["trade_pct"]
        self.position = None
        self.trades = []
        self._load()

    def _load(self):
        if os.path.exists(TRADE_FILE):
            try:
                with open(TRADE_FILE, "r") as f:
                    self.trades = json.load(f)
            except:
                self.trades = []

    def _save(self):
        os.makedirs("results", exist_ok=True)
        with open(TRADE_FILE, "w") as f:
            json.dump(self.trades, f, indent=2)

    def open_position(self, spread_bps, binance_price, okx_price):
        if self.position:
            return None
        locked = min(self.trade_size, self.capital * 0.9)
        qty = locked / 2 / min(binance_price, okx_price)

        if binance_price > okx_price:
            # Binance贵 → 空Binance 多OKX
            pos = {
                "side": "空币安 多OKX",
                "entry_time": datetime.now().isoformat(),
                "entry_spread_bps": round(spread_bps, 1),
                "binance_entry": binance_price,
                "okx_entry": okx_price,
                "qty": qty,
                "locked": locked,
                "peak_spread": abs(spread_bps),
            }
        else:
            pos = {
                "side": "多币安 空OKX",
                "entry_time": datetime.now().isoformat(),
                "entry_spread_bps": round(spread_bps, 1),
                "binance_entry": binance_price,
                "okx_entry": okx_price,
                "qty": qty,
                "locked": locked,
                "peak_spread": abs(spread_bps),
            }
        self.position = pos
        self.capital -= locked
        return pos

    def update_position(self, binance_price, okx_price):
        if not self.position:
            return None
        p = self.position
        spread = (binance_price - okx_price) / okx_price * 10000
        abs_spread = abs(spread)
        if abs_spread > p["peak_spread"]:
            p["peak_spread"] = abs_spread

        # 退出条件
        exit_threshold = p["peak_spread"] * CONFIG["exit_ratio"]
        timeout = (datetime.now() - datetime.fromisoformat(p["entry_time"])).total_seconds() > 300
        converged = abs_spread < exit_threshold

        if converged or timeout:
            qty = p["qty"]
            entry_b, entry_o = p["binance_entry"], p["okx_entry"]

            if "空币安" in p["side"]:
                pnl_b = qty * (entry_b - binance_price)
                pnl_o = qty * (okx_price - entry_o)
            else:
                pnl_b = qty * (binance_price - entry_b)
                pnl_o = qty * (entry_o - okx_price)

            gross = pnl_b + pnl_o
            fee = 2 * CONFIG["fee"] * qty * (entry_b + binance_price) * 0.5 + \
                  2 * CONFIG["fee"] * qty * (entry_o + okx_price) * 0.5
            net = gross - fee

            self.capital += p["locked"] + net
            reason = "CONVERGE" if converged else "TIMEOUT"
            trade = {
                "side": p["side"],
                "entry_time": p["entry_time"],
                "exit_time": datetime.now().isoformat(),
                "entry_spread": p["entry_spread_bps"],
                "exit_spread": round(spread, 1),
                "hold_seconds": round((datetime.now() - datetime.fromisoformat(p["entry_time"])).total_seconds()),
                "pnl": round(net, 2),
                "pnl_pct": round(net / p["locked"] * 100, 2),
                "reason": reason,
            }
            self.trades.append(trade)
            self._save()
            self.position = None
            return trade
        return None

    def get_summary(self):
        if not self.trades:
            return "暂无交易"
        closed = [t for t in self.trades if "pnl" in t]
        wins = [t for t in closed if t["pnl"] > 0]
        losses = [t for t in closed if t["pnl"] <= 0]
        total_pnl = sum(t["pnl"] for t in closed)
        return {
            "total": len(closed),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": round(len(wins)/len(closed)*100, 1) if closed else 0,
            "total_pnl": round(total_pnl, 2),
            "capital": round(self.capital, 2),
            "profit_pct": round(total_pnl / CONFIG["capital"] * 100, 2),
        }


def log_spread(ts, binance, okx, spread, elapsed, signal):
    """记录价差日志"""
    os.makedirs("results", exist_ok=True)
    header = not os.path.exists(LOG_FILE)
    import csv
    with open(LOG_FILE, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if header:
            w.writerow(["time", "binance", "okx", "spread_bps", "elapsed_s", "signal"])
        w.writerow([ts, round(binance,2), round(okx,2), round(spread,1), round(elapsed,2), signal])


def main():
    args = sys.argv[1:]
    interval = CONFIG["poll_interval"]
    threshold = CONFIG["spread_threshold"]
    paper = "--paper" in args or "--trade" in args
    CONFIG["paper_enabled"] = paper
    for i, a in enumerate(args):
        if a == "--interval" and i+1 < len(args):
            try: interval = int(args[i+1])
            except: pass
        if a == "--threshold" and i+1 < len(args):
            try: threshold = float(args[i+1])
            except: pass

    trader = ArbitrageTrader() if paper else None
    proxy = CONFIG["proxy"]

    print("=" * 70)
    print(" 跨交易所价差套利监控")
    print("=" * 70)
    print(f" 币安: {BINANCE_URL}")
    print(f" OKX:  {OKX_URL}")
    print(f" 代理: {proxy}")
    print(f" 轮询: 每{interval}秒")
    print(f" 触发: 价差>{threshold*100:.2f}%")
    print(f" 模拟: {'启用' if paper else '关闭'}")
    if trader:
        print(f" 资金: ${trader.capital:,.0f}")
    print()

    # 测试连接
    print("测试连接...")
    try:
        pb, _ = fetch_price(BINANCE_URL, proxy)
        po, _ = fetch_price(OKX_URL, proxy)
        print(f"  Binance: ${pb:,.2f}")
        print(f"  OKX:     ${po:,.2f}")
        print(f"  价差:    {(pb-po)/po*10000:+.1f} bps")
    except Exception as e:
        print(f"  连接失败: {e}")
        return

    print(f"\n{'='*70}")
    print(f"监控启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")

    history = deque(maxlen=60)
    start_time = time.time()
    signals = 0

    try:
        while True:
            loop_start = time.time()

            # 获取价格（失败时跳过本轮）
            try:
                pb, eb = fetch_price(BINANCE_URL, proxy)
                po, eo = fetch_price(OKX_URL, proxy)
            except Exception as e:
                print(f"\r[{time.time()-start_time:6.0f}s] 连接异常: {str(e)[:40]}, 等待重试...", end="")
                time.sleep(interval)
                continue
            spread_bps = (pb - po) / po * 10000
            timestamp = datetime.now().strftime("%H:%M:%S")
            history.append(spread_bps)

            # 记录
            is_signal = abs(spread_bps) > threshold * 10000
            log_spread(timestamp, pb, po, spread_bps, max(eb, eo), "SIGNAL" if is_signal else "")

            # 状态显示
            pos_indicator = " | 持仓中" if (trader and trader.position) else ""
            elapsed = time.time() - start_time
            print(f"\r[{elapsed:6.0f}s] {timestamp} "
                  f"B:${pb:,.0f} O:${po:,.0f} "
                  f"价差:{spread_bps:+.1f}bps"
                  f"{' **信号**' if is_signal else ''}"
                  f"{pos_indicator}   ", end="")

            # 信号检测 + 模拟交易
            if is_signal:
                signals += 1
                print(f"\n>>> 价差信号! {spread_bps:+.1f}bps (阈值{threshold*10000:.0f}bps)")
                wechat_send(
                    f"【价差套利信号】\n"
                    f"时间: {datetime.now().strftime('%H:%M:%S')}\n"
                    f"币安: ${pb:,.2f}\n"
                    f"OKX:  ${po:,.2f}\n"
                    f"价差: {spread_bps:+.1f}bps\n"
                    f"方向: {'空币安多OKX' if pb>po else '多币安空OKX'}"
                )

                if trader:
                    entry = trader.open_position(spread_bps, pb, po)
                    if entry:
                        print(f"  开仓: {entry['side']} @ ${entry['binance_entry']:,.0f}/${entry['okx_entry']:,.0f}")

            # 持仓管理
            if trader and trader.position:
                exit_info = trader.update_position(pb, po)
                if exit_info:
                    print(f"\n  平仓 [{exit_info['reason']}]: "
                          f"${exit_info['pnl']:+,.2f} ({exit_info['pnl_pct']:+.2f}%)")
                    wechat_send(
                        f"【价差平仓】\n"
                        f"盈亏: ${exit_info['pnl']:+,.2f} ({exit_info['pnl_pct']:+.2f}%)\n"
                        f"原因: {exit_info['reason']}\n"
                        f"资金: ${trader.capital:,.2f}"
                    )

            # 等待
            sleep_time = interval - (time.time() - loop_start)
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print(f"\n\n用户中断")

    # 报告
    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f" 监控报告")
    print(f"{'='*70}")
    print(f" 运行时间: {elapsed:.0f}秒")
    print(f" 价差信号: {signals}次")
    if history:
        print(f" 价差范围: {min(history):+.1f} ~ {max(history):+.1f} bps")
        print(f" 价差均值: {sum(history)/len(history):+.1f} bps")
    if trader:
        s = trader.get_summary()
        if isinstance(s, dict):
            print(f"\n 模拟交易:")
            print(f"   总交易: {s['total']}笔 | 胜率{s['win_rate']}%")
            print(f"   总盈亏: ${s['total_pnl']:+,.2f} ({s['profit_pct']:+.2f}%)")
            print(f"   资金: ${s['capital']:,.2f}")
    print(f" 日志: {LOG_FILE}")
    print(f" 交易: {TRADE_FILE}")


if __name__ == "__main__":
    main()
