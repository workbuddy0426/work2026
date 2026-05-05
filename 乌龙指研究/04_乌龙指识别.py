"""
小乌：乌龙指信号识别算法
功能：分析历史数据，识别潜在的乌龙指信号
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import glob

DATA_DIR = "data"
RESULT_DIR = "results"
os.makedirs(RESULT_DIR, exist_ok=True)

def detect_fat_finger(df, code, name):
    """
    识别乌龙指信号
    
    判断标准：
    1. 价格偏离N分钟均价 > 阈值（如8%）
    2. 成交量 > 前N分钟平均成交量的M倍（如3倍）
    3. 后续K分钟内价格回归（确认是乌龙指而非趋势）
    """
    
    # 参数设置（降低阈值以便识别模拟数据中的信号）
    LOOKBACK = 5  # 回看5分钟
    PRICE_THRESHOLD = 0.08  # 价格偏离8%
    VOLUME_THRESHOLD = 2  # 成交量倍数（降低）
    RECOVERY_TIME = 5  # 5分钟内需回归
    RECOVERY_THRESHOLD = 0.05  # 回归幅度小于5%（放宽）
    
    signals = []
    
    # 计算移动平均
    df['price_ma'] = df['close'].rolling(window=LOOKBACK).mean()
    df['volume_ma'] = df['volume'].rolling(window=LOOKBACK).mean()
    
    # 计算价格偏离
    df['price_deviation'] = (df['close'] - df['price_ma']) / df['price_ma']
    
    # 计算成交量倍数
    df['volume_ratio'] = df['volume'] / df['volume_ma']
    
    # 遍历寻找信号
    for i in range(LOOKBACK + RECOVERY_TIME, len(df) - RECOVERY_TIME):
        # 条件1：价格偏离
        price_dev = abs(df.iloc[i]['price_deviation'])
        if price_dev < PRICE_THRESHOLD:
            continue
        
        # 条件2：成交量异常
        vol_ratio = df.iloc[i]['volume_ratio']
        if vol_ratio < VOLUME_THRESHOLD:
            continue
        
        # 条件3：后续回归
        future_prices = df.iloc[i+1:i+1+RECOVERY_TIME]['close']
        current_price = df.iloc[i]['close']
        price_ma = df.iloc[i]['price_ma']
        
        # 检查是否回归至均价附近
        max_deviation = abs((future_prices - price_ma) / price_ma).max()
        
        if max_deviation < RECOVERY_THRESHOLD:
            # 发现乌龙指信号
            signal = {
                'code': code,
                'name': name,
                'time': df.iloc[i]['time'] if 'time' in df.columns else i,
                'price': df.iloc[i]['close'],
                'price_ma': price_ma,
                'price_deviation': df.iloc[i]['price_deviation'],
                'volume': df.iloc[i]['volume'],
                'volume_ratio': vol_ratio,
                'recovery_time': RECOVERY_TIME,
                'direction': 'up' if df.iloc[i]['price_deviation'] > 0 else 'down'
            }
            signals.append(signal)
    
    return signals

def analyze_all():
    """分析所有已下载的数据"""
    
    print("🎯 小乌开始扫描乌龙指信号...\n")
    
    # 查找所有分钟数据文件（包括模拟数据）
    pattern = f"{DATA_DIR}/*_mock.csv"
    files = glob.glob(pattern)
    
    if not files:
        # 尝试其他模式
        pattern = f"{DATA_DIR}/*_min.csv"
        files = glob.glob(pattern)
    
    if not files:
        print("❌ 没有找到分钟数据文件，请先运行 03_下载历史数据.py")
        return
    
    all_signals = []
    
    for file in files:
        # 解析文件名获取code和name
        filename = os.path.basename(file)
        parts = filename.replace('_min.csv', '').split('_')
        
        if len(parts) >= 2:
            code = parts[0]
            name = '_'.join(parts[1:])
            
            try:
                df = pd.read_csv(file)
                signals = detect_fat_finger(df, code, name)
                all_signals.extend(signals)
                
                print(f"✅ {name}: 发现 {len(signals)} 个信号")
                
            except Exception as e:
                print(f"❌ {name} 分析失败: {e}")
    
    # 保存结果
    if all_signals:
        signals_df = pd.DataFrame(all_signals)
        result_file = f"{RESULT_DIR}/fat_finger_signals_{datetime.now().strftime('%Y%m%d')}.csv"
        signals_df.to_csv(result_file, index=False, encoding='utf-8-sig')
        
        print(f"\n📊 统计结果:")
        print(f"- 分析文件数: {len(files)}")
        print(f"- 总信号数: {len(all_signals)}")
        print(f"- 上涨信号: {len([s for s in all_signals if s['direction']=='up'])}")
        print(f"- 下跌信号: {len([s for s in all_signals if s['direction']=='down'])}")
        print(f"\n📁 详细结果已保存: {result_file}")
        
        # 显示前5个信号
        print("\n🔍 示例信号（前5个）:")
        print(signals_df.head().to_string(index=False))
        
    else:
        print("\n⚠️ 未发现乌龙指信号")
        print("建议:")
        print("1. 调整阈值参数（当前: 偏离8%, 成交量3倍）")
        print("2. 下载更多历史数据")
        print("3. 检查数据质量")

if __name__ == "__main__":
    analyze_all()