#!/usr/bin/env python3
"""快速参数优化 - 直接加载DataFrame，不模拟实时流"""
import sys, os, json, time
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crypto_07_monitor import CONFIG, FlashCrashDetector, PaperTrader

data_file = "data/crypto/BTCUSDT_realistic_90days.csv"
df = pd.read_csv(data_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(f"加载 {len(df)} 条数据")

params = [
    (20, 0.6, 2.0, "当前参数"),
    (60, 0.6, 2.0, "延长持有60min"),
    (120, 0.6, 2.0, "延长持有120min"),
    (20, 0.4, 2.0, "降低止盈40%"),
    (20, 0.8, 2.0, "提高止盈80%"),
    (60, 0.4, 2.0, "长持有+低止盈"),
    (60, 0.6, 1.5, "长持有+低量比"),
    (20, 0.6, 1.5, "低量比(更多信号)"),
    (120, 0.4, 1.5, "最长持有+最激进"),
]

print("=" * 90)
print(f"  {'参数':<22} {'信号':>4} {'交易':>4} {'胜率':>6} {'盈亏':>10} {'收益%':>7} {'止盈':>4} {'止损':>4} {'到期':>4}")
print("=" * 90)

results = []
for hold, recovery, volume, desc in params:
    CONFIG["hold_minutes"] = hold
    CONFIG["volume_spike_threshold"] = volume
    CONFIG["push_enabled"] = False

    detector = FlashCrashDetector("BTCUSDT")
    trader = PaperTrader()
    trader.trades = []
    trader.capital = 10000.0
    trader.position = None
    trader.take_profit_recovery = recovery
    trader.hold_minutes = hold

    alerts_cnt = 0
    for _, row in df.iterrows():
        ts = row['timestamp']
        price = row['close']
        volume = row['volume']

        alert = detector.update(price, volume, ts)
        if alert:
            alerts_cnt += 1
            trader.open_position(alert)

        if trader.position is not None:
            trader.update(price, ts)

    summary = trader.get_summary()
    trades_cnt = summary['total_trades'] if isinstance(summary, dict) else 0
    win_rate = summary['win_rate'] if isinstance(summary, dict) else 0
    total_pnl = summary['total_pnl'] if isinstance(summary, dict) else 0
    profit_pct = summary['profit_pct'] if isinstance(summary, dict) else 0

    reasons = {"TAKE_PROFIT": 0, "STOP_LOSS": 0, "TIME_EXIT": 0}
    for t in trader.trades:
        r = t['exit_reason']
        if r in reasons:
            reasons[r] += 1

    print(f"  {desc:<20} {alerts_cnt:>4} {trades_cnt:>4} {win_rate:>5.1f}% {total_pnl:>+9.2f} {profit_pct:>+6.2f}% "
          f"{reasons['TAKE_PROFIT']:>4} {reasons['STOP_LOSS']:>4} {reasons['TIME_EXIT']:>4}")

    results.append({
        'desc': desc, 'hold': hold, 'recovery': recovery, 'volume': volume,
        'trades': trades_cnt, 'win_rate': win_rate, 'pnl': total_pnl,
        'profit_pct': profit_pct,
        'tp': reasons['TAKE_PROFIT'], 'sl': reasons['STOP_LOSS'], 'te': reasons['TIME_EXIT'],
    })

print("=" * 90)
best = max(results, key=lambda r: r['pnl'])
print(f"\n最佳盈利: {best['desc']}")
print(f"  持有{best['hold']}min | 止盈{best['recovery']*100:.0f}% | 量比{best['volume']}x")
print(f"  交易{best['trades']}笔 | 胜率{best['win_rate']}% | 收益${best['pnl']:+.2f} ({best['profit_pct']:+.2f}%)")

best_winrate = max(results, key=lambda r: r['win_rate'] if r['trades'] >= 5 else 0)
print(f"\n最佳胜率: {best_winrate['desc']}")
print(f"  持有{best_winrate['hold']}min | 止盈{best_winrate['recovery']*100:.0f}% | 量比{best_winrate['volume']}x")
print(f"  交易{best_winrate['trades']}笔 | 胜率{best_winrate['win_rate']}% | 收益${best_winrate['pnl']:+.2f}")
