"""VWAP vs TWAP 执行算法对比"""
import numpy as np

print("=" * 60)
print("VWAP vs TWAP 执行算法 模拟对比")
print("=" * 60)

np.random.seed(42)
minutes = 240  # 一天240分钟

# A股成交量曲线: 开盘高+尾盘高
vol = np.zeros(minutes)
vol[:30] = 0.08 + 0.04 * (1 - np.arange(30)/30)
vol[30:120] = 0.05
vol[120:210] = 0.04
vol[210:] = 0.10 + 0.05 * (1 - np.arange(30)/30)
vol = vol / vol.sum()

# 价格模拟 (随机游走)
np.random.seed(123)
price = 100.0
prices = []
for i in range(minutes):
    price *= (1 + np.random.normal(0, 0.0005))
    prices.append(price)
prices = np.array(prices)

total = 100000  # 10万股

# 一次性买入 (开盘价)
lump_p = prices[0]

# TWAP: 时间加权平均价 (每分钟等量)
twap_avg = np.mean(prices)

# VWAP: 成交量加权平均价 (按成交量比例)
vwap_per_min = vol * total
vwap_avg = np.sum(prices * vwap_per_min) / total

# 输出结果
print()
print(f"订单: 10万股 (约1000万元)")
print(f"开盘价: {prices[0]:.2f}  收盘价: {prices[-1]:.2f}  均价: {np.mean(prices):.2f}")
print()
print("策略         均价    比开盘      比均价")
print("-" * 42)
print(f"一次性买入   {lump_p:>8.2f}  {0:>+8.2f}    {np.mean(prices)-lump_p:>+8.2f}")
print(f"TWAP         {twap_avg:>8.2f}  {twap_avg-lump_p:>+8.2f}    {0:>+8.2f}")
print(f"VWAP         {vwap_avg:>8.2f}  {vwap_avg-lump_p:>+8.2f}    {vwap_avg-np.mean(prices):>+8.2f}")
print()
twap_vwap_diff = (twap_avg - vwap_avg) * 10000
print(f"TWAP vs VWAP 价差: {twap_vwap_diff:.1f} bp")
print()

# 解释
print("解读:")
print("* TWAP = 不分时间段, 每分钟下一样的量")
print("  -> 均价 = 全天所有分钟价格的算术平均")
print("* VWAP = 成交量大的时段多下, 成交量小的时段少下")
print("  -> 早盘30分钟下约25%, 尾盘30分钟下约30%")
print("  -> 午盘40分钟(11:00-11:30 + 13:00-13:30)一共只下10%")
print("* 机构用VWAP, 因为顺应流动性, 冲击成本更低")
print()
print("给你的建议:")
print("  < 50万: 直接一次性, 省心")
print("  50万~200万: TWAP分5-10笔, 每10分钟一笔")
print("  > 200万: 用VWAP策略, 按成交量分布下单")
print("  或者14:30-14:57集中下单 (A股尾盘流动性最佳)")
