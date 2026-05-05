#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币数据获取设置
尝试多种数据源
"""
import pandas as pd
import requests
import os
from datetime import datetime, timedelta

def download_from_yahoo(symbol="BTC-USD", period="1mo"):
    """从Yahoo Finance下载数据"""
    print(f"🎯 尝试从Yahoo Finance下载 {symbol} 数据...")
    
    try:
        # Yahoo Finance API
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
        params = {
            "period1": int((datetime.now() - timedelta(days=30)).timestamp()),
            "period2": int(datetime.now().timestamp()),
            "interval": "1d",
            "events": "history"
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            # 保存CSV
            os.makedirs("data/crypto", exist_ok=True)
            filename = f"data/crypto/{symbol.replace('-', '')}_yahoo.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            df = pd.read_csv(filename)
            print(f"✅ 成功下载 {len(df)} 天数据")
            print(df.head())
            return df
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def generate_crypto_mock_data():
    """生成逼真的加密货币模拟数据（用于测试算法）"""
    print("🎯 生成BTC模拟数据（含闪崩事件）...")
    
    # 生成30天的1分钟数据
    periods = 30 * 24 * 60  # 30天，每分钟
    dates = pd.date_range(end=datetime.now(), periods=periods, freq='1min')
    
    # 基础价格
    base_price = 65000
    
    # 生成随机游走价格
    np.random.seed(42)
    returns = np.random.normal(0.00001, 0.0005, periods)  # 微小漂移+波动
    
    # 植入闪崩事件（3次）
    crash_indices = [10000, 25000, 35000]  # 闪崩位置
    
    for idx in crash_indices:
        if idx < periods - 10:
            # 闪崩：1分钟内跌5-8%
            crash_size = np.random.uniform(0.05, 0.08)
            returns[idx] = -crash_size
            # 随后反弹3-5%
            returns[idx+1] = np.random.uniform(0.03, 0.05)
    
    # 计算价格序列
    prices = base_price * np.exp(np.cumsum(returns))
    
    # 生成OHLC数据
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices * (1 + np.random.normal(0, 0.001, periods)),
        'high': prices * (1 + abs(np.random.normal(0, 0.002, periods))),
        'low': prices * (1 - abs(np.random.normal(0, 0.002, periods))),
        'close': prices,
        'volume': np.random.exponential(100, periods)
    })
    
    # 确保high >= low
    df['high'] = df[['high', 'low', 'close']].max(axis=1)
    df['low'] = df[['high', 'low', 'close']].min(axis=1)
    
    # 保存
    os.makedirs("data/crypto", exist_ok=True)
    filename = "data/crypto/BTCUSDT_mock_30days.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ 生成完成！")
    print(f"   数据量: {len(df)} 条 (30天1分钟数据)")
    print(f"   价格范围: ${df['low'].min():.2f} - ${df['high'].max():.2f}")
    print(f"   植入闪崩: {len(crash_indices)} 次")
    print(f"   已保存: {filename}")
    
    return df

if __name__ == "__main__":
    import numpy as np
    
    # 先生成模拟数据用于测试
    df = generate_crypto_mock_data()
    
    print("\n🎉 设置完成！可以运行闪崩检测算法了。")