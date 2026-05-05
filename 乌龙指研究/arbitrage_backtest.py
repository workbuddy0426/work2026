#!/usr/bin/env python3
"""跨交易所价差套利 - 修复版"""
import json, os
import numpy as np

CONFIG = {
    "spread_threshold": 0.002,    # 0.2% 价差触发
    "exit_ratio": 0.3,            # 收敛到峰值的30%时退出
    "fee": 0.001,                 # 0.1%/边
    "capital": 10000.0,
    "per_trade_pct": 0.5,         # 50%资金用于一组套利
}
RESULT_FILE = "results/arbitrage_results.json"


def gen_data(length=129600, base=50000, events=30):
    """生成两个交易所的价格
    事件: 随机一个交易所价格偏离，持续5~60分钟后回归"""
    rng = np.random.RandomState(42)
    # 基础价格
    ret = rng.normal(0, 0.0002, length)
    price = base * np.exp(np.cumsum(np.log1p(ret)))
    # 交易所A和B: 基础+独立噪音
    a = price + price * rng.normal(0, 0.0003, length)
    b = price + price * rng.normal(0, 0.0003, length)

    # 注入价差事件
    evts = 0
    i = rng.randint(5000, 10000)
    while i < length - 60:
        spread = rng.uniform(0.003, 0.015)  # 0.3%~1.5%价差
        duration = rng.randint(5, 60)       # 持续5~60分钟
        side = 1 if rng.random() > 0.5 else -1
        for j in range(i, min(i + duration, length)):
            fade = (1 - (j - i) / duration) ** 0.8
            a[j] = price[j] * (1 + side * spread * fade)
        evts += 1
        i += duration + rng.randint(2000, 8000)

    # 基础价差统计
    raw = (a - b) / b * 10000
    return a, b, evts, raw


def run(cfg):
    threshold = cfg["spread_threshold"]
    fee = cfg["fee"]
    capital = cfg["capital"]
    trade_size = capital * cfg["per_trade_pct"]  # 每组套利资金

    a, b, evts, raw_spreads = gen_data(events=25)

    cash = capital
    pos = None  # {leg_a_qty, leg_b_qty, entry_spread, peak_spread, entry_i, side}
    trades = []

    for i in range(len(a)):
        pa, pb = a[i], b[i]
        spread = (pa - pb) / pb

        # ---- 持仓管理 ----
        if pos is not None:
            # 跟踪峰值价差
            current_abs = abs(spread)
            if current_abs > pos['peak_spread']:
                pos['peak_spread'] = current_abs

            # 退出条件: 收敛到峰值的30%
            exit_threshold = pos['peak_spread'] * CONFIG['exit_ratio']
            timeout = (i - pos['entry_i']) > 120

            if current_abs < exit_threshold or timeout:
                # 平仓计算
                entry_pa, entry_pb = pos['entry_pa'], pos['entry_pb']
                qty = pos['leg_qty']

                pnl_a = qty * (pa - entry_pa) * pos['side_a']
                pnl_b = qty * (pb - entry_pb) * pos['side_b']
                gross = pnl_a + pnl_b
                net = gross - 2 * fee * qty * (entry_pa + pa) * 0.5 - 2 * fee * qty * (entry_pb + pb) * 0.5

                cash += pos['locked'] + net
                reason = "CONVERGE" if current_abs < exit_threshold else "TIMEOUT"

                trades.append({
                    'entry_i': pos['entry_i'], 'exit_i': i,
                    'entry_spread_bps': round(pos['entry_spread'] * 10000, 1),
                    'exit_spread_bps': round(spread * 10000, 1),
                    'peak_spread_bps': round(pos['peak_spread'] * 10000, 1),
                    'hold_minutes': i - pos['entry_i'],
                    'pnl': round(net, 2),
                    'pnl_pct': round(net / pos['locked'] * 100, 2),
                    'reason': reason,
                    'label': pos['label'],
                })
                pos = None

        # ---- 开新仓 ----
        if pos is None and cash > trade_size and abs(spread) > threshold:
            locked = trade_size
            qty = locked / 2 / pa  # 一半资金用于每边

            if spread > 0:
                # A贵B便宜: 空A 多B
                pos = {
                    'leg_qty': qty, 'entry_pa': pa, 'entry_pb': pb,
                    'entry_spread': spread, 'peak_spread': abs(spread),
                    'entry_i': i, 'locked': locked,
                    'side_a': -1, 'side_b': 1,
                    'label': f"空A@{pa:.0f} 多B@{pb:.0f}",
                }
            else:
                pos = {
                    'leg_qty': qty, 'entry_pa': pa, 'entry_pb': pb,
                    'entry_spread': spread, 'peak_spread': abs(spread),
                    'entry_i': i, 'locked': locked,
                    'side_a': 1, 'side_b': -1,
                    'label': f"多A@{pa:.0f} 空B@{pb:.0f}",
                }
            cash -= locked

    return trades, cash, raw_spreads, evts


def main():
    print("=" * 70)
    print(" 跨交易所价差套利 - 模拟回测")
    print("=" * 70)
    print(f" 触发价差: {CONFIG['spread_threshold']*100:.2f}%")
    print(f" 退出条件: 收敛到峰值的{CONFIG['exit_ratio']*100:.0f}%")
    print(f" 手续费:   {CONFIG['fee']*100:.1f}%/边")
    print(f" 资金:     ${CONFIG['capital']:,.0f}")

    trades, final_cash, spreads, evts = run(CONFIG)
    total_pnl = final_cash - CONFIG['capital']

    print(f"\n 模拟数据: 注入{evts}个价差事件")
    print(f" 价差>50bps: {(abs(spreads)>50).sum()}次 | >100bps: {(abs(spreads)>100).sum()}次")

    print(f"\n{'='*70}")
    print(f" 回测结果")
    print(f"{'='*70}")
    print(f" 开仓: {len(trades)}笔")
    if trades:
        pnls = [t['pnl'] for t in trades]
        wins = [t for t in trades if t['pnl'] > 0]
        losses = [t for t in trades if t['pnl'] < 0]
        print(f" 胜/负: {len(wins)}/{len(losses)} ({len(wins)/len(trades)*100:.1f}%胜率)")
        print(f" 总盈亏: ${total_pnl:+,.2f} ({total_pnl/CONFIG['capital']*100:+.2f}%)")
        print(f" 最终资金: ${final_cash:,.2f}")
        if wins:
            print(f" 平均盈利: ${sum(t['pnl'] for t in wins)/len(wins):+.2f}")
        if losses:
            print(f" 平均亏损: ${sum(t['pnl'] for t in losses)/len(losses):+.2f}")

        # 退出分析
        reasons = {}
        for t in trades:
            r = t['reason']
            reasons.setdefault(r, {'n': 0, 'pnl': 0, 'w': 0})
            reasons[r]['n'] += 1
            reasons[r]['pnl'] += t['pnl']
            if t['pnl'] > 0:
                reasons[r]['w'] += 1
        print(f"\n 退出原因:")
        for r, d in sorted(reasons.items(), key=lambda x: -x[1]['n']):
            wr = d['w']/d['n']*100
            print(f"   {r}: {d['n']}次 胜率{wr:.0f}% 合计${d['pnl']:+.2f}")

        # 最大回撤
        peak = CONFIG['capital']
        dd = 0
        eq = CONFIG['capital']
        for t in trades:
            eq += t['pnl']
            if eq > peak:
                peak = eq
            dd = max(dd, (peak - eq) / peak)
        print(f"\n 最大回撤: {dd*100:.2f}%")
        print(f" 夏普(估): {total_pnl/CONFIG['capital']/0.02:.2f}" if total_pnl > 0 else "")

    # 不同阈值对比
    print(f"\n{'='*70}")
    print(f" 阈值敏感性分析")
    print(f"{'='*70}")
    print(f"  {'阈值':>8} {'开仓':>4} {'胜率':>6} {'盈亏':>10} {'收益%':>7}")
    for th in [0.001, 0.002, 0.003, 0.005, 0.008]:
        cfg2 = CONFIG.copy()
        cfg2['spread_threshold'] = th
        t2, fc, _, _ = run(cfg2)
        p = fc - CONFIG['capital']
        w = len([x for x in t2 if x['pnl'] > 0]) / max(len(t2), 1) * 100
        print(f"  {th*100:>7.2f}% {len(t2):>4} {w:>5.1f}% {p:>+9.2f} {p/CONFIG['capital']*100:>+6.2f}%")

    print(f"\n 详细记录: {RESULT_FILE}")
    with open(RESULT_FILE, 'w') as f:
        json.dump({'trades': trades, 'total_pnl': total_pnl}, f, indent=2)


if __name__ == "__main__":
    main()
