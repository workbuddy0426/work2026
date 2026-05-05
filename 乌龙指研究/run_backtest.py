#!/usr/bin/env python3
"""全量90天回测脚本 - 闪崩检测 + 模拟交易
运行: python run_backtest.py [--speed 2000]
"""
import sys
import time
import json
import os

# 禁用微信推送（回测不需要发微信）
os.environ["NO_WECHAT"] = "1"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crypto_07_monitor import (
    CONFIG, FlashCrashDetector, SimulatedStream,
    PaperTrader, save_alert, send_wechat_alert,
    log_to_csv
)

def save_alert_noop(alert, alert_file="results/alerts.json"):
    """回测模式：不发送微信通知"""
    os.makedirs("results", exist_ok=True)
    alerts = []
    if os.path.exists(alert_file):
        try:
            with open(alert_file, 'r', encoding='utf-8') as f:
                alerts = json.load(f)
        except:
            alerts = []
    alerts.append(alert)
    if len(alerts) > 200:
        alerts = alerts[-200:]
    with open(alert_file, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)

# 解析参数
speed = 2000
for i, a in enumerate(sys.argv):
    if a == "--speed" and i + 1 < len(sys.argv):
        try:
            speed = int(sys.argv[i + 1])
        except:
            pass

print("=" * 70)
print(" 90天全量回测 - 闪崩检测 + 模拟交易")
print("=" * 70)

data_file = "data/crypto/BTCUSDT_realistic_90days.csv"
if not os.path.exists(data_file):
    print(f"文件不存在: {data_file}")
    sys.exit(1)

# 初始化
stream = SimulatedStream(data_file, speed=speed, limit=None)
detector = FlashCrashDetector("BTCUSDT")
trader = PaperTrader()

CONFIG["push_enabled"] = False  # 不推微信

print(f"\n 数据: {data_file}")
print(f" 数据量: {stream.total}条 | 速度: {speed}x")
print(f" 参数: 下跌>{CONFIG['price_drop_threshold']*100:.0f}%, "
      f"回看{CONFIG['lookback_minutes']}分钟, 量比>={CONFIG['volume_spike_threshold']}x")
print(f" 初始资金: \${trader.capital:,.2f}")
print(f" 每笔风险: {trader.risk_per_trade*100:.0f}% = \${trader.capital * trader.risk_per_trade:,.0f}")
print()

# 运行
start_time = time.time()
alerts = []
last_pct = 0

try:
    while True:
        data = stream.get_next()
        if data is None:
            break

        price, volume, ts = data['price'], data['volume'], data['timestamp']

        # detector.update() 内部调用 _check_crash，返回闪崩预警dict
        alert_crash = detector.update(price, volume, ts)
        if alert_crash:
            alerts.append(alert_crash)
            # 保存但不发微信
            save_alert_noop(alert_crash)
            log_to_csv({
                'timestamp': alert_crash['timestamp'],
                'symbol': alert_crash['symbol'],
                'event': 'FLASH_CRASH',
                'drop_pct': alert_crash['drop_pct'],
                'baseline_price': alert_crash['baseline_price'],
                'crash_price': alert_crash['crash_price'],
                'volume_ratio': alert_crash['volume_ratio']
            })

            # 模拟交易
            entry = trader.open_position(alert_crash)
            if entry:
                print(f"  [{alert_crash['timestamp'][:19]}] 开仓 @ \${entry['entry_price']:,.0f} "
                      f"(跌{alert_crash['drop_pct']:.1f}%) "
                      f"止盈\${entry['take_profit']:,.0f} 止损\${entry['stop_loss']:,.0f}")

        # 交易跟踪
        if trader.position is not None:
            exit_info = trader.update(price, ts)
            if exit_info:
                print(f"  [{exit_info['exit_time'][:19]}] 平仓 [{exit_info['exit_reason']}] "
                      f"\${exit_info['pnl']:+,.2f} ({exit_info['pnl_pct']:+.2f}%) "
                      f"剩余资金 \${trader.capital:,.2f}")

        # 进度
        elapsed = time.time() - start_time
        pct = stream.index / stream.total * 100
        if pct - last_pct >= 5:
            last_pct = pct
            pos_str = f" | 持仓中" if trader.position else ""
            print(f"  进度: {pct:.0f}% | 闪崩: {len(alerts)}次 | "
                  f"资金: \${trader.capital:,.2f}{pos_str}")
            sys.stdout.flush()

except KeyboardInterrupt:
    print(f"\n\n 用户中断")

# 结果汇总
elapsed = time.time() - start_time
print(f"\n{'='*70}")
print(f" 回测完成! 耗时 {elapsed:.0f}秒 ({stream.total}条数据)")
print(f"{'='*70}")

print(f"\n 闪崩检测:")
print(f"   总信号: {len(alerts)}次")
print(f"   平均跌幅: {sum(abs(a['drop_pct']) for a in alerts) / len(alerts):.1f}%" if alerts else "   -")

summary = trader.get_summary()
if isinstance(summary, dict) and summary.get('total_trades', 0) > 0:
    print(f"\n 模拟交易:")
    print(f"   总交易: {summary['total_trades']}笔")
    print(f"   胜/负: {summary['wins']}/{summary['losses']} ({summary['win_rate']}%胜率)")
    print(f"   总盈亏: \${summary['total_pnl']:+,.2f} ({summary['profit_pct']:+.2f}%)")
    print(f"   平均盈利/亏损: +\${summary['avg_win']} / -\${summary.get('avg_loss', 0):.2f}")
    print(f"   初始资金: \$10,000.00")
    print(f"   最终资金: \${summary['capital']:+,.2f}")
    
    # 按退出原因统计
    reasons = {}
    for t in trader.trades:
        r = t['exit_reason']
        if r not in reasons:
            reasons[r] = {'count': 0, 'pnl': 0, 'wins': 0}
        reasons[r]['count'] += 1
        reasons[r]['pnl'] += t['pnl']
        if t['pnl'] > 0:
            reasons[r]['wins'] += 1
    
    print(f"\n   退出原因分布:")
    for r, d in sorted(reasons.items(), key=lambda x: -x[1]['count']):
        win_pct = d['wins'] / d['count'] * 100
        avg_pnl = d['pnl'] / d['count']
        print(f"     {r}: {d['count']}次, 胜率{win_pct:.0f}%, "
              f"平均\${avg_pnl:+.2f}, 总\${d['pnl']:+,.2f}")

print(f"\n   详细记录: results/trades.json")
print(f"   预警记录: results/alerts.json")
print(f"   监控日志: results/monitor_log.csv")
print(f"\n{'='*70}")
