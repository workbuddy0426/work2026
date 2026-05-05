"""
小乌：乌龙指信号识别算法 V2
功能：分析历史数据，识别潜在的乌龙指信号
优化：专门针对"瞬间偏离+快速回归"的特征
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import glob

DATA_DIR = "data"
RESULT_DIR = "results"
os.makedirs(RESULT_DIR, exist_ok=True)

def detect_fat_finger_v2(df, code, name):
    """
    识别乌龙指信号 V2
    
    判断标准：
    1. 当前价格相对前一分钟变化 > 阈值（如8%）
    2. 下一分钟价格回归到正常区间
    3. 成交量异常放大
    """
    
    # 参数设置
    PRICE_CHANGE_THRESHOLD = 0.08  # 单分钟价格变化8%
    RECOVERY_THRESHOLD = 0.05  # 1分钟内回归5%以内
    MIN_VOLUME = 300000  # 最小成交量30万
    
    signals = []
    
    # 计算价格变化率（相对前一分钟）
    df['price_change'] = df['close'].pct_change()
    df['price_change_abs'] = df['price_change'].abs()
    
    # 计算下一分钟的回归情况
    df['next_price'] = df['close'].shift(-1)
    df['next_change'] = (df['next_price'] - df['close']) / df['close']
    
    # 遍历寻找信号
    for i in range(1, len(df) - 1):
        # 条件1：当前分钟价格大幅变化
        price_change = df.iloc[i]['price_change_abs']
        if price_change < PRICE_CHANGE_THRESHOLD:
            continue
        
        # 条件2：下一分钟反向回归
        next_change = df.iloc[i]['next_change']
        # 如果当前是暴跌，下一分钟应该上涨；如果当前是暴涨，下一分钟应该下跌
        current_direction = np.sign(df.iloc[i]['price_change'])
        if current_direction * next_change < 0:  # 方向相反，说明回归
            recovery_good = True
        else:
            recovery_good = False
        
        if not recovery_good:
            continue
        
        # 条件3：成交量检查
        volume = df.iloc[i]['volume']
        if volume < MIN_VOLUME:
            continue
        
        # 发现乌龙指信号
        signal = {
            'code': code,
            'name': name,
            'time': df.iloc[i]['time'],
            'price': df.iloc[i]['close'],
            'prev_price': df.iloc[i-1]['close'],
            'price_change': df.iloc[i]['price_change'],
            'price_change_pct': f"{df.iloc[i]['price_change']*100:.2f}%",
            'next_price': df.iloc[i]['next_price'],
            'next_change': f"{next_change*100:.2f}%",
            'volume': volume,
            'direction': 'up' if df.iloc[i]['price_change'] > 0 else 'down',
            'is_true_fat_finger': df.iloc[i].get('is_fat_finger', False)  # 如果是模拟数据，检查是否真实植入
        }
        signals.append(signal)
    
    return signals

def analyze_all():
    """分析所有已下载的数据"""
    
    print("🎯 小乌开始扫描乌龙指信号（V2算法）...\n")
    
    # 查找所有数据文件
    patterns = [
        f"{DATA_DIR}/*_mock.csv",
        f"{DATA_DIR}/*_min.csv",
        f"{DATA_DIR}/*_daily.csv"
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))
    
    if not files:
        print("❌ 没有找到数据文件，请先运行数据下载/生成脚本")
        return
    
    all_signals = []
    
    for file in files:
        # 解析文件名获取code和name
        filename = os.path.basename(file)
        
        # 尝试提取code和name
        if '_mock.csv' in filename:
            parts = filename.replace('_mock.csv', '').split('_')
        elif '_min.csv' in filename:
            parts = filename.replace('_min.csv', '').split('_')
        elif '_daily.csv' in filename:
            parts = filename.replace('_daily.csv', '').split('_')
        else:
            continue
        
        if len(parts) >= 2:
            code = parts[0]
            name = '_'.join(parts[1:])
            
            try:
                df = pd.read_csv(file)
                signals = detect_fat_finger_v2(df, code, name)
                all_signals.extend(signals)
                
                # 统计真实乌龙指命中数（模拟数据）
                true_hits = sum(1 for s in signals if s.get('is_true_fat_finger'))
                
                print(f"✅ {name}: 发现 {len(signals)} 个信号", end="")
                if true_hits > 0:
                    print(f" (命中真实乌龙指: {true_hits}个)")
                else:
                    print()
                
            except Exception as e:
                print(f"❌ {name} 分析失败: {e}")
    
    # 保存结果
    if all_signals:
        signals_df = pd.DataFrame(all_signals)
        result_file = f"{RESULT_DIR}/fat_finger_signals_v2_{datetime.now().strftime('%Y%m%d')}.csv"
        signals_df.to_csv(result_file, index=False, encoding='utf-8-sig')
        
        print(f"\n📊 统计结果:")
        print(f"- 分析文件数: {len(files)}")
        print(f"- 总信号数: {len(all_signals)}")
        print(f"- 上涨信号: {len([s for s in all_signals if s['direction']=='up'])}")
        print(f"- 下跌信号: {len([s for s in all_signals if s['direction']=='down'])}")
        
        true_signals = [s for s in all_signals if s.get('is_true_fat_finger')]
        if true_signals:
            print(f"- 命中真实乌龙指: {len(true_signals)}个")
            accuracy = len(true_signals) / len(all_signals) * 100
            print(f"- 识别准确率: {accuracy:.1f}%")
        
        print(f"\n📁 详细结果已保存: {result_file}")
        
        # 显示前5个信号
        print("\n🔍 示例信号（前5个）:")
        display_cols = ['name', 'time', 'price_change_pct', 'next_change', 'direction']
        print(signals_df[display_cols].head().to_string(index=False))
        
    else:
        print("\n⚠️ 未发现乌龙指信号")
        print("建议:")
        print("1. 调整阈值参数（当前: 单分钟变化8%）")
        print("2. 下载更多历史数据")
        print("3. 检查数据质量")

if __name__ == "__main__":
    analyze_all()