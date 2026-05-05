"""
小乌：生成模拟数据（用于演示乌龙指识别算法）
说明：AKShare免费版分钟数据有限制，先用模拟数据演示核心逻辑
实际使用时需要：
1. Tushare付费版
2. 券商API（如QMT、聚宽）
3. 购买专业数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def generate_mock_data(code, name, days=30, num_fat_fingers=3):
    """
    生成模拟的1分钟K线数据，包含几个乌龙指信号
    
    参数:
        code: 可转债代码
        name: 可转债名称
        days: 生成多少天的数据
        num_fat_fingers: 植入多少个乌龙指信号
    """
    print(f"🎯 生成 {name}({code}) 的模拟数据...")
    
    # 生成时间序列（交易时间 9:30-11:30, 13:00-15:00）
    periods_per_day = 240  # 4小时 * 60分钟
    total_periods = days * periods_per_day
    
    # 基础价格（随机起点 100-150）
    base_price = np.random.uniform(100, 150)
    
    # 生成正常波动数据
    np.random.seed(42)  # 固定随机种子，便于复现
    
    prices = [base_price]
    for i in range(1, total_periods):
        # 正常波动：-0.5% 到 +0.5%
        change = np.random.normal(0, 0.002)
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)
    
    # 植入乌龙指信号
    fat_finger_indices = np.random.choice(
        range(periods_per_day, total_periods - 10), 
        size=num_fat_fingers, 
        replace=False
    )
    
    for idx in fat_finger_indices:
        # 乌龙指：突然下跌/上涨 10-15%
        direction = np.random.choice([-1, 1])
        magnitude = np.random.uniform(0.10, 0.15)
        
        # 瞬间偏离
        prices[idx] = prices[idx-1] * (1 + direction * magnitude)
        
        # 1-3分钟内回归
        recovery_time = np.random.randint(1, 4)
        for j in range(1, recovery_time + 1):
            if idx + j < len(prices):
                prices[idx + j] = prices[idx-1] * (1 + np.random.normal(0, 0.005))
    
    # 生成DataFrame
    df = pd.DataFrame({
        'time': range(total_periods),
        'open': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.001))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.001))) for p in prices],
        'close': prices,
        'volume': [np.random.randint(100000, 1000000) for _ in prices],
    })
    
    # 确保 high >= close >= low
    df['high'] = df[['high', 'close', 'open']].max(axis=1)
    df['low'] = df[['low', 'close', 'open']].min(axis=1)
    
    # 标记乌龙指位置（用于验证）
    df['is_fat_finger'] = False
    df.loc[fat_finger_indices, 'is_fat_finger'] = True
    
    # 保存数据
    filename = f"{DATA_DIR}/{code}_{name}_mock.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"✅ 生成 {len(df)} 条记录，植入 {num_fat_fingers} 个乌龙指信号")
    print(f"📁 数据已保存: {filename}")
    
    return df, fat_finger_indices

if __name__ == "__main__":
    print("🎯 小乌生成模拟数据（用于演示）\n")
    print("说明：这是模拟数据，用于演示乌龙指识别算法")
    print("实际交易请使用真实数据源（Tushare付费版/券商API）\n")
    
    # 生成3只可转债的模拟数据
    mock_list = [
        ('128136', '立讯转债'),
        ('110085', '通22转债'),
        ('127045', '牧原转债'),
    ]
    
    all_results = []
    for code, name in mock_list:
        df, ff_indices = generate_mock_data(code, name, days=10, num_fat_fingers=2)
        all_results.append({
            'code': code,
            'name': name,
            'records': len(df),
            'fat_fingers': len(ff_indices),
            'fat_finger_indices': list(ff_indices)
        })
    
    print("\n" + "="*50)
    print("📊 生成汇总")
    print("="*50)
    for r in all_results:
        print(f"{r['name']}: {r['records']}条记录, {r['fat_fingers']}个乌龙指")
        print(f"  乌龙指位置: {r['fat_finger_indices']}")
    
    print("\n🎯 模拟数据生成完成！")
    print("现在可以运行 04_乌龙指识别.py 来测试识别算法")