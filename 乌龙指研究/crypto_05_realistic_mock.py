#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成逼真的加密货币模拟数据
基于真实BTC市场统计特征（波动率、自相关性、闪崩频率）
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_realistic_btc_data(days=90, seed=42):
    """
    生成逼真的BTC 1分钟数据
    
    基于真实市场特征：
    - 年化波动率：约60-80%
    - 日波动率：约3-5%
    - 闪崩频率：每月1-3次（>10%跌幅）
    - 闪崩反弹：平均恢复50-70%跌幅
    - 波动聚集（GARCH效应）：大跌后波动率上升
    """
    print(f"🎯 小乌正在生成逼真的BTC模拟数据（{days}天）...")
    print("   基于真实市场统计特征")
    
    np.random.seed(seed)
    
    # 生成时间序列（1分钟粒度）
    periods = days * 24 * 60
    dates = pd.date_range(end=datetime.now(), periods=periods, freq='1min')
    
    # 基础价格
    base_price = 65000
    
    # 基础波动率参数（年化60% → 分钟级波动率）
    annual_vol = 0.60
    minute_vol = annual_vol / np.sqrt(365 * 24 * 60)
    
    # 生成GARCH-like波动率过程
    returns = []
    volatilities = []
    current_vol = minute_vol
    
    for i in range(periods):
        # GARCH(1,1) 简化模型：波动聚集
        if i > 0 and len(returns) > 0:
            # 前一期收益平方影响当前波动率
            shock = returns[-1] ** 2
            current_vol = np.sqrt(0.000001 + 0.85 * current_vol**2 + 0.10 * shock)
        
        volatilities.append(current_vol)
        ret = np.random.normal(0, current_vol)
        returns.append(ret)
    
    returns = np.array(returns)
    
    # 植入真实的闪崩事件
    num_crashes = int(days / 30 * 2)  # 每30天约2次
    crash_indices = np.random.choice(range(1000, periods-100), num_crashes, replace=False)
    
    crashes_info = []
    for idx in sorted(crash_indices):
        # 闪崩特征：5分钟内快速下跌8-15%
        crash_duration = np.random.randint(3, 8)  # 3-8分钟
        crash_magnitude = np.random.uniform(0.08, 0.15)  # 8-15%
        
        # 生成闪崩价格路径（加速下跌）
        for i in range(crash_duration):
            if idx + i < periods:
                # 指数式下跌
                progress = i / crash_duration
                crash_return = -crash_magnitude * (progress ** 0.5) / crash_duration
                returns[idx + i] = crash_return
        
        # 反弹特征：恢复50-70%的跌幅，持续10-30分钟
        recovery_duration = np.random.randint(10, 30)
        recovery_magnitude = crash_magnitude * np.random.uniform(0.5, 0.7)
        
        for i in range(recovery_duration):
            if idx + crash_duration + i < periods:
                progress = i / recovery_duration
                # 指数式反弹后平稳
                recovery_return = recovery_magnitude * np.exp(-3 * progress) / 5
                returns[idx + crash_duration + i] = recovery_return
        
        crashes_info.append({
            'index': idx,
            'timestamp': dates[idx],
            'duration': crash_duration,
            'magnitude': crash_magnitude,
            'recovery': recovery_magnitude
        })
    
    # 计算价格序列
    log_prices = np.cumsum(returns)
    prices = base_price * np.exp(log_prices)
    
    # 生成OHLC数据（基于价格序列添加微观结构噪声）
    df = pd.DataFrame({'timestamp': dates})
    
    # 每个周期的OHLC
    for i in range(len(dates)):
        if i == 0:
            df.loc[i, 'close'] = prices[i]
        else:
            df.loc[i, 'close'] = prices[i]
        
        # 添加微观噪声生成OHLC
        noise_high = abs(np.random.normal(0, 0.001))
        noise_low = abs(np.random.normal(0, 0.001))
        
        df.loc[i, 'high'] = prices[i] * (1 + noise_high)
        df.loc[i, 'low'] = prices[i] * (1 - noise_low)
        df.loc[i, 'open'] = prices[i-1] if i > 0 else prices[i] * (1 + np.random.normal(0, 0.0005))
        
        # 成交量（与波动率正相关）
        base_volume = 100
        volume_boost = 1 + volatilities[i] * 1000  # 高波动时成交量放大
        df.loc[i, 'volume'] = np.random.exponential(base_volume * volume_boost)
    
    # 确保OHLC逻辑正确
    df['high'] = df[['high', 'open', 'close']].max(axis=1) * 1.001
    df['low'] = df[['low', 'open', 'close']].min(axis=1) * 0.999
    
    # 保存数据
    os.makedirs("data/crypto", exist_ok=True)
    filename = f"data/crypto/BTCUSDT_realistic_{days}days.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    # 统计报告
    print(f"\n✅ 生成完成！")
    print(f"   数据量: {len(df):,} 条 ({days}天1分钟数据)")
    print(f"   价格范围: ${df['low'].min():,.2f} - ${df['high'].max():,.2f}")
    print(f"   最终价格: ${df['close'].iloc[-1]:,.2f}")
    
    print(f"\n📊 统计特征:")
    print(f"   平均波动率(分钟): {np.mean(volatilities)*100:.4f}%")
    print(f"   年化波动率: {np.mean(volatilities)*np.sqrt(365*24*60)*100:.1f}%")
    
    print(f"\n⚡ 植入闪崩事件: {len(crashes_info)} 次")
    for i, crash in enumerate(crashes_info, 1):
        print(f"   {i}. {crash['timestamp']}: "
              f"跌{crash['magnitude']*100:.1f}% → 弹{crash['recovery']*100:.1f}% "
              f"(持续{crash['duration']}分钟)")
    
    # 计算实际检测到的闪崩
    df['returns'] = df['close'].pct_change()
    detected_crashes = []
    
    for i in range(5, len(df) - 10):
        window_return = (df.iloc[i]['close'] - df.iloc[i-5]['close']) / df.iloc[i-5]['close']
        if window_return <= -0.05:  # 5分钟内跌5%
            recovery = (df.iloc[i+10]['close'] - df.iloc[i]['close']) / df.iloc[i]['close']
            if recovery >= 0.02:  # 10分钟内反弹2%
                detected_crashes.append({
                    'timestamp': df.iloc[i]['timestamp'],
                    'drop': window_return * 100,
                    'recovery': recovery * 100
                })
    
    print(f"\n🎯 算法可检测闪崩: {len(detected_crashes)} 次")
    if detected_crashes:
        avg_profit = np.mean([c['recovery'] for c in detected_crashes])
        print(f"   平均套利收益: {avg_profit:.2f}%")
    
    print(f"\n📁 已保存: {filename}")
    
    return df, crashes_info

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 生成高保真加密货币模拟数据")
    print("=" * 60)
    
    df, crashes = generate_realistic_btc_data(days=90, seed=2026)
    
    print("\n" + "=" * 60)
    print("🎉 完成！可以运行闪崩检测算法了。")
    print("=" * 60)