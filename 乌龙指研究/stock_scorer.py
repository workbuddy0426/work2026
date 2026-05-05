"""
第9课：多因子选股打分器
—— 给股票"期末考试"，自动排名
"""

import urllib.request
import json

# ===== 股票池（手动输入几只你感兴趣的） =====
stocks = [
    {"name": "贵州茅台", "code": "600519", "pe": 21, "pb": 8, "roe": 30},
    {"name": "腾讯控股", "code": "00700", "pe": 18, "pb": 4, "roe": 22},
    {"name": "小米集团", "code": "01810", "pe": 16, "pb": 3, "roe": 18},
    {"name": "捷佳伟创", "code": "300724", "pe": 15, "pb": 2.4, "roe": 2},
    {"name": "比亚迪",   "code": "002594", "pe": 25, "pb": 6, "roe": 15},
    {"name": "招商银行", "code": "600036", "pe": 7,  "pb": 0.9, "roe": 13},
]

def score_roe(roe):
    """ROE打分（满分40）"""
    if roe >= 30: return 40
    if roe >= 25: return 35
    if roe >= 20: return 30
    if roe >= 15: return 25
    if roe >= 10: return 18
    if roe >= 5:  return 10
    if roe > 0:   return 5
    return 0

def score_pe(pe):
    """PE打分（满分30）"""
    if pe <= 0:    return 0     # 亏损
    if pe <= 8:    return 28    # 非常便宜
    if pe <= 15:   return 25    # 便宜
    if pe <= 20:   return 20    # 合理
    if pe <= 30:   return 12    # 偏贵
    if pe <= 50:   return 5     # 贵
    return 0                     # 太贵

def score_pb(pb):
    """PB打分（满分15）"""
    if pb <= 0:    return 0
    if pb <= 1:    return 13    # 破净
    if pb <= 3:    return 12    # 合理偏低
    if pb <= 5:    return 8     # 合理偏高
    if pb <= 10:   return 5     # 偏贵
    return 2                     # 很贵

def score_momentum(mom):
    """动量打分（满分15）"""
    # mom是最近3个月涨跌幅百分比
    if mom > 30:   return 15
    if mom > 15:   return 13
    if mom > 5:    return 10
    if mom > -5:   return 8     # 横盘
    if mom > -15:  return 5     # 小幅下跌
    if mom > -30:  return 2     # 大跌
    return 0                     # 暴跌

# ===== 打分 =====
print("=" * 60)
print("📊 多因子选股评分报告")
print("=" * 60)
print(f"{'排名':<4} {'股票':<10} {'ROE分':<6} {'PE分':<6} {'PB分':<6} {'动量分':<6} {'总分':<6}")
print("-" * 60)

# 用模拟的动量数据（此处手动输入，第3课你学过怎么抓实时价格算动量）
momentum_data = {
    "600519": 8,    # 茅台最近3个月涨8%
    "00700": 5,     # 腾讯最近3个月涨5%
    "01810": 15,    # 小米最近3个月涨15%（汽车业务带飞）
    "300724": -20,  # 捷佳伟创最近3个月跌20%
    "002594": 12,   # 比亚迪最近3个月涨12%
    "600036": -3,   # 招商银行最近3个月跌3%
}

results = []
for s in stocks:
    roe_s = score_roe(s["roe"])
    pe_s = score_pe(s["pe"])
    pb_s = score_pb(s["pb"])
    mom_s = score_momentum(momentum_data.get(s["code"], 0))
    total = roe_s + pe_s + pb_s + mom_s
    results.append((total, s["name"], roe_s, pe_s, pb_s, mom_s))

# 按总分排名
results.sort(reverse=True)

for i, (total, name, rs, ps, pbs, ms) in enumerate(results, 1):
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "  ")
    print(f"{medal} {i:<3} {name:<10} {rs:<6} {ps:<6} {pbs:<6} {ms:<6} {total:<6}")

print("-" * 60)
print(f"\n评分标准：ROE(满分40) + PE(满分30) + PB(满分15) + 动量(满分15) = 100")
print(f"数据来源：手动输入（第10课会教你怎么自动抓取）")
