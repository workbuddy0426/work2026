#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取真实可转债数据
尝试多种数据源：AKShare分钟数据、日线数据
"""
import pandas as pd
import numpy as np
import akshare as ak
import os
import sys
import time
from datetime import datetime, timedelta

def test_akshare_minute():
    """测试AKShare分钟数据接口"""
    print("🎯 测试AKShare可转债分钟数据...")
    try:
        # 尝试获取一只可转债的分钟数据（如128136立讯转债）
        df = ak.bond_zh_hs_cov_min(symbol="sz128136", period="1", adjust="")
        if df is not None and not df.empty:
            print(f"✅ 成功获取分钟数据，形状: {df.shape}")
            print(df.head())
            return df
        else:
            print("❌ 数据为空")
    except Exception as e:
        print(f"❌ AKShare分钟数据接口错误: {e}")
    return None

def test_akshare_daily():
    """测试AKShare日线数据接口"""
    print("🎯 测试AKShare可转债日线数据...")
    try:
        # 获取可转债日线数据
        df = ak.bond_zh_hs_cov_daily(symbol="sz128136")
        if df is not None and not df.empty:
            print(f"✅ 成功获取日线数据，形状: {df.shape}")
            print(df.head())
            return df
        else:
            print("❌ 数据为空")
    except Exception as e:
        print(f"❌ AKShare日线数据接口错误: {e}")
    return None

def test_akshare_spot():
    """测试实时行情"""
    print("🎯 测试可转债实时行情...")
    try:
        df = ak.bond_zh_hs_cov_spot()
        if df is not None and not df.empty:
            print(f"✅ 成功获取实时行情，形状: {df.shape}")
            print(f"共{len(df)}只可转债")
            print(df[['代码', '名称', '最新价', '涨跌幅', '成交额']].head())
            return df
        else:
            print("❌ 数据为空")
    except Exception as e:
        print(f"❌ AKShare实时行情错误: {e}")
    return None

def main():
    print("=" * 60)
    print("🔄 开始测试真实数据获取")
    print("=" * 60)
    
    # 1. 测试实时行情
    spot_df = test_akshare_spot()
    
    # 2. 测试日线数据
    daily_df = test_akshare_daily()
    
    # 3. 测试分钟数据
    minute_df = test_akshare_minute()
    
    print("=" * 60)
    print("📊 测试结果汇总:")
    print(f"实时行情: {'✅' if spot_df is not None else '❌'}")
    print(f"日线数据: {'✅' if daily_df is not None else '❌'}")
    print(f"分钟数据: {'✅' if minute_df is not None else '❌'}")
    
    # 建议下一步
    print("\n💡 建议:")
    if minute_df is not None:
        print("- 使用AKShare分钟数据进行回测（数据可能有限）")
    elif daily_df is not None:
        print("- 使用日线数据识别大幅波动日（精度较低）")
    else:
        print("- 考虑其他数据源：Tushare Pro、聚宽、券商API")
    
    # 保存样例数据
    if daily_df is not None:
        os.makedirs("data", exist_ok=True)
        daily_df.to_csv("data/sz128136_daily_sample.csv", index=False, encoding='utf-8-sig')
        print(f"\n📁 日线样例已保存: data/sz128136_daily_sample.csv")
    
    print("=" * 60)

if __name__ == "__main__":
    main()