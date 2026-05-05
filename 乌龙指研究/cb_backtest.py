#!/usr/bin/env python3
"""可转债乌龙指回测：跑一个月数据，统计准确率"""
import pandas as pd, glob, json, os

def run_backtest(df, name, threshold=0.08):
    """回测乌龙指检测"""
    signals = 0
    hits = 0
    false_alarms = 0
    actual = 0
    trade_pnl = 0
    
    df['price_chg'] = df['close'].pct_change()
    
    for i in range(1, len(df)):
        chg = abs(df.loc[i, 'price_chg'])
        is_real = df.loc[i, 'is_fat_finger']
        
        if is_real:
            actual += 1
        
        if chg > threshold and df.loc[i, 'close'] > 50:
            signals += 1
            if is_real:
                hits += 1
            else:
                false_alarms += 1
            
            # 模拟交易：假设在下一分钟回归50%
            if i + 1 < len(df):
                entry = df.loc[i, 'close']
                exit_p = df.loc[i + 1, 'close']
                pnl = abs(exit_p - entry) * 1000 / entry  # 按1000张算
                if not is_real:
                    pnl = -pnl * 0.5  # 假信号亏一半
                trade_pnl += pnl
    
    precision = hits / signals * 100 if signals > 0 else 0
    recall = hits / actual * 100 if actual > 0 else 0
    
    return {
        "name": name,
        "total_rows": len(df),
        "real_fatfingers": int(actual),
        "signals": signals,
        "hits": hits,
        "false_alarms": false_alarms,
        "missed": int(actual - hits),
        "precision": round(precision, 1),
        "recall": round(recall, 1),
        "pnl": round(trade_pnl, 2),
    }

def main():
    files = glob.glob('data/*_mock.csv')
    results = []
    total = {"signals": 0, "hits": 0, "false": 0, "real": 0, "pnl": 0}
    keymap = {"signals": "signals", "hits": "hits", "false": "false_alarms", "real": "real_fatfingers", "pnl": "pnl"}
    
    for f in files:
        df = pd.read_csv(f)
        name = os.path.basename(f).replace('_mock.csv', '')
        r = run_backtest(df, name)
        results.append(r)
        for k, src in keymap.items():
            total[k] += r[src]
    
    total["precision"] = round(total["hits"] / total["signals"] * 100, 1) if total["signals"] > 0 else 0
    total["recall"] = round(total["hits"] / total["real"] * 100, 1) if total["real"] > 0 else 0
    total["name"] = "合计"
    
    output = {"results": results, "total": total}
    os.makedirs("results", exist_ok=True)
    with open("results/cb_backtest.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print(" 可转债乌龙指回测结果（一个月模拟数据）")
    print("=" * 60)
    print(f" {'债券':<18} {'真实':>4} {'检测':>4} {'命中':>4} {'误报':>4} {'漏检':>4} {'精准率':>6} {'召回率':>6} {'收益':>8}")
    print("-" * 60)
    for r in results:
        print(f" {r['name']:<16} {r['real_fatfingers']:>4} {r['signals']:>4} {r['hits']:>4} "
              f"{r['false_alarms']:>4} {r['missed']:>4} {r['precision']:>5.1f}% {r['recall']:>5.1f}% ${r['pnl']:>+7.2f}")
    t = total
    print("-" * 60)
    print(f" {'合计':<16} {t['real']:>4} {t['signals']:>4} {t['hits']:>4} "
          f"{t['false']:>4} {t['real']-t['hits']:>4} {t['precision']:>5.1f}% {t['recall']:>5.1f}% ${t['pnl']:>+7.2f}")
    print(f"\n结果已保存: results/cb_backtest.json")

if __name__ == "__main__":
    main()
