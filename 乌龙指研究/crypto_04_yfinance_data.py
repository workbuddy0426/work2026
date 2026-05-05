#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用yfinance获取加密货币相关数据
获取BTC-USD、ETH-USD或加密货币ETF数据
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def download_crypto_yf(symbol="BTC-USD", period="1mo", interval="1m"):
    """
    从Yahoo Finance下载加密货币数据
    
    参数:
    - symbol: BTC-USD, ETH-USD, BITO, MSTR等
    - period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    - interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """
    print(f"🎯 小乌正在从Yahoo Finance下载 {symbol} {interval} 数据...")
    
    try:
        # 下载数据
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            print(f"❌ 未能获取数据")
            return None
        
        # 重置索引，将时间作为列
        df.reset_index(inplace=True)
        
        # 重命名列
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock_splits']
        
        # 删除不需要的列
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
        # 保存数据
        os.makedirs("data/crypto", exist_ok=True)
        filename = f"data/crypto/{symbol.replace('-', '')}_{interval}_{period}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ 成功获取 {len(df)} 条数据")
        print(f"📁 已保存: {filename}")
        print(f"\n📊 数据概览:")
        print(f"  时间范围: {df['timestamp'].min()} 至 {df['timestamp'].max()}")
        print(f"  价格范围: ${df['low'].min():,.2f} - ${df['high'].max():,.2f}")
        print(f"  平均成交量: {df['volume'].mean():.0f}")
        
        # 统计价格变化
        df['returns'] = df['close'].pct_change()
        max_drop = df['returns'].min()
        max_gain = df['returns'].max()
        volatility = df['returns'].std()
        
        print(f"\n📉 波动统计:")
        print(f"  最大单周期跌幅: {max_drop*100:.2f}%")
        print(f"  最大单周期涨幅: {max_gain*100:.2f}%")
        print(f"  波动率(标准差): {volatility*100:.2f}%")
        
        # 查找潜在的闪崩事件（单日跌幅>5%且反弹）
        df['future_return'] = df['close'].shift(-1) / df['close'] - 1
        crashes = df[(df['returns'] < -0.05) & (df['future_return'] > 0.02)]
        
        if not crashes.empty:
            print(f"\n⚡ 历史闪崩事件（跌>5%且下周期反弹>2%）:")
            print(f"   发现 {len(crashes)} 次")
            for _, row in crashes.head(5).iterrows():
                print(f"   {row['timestamp']}: 跌{row['returns']*100:.1f}% → 弹{row['future_return']*100:.1f}%")
        
        return df
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def main():
    print("=" * 60)
    print("🔄 使用Yahoo Finance获取加密货币数据")
    print("=" * 60)
    
    # 下载BTC-USD数据（1分钟粒度，最近7天）
    print("\n" + "="*60)
    df1 = download_crypto_yf("BTC-USD", period="5d", interval="1m")
    
    if df1 is not None:
        print("\n🎉 BTC数据获取成功！")
    
    print("=" * 60)

if __name__ == "__main__":
    main()