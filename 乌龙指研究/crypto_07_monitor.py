#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币闪崩实时监控系统
支持两种数据源：
  - 模拟回测（默认）：从CSV历史数据模拟实时流
  - 实时监控（--live）：通过 Gate.io REST API 轮询获取实时价格

用法：
  python crypto_07_monitor.py                     # 模拟模式（500条，500倍速）
  python crypto_07_monitor.py --live               # 实时轮询模式（每60秒检测一次）
  python crypto_07_monitor.py --live --interval 30 # 实时模式，30秒轮询一遍
  python crypto_07_monitor.py --live --paper       # 实时 + 模拟交易
  python crypto_07_monitor.py --paper              # 回测 + 模拟交易（验证策略历史表现）
"""
import json
import os
import sys
import time
import urllib.request
import pandas as pd
import numpy as np
import subprocess
import platform
from datetime import datetime
from collections import deque

# ============================================================
# 微信推送配置
# ============================================================
SEND_WECHAT_PY = os.path.join(
    os.environ.get("SKILL_DIR", r"C:\Users\user\.workbuddy\skills\alarm-memo-assistant-pro"),
    "scripts", "send_wechat.py"
)
PYTHON_EXE = r"C:\Users\user\.workbuddy\binaries\python\versions\3.13.12\python.exe"


def get_wechat_exe():
    """获取Python解释器路径（优先系统python，其次指定路径）"""
    try:
        import shutil
        if shutil.which("python"):
            return "python"
    except Exception:
        pass
    if platform.system() == "Windows":
        return PYTHON_EXE
    return sys.executable or "python3"


def send_wechat_alert(alert):
    """发送闪崩预警到微信"""
    msg = (
        f"【闪崩预警】\n"
        f"标的: {alert['symbol']}\n"
        f"时间: {alert['timestamp']}\n"
        f"价格: ${alert['baseline_price']:,} -> ${alert['crash_price']:,}\n"
        f"跌幅: {alert['drop_pct']:.2f}%\n"
        f"成交量放大: {alert['volume_ratio']:.1f}x\n"
        f"建议持有: {alert['suggested_hold']}分钟\n"
        f"信号ID: {alert['detection_id']}"
    )
    try:
        env = os.environ.copy()
        env["SKILL_DIR"] = os.path.dirname(os.path.dirname(SEND_WECHAT_PY))
        result = subprocess.run(
            [get_wechat_exe(), SEND_WECHAT_PY, "send", msg],
            capture_output=True, text=True, encoding="utf-8", timeout=30, env=env
        )
        if result.returncode == 0:
            print(f"  >>> 微信推送成功")
            return True
        else:
            print(f"  >>> 微信推送失败: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"  >>> 微信推送异常: {e}")
        return False

# ============================================================
# 配置参数
# ============================================================
CONFIG = {
    # 闪崩检测参数
    "price_drop_threshold": 0.05,
    "lookback_minutes": 5,
    "hold_minutes": 20,
    "volume_spike_threshold": 2,

    # 监控标的
    "symbols": ["BTCUSDT", "ETHUSDT"],

    # 预警文件
    "alert_file": "results/alerts.json",
    "log_file": "results/monitor_log.csv",

    # 微信推送
    "push_enabled": True,

    # 模拟交易参数
    "paper_trading": {
        "enabled": False,          # --paper 开启
        "capital": 10000.0,        # 初始资金
        "risk_per_trade": 0.1,     # 每笔投入资金比例
        "stop_loss_pct": 0.03,     # 止损: 低于入场价3%
        "take_profit_recovery": 0.6,  # 止盈: 收复暴跌的60%
        "slippage": 0.001,         # 滑点 0.1%
    },
    "trade_file": "results/trades.json",
}


class PaperTrader:
    """模拟交易管理器"""

    def __init__(self, config=None):
        cfg = (config or CONFIG).get("paper_trading", {})
        self.capital = float(cfg.get("capital", 10000))
        self.risk_per_trade = float(cfg.get("risk_per_trade", 0.1))
        self.stop_loss_pct = float(cfg.get("stop_loss_pct", 0.03))
        self.take_profit_recovery = float(cfg.get("take_profit_recovery", 0.6))
        self.slippage = float(cfg.get("slippage", 0.001))
        self.hold_minutes = CONFIG.get("hold_minutes", 20)
        self.trade_file = CONFIG.get("trade_file", "results/trades.json")

        self.position = None  # current open position
        self.trades = []      # completed trades
        self._load_trades()

    def _load_trades(self):
        if os.path.exists(self.trade_file):
            try:
                with open(self.trade_file, 'r', encoding='utf-8') as f:
                    self.trades = json.load(f)
            except:
                self.trades = []

    def open_position(self, alert):
        """收到闪崩信号时开仓"""
        if self.position is not None:
            return None  # 已有持仓，不开新仓

        entry_price = alert['crash_price'] * (1 + self.slippage)  # 买在更低点
        position_size = self.capital * self.risk_per_trade
        quantity = position_size / entry_price

        crash_magnitude = abs(alert['drop_pct']) / 100  # e.g. 9.87 -> 0.0987
        take_profit_price = entry_price * (1 + crash_magnitude * self.take_profit_recovery)
        stop_loss_price = entry_price * (1 - self.stop_loss_pct)

        entry_time = alert.get('entry_time', alert['timestamp'])
        hold_until = None
        try:
            from datetime import timedelta
            dt = datetime.fromisoformat(entry_time) if isinstance(entry_time, str) else entry_time
            hold_until = (dt + timedelta(minutes=self.hold_minutes)).isoformat()
        except:
            pass

        self.position = {
            'symbol': alert['symbol'],
            'detection_id': alert['detection_id'],
            'entry_time': entry_time,
            'entry_price': round(entry_price, 2),
            'quantity': round(quantity, 6),
            'cost': round(position_size, 2),
            'stop_loss': round(stop_loss_price, 2),
            'take_profit': round(take_profit_price, 2),
            'hold_until': hold_until,
            'crash_pct': alert['drop_pct'],
            'high_since_entry': entry_price,
            'status': 'OPEN',
        }
        self._save_trade(self.position)
        return self.position

    def update(self, current_price, timestamp):
        """用新价格更新持仓，返回平仓结果（如触发退出）"""
        if self.position is None:
            return None

        # 跟踪持仓期间的最高价
        self.position['high_since_entry'] = max(self.position['high_since_entry'], current_price)

        # 检查止损
        if current_price <= self.position['stop_loss']:
            return self._close_position(current_price, timestamp, 'STOP_LOSS')

        # 检查止盈
        if current_price >= self.position['take_profit']:
            return self._close_position(current_price, timestamp, 'TAKE_PROFIT')

        # 检查时间退出
        if self.position.get('hold_until'):
            try:
                exit_dt = datetime.fromisoformat(self.position['hold_until'])
                current_dt = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp
                if current_dt >= exit_dt:
                    return self._close_position(current_price, timestamp, 'TIME_EXIT')
            except:
                pass

        return None

    def _close_position(self, exit_price, exit_time, reason):
        """平仓"""
        pos = self.position
        exit_price_real = exit_price * (1 - self.slippage)  # 卖在更低点
        exit_value = exit_price_real * pos['quantity']
        pnl = exit_value - pos['cost']
        pnl_pct = (pnl / pos['cost']) * 100

        trade_result = {
            'symbol': pos['symbol'],
            'detection_id': pos['detection_id'],
            'entry_time': pos['entry_time'],
            'exit_time': exit_time.isoformat() if hasattr(exit_time, 'isoformat') else str(exit_time),
            'entry_price': pos['entry_price'],
            'exit_price': round(exit_price_real, 2),
            'quantity': pos['quantity'],
            'cost': pos['cost'],
            'exit_value': round(exit_value, 2),
            'pnl': round(pnl, 2),
            'pnl_pct': round(pnl_pct, 2),
            'exit_reason': reason,
            'crash_pct': pos['crash_pct'],
        }

        self.trades.append(trade_result)
        self.capital += pnl  # 更新资金

        # 保存开仓记录时加上平仓信息
        self.position['status'] = 'CLOSED'
        self.position['exit_time'] = trade_result['exit_time']
        self.position['exit_price'] = trade_result['exit_price']
        self.position['exit_reason'] = reason
        self.position['pnl'] = trade_result['pnl']
        self.position['pnl_pct'] = trade_result['pnl_pct']

        self._save_trade(self.position)

        # 更新trades.json
        self._save_trades()

        self.position = None
        return trade_result

    def _save_trade(self, trade_data):
        """追加记录到trades.json"""
        os.makedirs("results", exist_ok=True)
        all_trades = []
        if os.path.exists(self.trade_file):
            try:
                with open(self.trade_file, 'r', encoding='utf-8') as f:
                    all_trades = json.load(f)
            except:
                all_trades = []
        # 更新或追加
        existing = [t for t in all_trades if t.get('detection_id') != trade_data.get('detection_id')]
        existing.append(trade_data)
        if len(existing) > 200:
            existing = existing[-200:]
        with open(self.trade_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    def _save_trades(self):
        """保存完整交易历史"""
        os.makedirs("results", exist_ok=True)
        with open(self.trade_file, 'w', encoding='utf-8') as f:
            json.dump(self.trades, f, ensure_ascii=False, indent=2)

    def get_summary(self):
        """交易统计摘要"""
        closed = [t for t in self.trades if 'pnl' in t]
        if not closed:
            return "暂无已完成交易"

        wins = [t for t in closed if t['pnl'] > 0]
        losses = [t for t in closed if t['pnl'] <= 0]
        total_pnl = sum(t['pnl'] for t in closed)
        win_rate = len(wins) / len(closed) * 100 if closed else 0
        avg_win = sum(t['pnl'] for t in wins) / len(wins) if wins else 0
        avg_loss = sum(t['pnl'] for t in losses) / len(losses) if losses else 0

        return {
            'total_trades': len(closed),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': round(win_rate, 1),
            'total_pnl': round(total_pnl, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'capital': round(self.capital, 2),
            'profit_pct': round((total_pnl / (self.capital - total_pnl)) * 100, 2) if total_pnl != self.capital else 0,
        }


class GateioStream:
    """实时数据源：通过 Gate.io REST API 轮询获取最新1分钟K线"""
    BASE_URL = "https://api.gateio.ws/api/v4"

    def __init__(self, symbols, interval=60):
        self.symbols = symbols
        self.interval = interval
        self.seen_candles = {s: set() for s in symbols}
        self.total = 0
        self.index = 0
        self._start = datetime.now()

    def _fetch(self, symbol, limit=10):
        url = f"{self.BASE_URL}/spot/candlesticks?currency_pair={symbol}&interval=1m&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode())

    def get_next(self):
        """轮询获取最新未处理蜡烛"""
        while True:
            for symbol in self.symbols:
                try:
                    candles = self._fetch(symbol)
                    for c in candles:
                        ts = c[0]
                        if ts in self.seen_candles[symbol]:
                            continue
                        self.seen_candles[symbol].add(ts)

                        price = float(c[5])
                        volume = float(c[6])
                        ktime = datetime.fromtimestamp(int(ts))
                        self.total += 1
                        self.index += 1

                        return {
                            'timestamp': ktime,
                            'price': price,
                            'volume': volume,
                            'high': float(c[4]),
                            'low': float(c[3]),
                            'symbol': symbol,
                        }
                except Exception as e:
                    print(f"\r  [Gate.io请求失败] {e}", end="")
                    time.sleep(5)

            # 本轮没有新数据，等待后重试
            elapsed = (datetime.now() - self._start).total_seconds()
            status = self.progress()
            print(f"\r[{elapsed:.0f}s] {status} | 无新K线，等待{self.interval}秒...", end="")
            time.sleep(self.interval)

    def progress(self):
        return f"已获取 {self.total} 条"

    def get_name(self):
        return f"Gate.io实时数据 ({', '.join(self.symbols)}, 每{self.interval}s轮询)"


class FlashCrashDetector:
    """闪崩检测器"""

    def __init__(self, symbol, config=None):
        self.symbol = symbol
        self.config = config or CONFIG

        self.price_window = deque(maxlen=self.config['lookback_minutes'] + 5)
        self.volume_window = deque(maxlen=self.config['lookback_minutes'] + 5)

        self.last_price = None
        self.last_alert_time = None
        self.alert_cooldown = 300
        self.crashes_detected = 0
        self.start_time = datetime.now()

    def update(self, price, volume, timestamp):
        self.price_window.append((timestamp, price))
        self.volume_window.append((timestamp, volume))
        self.last_price = price
        return self._check_crash(timestamp)

    def _check_crash(self, timestamp):
        if len(self.price_window) < self.config['lookback_minutes']:
            return None

        baseline_price = self.price_window[0][1]
        current_price = self.price_window[-1][1]
        drop_pct = (current_price - baseline_price) / baseline_price

        baseline_volume = np.mean([v for _, v in self.volume_window]) if len(self.volume_window) > 3 else 0
        current_volume = self.volume_window[-1][1]
        volume_ratio = current_volume / max(baseline_volume, 1)

        is_crash = (
            drop_pct <= -self.config['price_drop_threshold'] and
            volume_ratio >= self.config['volume_spike_threshold'] and
            (self.last_alert_time is None or
             (timestamp - self.last_alert_time).total_seconds() > self.alert_cooldown)
        )

        if is_crash:
            self.crashes_detected += 1
            self.last_alert_time = timestamp
            return {
                'symbol': self.symbol,
                'timestamp': timestamp.isoformat(),
                'baseline_price': round(baseline_price, 2),
                'crash_price': round(current_price, 2),
                'drop_pct': round(drop_pct * 100, 2),
                'volume_ratio': round(volume_ratio, 2),
                'suggested_hold': self.config['hold_minutes'],
                'detection_id': f"{self.symbol}_CRASH_{self.crashes_detected}"
            }
        return None

    def get_status(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return {
            'symbol': self.symbol,
            'uptime_seconds': round(elapsed),
            'data_points': len(self.price_window),
            'crashes_detected': self.crashes_detected,
            'last_price': self.last_price,
        }


class SimulatedStream:
    """模拟实时数据流（从CSV文件读取）"""

    def __init__(self, csv_file, speed=1, limit=None):
        self.df = pd.read_csv(csv_file)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        if limit:
            self.df = self.df.iloc[-limit:]
        self.index = 0
        self.speed = speed
        self.total = len(self.df)

    def get_next(self):
        if self.index >= len(self.df):
            return None
        row = self.df.iloc[self.index]
        self.index += 1
        time.sleep(1 / self.speed)
        return {
            'timestamp': row['timestamp'],
            'price': row['close'],
            'volume': row['volume'],
            'high': row['high'],
            'low': row['low']
        }

    def progress(self):
        return f"{self.index}/{self.total} ({self.index/self.total*100:.1f}%)"

    def get_name(self):
        return f"模拟回测 ({self.total}条, {self.speed}x速度)"


def save_alert(alert, alert_file="results/alerts.json"):
    """保存预警到文件 + 微信推送"""
    os.makedirs("results", exist_ok=True)
    alerts = []
    if os.path.exists(alert_file):
        try:
            with open(alert_file, 'r', encoding='utf-8') as f:
                alerts = json.load(f)
        except:
            alerts = []
    alerts.append(alert)
    if len(alerts) > 100:
        alerts = alerts[-100:]
    with open(alert_file, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)
    print(f"\n!!! 预警: {alert['symbol']} 下跌 {alert['drop_pct']}%")
    if CONFIG.get("push_enabled", True):
        send_wechat_alert(alert)


def log_to_csv(data, log_file="results/monitor_log.csv"):
    """记录监控日志"""
    os.makedirs("results", exist_ok=True)
    file_exists = os.path.exists(log_file)
    df = pd.DataFrame([data])
    df.to_csv(log_file, mode='a', header=not file_exists, index=False, encoding='utf-8-sig')


def print_header(source_name, config):
    """打印启动信息"""
    print("=" * 70)
    print(" 加密货币闪崩实时监控系统")
    print("=" * 70)
    print(f"\n 数据源: {source_name}")
    print(f" 监控标的: {', '.join(config['symbols'])}")
    print(f" 检测参数: 下跌>{config['price_drop_threshold']*100:.0f}%, "
          f"回看{config['lookback_minutes']}分钟, 量比>={config['volume_spike_threshold']}x")
    print(f" 微信推送: {'启用' if config.get('push_enabled', True) else '关闭'}")


def run_monitor(stream, detectors, paper_trader=None):
    """通用监控循环（支持多标的独立检测器 + 模拟交易）"""
    print(f"\n{'='*70}")
    print(f"监控启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")

    if paper_trader:
        print(f"  模拟交易: 启用 | 初始资金 ${paper_trader.capital:,.2f}")

    alerts = []
    last_status_print = 0

    try:
        while True:
            data = stream.get_next()
            if data is None:
                print(f"\n{'='*70}")
                print(f"数据流结束")
                break

            # 提取数据
            symbol = data.get('symbol', 'BTCUSDT')
            normalized = symbol.replace('_USDT', 'USDT').replace('_', '')
            price = data['price']
            volume = data['volume']
            timestamp = data['timestamp']

            detector = detectors.get(normalized) or detectors.get('BTCUSDT')
            if detector is None:
                continue

            # 1) 闪崩检测
            alert = detector.update(price=price, volume=volume, timestamp=timestamp)
            if alert:
                alerts.append(alert)
                save_alert(alert)
                log_to_csv({
                    'timestamp': alert['timestamp'],
                    'symbol': alert['symbol'],
                    'event': 'FLASH_CRASH',
                    'drop_pct': alert['drop_pct'],
                    'baseline_price': alert['baseline_price'],
                    'crash_price': alert['crash_price'],
                    'volume_ratio': alert['volume_ratio']
                })
                print()

                # 2) 模拟交易：闪崩信号 → 开仓
                if paper_trader:
                    entry = paper_trader.open_position(alert)
                    if entry:
                        send_wechat_trade("开仓", entry)
                        print(f"  -> 开仓: ${entry['entry_price']:,.2f} x {entry['quantity']:.4f} "
                              f"(止损 ${entry['stop_loss']:,.2f}, 止盈 ${entry['take_profit']:,.2f})")

            # 3) 模拟交易：价格更新 → 检查退出条件
            if paper_trader and paper_trader.position is not None:
                trade_exit = paper_trader.update(price, timestamp)
                if trade_exit:
                    send_wechat_trade("平仓", trade_exit)
                    print(f"\n  -> 平仓 [{trade_exit['exit_reason']}]: "
                          f"${trade_exit['pnl']:+.2f} ({trade_exit['pnl_pct']:+.2f}%) "
                          f"资金: ${paper_trader.capital:,.2f}")

            # 状态显示（每秒最多刷新一次）
            now = time.time()
            if now - last_status_print > 1:
                last_status_print = now
                total_crashes = sum(d.get_status()['crashes_detected'] for d in detectors.values())
                status_parts = [f"${d.get_status()['last_price']:,.2f}" if d.get_status()['last_price']
                                else "--" for d in detectors.values()]
                names = list(detectors.keys())
                prices = " | ".join(f"{n}: {p}" for n, p in zip(names, status_parts))
                pos_str = f" | 持仓: ${paper_trader.position['entry_price']:,.0f}" if (paper_trader and paper_trader.position) else ""
                print(f"\r  [{stream.progress()}] {prices} | 闪崩: {total_crashes}{pos_str}   ", end="")

    except KeyboardInterrupt:
        print(f"\n\n 用户中断")

    # ---------- 最终报告 ----------
    print(f"\n\n{'='*70}")
    print(f" 监控报告")
    print(f"{'='*70}")

    for name, detector in detectors.items():
        status = detector.get_status()
        print(f"\n {name}:")
        print(f"   运行时间: {status['uptime_seconds']:.0f}秒")
        print(f"   数据点数: {status['data_points']}条")
        print(f"   闪崩检测: {status['crashes_detected']}次")

    if alerts:
        print(f"\n 闪崩事件列表:")
        for i, a in enumerate(alerts, 1):
            print(f"   {i}. {a['timestamp']} - {a['symbol']} "
                  f"${a['baseline_price']:,}->${a['crash_price']:,} "
                  f"(跌{a['drop_pct']:.1f}%, 量比{a['volume_ratio']:.1f}x)")

        total_profit = sum(abs(a['drop_pct']) * 0.6 for a in alerts)
        print(f"\n 收益估计 (假设反弹60%):")
        print(f"   总信号: {len(alerts)}次")
        print(f"   平均跌幅: {np.mean([a['drop_pct'] for a in alerts]):.1f}%")
        print(f"   估计总收益: {total_profit:.1f}%")
        print(f"   若每次$100: ${len(alerts) * 100:.0f}")

    # 模拟交易报告
    if paper_trader:
        summary = paper_trader.get_summary()
        if isinstance(summary, dict):
            print(f"\n{'='*70}")
            print(f" 模拟交易报告")
            print(f"{'='*70}")
            print(f"   总交易: {summary['total_trades']}笔")
            print(f"   胜/负: {summary['wins']}/{summary['losses']} ({summary['win_rate']}%胜率)")
            print(f"   总盈亏: ${summary['total_pnl']:+,.2f} ({summary['profit_pct']:+.2f}%)")
            print(f"   平均盈利: ${summary['avg_win']:+,.2f}")
            print(f"   平均亏损: ${summary['avg_loss']:+,.2f}")
            print(f"   当前资金: ${summary['capital']:+,.2f}")
            if paper_trader.position:
                print(f"   持仓中: ${paper_trader.position['entry_price']:,.0f} | "
                      f"止损 ${paper_trader.position['stop_loss']:,.0f} | "
                      f"止盈 ${paper_trader.position['take_profit']:,.0f}")

    print(f"\n 预警文件: results/alerts.json")
    print(f" 交易记录: results/trades.json")
    print(f" 监控日志: results/monitor_log.csv")
    print(f"\n{'='*70}")


def send_wechat_trade(etype, data):
    """发送交易（开仓/平仓）通知到微信"""
    if not CONFIG.get("push_enabled", True):
        return
    if etype == "开仓":
        msg = (
            f"【闪崩开仓】\n"
            f"标的: {data['symbol']}\n"
            f"入场价: ${data['entry_price']:,.2f}\n"
            f"数量: {data['quantity']:.4f}\n"
            f"金额: ${data['cost']:,.2f}\n"
            f"止盈: ${data['take_profit']:,.2f}\n"
            f"止损: ${data['stop_loss']:,.2f}\n"
            f"信号ID: {data['detection_id']}"
        )
    elif etype == "平仓":
        msg = (
            f"【闪崩平仓】\n"
            f"标的: {data['symbol']}\n"
            f"出场价: ${data['exit_price']:,.2f}\n"
            f"盈亏: ${data['pnl']:+,.2f} ({data['pnl_pct']:+.2f}%)\n"
            f"原因: {data['exit_reason']}\n"
            f"信号ID: {data['detection_id']}"
        )
    else:
        return
    try:
        env = os.environ.copy()
        env["SKILL_DIR"] = os.path.dirname(os.path.dirname(SEND_WECHAT_PY))
        subprocess.run(
            [get_wechat_exe(), SEND_WECHAT_PY, "send", msg],
            capture_output=True, text=True, encoding="utf-8", timeout=30, env=env
        )
    except:
        pass


def main():
    # 解析命令行参数
    args = sys.argv[1:]
    live_mode = "--live" in args
    paper_mode = "--paper" in args or "--trade" in args
    interval = 60
    for i, a in enumerate(args):
        if a == "--interval" and i + 1 < len(args):
            try:
                interval = int(args[i + 1])
            except:
                pass

    # 如果paper模式，启用模拟交易
    CONFIG["paper_trading"]["enabled"] = paper_mode

    # >>> 检测Gate.io连通性（如果请求live模式） <<<
    if live_mode:
        print("正在检查Gate.io连通性...")
        try:
            url = "https://api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT"
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7"})
            resp = urllib.request.urlopen(req, timeout=8)
            data = json.loads(resp.read().decode())
            btc_price = float(data[0]['last'])
            print(f"  Gate.io连接成功！BTC/USDT = ${btc_price:,.2f}")
        except Exception as e:
            print(f"  Gate.io连接失败: {e}")
            print("  回退到模拟模式...")
            live_mode = False

    # ---------- 初始化 ----------
    paper_trader = PaperTrader() if paper_mode else None

    if live_mode:
        gateio_symbols = ["BTC_USDT"]
        stream = GateioStream(gateio_symbols, interval=interval)
        detectors = {
            "BTCUSDT": FlashCrashDetector("BTCUSDT"),
        }
        print_header(stream.get_name(), CONFIG)
    else:
        data_file = "data/crypto/BTCUSDT_realistic_90days.csv"
        if not os.path.exists(data_file):
            data_file = "data/crypto/BTCUSDT_mock_30days.csv"
            if not os.path.exists(data_file):
                print("错误: 未找到数据文件")
                return
        stream = SimulatedStream(data_file, speed=500, limit=500)
        detectors = {"BTCUSDT": FlashCrashDetector("BTCUSDT")}
        print_header(stream.get_name(), CONFIG)

    run_monitor(stream, detectors, paper_trader)


if __name__ == "__main__":
    main()
