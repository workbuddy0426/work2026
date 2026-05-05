"""
小乌：下载可转债基础数据
功能：获取当前所有可转债的代码、名称、成交额等信息
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import os

# 创建数据目录
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def download_cb_basic():
    """下载可转债基础信息"""
    print("🎯 小乌正在获取可转债基础数据...")
    
    try:
        # 获取可转债实时行情（使用bond_zh_hs_cov_spot接口）
        df = ak.bond_zh_hs_cov_spot()
        
        print(f"✅ 共获取 {len(df)} 只可转债")
        
        # 查看列名
        print(f"\n📋 数据列: {list(df.columns)}")
        
        # 重命名列（根据实际列名调整）
        column_mapping = {}
        
        # 尝试匹配常见列名
        if 'symbol' in df.columns:
            column_mapping['symbol'] = 'code'
        if 'name' in df.columns:
            column_mapping['name'] = 'name'
        if 'amount' in df.columns:
            column_mapping['amount'] = 'volume'
        if 'volume' in df.columns and 'amount' not in df.columns:
            column_mapping['volume'] = 'volume'
        if 'changepercent' in df.columns:
            column_mapping['changepercent'] = 'change_pct'
        if 'trade' in df.columns:
            column_mapping['trade'] = 'price'
            
        if column_mapping:
            df = df.rename(columns=column_mapping)
        
        # 确保volume是数值型
        if 'volume' in df.columns:
            df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
            
            # 筛选高流动性品种（日均成交额>1亿）
            # 注意：amount字段可能是成交额，volume是成交量
            df_filtered = df[df['volume'] > 100000000].copy()
            
            print(f"✅ 筛选出 {len(df_filtered)} 只高流动性品种（成交额>1亿）")
        else:
            df_filtered = df.copy()
            print("⚠️ 未找到成交额字段，返回全部数据")
        
        # 保存数据
        today = datetime.now().strftime('%Y%m%d')
        filename = f"{DATA_DIR}/cb_list_{today}.csv"
        df_filtered.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ 数据已保存: {filename}")
        
        # 显示前10
        print("\n📊 Top 10 可转债:")
        display_cols = ['code', 'name']
        if 'volume' in df_filtered.columns:
            display_cols.append('volume')
        if 'change_pct' in df_filtered.columns:
            display_cols.append('change_pct')
        if 'price' in df_filtered.columns:
            display_cols.append('price')
            
        top10 = df_filtered.head(10)[display_cols]
        print(top10.to_string(index=False))
        
        return df_filtered
        
    except Exception as e:
        print(f"❌ 出错了: {e}")
        print("尝试备用接口...")
        
        try:
            # 备用接口：获取可转债一览表
            df = ak.bond_cb_redeem_jsl()
            print(f"✅ 备用接口获取 {len(df)} 只可转债")
            
            today = datetime.now().strftime('%Y%m%d')
            filename = f"{DATA_DIR}/cb_list_{today}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            print(f"✅ 数据已保存: {filename}")
            print("\n📊 Top 10:")
            print(df.head(10).to_string(index=False))
            
            return df
            
        except Exception as e2:
            print(f"❌ 备用接口也失败: {e2}")
            return None

if __name__ == "__main__":
    df = download_cb_basic()
    if df is not None:
        print("\n🎯 小乌：基础数据下载完成！")
    else:
        print("\n❌ 数据下载失败，请检查网络或AKShare版本")