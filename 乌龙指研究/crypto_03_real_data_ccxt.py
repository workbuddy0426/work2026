#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用CCXT获取真实加密货币历史数据
支持多个交易所：Binance, OKX, Bybit等
"""
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import os
import time

def fetch_ohlcv(exchange_name='binance', symbol='BTC/USDT', timeframe='1m', days=30):
    """
    获取K线数据
    
    参数:
    - exchange_name: 交易所名称
    - symbol: 交易对
    - timeframe: 时间周期 (1m, 5m, 1h, 1d)
    - days: 获取天数
    """
    print(f"🎯 小乌正在从 {exchange_name} 获取 {symbol} {timeframe} 数据...")
    
    try:
        # 创建交易所实例
        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class({
            'enableRateLimit': True,  # 遵守API频率限制
        })
        
        # 计算时间范围
        since = exchange.parse8601((datetime.now() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ'))
        
        all_ohlcv = []
        limit = 1000  # 每次获取的最大条数
        
        while since < exchange.parse8601(datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')):
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
                if not ohlcv:
                    break
                    
                all_ohlcv.extend(ohlcv)
                
                # 更新since为最后一条数据的时间
                since = ohlcv[-1][0] + 1
                
                print(f"   已获取 {len(all_ohlcv)} 条数据...")
                
                # 遵守频率限制
                time.sleep(exchange.rateLimit / 1000)
                
            except Exception as e:
                print(f"   获取数据出错: {e}")
                break
        
        if not all_ohlcv:
            print(f"❌ 未能获取数据")
            return None
        
        # 转换为DataFrame
        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # 去重
        df = df.drop_duplicates(subset=['timestamp'])
        
        # 保存数据
        os.makedirs("data/crypto", exist_ok=True)
        filename = f"data/crypto/{symbol.replace('/', '')}_{timeframe}_{exchange_name}_{days}d.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ 成功获取 {len(df)} 条数据")
        print(f"📁 已保存: {filename}")
        print(f"\n📊 数据概览:")
        print(f"  时间范围: {df['timestamp'].min()} 至 {df['timestamp'].max()}")
        print(f"  价格范围: ${df['low'].min():,.2f} - ${df['high'].max():,.2f}")
        print(f"  平均成交量: {df['volume'].mean():.4f}")
        
        # 简单统计：查找最大单日跌幅
        df['returns'] = df['close'].pct_change()
        max_drop = df['returns'].min()
        max_gain = df['returns'].max()
        
        print(f"\n📉 波动统计:")
        print(f"  最大单周期跌幅: {max_drop*100:.2f}%")
        print(f"  最大单周期涨幅: {max_gain*100:.2f}%")
        print(f"  波动率(标准差): {df['returns'].std()*100:.2f}%")
        
        return df
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def main():
    print("=" * 60)
    print("🔄 开始获取真实加密货币数据")
    print("=" * 60)
    
    # 尝试多个交易所
    exchanges = ['binance', 'okx', 'bybit']
    
    for exchange in exchanges:
        print(f"\n{'='*60}")
        df = fetch_ohlcv(exchange_name=exchange, symbol='BTC/USDT', timeframe='1m', days=7)
        
        if df is not None and len(df) > 100:
            print(f"\n🎉 成功从 {exchange} 获取数据！")
            break
        else:
            print(f"\n⚠️ {exchange} 获取失败，尝试下一个...")
    
    print("=" * 60)

if __name__ == "__main__":
    main()