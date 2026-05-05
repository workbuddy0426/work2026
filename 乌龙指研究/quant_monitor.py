"""
🎓 第12课 毕业设计：量化监控系统
═══════════════════════════════════
把12课学的东西合体：
  第3课    - 多源行情采集
  第4-5课  - 套利策略 + 均值回归
  第6课    - 自动循环扫描
  第7-9课  - 选股指标
  第10课   - 回测思路（记录日志）
  第11课   - 风控检查
═══════════════════════════════════
"""

import urllib.request
import json
import time
import csv
import os
from datetime import datetime

# ===== 配置区（你可以自己改） =====
CONFIG = {
    "check_interval": 30,          # 每30秒扫描一次
    "spread_alert_bps": 10,        # 价差报警阈值
    "stop_loss_pct": 0.08,         # 止损线 8%
    "max_position_pct": 0.20,      # 单笔最大仓位 20%
    "max_drawdown_pct": 0.15,      # 最大回撤 15%
    "capital": 1000,               # 模拟本金 $1000
}

# ===== 日志文件 =====
log_dir = "C:/Users/user/WorkBuddy/Claw/乌龙指研究/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = f"{log_dir}/trade_log.csv"

# 如果日志文件不存在，写表头
if not os.path.exists(log_file):
    with open(log_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["时间", "类型", "标的", "价格", "价差(bps)", "仓位", "风控", "备注"])

# ===== 工具函数 =====
def fetch_price(name, url, parser):
    """第3课：抓取价格"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        return parser(data)
    except:
        return None

def log_trade(trade_type, symbol, price, spread, position, risk_status, note):
    """第10课：记录交易日志"""
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            trade_type, symbol, price, spread,
            f"{position:.1%}", risk_status, note
        ])

# ===== 风控模块（第11课） =====
class RiskManager:
    def __init__(self, config):
        self.capital = config["capital"]
        self.position = 0          # 当前持仓金额
        self.entry_price = 0       # 买入价
        self.peak_capital = config["capital"]
        self.max_position_pct = config["max_position_pct"]
        self.stop_loss_pct = config["stop_loss_pct"]
        self.max_drawdown_pct = config["max_drawdown_pct"]
        self.trades = 0

    def check_position(self, amount):
        """仓位检查"""
        if amount > self.capital * self.max_position_pct:
            return False, f"仓位超限：{amount/self.capital:.1%} > {self.max_position_pct:.0%}"
        return True, "仓位通过"

    def check_stop_loss(self, current_price):
        """止损检查"""
        if self.position > 0 and self.entry_price > 0:
            loss_pct = (current_price - self.entry_price) / self.entry_price
            if loss_pct < -self.stop_loss_pct:
                return True, f"触发止损！亏损 {loss_pct:.1%}"
        return False, ""

    def check_drawdown(self):
        """回撤检查"""
        drawdown = (self.peak_capital - self.capital) / self.peak_capital
        if drawdown > self.max_drawdown_pct:
            return False, f"回撤超限：{drawdown:.1%} > {self.max_drawdown_pct:.0%}"
        return True, f"回撤 {drawdown:.1%}"

    def update_peak(self):
        if self.capital > self.peak_capital:
            self.peak_capital = self.capital

risk = RiskManager(CONFIG)

# ===== 主循环 =====
print("=" * 55)
print("🎓 QUANT MONITOR v1.0 — 毕业设计")
print("=" * 55)
print(f"  模拟本金: ${CONFIG['capital']}")
print(f"  扫描间隔: {CONFIG['check_interval']}秒")
print(f"  止损线:   {CONFIG['stop_loss_pct']:.0%}")
print(f"  单笔仓位: {CONFIG['max_position_pct']:.0%}")
print(f"  日志文件: {log_file}")
print("=" * 55)
print("  按 Ctrl+C 停止")
print("=" * 55)

round_num = 0

while True:
    round_num += 1
    t = datetime.now()
    ts = t.strftime("%H:%M:%S")

    print(f"\n[{ts}] === 第 {round_num} 轮扫描 ===")

    # ===== 第1步：行情采集（第3课+第6课） =====
    cg = fetch_price("CoinGecko",
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
        lambda d: d["bitcoin"]["usd"])

    ba = fetch_price("币安",
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        lambda d: float(d["price"]))

    ok = fetch_price("OKX",
        "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
        lambda d: float(d["data"][0]["last"]))

    # 显示行情
    prices_ok = []
    if cg: print(f"  CoinGecko: ${cg:,.2f}"); prices_ok.append(("CoinGecko", cg))
    if ba: print(f"  币安:      ${ba:,.2f}"); prices_ok.append(("币安", ba))
    if ok: print(f"  OKX:       ${ok:,.2f}"); prices_ok.append(("OKX", ok))

    # ===== 第2步：策略分析（第4-5课） =====
    signals = []
    if ba and ok:
        spread = (ba - ok) / ((ba + ok) / 2) * 10000
        status = "🔴 报警" if abs(spread) > CONFIG["spread_alert_bps"] else "🟢 正常"
        print(f"  币安vsOKX价差: {spread:+.2f} bps {status}")
        if abs(spread) > CONFIG["spread_alert_bps"]:
            if spread > 0:
                signals.append(("套利信号", "卖币安买OKX", ba, spread))
            else:
                signals.append(("套利信号", "卖OKX买币安", ok, abs(spread)))

    # ===== 第3步：风控检查（第11课） =====
    risk.update_peak()

    # 回撤检查
    dd_ok, dd_msg = risk.check_drawdown()
    print(f"  风控: {dd_msg}")

    if not dd_ok:
        print(f"  ⛔ 回撤超限！停止交易！")
        log_trade("风控", "系统", 0, 0, 0, "拒绝", dd_msg)
        time.sleep(CONFIG["check_interval"])
        continue

    # ===== 第4步：执行信号（模拟） =====
    for sig_type, action, price, spread in signals:
        # 仓位检查
        pos_ok, pos_msg = risk.check_position(CONFIG["capital"] * CONFIG["max_position_pct"])
        if not pos_ok:
            print(f"  ⛔ {pos_msg}")
            log_trade(sig_type, action, price, spread, 
                     risk.position/risk.capital, "拒绝", pos_msg)
            continue

        # 模拟交易
        trade_amount = risk.capital * CONFIG["max_position_pct"]
        risk.position = trade_amount
        risk.entry_price = price
        risk.trades += 1

        print(f"  ✅ 模拟执行: {action}")
        print(f"     金额: ${trade_amount:.2f}")
        log_trade(sig_type, action, price, spread,
                 risk.position/risk.capital, "通过", f"交易#{risk.trades}")

    # ===== 第5步：止损检查 =====
    if risk.position > 0 and ba:
        triggered, msg = risk.check_stop_loss(ba)
        if triggered:
            print(f"  ⛔ {msg}")
            loss = risk.position * CONFIG["stop_loss_pct"]
            risk.capital -= loss
            risk.position = 0
            risk.entry_price = 0
            print(f"     剩余本金: ${risk.capital:.2f}")
            log_trade("止损", "BTC", ba, 0, 0, "触发", msg)

    # ===== 状态显示 =====
    print(f"  📊 账户: ${risk.capital:.2f} | 持仓: ${risk.position:.2f} | 交易次数: {risk.trades}")

    # ===== 等待 =====
    time.sleep(CONFIG["check_interval"])
