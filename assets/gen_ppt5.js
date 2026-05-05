const pptxgen = require("pptxgenjs");

const NAVY = "1E2761";
const ICE = "CADCFC";
const WHITE = "FFFFFF";
const ACCENT = "F96167";
const DARK = "212121";
const MUTED = "666666";
const LIGHTBG = "F5F7FA";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "行者";
pres.title = "第5章 交易执行与算法交易";

const makeShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });

// ======= Slide 1: Title =======
let s1 = pres.addSlide();
s1.background = { color: NAVY };
s1.addText("第5章", { x: 0.5, y: 1.0, w: 9, h: 0.6, fontSize: 16, color: ICE, fontFace: "Calibri", charSpacing: 4 });
s1.addText("交易执行与算法交易", { x: 0.5, y: 1.6, w: 9, h: 1.0, fontSize: 38, color: WHITE, fontFace: "Calibri", bold: true });
s1.addText("市场微观结构 · Almgren-Chriss · VWAP/TWAP · A股实战", {
  x: 0.5, y: 2.8, w: 9, h: 0.5, fontSize: 14, color: ICE, fontFace: "Calibri" });
s1.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.6, w: 2, h: 0.03, fill: { color: ACCENT } });
s1.addText("《量化交易：算法、分析、数据、模型和优化》", {
  x: 0.5, y: 4.0, w: 9, h: 0.4, fontSize: 11, color: ICE, fontFace: "Calibri" });
s1.addText("行者 · 2026-05", { x: 0.5, y: 4.4, w: 9, h: 0.4, fontSize: 10, color: MUTED, fontFace: "Calibri" });

// ======= Slide 2: Why execution matters =======
let s2 = pres.addSlide();
s2.background = { color: WHITE };
s2.addText("为什么执行很重要", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 28, color: NAVY, fontFace: "Calibri", bold: true });
s2.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

s2.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 8.8, h: 0.8,
  fill: { color: "FCEBEB" }
});
s2.addText("你的策略年化收益 20% ，如果执行成本吃掉 15% ，实际只剩 5%", {
  x: 0.8, y: 1.2, w: 8.4, h: 0.8,
  fontSize: 16, color: "A32D2D", fontFace: "Calibri", bold: true, valign: "middle"
});

s2.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.3, w: 4.2, h: 2.8, fill: { color: LIGHTBG }, shadow: makeShadow() });
s2.addText("理论世界", { x: 0.8, y: 2.4, w: 3.8, h: 0.4, fontSize: 14, color: NAVY, fontFace: "Calibri", bold: true });
s2.addText([
  { text: "下单 = 按当前价格成交", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "没有摩擦, 没有成本", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "量化策略算多少就是多少", options: { bullet: true, color: DARK } },
], { x: 0.8, y: 2.9, w: 3.8, h: 2.0, fontSize: 12, fontFace: "Calibri" });

s2.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 2.3, w: 4.2, h: 2.8, fill: { color: "FCEBEB" }, shadow: makeShadow() });
s2.addText("真实世界", { x: 5.4, y: 2.4, w: 3.8, h: 0.4, fontSize: 14, color: "A32D2D", fontFace: "Calibri", bold: true });
s2.addText([
  { text: "买单推高价格, 卖单压低价格", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "大单暴露意图, 被市场狙击", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "策略实际收益 = 理论收益 − 执行成本", options: { bullet: true, color: "A32D2D", bold: true } },
], { x: 5.4, y: 2.9, w: 3.8, h: 2.0, fontSize: 12, fontFace: "Calibri" });

// ======= Slide 3: The trade-off =======
let s3 = pres.addSlide();
s3.background = { color: WHITE };
s3.addText("核心权衡：冲击成本 vs 时间风险", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s3.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

const tradeoff = [
  { title: "快买", impact: "高 (冲击成本大)", risk: "低 (时间风险小)", color: "FCEBEB" },
  { title: "适中", impact: "中 (平衡点)", risk: "中 (平衡点)", color: "EAF3DE" },
  { title: "慢买", impact: "低 (冲击成本小)", risk: "高 (时间风险大)", color: "EEEDFE" },
];

tradeoff.forEach((t, i) => {
  const x = 0.6 + i * 3.1;
  s3.addShape(pres.shapes.RECTANGLE, { x: x, y: 1.2, w: 2.8, h: 1.8, fill: { color: LIGHTBG }, shadow: makeShadow() });
  s3.addShape(pres.shapes.RECTANGLE, { x: x, y: 1.2, w: 2.8, h: 0.45, fill: { color: NAVY } });
  s3.addText(t.title, { x: x + 0.1, y: 1.2, w: 2.6, h: 0.45, fontSize: 14, color: WHITE, fontFace: "Calibri", bold: true, valign: "middle", margin: 0 });
  s3.addText("冲击成本: " + t.impact, { x: x + 0.1, y: 1.75, w: 2.6, h: 0.35, fontSize: 11, color: "A32D2D", fontFace: "Calibri" });
  s3.addText("时间风险: " + t.risk, { x: x + 0.1, y: 2.2, w: 2.6, h: 0.35, fontSize: 11, color: "185FA5", fontFace: "Calibri" });
  s3.addText("→ " + (i === 1 ? "最佳" : "不是最佳"), { x: x + 0.1, y: 2.6, w: 2.6, h: 0.35, fontSize: 11, color: i === 1 ? "1D9E75" : MUTED, fontFace: "Calibri", bold: true });
});

s3.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.3, w: 8.8, h: 0.8, fill: { color: NAVY } });
s3.addText("Almgren-Chriss 模型：找到总成本最低的执行速度", {
  x: 0.6, y: 3.3, w: 8.8, h: 0.8,
  fontSize: 14, color: WHITE, fontFace: "Calibri", bold: true, align: "center", valign: "middle"
});

s3.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 4.3, w: 8.8, h: 1.0, fill: { color: LIGHTBG } });
s3.addText("总成本 = Σ [ η·v_t^(1+β) + σ·ΔW_t ]", {
  x: 0.6, y: 4.35, w: 8.8, h: 0.4,
  fontSize: 16, color: ACCENT, fontFace: "Consolas", bold: true, align: "center"
});
s3.addText("η = 冲击系数 (流动性差则大)    σ = 波动率    β ≈ 0.5", {
  x: 0.6, y: 4.75, w: 8.8, h: 0.3,
  fontSize: 11, color: MUTED, fontFace: "Calibri", align: "center"
});
s3.addText("最优速度 v* = (σ/η)^(1/1+β)   |   波动大 → 快买   |   冲击大 → 慢买", {
  x: 0.6, y: 4.95, w: 8.8, h: 0.3,
  fontSize: 11, color: NAVY, fontFace: "Calibri", align: "center", bold: true
});

// ======= Slide 4: A-share rules =======
let s4 = pres.addSlide();
s4.background = { color: WHITE };
s4.addText("A股交易四大规则", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s4.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

const arules = [
  { num: "1", title: "T+1", desc1: "当日买入不能当日卖出", desc2: "隔夜风险是最大风控维度", tip: "尾盘信号更可靠, 单日开仓≤5%" },
  { num: "2", title: "涨跌停±10%", desc1: "封板时代理不能成交", desc2: "流动性瞬间消失", tip: "涨停不追买, 跌停不割肉" },
  { num: "3", title: "交易成本", desc1: "卖出有0.05%印花税", desc2: "来回成本约0.08%-0.13%", tip: "日换手率<20%, 少卖多持" },
  { num: "4", title: "流动性分层", desc1: "开盘30min+尾盘30min占55%", desc2: "午休1.5小时不能交易", tip: "大单限14:30-14:57执行" },
];
arules.forEach((r, i) => {
  const row = Math.floor(i / 2);
  const col = i % 2;
  const x = 0.6 + col * 4.6;
  const y = 1.1 + row * 2.0;
  s4.addShape(pres.shapes.RECTANGLE, { x: x, y: y, w: 4.3, h: 1.7, fill: { color: LIGHTBG }, shadow: makeShadow() });
  s4.addShape(pres.shapes.OVAL, { x: x + 0.15, y: y + 0.15, w: 0.45, h: 0.45, fill: { color: ACCENT } });
  s4.addText(r.num, { x: x + 0.15, y: y + 0.15, w: 0.45, h: 0.45, fontSize: 16, color: WHITE, fontFace: "Calibri", bold: true, align: "center", valign: "middle", margin: 0 });
  s4.addText(r.title, { x: x + 0.7, y: y + 0.1, w: 3.3, h: 0.4, fontSize: 14, color: NAVY, fontFace: "Calibri", bold: true });
  s4.addText("→ " + r.desc1, { x: x + 0.7, y: y + 0.55, w: 3.3, h: 0.3, fontSize: 11, color: DARK, fontFace: "Calibri" });
  s4.addText("→ " + r.desc2, { x: x + 0.7, y: y + 0.85, w: 3.3, h: 0.3, fontSize: 11, color: DARK, fontFace: "Calibri" });
  s4.addShape(pres.shapes.RECTANGLE, { x: x + 0.15, y: y + 1.25, w: 3.9, h: 0.32, fill: { color: "EAF3DE" } });
  s4.addText("应对: " + r.tip, { x: x + 0.25, y: y + 1.25, w: 3.7, h: 0.32, fontSize: 10, color: "3B6D11", fontFace: "Calibri", valign: "middle" });
});

// ======= Slide 5: VWAP vs TWAP =======
let s5 = pres.addSlide();
s5.background = { color: WHITE };
s5.addText("VWAP vs TWAP 执行算法", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s5.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// TWAP card
s5.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.1, w: 4.2, h: 2.2, fill: { color: LIGHTBG }, shadow: makeShadow() });
s5.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.1, w: 4.2, h: 0.45, fill: { color: NAVY } });
s5.addText("TWAP (Time-Weighted)", { x: 0.8, y: 1.1, w: 3.8, h: 0.45, fontSize: 13, color: WHITE, fontFace: "Calibri", bold: true, valign: "middle" });
s5.addText("时间加权平均价格", { x: 0.8, y: 1.55, w: 3.8, h: 0.3, fontSize: 11, color: MUTED, fontFace: "Calibri", italic: true });
s5.addText([
  { text: "每分钟下等量的单", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "不需要知道成交量分布", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "简单可预测, 适合中小单", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "均价 = 全天价格的简单平均", options: { bullet: true, color: MUTED } },
], { x: 0.8, y: 1.9, w: 3.8, h: 1.2, fontSize: 11, fontFace: "Calibri" });

// VWAP card
s5.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.1, w: 4.2, h: 2.2, fill: { color: LIGHTBG }, shadow: makeShadow() });
s5.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.1, w: 4.2, h: 0.45, fill: { color: ACCENT } });
s5.addText("VWAP (Volume-Weighted)", { x: 5.4, y: 1.1, w: 3.8, h: 0.45, fontSize: 13, color: WHITE, fontFace: "Calibri", bold: true, valign: "middle" });
s5.addText("成交量加权平均价格", { x: 5.4, y: 1.55, w: 3.8, h: 0.3, fontSize: 11, color: MUTED, fontFace: "Calibri", italic: true });
s5.addText([
  { text: "按成交量比例分配下单量", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "顺应市场流动性", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "机构基准, 冲击成本更低", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "均价 = 价格 × 成交量权重", options: { bullet: true, color: MUTED } },
], { x: 5.4, y: 1.9, w: 3.8, h: 1.2, fontSize: 11, fontFace: "Calibri" });

// Comparison table
s5.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.5, w: 8.8, h: 1.8, fill: { color: LIGHTBG } });
const th = { fill: { color: NAVY }, color: WHITE, bold: true, fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle" };
const tc = { fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle" };
s5.addTable([
  [{ text: "维度", options: th }, { text: "TWAP", options: th }, { text: "VWAP", options: th }, { text: "适用场景", options: th }],
  [{ text: "下单规则", options: tc }, { text: "每分钟等量", options: tc }, { text: "按成交量比例", options: tc }, { text: "~100万以上用VWAP", options: tc }],
  [{ text: "数据需求", options: tc }, { text: "无需数据", options: tc }, { text: "需历史成交量曲线", options: tc }, { text: "~100万以下TWAP即可", options: tc }],
  [{ text: "执行成本", options: tc }, { text: "中等", options: tc }, { text: "更低", options: tc }, { text: "A股尾盘集中下单也行", options: tc }],
  [{ text: "开发难度", options: tc }, { text: "极低", options: tc }, { text: "低", options: tc }, { text: "代码20行搞定", options: tc }],
], { x: 0.8, y: 3.6, w: 8.4, colW: [2.0, 2.0, 2.2, 2.2], rowH: [0.3, 0.3, 0.3, 0.3, 0.3], border: { pt: 0.5, color: "DDDDDD" } });

// ======= Slide 6: Practical guide =======
let s6 = pres.addSlide();
s6.background = { color: WHITE };
s6.addText("实盘执行指南", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s6.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// Table
const th2 = { fill: { color: NAVY }, color: WHITE, bold: true, fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle" };
const tc2 = { fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle" };
s6.addTable([
  [{ text: "资金量", options: th2 }, { text: "建议策略", options: th2 }, { text: "具体方式", options: th2 }],
  [{ text: "< 20万", options: tc2 }, { text: "一次性市价单", options: tc2 }, { text: "直接下单, 省心省力", options: tc2 }],
  [{ text: "20万~100万", options: tc2 }, { text: "TWAP 分3-5笔", options: tc2 }, { text: "每5分钟下一笔, 10分钟内完成", options: tc2 }],
  [{ text: "100万~500万", options: tc2 }, { text: "TWAP / VWAP", options: tc2 }, { text: "分10-20笔, 按成交量曲线分配", options: tc2 }],
  [{ text: "> 500万", options: tc2 }, { text: "VWAP 算法", options: tc2 }, { text: "需要自动化执行系统", options: tc2 }],
], { x: 0.6, y: 1.1, w: 8.8, colW: [2.0, 3.0, 3.8], rowH: [0.35, 0.35, 0.35, 0.35, 0.35], border: { pt: 0.5, color: "DDDDDD" } });

s6.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.3, w: 8.8, h: 1.5, fill: { color: LIGHTBG }, shadow: makeShadow() });
s6.addText("6条A股执行规则（可直接写入你的系统）", { x: 0.8, y: 3.4, w: 8.4, h: 0.4, fontSize: 13, color: NAVY, fontFace: "Calibri", bold: true });
s6.addText([
  { text: "1. 交易时间：开盘前10分钟不下单, 尾盘30分钟是主要窗口", options: { breakLine: true, color: DARK, fontSize: 11 } },
  { text: "2. T+1风控：单日开仓 ≤ 总资金5%", options: { breakLine: true, color: DARK, fontSize: 11 } },
  { text: "3. 涨跌停：涨停不追买, 跌停不割肉", options: { breakLine: true, color: DARK, fontSize: 11 } },
  { text: "4. 成本控制：每日换手率 ≤ 20%, 减少卖出频率", options: { breakLine: true, color: DARK, fontSize: 11 } },
  { text: "5. 流动性：单笔交易 ≤ 该股日均成交额的1%", options: { breakLine: true, color: DARK, fontSize: 11 } },
  { text: "6. 执行算法：> 50万用VWAP分批, < 50万一次市价单", options: { color: DARK, fontSize: 11 } },
], { x: 0.8, y: 3.85, w: 8.4, h: 1.0, fontFace: "Calibri" });

// ======= Slide 7: Summary =======
let s7 = pres.addSlide();
s7.background = { color: NAVY };
s7.addText("总  结", { x: 0.5, y: 0.5, w: 9, h: 0.6, fontSize: 30, color: WHITE, fontFace: "Calibri", bold: true });
s7.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.05, w: 1.5, h: 0.03, fill: { color: ACCENT } });

const chain = ["执行重要性", "冲击vs时间", "Almgren-Chriss", "A股四大规则", "VWAP/TWAP", "实盘指南"];
chain.forEach((item, i) => {
  const x = 0.5 + i * 1.6;
  s7.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.5, w: 1.3, h: 0.7,
    fill: { color: i < 3 ? ICE : ACCENT }
  });
  s7.addText(item, {
    x: x, y: 1.5, w: 1.3, h: 0.7,
    fontSize: 11, color: NAVY, fontFace: "Calibri", bold: true,
    align: "center", valign: "middle", margin: 0
  });
  if (i < chain.length - 1) {
    s7.addText("→", {
      x: x + 1.25, y: 1.5, w: 0.4, h: 0.7,
      fontSize: 18, color: WHITE, fontFace: "Calibri", bold: true,
      valign: "middle", margin: 0
    });
  }
});

s7.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.6, w: 9.0, h: 2.0, fill: { color: ACCENT } });
s7.addText("全书知识链（第1~5章）", { x: 0.7, y: 2.7, w: 8.6, h: 0.4, fontSize: 16, color: WHITE, fontFace: "Calibri", bold: true });
s7.addText([
  { text: "第1-3章: Alpha模型 + 风险模型", options: { breakLine: true, color: ICE, fontSize: 12 } },
  { text: "第4章:  资产配置与风险管理", options: { breakLine: true, color: WHITE, fontSize: 12, bold: true } },
  { text: "第5章:  交易执行与算法交易", options: { breakLine: true, color: ICE, fontSize: 12 } },
  { text: "从\'买什么\' 到 \'买多少\' 到 \'怎么买\' 的完整链路", options: { color: NAVY, fontSize: 12, bold: true } },
], { x: 0.7, y: 3.2, w: 8.6, h: 1.2, fontFace: "Calibri" });

s7.addText("《量化交易》第5章 · 行者 · 2026-05", {
  x: 0.5, y: 5.0, w: 9, h: 0.4,
  fontSize: 10, color: ICE, fontFace: "Calibri", align: "center"
});

const outputPath = "C:\\Users\\user\\WorkBuddy\\Claw\\assets\\第5章_交易执行与算法交易.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("PPTX saved to: " + outputPath);
}).catch(err => {
  console.error("Error:", err);
});
