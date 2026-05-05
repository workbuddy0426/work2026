#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载加密货币历史数据（Binance）
获取BTC/USDT 1分钟K线数据
"""
import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime, timedelta
import os
import time

def download_btc_data():
    """下载BTC 1分钟K线数据（无需API Key）"""
    print("🎯 小乌正在下载BTC历史数据...")
    
    # 创建客户端（不需要API Key即可获取公共数据）
    client = Client()
    
    # 下载最近30天的1分钟K线
    symbol = "BTCUSDT"
    interval = Client.KLINE_INTERVAL_1MINUTE
    
    # 计算时间范围
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    print(f"📅 时间范围: {start_time.strftime('%Y-%m-%d')} 至 {end_time.strftime('%Y-%m-%d')}")
    
    try:
        # 获取K线数据
        klines = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_time.strftime("%Y-%m-%d"),
            end_str=end_time.strftime("%Y-%m-%d")
        )
        
        if not klines:
            print("❌ 未获取到数据")
            return None
        
        # 转换为DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        # 转换数据类型
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        
        # 保存数据
        os.makedirs("data/crypto", exist_ok=True)
        filename = f"data/crypto/BTCUSDT_1min_{start_time.strftime('%Y%m%d')}_{end_time.strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ 成功下载 {len(df)} 条数据")
        print(f"📁 已保存: {filename}")
        print(f"\n📊 数据概览:")
        print(f"  时间范围: {df['timestamp'].min()} 至 {df['timestamp'].max()}")
        print(f"  价格范围: ${df['low'].min():.2f} - ${df['high'].max():.2f}")
        print(f"  平均成交量: {df['volume'].mean():.4f} BTC")
        
        return df
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

if __name__ == "__main__":
    df = download_btc_data()
    
    if df is not None:
        print("\n🎉 数据下载完成！准备进行闪崩分析...")