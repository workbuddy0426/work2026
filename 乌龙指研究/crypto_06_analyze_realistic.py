#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析高保真模拟数据的闪崩事件
"""
import pandas as pd
import numpy as np
import glob
import os

def analyze_flash_crashes_v2(df, price_drop=0.05, recovery=0.03, lookback=5, hold_time=10):
    """
    增强版闪崩检测算法
    
    参数:
    - price_drop: 价格下跌阈值
    - recovery: 反弹阈值
    - lookback: 观察窗口
    - hold_time: 持有时间（分钟）
    """
    print(f"🎯 分析参数: 下跌>{price_drop*100:.0f}%, 持有{hold_time}分钟, 反弹>{recovery*100:.0f}%")
    
    signals = []
    
    for i in range(lookback, len(df) - hold_time):
        # 计算窗口内的价格变化
        baseline = df.iloc[i-lookback]['close']
        current = df.iloc[i]['close']
        drop_pct = (current - baseline) / baseline
        
        # 检查是否达到闪崩条件
        if drop_pct <= -price_drop:
            # 计算未来持有时间的收益
            future_price = df.iloc[min(i+hold_time, len(df)-1)]['close']
            actual_return = (future_price - current) / current
            
            # 计算过程中的最大回撤
            min_price = df.iloc[i:min(i+hold_time, len(df))]['low'].min()
            max_drawdown = (min_price - current) / current
            
            signals.append({
                'timestamp': df.iloc[i]['timestamp'],
                'baseline_price': baseline,
                'entry_price': current,
                'exit_price': future_price,
                'drop_pct': drop_pct * 100,
                'actual_return': actual_return * 100,
                'max_drawdown': max_drawdown * 100,
                'volume': df.iloc[i]['volume'],
                'hold_time': hold_time
            })
    
    if signals:
        signals_df = pd.DataFrame(signals)
        
        # 统计
        profitable = signals_df[signals_df['actual_return'] > 0]
        unprofitable = signals_df[signals_df['actual_return'] <= 0]
        
        print(f"\n📊 检测结果:")
        print(f"   总信号数: {len(signals_df)}")
        print(f"   盈利次数: {len(profitable)} ({len(profitable)/len(signals_df)*100:.1f}%)")
        print(f"   亏损次数: {len(unprofitable)} ({len(unprofitable)/len(signals_df)*100:.1f}%)")
        print(f"   平均收益: {signals_df['actual_return'].mean():.2f}%")
        print(f"   最大单笔收益: {signals_df['actual_return'].max():.2f}%")
        print(f"   最大单笔亏损: {signals_df['actual_return'].min():.2f}%")
        print(f"   平均最大回撤: {signals_df['max_drawdown'].mean():.2f}%")
        
        # 收益分布
        print(f"\n💰 收益分布:")
        bins = [-np.inf, -5, -2, 0, 2, 5, np.inf]
        labels = ['<-5%', '-5~-2%', '-2~0%', '0~2%', '2~5%', '>5%']
        distribution = pd.cut(signals_df['actual_return'], bins=bins, labels=labels).value_counts()
        for label, count in distribution.items():
            print(f"   {label}: {count}次 ({count/len(signals_df)*100:.1f}%)")
        
        return signals_df
    else:
        print("\n⚠️ 未发现信号")
        return None

def parameter_sensitivity(df):
    """参数敏感性分析"""
    print("\n" + "="*60)
    print("📈 参数敏感性分析")
    print("="*60)
    
    results = []
    
    # 测试不同阈值
    for drop in [0.03, 0.05, 0.08, 0.10]:
        for hold in [5, 10, 15, 20]:
            signals = []
            for i in range(5, len(df) - hold):
                baseline = df.iloc[i-5]['close']
                current = df.iloc[i]['close']
                drop_pct = (current - baseline) / baseline
                
                if drop_pct <= -drop:
                    future_price = df.iloc[min(i+hold, len(df)-1)]['close']
                    actual_return = (future_price - current) / current
                    signals.append(actual_return)
            
            if signals:
                results.append({
                    'drop_threshold': f"{drop*100:.0f}%",
                    'hold_time': f"{hold}m",
                    'signals': len(signals),
                    'avg_return': np.mean(signals) * 100,
                    'win_rate': sum(1 for r in signals if r > 0) / len(signals) * 100
                })
    
    results_df = pd.DataFrame(results)
    print("\n" + results_df.to_string(index=False))
    
    # 找出最佳参数
    best = results_df.loc[results_df['avg_return'].idxmax()]
    print(f"\n🎯 最佳参数组合:")
    print(f"   下跌阈值: {best['drop_threshold']}")
    print(f"   持有时间: {best['hold_time']}")
    print(f"   平均收益: {best['avg_return']:.2f}%")
    print(f"   胜率: {best['win_rate']:.1f}%")
    
    return results_df

def main():
    print("=" * 60)
    print("🔄 分析高保真加密货币数据")
    print("=" * 60)
    
    # 查找数据文件
    files = glob.glob("data/crypto/BTCUSDT_realistic_*.csv")
    
    if not files:
        print("❌ 未找到数据文件，请先运行 crypto_05_realistic_mock.py")
        return
    
    for file in files:
        print(f"\n{'='*60}")
        print(f"📁 分析: {file}")
        print("="*60)
        
        df = pd.read_csv(file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 基础分析
        print(f"\n📊 数据概览:")
        print(f"   总记录: {len(df):,}")
        print(f"   时间跨度: {(df['timestamp'].max() - df['timestamp'].min()).days}天")
        print(f"   价格范围: ${df['low'].min():,.0f} - ${df['high'].max():,.0f}")
        
        # 使用不同参数检测
        print("\n" + "-"*60)
        print("策略A: 保守型 (跌5%, 持有10分钟)")
        signals_a = analyze_flash_crashes_v2(df, price_drop=0.05, recovery=0.00, hold_time=10)
        
        print("\n" + "-"*60)
        print("策略B: 激进型 (跌8%, 持有5分钟)")
        signals_b = analyze_flash_crashes_v2(df, price_drop=0.08, recovery=0.00, hold_time=5)
        
        # 参数敏感性分析
        sensitivity = parameter_sensitivity(df)
        
        # 保存结果
        if signals_a is not None:
            os.makedirs("results", exist_ok=True)
            signals_a.to_csv("results/crypto_signals_conservative.csv", index=False, encoding='utf-8-sig')
            print(f"\n📁 保守策略结果已保存")
        
        print("\n" + "="*60)
        print("🎉 分析完成！")
        print("="*60)

if __name__ == "__main__":
    main()