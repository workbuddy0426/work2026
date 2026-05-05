const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "运营";
pres.title = "第2章 量化交易中的统计模型与方法";

const C = {
  primary: "1E2761", secondary: "3B82F6", accent: "F59E0B",
  dark: "0F172A", white: "FFFFFF", light: "F1F5F9",
  text: "1E293B", muted: "64748B", cardBg: "F8FAFC",
  border: "E2E8F0", purple: "7C3AED", teal: "0D9488",
  red: "EF4444", green: "10B981", amber: "D97706",
};

const FT = "Arial Black"; const FB = "Calibri";
const mkShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });

function addHeader(s, title, subtitle) {
  s.background = { color: C.white };
  s.addText(title, { x: 0.6, y: 0.2, w: 8.8, h: 0.5, fontSize: 20, fontFace: FT, color: C.text, margin: 0 });
  if (subtitle) s.addText(subtitle, { x: 0.6, y: 0.65, w: 8.8, h: 0.25, fontSize: 10, fontFace: FB, color: C.muted, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.9, w: 1.0, h: 0.03, fill: { color: C.primary } });
}

function addCard(s, x, y, w, h, color, items, title, opts) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.cardBg }, shadow: mkShadow(), line: { color: C.border, width: 0.5 } });
  if (color) s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.06, fill: { color } });
  if (title) s.addText(title, { x: x + 0.1, y: y + 0.15, w: w - 0.2, h: 0.35, fontSize: 11, fontFace: FB, color: C.text, bold: true, margin: 0 });
  if (items) {
    const txt = items.map((t, j) => ({ text: t, options: { bullet: !opts?.noBullet, breakLine: j < items.length - 1, fontSize: opts?.fs || 10, color: C.text, paraSpaceAfter: 4 } }));
    s.addText(txt, { x: x + 0.1, y: y + (title ? 0.55 : 0.15), w: w - 0.2, h: h - (title ? 0.7 : 0.3), fontFace: FB, valign: "top", margin: 0 });
  }
}

// ===== S1: Title =====
let s1 = pres.addSlide(); s1.background = { color: C.dark };
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s1.addText("第2章", { x: 0.8, y: 0.8, w: 8.4, h: 0.5, fontSize: 16, fontFace: FB, color: C.accent, margin: 0 });
s1.addText("量化交易中的统计模型与方法", { x: 0.8, y: 1.3, w: 8.4, h: 1.0, fontSize: 28, fontFace: FT, color: C.white, margin: 0 });
s1.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 2.4, w: 1.8, h: 0.04, fill: { color: C.accent } });
s1.addText("股票价格特征 · 布朗运动 · 现代投资组合理论\nCAPM → 多因子 · ARIMA/GARCH/鞅回归 · NPEB\n动量 · 配对交易 · 逆向投资 · 价值投资 · 策略评估", {
  x: 0.8, y: 2.7, w: 8.4, h: 1.5, fontSize: 13, fontFace: FB, color: C.white, margin: 0, lineSpacingMultiple: 1.5
});

// ===== S2: Overview =====
let s2 = pres.addSlide();
addHeader(s2, "本章结构", "完整版 · 共14页详细讲解");
const secs = [
  { num: "2.1-2.2", title: "股票价格特征", desc: "非正态分布/波动率集聚\n布朗运动/随机游走", color: C.primary },
  { num: "2.3-2.4", title: "CAPM到多因子", desc: "CAPM→Fama-French→\nCarhart四因子→Black-Litterman", color: C.secondary },
  { num: "2.5-2.7", title: "NPEB+鞅回归", desc: "参数不确定性处理\nARIMA/GARCH/鞅回归模型演进", color: C.purple },
  { num: "2.8", title: "五大统计套利策略", desc: "动量/配对/逆向/价值/宏观\n样本内外评估方法", color: C.teal },
];
secs.forEach((s, i) => {
  const x = 0.3 + i * 2.4;
  s2.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.2, h: 2.5, fill: { color: C.cardBg }, shadow: mkShadow(), line: { color: C.border, width: 0.5 } });
  s2.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.2, h: 0.06, fill: { color: s.color } });
  s2.addText(s.num, { x: x + 0.1, y: 1.3, w: 2.0, h: 0.3, fontSize: 10, fontFace: FB, color: s.color, bold: true, margin: 0 });
  s2.addText(s.title, { x: x + 0.1, y: 1.6, w: 2.0, h: 0.4, fontSize: 12, fontFace: FB, color: C.text, bold: true, margin: 0 });
  s2.addText(s.desc, { x: x + 0.1, y: 2.1, w: 2.0, h: 1.2, fontSize: 10, fontFace: FB, color: C.muted, margin: 0, lineSpacingMultiple: 1.5 });
});

// ===== S3: Stock Price Features =====
let s3 = pres.addSlide();
addHeader(s3, "2.1 股票价格四大特征", "原书p.17-19");
const features = [
  { title: "非正态分布", color: C.red, items: ["尖峰厚尾 (Fat Tails)","极端值比正态预期更多","「黑天鹅」事件更常发生"] },
  { title: "波动率集聚", color: C.secondary, items: ["大波动之后跟着大波动","平静之后跟着平静","这正是GARCH模型要刻画的"] },
  { title: "收益自相关", color: C.teal, items: ["短期轻微正相关(趋势)","长期负相关(均值回归)","动量和逆向策略的根源"] },
  { title: "价格跳跃", color: C.amber, items: ["价格不是连续变动的","消息冲击导致不连续跳跃","建模时需区分跳跃和波动"] },
];
features.forEach((f, i) => {
  const x = 0.3 + i * 2.4;
  s3.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 2.2, h: 2.6, fill: { color: C.cardBg }, shadow: mkShadow(), line: { color: C.border, width: 0.5 } });
  s3.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 2.2, h: 0.45, fill: { color: f.color } });
  s3.addText(f.title, { x: x + 0.1, y: 1.25, w: 2.0, h: 0.35, fontSize: 13, fontFace: FB, color: C.white, bold: true, margin: 0 });
  const items = f.items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < f.items.length - 1, fontSize: 11, color: C.text, paraSpaceAfter: 6 } }));
  s3.addText(items, { x: x + 0.1, y: 1.85, w: 2.0, h: 1.7, fontFace: FB, valign: "top", margin: 0 });
});
s3.addText("原书引用Lai和Xing(2008)前六章结论 · 高频数据离散化价格变动(2.1.2节)", {
  x: 0.6, y: 4.8, w: 8.8, h: 0.3, fontSize: 9, fontFace: FB, color: C.muted, italic: true, margin: 0
});

// ===== S4: Brownian Motion =====
let s4 = pres.addSlide();
addHeader(s4, "2.2 布朗运动与随机游走", "Bachelier(1900)博士论文《投机理论》· 原书p.20");
addCard(s4, 0.3, 1.1, 3.0, 1.8, C.amber, ["Louis Bachelier在巴黎-索邦大学研究","巴黎证交所债券价格变动规律","结论：价格变动完全随机","比爱因斯坦研究布朗运动早5年","但当时没人在意..."], "📜 1900年巴黎：一个被忽视的发现", { fs: 10 });
addCard(s4, 3.5, 1.1, 3.0, 1.8, "6366F1", ["1827年植物学家Robert Brown发现","花粉颗粒在水中无规则乱跳","1905年爱因斯坦用数学解释","→ 被无数水分子随机撞击的结果"], "物理上的布朗运动", { fs: 10 });
addCard(s4, 6.7, 1.1, 3.0, 1.8, "3B82F6", ["Bachelier将布朗运动引入金融","证券价格每一步随机","向上或向下概率相等","无法预测下一步方向","→ 有效市场假说的数学基础"], "金融上的随机游走", { fs: 10 });
s4.addText("随机游走 → 如果市场有效，技术分析没用，主动管理没用，买指数就够了。但2.8节会告诉你：存在可被利用的统计规律。", {
  x: 0.6, y: 4.5, w: 8.8, h: 0.8, fontSize: 11, fontFace: FB, color: C.red, margin: 0
});

// ===== S5: CAPM =====
let s5 = pres.addSlide();
addHeader(s5, "2.3 CAPM：最早的定价模型", "Sharpe(1964) · 资本资产定价模型 · 原书p.21-22");
s5.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 9.0, h: 0.6, fill: { color: "EEEDFE" }, line: { color: C.primary, width: 0.5 } });
s5.addText("E(Rᵢ) = R_f + βᵢ × (E(R_m) - R_f)", {
  x: 0.7, y: 1.15, w: 8.6, h: 0.5, fontSize: 14, fontFace: "Consolas", color: C.red, align: "center", valign: "middle", margin: 0
});
addCard(s5, 0.3, 2.0, 2.2, 1.2, "3B82F6", ["存银行/买国债的收益","在中国≈2%（国债利率）","基准收益"], "R_f 无风险利率", { fs: 10 });
addCard(s5, 2.7, 2.0, 2.2, 1.2, "EF4444", ["股票跟大盘的同步程度","β=1 → 和大盘同涨同跌","β=1.2 → 比大盘波动大20%"], "β 贝塔系数", { fs: 10 });
addCard(s5, 5.1, 2.0, 2.2, 1.2, "10B981", ["股市比存银行多赚多少","历史≈6%（美股）","是承担风险的回报"], "E(R_m)-R_f 市场溢价", { fs: 10 });
addCard(s5, 7.5, 2.0, 2.2, 1.2, "D97706", ["综合以上得出的合理回报","CAPM说这就是应有的收益","超额收益部分叫α"], "E(Rᵢ) 预期收益", { fs: 10 });
s5.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.5, w: 9.0, h: 0.8, fill: { color: "F1F5F9" } });
s5.addText("📊 实例：假设R_f=2%（国债），β=1.2（茅台比大盘波动大20%），市场溢价=6% → 茅台预期收益 = 2% + 1.2×6% = 9.2%", {
  x: 0.7, y: 3.55, w: 8.6, h: 0.35, fontSize: 11, fontFace: FB, color: C.text, margin: 0
});
s5.addText("问题是：CAPM只有一个因子 → 解释不了小盘股跑赢、价值股跑赢的现象", {
  x: 0.7, y: 3.95, w: 8.6, h: 0.3, fontSize: 11, fontFace: FB, color: C.red, margin: 0
});

// ===== S5.5: Markowitz Core Problem =====
let s55 = pres.addSlide();
addHeader(s55, "Markowitz均值-方差的致命问题", "原书2.3-2.4节 · 所有后续方法都是为了解决它");
addCard(s55, 0.3, 1.1, 6.0, 0.8, "3B82F6", ["Markowitz(1952)把选股变成了数学优化：给定风险找最大收益组合","核心输入：预期收益 + 方差(风险) + 相关系数 → 算出最优权重"], "Markowitz的贡献", { fs: 10 });
s55.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.1, w: 9.0, h: 0.6, fill: { color: "FEF2F2" }, line: { color: C.red, width: 0.5 } });
s55.addText("但问题来了——输入参数极度敏感！用2024年数据算的\"最优组合\"，换成2025年数据就完全不一样。预期收益微调0.5%，权重从50%变成80%。", {
  x: 0.7, y: 2.15, w: 8.6, h: 0.5, fontSize: 11, fontFace: FB, color: C.red, margin: 0
});
addCard(s55, 0.3, 2.9, 2.9, 1.5, "10B981", ["股票A 50%","股票B 30%","股票C 20%"], "用2024年数据", { fs: 11, noBullet: true });
addCard(s55, 3.4, 2.9, 2.9, 1.5, "D97706", ["股票A 10%","股票B 60%","股票C 30%"], "用2025年数据", { fs: 11, noBullet: true });
addCard(s55, 6.5, 2.9, 3.2, 1.5, "EF4444", ["股票A 80%","股票B -10%（做空）","股票C 30%"], "收益微调0.5%", { fs: 11, noBullet: true });
s55.addText("所以后续所有方法（2.4.2-2.5节）都是为了解决这个问题", { x: 0.6, y: 4.6, w: 8.8, h: 0.4, fontSize: 11, fontFace: FB, color: C.primary, bold: true, margin: 0 });

// ===== S6: Fama-French =====
let s6 = pres.addSlide();
addHeader(s6, "2.4.1 Fama-French三因子模型(1993)", "原书p.23 · 为什么一个因子不够？");
s6.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 9.0, h: 0.5, fill: { color: "FEF2F2" }, line: { color: C.red, width: 0.5 } });
s6.addText("CAPM解决不了的两个谜题：①小盘股长期跑赢大盘股，β却没高多少 ②价值股跑赢成长股，β也解释不了", {
  x: 0.7, y: 1.15, w: 8.6, h: 0.4, fontSize: 10, fontFace: FB, color: C.red, margin: 0
});
s6.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.8, w: 9.0, h: 0.6, fill: { color: "EEEDFE" }, line: { color: C.primary, width: 0.5 } });
s6.addText("Rᵢ - R_f = β₁(R_m - R_f) + β₂×SMB + β₃×HML + α", {
  x: 0.7, y: 1.85, w: 8.6, h: 0.5, fontSize: 13, fontFace: "Consolas", color: C.primary, align: "center", valign: "middle", margin: 0
});
addCard(s6, 0.3, 2.7, 3.0, 1.7, "3B82F6", ["和CAPM一样","全市场的超额收益","描述：大盘涨跌对你的影响"], "MKT 市场因子", { fs: 10 });
addCard(s6, 3.5, 2.7, 3.0, 1.7, "10B981", ["Small Minus Big","小盘股收益 - 大盘股收益","小盘股年化跑赢约3-5%","承担了额外流动风险"], "SMB 规模因子", { fs: 10 });
addCard(s6, 6.7, 2.7, 3.0, 1.7, "D97706", ["High Minus Low","高账面市值比-低账面市值比","价值股年化跑赢约4-6%","低PE/PB的长期溢价"], "HML 价值因子", { fs: 10 });

// ===== S7: Carhart + Alpha =====
let s7 = pres.addSlide();
addHeader(s7, "Carhart四因子(1997) + α的意义", "原书p.23 · 与你第9课打分器的关系");
addCard(s7, 0.3, 1.1, 2.15, 1.0, "3B82F6", ["大盘涨跌"], "MKT 市场", { fs: 10, noBullet: true });
addCard(s7, 2.6, 1.1, 2.15, 1.0, "10B981", ["大盘 vs 小盘"], "SMB 规模", { fs: 10, noBullet: true });
addCard(s7, 4.9, 1.1, 2.15, 1.0, "D97706", ["价值 vs 成长"], "HML 价值", { fs: 10, noBullet: true });
addCard(s7, 7.2, 1.1, 2.5, 1.0, "7C3AED", ["过去涨 vs 过去跌"], "MOM 动量", { fs: 10, noBullet: true });
s7.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.3, w: 9.0, h: 0.5, fill: { color: "EEEDFE" }, line: { color: C.primary, width: 0.5 } });
s7.addText("Rᵢ - R_f = β₁MKT + β₂SMB + β₃HML + β₄MOM + α", {
  x: 0.7, y: 2.35, w: 8.6, h: 0.4, fontSize: 12, fontFace: "Consolas", color: C.primary, align: "center", valign: "middle", margin: 0
});
addCard(s7, 0.3, 3.0, 4.3, 1.5, "10B981", ["四因子都解释不了的超额收益","α > 0 → 基金经理真的有选股能力","α ≈ 0 → 收益来自因子暴露（运气）","没有α的策略，大盘跌时扛不住"], "α（阿尔法）：真正的本事", { fs: 10 });
addCard(s7, 4.8, 3.0, 4.9, 1.5, "D97706", ["你的stock_scorer.py用4个维度打分：","ROE分(40) + PE分(30) + PB分(15) + 动量分(15)","与四因子模型逻辑相通：","PE/PB→价值因子Roe→盈利质量 动量→MOM"], "跟你的打分器对比", { fs: 10 });

// ===== S7.5: Four Solutions =====
let s75 = pres.addSlide();
addHeader(s75, "2.4.2-2.5 四种解决方法", "核心目标：让最优组合不因微小参数变化而剧烈变动");
addCard(s75, 0.3, 1.1, 3.0, 1.5, "6366F1", ["把极端估计往均值方向\"拉\"","Shrinkage Estimator = α×原始+(1-α)×全局均值","例：股票历史收益30%→缩减后20%","以降低极端值的影响力"], "① 缩减技术(Shrinkage)", { fs: 10 });
addCard(s75, 3.5, 1.1, 3.0, 1.5, "3B82F6", ["先验信念 + 数据 = 后验估计","先猜一个大概（先验）","用数据修正这个猜想","结果不会太离谱"], "② 贝叶斯方法(Bayesian)", { fs: 10 });
addCard(s75, 6.7, 1.1, 3.0, 1.5, "10B981", ["第①步：从市场均衡反推预期收益","第②步：加入投资者主观观点","第③步：贝叶斯融合两者","结果比Markowitz稳健得多"], "③ Black-Litterman ★", { fs: 10 });
addCard(s75, 0.3, 2.9, 3.0, 1.5, "D97706", ["从历史数据有放回地反复抽样","每次抽一个Bootstrap样本","每个样本算一次最优组合","1000次结果取平均"], "④ Bootstrap方法", { fs: 10 });
addCard(s75, 3.5, 2.9, 3.0, 1.5, "7C3AED", ["在Bootstrap基础上加入NPEB法则","自动惩罚\"只在某些样本最优\"的极端权重","样本外表现优于传统方法","本书重要理论贡献"], "⑤ NPEB新方法 ★★", { fs: 10 });
s75.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 4.6, w: 9.0, h: 0.5, fill: { color: "1E293B" } });
s75.addText("演进路线：Shrinkage → Bayesian → Black-Litterman → Bootstrap → NPEB（越来越复杂，也越来越稳健）", { x: 0.7, y: 4.65, w: 8.6, h: 0.4, fontSize: 10, fontFace: FB, color: C.white, valign: "middle", margin: 0 });

// ===== S7.6: Black-Litterman + NPEB Detail =====
let s76 = pres.addSlide();
addHeader(s76, "Black-Litterman + NPEB 详解", "原书2.4.2节(Black-Litterman) · 2.5节(NPEB)");
addCard(s76, 0.3, 1.1, 4.3, 1.6, "10B981", ["第①步：从市场均衡反推预期收益——\"如果市场有效，当前价格隐含了什么收益？\"","第②步：加入你的主观观点——\"茅台ROE会提升\"或\"芯片股估值过高\"","第③步：贝叶斯融合——有信心→观点权重大，没把握→均衡权重大","结果：不会出现极端权重，比纯Markowitz实用得多"], "Black-Litterman 三步走", { fs: 10 });
addCard(s76, 4.8, 1.1, 4.9, 1.6, "7C3AED", ["第一步：从历史数据中有放回地抽取1000个Bootstrap样本","第二步：对每个样本算一个\"最优组合\"→得到1000组不同权重","第三步：取1000组权重的平均值→自动惩罚不稳定极端权重","加上时间序列效应后→新现代投资组合理论(2.7节)"], "NPEB（非参数经验贝叶斯）", { fs: 10 });
s76.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.0, w: 9.0, h: 1.5, fill: { color: "F1F5F9" } });
s76.addText("2.7 新现代投资组合理论", { x: 0.7, y: 3.1, w: 8.6, h: 0.35, fontSize: 12, fontFace: FB, color: C.primary, bold: true, margin: 0 });
s76.addText("2.7.1 在NPEB中加入时间序列效应 → 联合建模", { x: 0.7, y: 3.5, w: 8.6, h: 0.3, fontSize: 10, fontFace: FB, color: C.text, margin: 0 });
s76.addText("2.7.2 在有效前沿上找最优信息比率（不再是单纯的均值-方差）", { x: 0.7, y: 3.8, w: 8.6, h: 0.3, fontSize: 10, fontFace: FB, color: C.text, margin: 0 });
s76.addText("2.7.3 实证检验：新方法在样本外表现优于传统ARIMA+GARCH分开建模", { x: 0.7, y: 4.1, w: 8.6, h: 0.3, fontSize: 10, fontFace: FB, color: C.red, margin: 0 });

// ===== S7.7: Complete Timeline =====
let s77 = pres.addSlide();
s77.background = { color: C.dark };
s77.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s77.addText("第2章 完整时间线", { x: 0.6, y: 0.3, w: 8.8, h: 0.5, fontSize: 22, fontFace: FT, color: C.white, margin: 0 });
s77.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.8, w: 1.5, h: 0.04, fill: { color: C.accent } });
const leftItems = [
  { year: "1900", event: "Bachelier 布朗运动/随机游走", note: "巴黎证交所" },
  { year: "1960s", event: "随机游走模型定型", note: "有效市场假说基石" },
  { year: "1970s", event: "Box-Jenkins ARIMA", note: "用过去预测未来" },
  { year: "1982", event: "Engle ARCH → GARCH", note: "2003诺贝尔奖·猜波动率" },
  { year: "2000s", event: "鞅回归模型", note: "均值+方差联合建模" },
  { year: "近年", event: "NPEB + 鞅回归 ★", note: "本书重要贡献" },
];
const rightItems = [
  { year: "1952", event: "Markowitz均值-方差", note: "开创性但参数敏感" },
  { year: "1964", event: "Sharpe CAPM", note: "β和市场定价" },
  { year: "1990s", event: "Black-Litterman", note: "均衡+观点融合" },
  { year: "1993", event: "Fama-French三因子", note: "MKT+SMB+HML" },
  { year: "1997", event: "Carhart四因子", note: "+MOM动量因子" },
  { year: "2000s", event: "Shrinkage/Bootstrap", note: "解决参数敏感问题" },
];
s77.addText("时间序列模型", { x: 1.5, y: 1.0, w: 3, h: 0.3, fontSize: 11, fontFace: FB, color: "3B82F6", margin: 0 });
s77.addText("投资组合理论", { x: 5.5, y: 1.0, w: 3, h: 0.3, fontSize: 11, fontFace: FB, color: "D97706", margin: 0 });
leftItems.forEach((item, i) => {
  const y = 1.4 + i * 0.65;
  s77.addText(`● ${item.year}`, { x: 0.5, y, w: 0.8, h: 0.25, fontSize: 8, fontFace: FB, color: "3B82F6", bold: true, margin: 0 });
  s77.addText(item.event, { x: 1.3, y, w: 2.8, h: 0.25, fontSize: 8, fontFace: FB, color: C.white, margin: 0 });
  s77.addText(item.note, { x: 1.3, y: y + 0.25, w: 2.8, h: 0.2, fontSize: 7, fontFace: FB, color: "64748B", margin: 0 });
});
rightItems.forEach((item, i) => {
  const y = 1.4 + i * 0.65;
  s77.addText(`● ${item.year}`, { x: 4.5, y, w: 0.8, h: 0.25, fontSize: 8, fontFace: FB, color: "D97706", bold: true, margin: 0 });
  s77.addText(item.event, { x: 5.3, y, w: 3.0, h: 0.25, fontSize: 8, fontFace: FB, color: C.white, margin: 0 });
  s77.addText(item.note, { x: 5.3, y: y + 0.25, w: 3.0, h: 0.2, fontSize: 7, fontFace: FB, color: "64748B", margin: 0 });
});
s77.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 5.0, w: 9.0, h: 0.4, fill: { color: "1E2761" } });
s77.addText("两条线在NPEB汇合 → 你的spread_monitor(配对交易)←统计套利(2.8) | 你的stock_scorer(选股评分)←多因子模型(2.4.1)", {
  x: 0.7, y: 5.05, w: 8.6, h: 0.3, fontSize: 8, fontFace: FB, color: "94A3B8", valign: "middle", margin: 0
});

// ===== S8: Time Series Models =====
let s8 = pres.addSlide();
addHeader(s8, "2.6 时间序列模型演进", "随机游走→ARIMA→GARCH→鞅回归+NPEB");
const models = [
  { name: "随机游走", period: "Bachelier(1900)", desc: "价格变化独立同分布\n布朗运动基础\n有效市场假说基石\n完全随机", color: "6366F1" },
  { name: "ARIMA", period: "Box-Jenkins", desc: "自回归移动平均\n用过去价格预测未来\n线性时间序列\n短期有一定预测力", color: "3B82F6" },
  { name: "GARCH", period: "Engle(1982)", desc: "条件异方差模型\n波动率时变集聚\n大波动→大波动\n刻画肥尾特征", color: "059669" },
  { name: "鞅回归", period: "新方法", desc: "条件均值+方差\n联合建模\n趋势和风险互相影响\n优于分开建模", color: "D97706" },
  { name: "NPEB", period: "本书贡献", desc: "非参经验贝叶斯\nBootstrap估计\n自动惩罚极端权重\n样本外更稳健", color: "7C3AED" },
];
models.forEach((m, i) => {
  const x = 0.2 + i * 1.95;
  s8.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 1.8, h: 3.0, fill: { color: C.cardBg }, shadow: mkShadow(), line: { color: C.border, width: 0.5 } });
  s8.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 1.8, h: 0.5, fill: { color: m.color } });
  s8.addText(m.name, { x: x + 0.1, y: 1.25, w: 1.6, h: 0.4, fontSize: 12, fontFace: FB, color: C.white, bold: true, margin: 0 });
  s8.addText(m.period, { x: x + 0.1, y: 1.8, w: 1.6, h: 0.25, fontSize: 8, fontFace: FB, color: m.color, italic: true, margin: 0 });
  s8.addText(m.desc, { x: x + 0.1, y: 2.15, w: 1.6, h: 1.8, fontSize: 9, fontFace: FB, color: C.text, margin: 0, lineSpacingMultiple: 1.4 });
  if (i < 4) s8.addText("→", { x: x + 1.78, y: 2.5, w: 0.17, h: 0.4, fontSize: 12, color: C.muted, align: "center", margin: 0 });
});

// ===== S9: Portfolio Theory Overview =====
let s9 = pres.addSlide();
addHeader(s9, "2.3-2.5 投资组合理论与新方法总览", "从经典到前沿");
const approaches = [
  { title: "Markowitz均值-方差", color: C.primary, items: ["有效前沿理论","期望收益最大/风险最小","问题：对参数极度敏感","输入微变，权重大变"] },
  { title: "Fama-French多因子", color: C.secondary, items: ["市场(MKT)+规模(SMB)","+价值(HML)+动量(MOM)","收益 = Σβ_i × Factor_i","解释90%收益差异"] },
  { title: "Black-Litterman", color: C.teal, items: ["先验=市场均衡收益","观点=投资者主观判断","后验=两者贝叶斯融合","结果更稳健"] },
  { title: "NPEB新方法", color: C.purple, items: ["Bootstrap估计不确定性","自动惩罚极端权重","样本外表现更优","本书重点贡献的方法"] },
];
approaches.forEach((a, i) => {
  const x = 0.3 + i * 2.4;
  s9.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.2, h: 3.0, fill: { color: C.cardBg }, shadow: mkShadow(), line: { color: C.border, width: 0.5 } });
  s9.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.2, h: 0.45, fill: { color: a.color } });
  s9.addText(a.title, { x: x + 0.1, y: 1.15, w: 2.0, h: 0.35, fontSize: 11, fontFace: FB, color: C.white, bold: true, margin: 0 });
  const items = a.items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < a.items.length - 1, fontSize: 10, color: C.text, paraSpaceAfter: 5 } }));
  s9.addText(items, { x: x + 0.1, y: 1.7, w: 2.0, h: 2.2, fontFace: FB, valign: "top", margin: 0 });
});

// ===== S10: Momentum Strategy =====
let s10 = pres.addSlide();
addHeader(s10, "2.8.2 动量策略（Momentum）", "Jegadeesh & Titman(1993) · 时间跨度：3-12个月");
addCard(s10, 0.3, 1.1, 4.3, 1.2, "3B82F6", ["过去涨的股票，未来3-12个月还会继续涨","不是追涨杀跌，而是有统计支撑的金融异象(Anomaly)","投资者反应不足 + 信息缓慢扩散 = 动量利润"], "核心思想", { fs: 10 });
addCard(s10, 4.8, 1.1, 4.9, 1.2, "10B981", ["每6个月按过去6个月涨幅排名","买涨幅前10% + 卖跌幅前10%","持有6个月后重新排名"], "具体做法", { fs: 10 });
addCard(s10, 0.3, 2.6, 3.0, 1.5, "10B981", ["投资者对好消息反应不足","价格调整需要时间","大机构分批建仓/减仓","信息缓慢扩散"], "为什么有效？", { fs: 10 });
addCard(s10, 3.5, 2.6, 3.0, 1.5, "EF4444", ["动量崩溃(Momentum Crash)","市场急转直下时巨亏","如2008年金融危机","换手率高→交易成本大"], "风险", { fs: 10 });
addCard(s10, 6.7, 2.6, 3.0, 1.5, "D97706", ["2025年6月排名","买：AI概念股（过去涨40%）","卖：房地产股（过去跌30%）","持有6个月后净赚25%"], "实例", { fs: 10 });

// ===== S11: Pairs Trading =====
let s11 = pres.addSlide();
addHeader(s11, "2.8.2 配对交易（Pairs Trading）", "统计套利的经典 · 直接对应你的spread_monitor.py");
addCard(s11, 0.3, 1.1, 4.3, 0.8, "D97706", ["双胞胎比喻：兄弟俩身高几乎一样，突然差3cm → 过几天会恢复","找两只高度相关的资产（相关性>0.8），价差拉大时赌它们回归"], "👬 核心思想", { fs: 10 });
const steps = [
  { title: "①找兄弟", desc: "两只高相关股票\n茅台和五粮液", color: "3B82F6" },
  { title: "②算价差", desc: "价格比值或差值\n茅台价/五粮液价", color: "10B981" },
  { title: "③定阈值", desc: "偏离均值超2σ入场\n回到均值出场", color: "D97706" },
  { title: "④执行", desc: "做多低的\n做空高的", color: "7C3AED" },
];
steps.forEach((st, i) => {
  const x = 0.3 + i * 2.4;
  s11.addShape(pres.shapes.RECTANGLE, { x, y: 2.2, w: 2.2, h: 1.1, fill: { color: C.cardBg }, line: { color: C.border, width: 0.5 } });
  s11.addShape(pres.shapes.RECTANGLE, { x, y: 2.2, w: 0.06, h: 1.1, fill: { color: st.color } });
  s11.addText(st.title, { x: x + 0.15, y: 2.25, w: 1.9, h: 0.3, fontSize: 10, fontFace: FB, color: st.color, bold: true, margin: 0 });
  s11.addText(st.desc, { x: x + 0.15, y: 2.55, w: 1.9, h: 0.6, fontSize: 9, fontFace: FB, color: C.text, margin: 0, lineSpacingMultiple: 1.3 });
});
s11.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.6, w: 9.0, h: 0.8, fill: { color: "EEEDFE" }, line: { color: C.primary, width: 0.5 } });
s11.addText("📊 你的spread_monitor.py已实现：多源同时抓价格 + 计算价差bps + 超过阈值报警\n完整的配对交易还需：确定入场阈值(标准差法) + 同时做多/做空 + 设定止损线", {
  x: 0.7, y: 3.65, w: 8.6, h: 0.7, fontSize: 10, fontFace: FB, color: C.primary, margin: 0
});

// ===== S12: Remaining Strategies =====
let s12 = pres.addSlide();
addHeader(s12, "2.8.3-2.8.4 逆向投资·价值投资·全球宏观", "原书p.43-44");
addCard(s12, 0.3, 1.1, 3.0, 1.5, "EF4444", ["时间跨度：1-3年","买跌得最惨的股票","卖涨得最好的股票","理论基础：过度反应后反转","行为金融学偏差"], "③ 逆向投资", { fs: 10 });
addCard(s12, 3.5, 1.1, 3.0, 1.5, "D97706", ["时间跨度：长期(年)","买被低估的好公司","PE低、PB低、ROE高","格雷厄姆→巴菲特","价值溢价(HML因子)"], "④ 价值投资", { fs: 10 });
addCard(s12, 6.7, 1.1, 3.0, 1.5, "7C3AED", ["时间跨度：约1个月","利用宏观事件和趋势","酌情型 vs 系统型","美元涨→买美元","依赖经济数据分析"], "⑤ 全球宏观", { fs: 10 });
s12.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.9, w: 9.0, h: 1.3, fill: { color: "1E293B" } });
s12.addText("策略选择地图", { x: 0.7, y: 3.0, w: 8.6, h: 0.35, fontSize: 12, fontFace: FB, color: C.accent, bold: true, margin: 0 });
s12.addText("短期(天-周)→配对交易 | 中期(3-12月)→动量 | 中期(1-3年)→逆向 | 长期(年)→价值投资 | 事件驱动→宏观", {
  x: 0.7, y: 3.4, w: 8.6, h: 0.3, fontSize: 10, fontFace: FB, color: C.white, margin: 0
});
s12.addText("2.8.5 策略评估铁律：样本内调参数，样本外验证真水平。测试100次→即使全是随机也有5个假阳性。", {
  x: 0.7, y: 3.8, w: 8.6, h: 0.3, fontSize: 10, fontFace: FB, color: C.red, margin: 0
});

// ===== S13: Summary =====
let s13 = pres.addSlide(); s13.background = { color: C.dark };
s13.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s13.addText("第2章 核心总结", { x: 0.8, y: 0.5, w: 8.4, h: 0.5, fontSize: 24, fontFace: FT, color: C.white, margin: 0 });
s13.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 1.0, w: 1.5, h: 0.04, fill: { color: C.accent } });
s13.addText([
  { text: "数据特征", options: { breakLine: true, fontSize: 12, bold: true, color: C.accent } },
  { text: "股票收益 ≠ 正态分布 | 波动率会集聚 | 存在跳跃", options: { breakLine: true, fontSize: 10, color: C.white, paraSpaceAfter: 4 } },
  { text: "模型演进", options: { breakLine: true, fontSize: 12, bold: true, color: C.accent } },
  { text: "随机游走 → ARIMA → GARCH → 鞅回归 → NPEB", options: { breakLine: true, fontSize: 10, color: C.white, paraSpaceAfter: 4 } },
  { text: "投资组合理论", options: { breakLine: true, fontSize: 12, bold: true, color: C.accent } },
  { text: "CAPM → Fama-French三因子 → Carhart四因子 → Black-Litterman", options: { breakLine: true, fontSize: 10, color: C.white, paraSpaceAfter: 4 } },
  { text: "统计套利策略", options: { breakLine: true, fontSize: 12, bold: true, color: C.accent } },
  { text: "动量(3-12月) · 配对交易(天-周) · 逆向(1-3年) · 价值(长期) · 宏观(月)", options: { breakLine: true, fontSize: 10, color: C.white, paraSpaceAfter: 4 } },
  { text: "评估纪律", options: { breakLine: true, fontSize: 12, bold: true, color: C.accent } },
  { text: "样本内 + 样本外双重验证 · 多重检验校正", options: { fontSize: 10, color: C.white } }
], { x: 0.8, y: 1.3, w: 8.4, h: 3.8, fontFace: FB, margin: 0, lineSpacingMultiple: 1.0 });

// ===== S14: End =====
let s14 = pres.addSlide(); s14.background = { color: C.dark };
s14.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s14.addText("第2章 · 完", { x: 1, y: 1.5, w: 8, h: 1.0, fontSize: 36, fontFace: FT, color: C.white, align: "center", margin: 0 });
s14.addShape(pres.shapes.RECTANGLE, { x: 4.2, y: 2.5, w: 1.6, h: 0.04, fill: { color: C.accent } });
s14.addText("下一章：积极型投资组合管理和投资策略", { x: 1, y: 3.0, w: 8, h: 0.5, fontSize: 14, fontFace: FB, color: C.muted, align: "center", margin: 0 });

const outPath = "C:/Users/user/WorkBuddy/Claw/乌龙指研究/第2章_统计模型与方法_视觉讲解.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("✅ 已生成: " + outPath));
