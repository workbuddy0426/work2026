"""
小乌：下载可转债历史数据
功能：获取指定可转债的历史K线数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import os
import time

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def download_daily_data(code, name, start_date=None, end_date=None):
    """
    下载单只可转债的历史日线数据
    
    参数:
        code: 可转债代码（如 '128136'）
        name: 可转债名称
        start_date: 开始日期 '20240101'
        end_date: 结束日期 '20241231'
    """
    print(f"📥 正在下载 {name}({code}) 的历史数据...")
    
    try:
        # 获取日线数据（AKShare的分钟数据接口有限制，先用日线演示）
        # 实际生产环境需要用付费数据源或券商API
        df = ak.bond_zh_hs_cov_daily(symbol=code)
        
        if df.empty:
            print(f"⚠️ {name} 无数据")
            return None
        
        # 标准化列名
        df.columns = [col.lower() for col in df.columns]
        
        # 保存数据
        filename = f"{DATA_DIR}/{code}_{name}_daily.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ {name}: 下载了 {len(df)} 条记录")
        return df
        
    except Exception as e:
        print(f"❌ {name} 下载失败: {e}")
        return None

def download_batch(codes_df, max_count=10):
    """
    批量下载多只可转债的数据
    
    参数:
        codes_df: 包含code和name的DataFrame
        max_count: 最多下载多少只（避免请求过多）
    """
    print(f"\n🎯 小乌开始批量下载，计划下载 {min(max_count, len(codes_df))} 只可转债...\n")
    
    results = []
    for idx, row in codes_df.head(max_count).iterrows():
        # 适配不同数据源的可能列名
        code = row.get('code') or row.get('代码') or row.get('symbol')
        name = row.get('name') or row.get('名称') or row.get('债券简称')
        
        if pd.isna(code) or pd.isna(name):
            continue
            
        df = download_daily_data(str(code), str(name))
        if df is not None:
            results.append({
                'code': code,
                'name': name,
                'records': len(df)
            })
        
        # 添加延迟，避免请求过快
        time.sleep(0.5)
    
    # 保存下载记录
    if results:
        summary_df = pd.DataFrame(results)
        summary_file = f"{DATA_DIR}/download_summary_{datetime.now().strftime('%Y%m%d')}.csv"
        summary_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ 批量下载完成！共成功 {len(results)} 只")
        print(f"📁 下载记录已保存: {summary_file}")
    else:
        print("\n⚠️ 没有成功下载任何数据")
    
    return results

if __name__ == "__main__":
    # 先运行02脚本获取列表，或者手动指定要下载的代码
    
    # 方式1：读取已保存的列表
    try:
        list_files = [f for f in os.listdir(DATA_DIR) if f.startswith('cb_list_')]
        if list_files:
            latest_list = sorted(list_files)[-1]
            cb_df = pd.read_csv(f"{DATA_DIR}/{latest_list}")
            print(f"📂 读取列表: {latest_list}")
            
            # 筛选剩余规模适中的（避免强赎风险）
            if '剩余规模' in cb_df.columns:
                cb_df = cb_df[cb_df['剩余规模'] > 0.5]  # 剩余规模大于0.5亿
                print(f"📊 筛选后剩余 {len(cb_df)} 只")
            
            download_batch(cb_df, max_count=10)
        else:
            print("❌ 没有找到可转债列表，请先运行 02_下载可转债列表.py")
    except Exception as e:
        print(f"❌ 出错了: {e}")