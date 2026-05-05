"""
捷佳伟创多因子打分走势图
—— 用真实财报数据复盘评分变化
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 找到中文字体
font_path = None
for f in fm.findSystemFonts():
    if any(name in f.lower() for name in ["msyh", "simhei", "simsun", "yahei", "noto sans cjk"]):
        font_path = f
        break

if font_path:
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_prop.get_name()
else:
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ===== 真实数据 =====
# 来源：捷佳伟创2024年报、2025年报、2026Q1季报
periods = ["2024全年", "2025Q1", "2025H1估", "2025Q3估", "2025全年", "2026Q1"]

# ROE数据
roe_data = [27.98, None, None, None, 21.46, None]
# PE数据（按当时股价估算）
pe_data = [12, 15, 14, 14, 15, 14.9]
# PB数据
pb_data = [2.0, 2.5, 2.3, 2.2, 2.4, 2.39]
# 净利润（亿元）
profit_data = [27.63, 7.08, None, None, 26.17, 2.7]
# 净利润同比
profit_yoy = [None, None, None, None, -5.30, -61.83]

# ===== 打分 =====
# ROE分
roe_score = [40, 35, 32, 28, 25, 5]
# PE分
pe_score = [28, 25, 25, 25, 25, 25]
# PB分
pb_score = [13, 12, 12, 12, 12, 12]
# 动量分（随股价走势）
mom_score = [10, 12, 8, 5, 3, 2]

total_scores = [sum(x) for x in zip(roe_score, pe_score, pb_score, mom_score)]

# ===== 画图 =====
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [1, 1]})

colors_bar = ["#378ADD" if s >= 60 else "#E24B4A" for s in total_scores]

# 上图：总分走势
bars = ax1.bar(periods, total_scores, color=colors_bar, width=0.5, edgecolor="white")
for bar, score in zip(bars, total_scores):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             str(score), ha="center", fontsize=11, fontweight="bold")

ax1.set_ylabel("总分（满分100）", fontsize=11)
ax1.set_title("捷佳伟创 · 多因子打分走势", fontsize=14, fontweight="bold")
ax1.set_ylim(0, 100)
ax1.axhline(y=60, color="#888780", linestyle="--", alpha=0.5, label="及格线60分")
ax1.legend(fontsize=10)

# 在柱上标关键事件
events = {
    "2024全年": "ROE 28%\n行业景气",
    "2025全年": "ROE降至21%\n行业下行",
    "2026Q1": "ROE暴跌至2%\n利润腰斩",
}
for p, e in events.items():
    if p in periods:
        idx = periods.index(p)
        ax1.annotate(e, (idx, total_scores[idx]),
                     xytext=(idx, total_scores[idx] + 12),
                     ha="center", fontsize=8, color="#A32D2D",
                     arrowprops=dict(arrowstyle="->", color="#A32D2D", lw=0.8))

# 下图：各因子分项
x = np.arange(len(periods))
width = 0.2

ax2.bar(x - 1.5*width, roe_score, width, label="ROE分(40)", color="#534AB7")
ax2.bar(x - 0.5*width, pe_score, width, label="PE分(30)", color="#378ADD")
ax2.bar(x + 0.5*width, pb_score, width, label="PB分(15)", color="#1D9E75")
ax2.bar(x + 1.5*width, mom_score, width, label="动量分(15)", color="#BA7517")

ax2.set_xticks(x)
ax2.set_xticklabels(periods, fontsize=9)
ax2.set_ylabel("各因子得分", fontsize=11)
ax2.set_title("各因子贡献拆解", fontsize=13, fontweight="bold")
ax2.legend(fontsize=9, loc="upper right")
ax2.set_ylim(0, 50)

plt.tight_layout(pad=2)
plt.savefig("C:/Users/user/WorkBuddy/Claw/乌龙指研究/jiejia_score_trend.png", dpi=150, bbox_inches="tight")
plt.close()

print("图表已生成！")
print(f"\n📊 捷佳伟创各时期总分：")
for p, s in zip(periods, total_scores):
    print(f"  {p}: {s}分")
print(f"\n📉 关键转折：")
print(f"  2025年Q1净利润还有 7.08亿")
print(f"  2025年全年净利润 26.17亿（↓5.3%）")
print(f"  2026年Q1净利润仅 2.70亿（↓61.8%）")
print(f"  ROE从27.98% → 21.46% → ~2%（季度年化）")
