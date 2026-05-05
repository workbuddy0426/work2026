#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币闪崩检测算法
识别BTC/USDT 1分钟数据中的闪崩事件
"""
import pandas as pd
import numpy as np
import glob
import os

def detect_flash_crashes(df, price_drop=0.05, recovery=0.03, lookback=5):
    """
    检测闪崩事件
    
    参数:
    - price_drop: 价格下跌阈值（默认5%）
    - recovery: 反弹阈值（默认3%）
    - lookback: 观察窗口（分钟）
    """
    print(f"🎯 小乌正在分析闪崩事件...")
    print(f"   参数: 下跌>{price_drop*100}%, 反弹>{recovery*100}%, 窗口{lookback}分钟")
    
    crashes = []
    
    for i in range(lookback, len(df) - lookback):
        # 获取当前窗口数据
        window = df.iloc[i-lookback:i+lookback+1].copy()
        
        # 计算窗口内的价格变化
        baseline = df.iloc[i-lookback]['close']  # 基准价格
        current = df.iloc[i]['close']            # 当前价格
        
        # 计算下跌幅度
        drop_pct = (current - baseline) / baseline
        
        # 检查是否达到闪崩条件
        if drop_pct <= -price_drop:
            # 检查是否反弹
            future_prices = df.iloc[i+1:i+lookback+1]['close']
            if len(future_prices) > 0:
                recovery_price = future_prices.max()
                recovery_pct = (recovery_price - current) / current
                
                if recovery_pct >= recovery:
                    # 记录闪崩事件
                    crashes.append({
                        'timestamp': df.iloc[i]['timestamp'],
                        'baseline_price': baseline,
                        'crash_price': current,
                        'recovery_price': recovery_price,
                        'drop_pct': drop_pct * 100,
                        'recovery_pct': recovery_pct * 100,
                        'duration_min': lookback,
                        'volume': df.iloc[i]['volume'],
                        'profit_potential': recovery_pct * 100
                    })
    
    if crashes:
        crashes_df = pd.DataFrame(crashes)
        print(f"\n✅ 发现 {len(crashes)} 次闪崩事件")
        print(f"\n📊 闪崩统计:")
        print(f"  平均下跌: {crashes_df['drop_pct'].mean():.2f}%")
        print(f"  平均反弹: {crashes_df['recovery_pct'].mean():.2f}%")
        print(f"  最大下跌: {crashes_df['drop_pct'].min():.2f}%")
        print(f"  最大反弹: {crashes_df['recovery_pct'].max():.2f}%")
        
        # 显示前5个闪崩事件
        print(f"\n🏆 最大反弹机会Top 5:")
        top5 = crashes_df.nlargest(5, 'recovery_pct')
        for idx, row in top5.iterrows():
            print(f"  {row['timestamp']}: 跌{row['drop_pct']:.1f}% → 弹{row['recovery_pct']:.1f}%")
        
        return crashes_df
    else:
        print("\n⚠️ 未发现闪崩事件（尝试降低阈值）")
        return None

def analyze_all_data():
    """分析所有下载的数据文件"""
    # 查找所有BTC数据文件
    files = glob.glob("data/crypto/BTCUSDT*.csv")
    
    if not files:
        print("❌ 未找到数据文件，请先运行 crypto_01_download_data.py")
        return
    
    all_crashes = []
    
    for file in files:
        print(f"\n📁 分析文件: {file}")
        df = pd.read_csv(file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 使用不同参数检测
        for threshold in [0.03, 0.05, 0.08]:
            crashes = detect_flash_crashes(df, price_drop=threshold, recovery=0.02, lookback=5)
            if crashes is not None:
                all_crashes.append(crashes)
    
    if all_crashes:
        combined = pd.concat(all_crashes, ignore_index=True)
        
        # 去重
        combined = combined.drop_duplicates(subset=['timestamp'])
        
        # 保存结果
        os.makedirs("results", exist_ok=True)
        output_file = "results/crypto_flash_crashes.csv"
        combined.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n🎉 分析完成！")
        print(f"   总共发现 {len(combined)} 次闪崩事件")
        print(f"   结果已保存: {output_file}")
        
        # 套利潜力分析
        print(f"\n💰 套利潜力分析:")
        print(f"   平均每次机会收益: {combined['recovery_pct'].mean():.2f}%")
        print(f"   最大单次收益: {combined['recovery_pct'].max():.2f}%")
        print(f"   假设月交易10次，资金1万美元:")
        monthly_return = combined['recovery_pct'].mean() * 10
        print(f"   月收益潜力: {monthly_return:.2f}% (${monthly_return * 100:.0f})")

if __name__ == "__main__":
    analyze_all_data()