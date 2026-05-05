const pptxgen = require("pptxgenjs");
const fs = require("fs");

// Theme colors
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
pres.title = "第4章 资产配置与风险管理";

const makeShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });

// ======= Slide 1: Title =======
let s1 = pres.addSlide();
s1.background = { color: NAVY };
s1.addText("第4章", { x: 0.5, y: 1.0, w: 9, h: 0.6, fontSize: 16, color: ICE, fontFace: "Calibri", charSpacing: 4 });
s1.addText("资产配置与风险管理", { x: 0.5, y: 1.6, w: 9, h: 1.0, fontSize: 38, color: WHITE, fontFace: "Calibri", bold: true });
s1.addText("马克维茨均值-方差 · Black-Litterman · 风险平价 · 实际约束", {
  x: 0.5, y: 2.8, w: 9, h: 0.5, fontSize: 14, color: ICE, fontFace: "Calibri" });
s1.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.6, w: 2, h: 0.03, fill: { color: ACCENT } });
s1.addText("《量化交易：算法、分析、数据、模型和优化》", {
  x: 0.5, y: 4.0, w: 9, h: 0.4, fontSize: 11, color: ICE, fontFace: "Calibri" });
s1.addText("行者 · 2026-05", { x: 0.5, y: 4.4, w: 9, h: 0.4, fontSize: 10, color: MUTED, fontFace: "Calibri" });

// ======= Slide 2: Chapter Overview =======
let s2 = pres.addSlide();
s2.background = { color: WHITE };
s2.addText("本章概览", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 28, color: NAVY, fontFace: "Calibri", bold: true });
s2.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

const layers = [
  { num: "1", title: "投资组合理论基础", desc: "预期收益与风险的数学框架" },
  { num: "2", title: "马克维茨均值-方差", desc: "有效前沿与最小方差组合" },
  { num: "3", title: "切线组合 & CAL", desc: "引入无风险资产 → 夏普比率最大化" },
  { num: "4", title: "Black-Litterman & 风险平价", desc: "贝叶斯更新 + 等风险贡献" },
  { num: "5", title: "实际约束与工程实践", desc: "交易成本 · 卖空 · 集中度" },
  { num: "6", title: "Python 实现", desc: "scipy 凸优化求解器" },
];

const startY = 1.2;
const boxH = 0.58;
const gap = 0.08;
layers.forEach((layer, i) => {
  const y = startY + i * (boxH + gap);
  // Number circle
  s2.addShape(pres.shapes.OVAL, {
    x: 0.6, y: y + 0.04, w: 0.5, h: 0.5,
    fill: { color: i < 3 ? NAVY : ACCENT }
  });
  s2.addText(layer.num, {
    x: 0.6, y: y + 0.04, w: 0.5, h: 0.5,
    fontSize: 16, color: WHITE, fontFace: "Calibri", bold: true,
    align: "center", valign: "middle", margin: 0
  });
  // Title
  s2.addText(layer.title, {
    x: 1.3, y: y, w: 4, h: 0.3,
    fontSize: 14, color: DARK, fontFace: "Calibri", bold: true, margin: 0
  });
  s2.addText(layer.desc, {
    x: 1.3, y: y + 0.28, w: 4, h: 0.25,
    fontSize: 10, color: MUTED, fontFace: "Calibri", margin: 0
  });
  // Connector line
  if (i < layers.length - 1) {
    s2.addShape(pres.shapes.LINE, {
      x: 0.85, y: y + boxH, w: 0, h: gap + 0.02,
      line: { color: ACCENT, width: 1.5 }
    });
  }
});

// Right side: visual summary
s2.addShape(pres.shapes.RECTANGLE, {
  x: 5.8, y: 1.0, w: 3.8, h: 4.2,
  fill: { color: LIGHTBG }, shadow: makeShadow()
});
s2.addText("知识链", {
  x: 5.9, y: 1.1, w: 3.6, h: 0.4,
  fontSize: 12, color: NAVY, fontFace: "Calibri", bold: true
});
s2.addText([
  { text: "马克维茨", options: { bullet: true, breakLine: true, color: NAVY, bold: true } },
  { text: "↓ 切线组合 T", options: { breakLine: true, color: MUTED, fontSize: 11 } },
  { text: "↓ Black-Litterman", options: { bullet: true, breakLine: true, color: NAVY, bold: true } },
  { text: "↓ 风险平价", options: { breakLine: true, color: MUTED, fontSize: 11 } },
  { text: "↓ 实际约束", options: { bullet: true, breakLine: true, color: NAVY, bold: true } },
  { text: "↓ Python实现", options: { breakLine: true, color: MUTED, fontSize: 11 } },
], { x: 5.9, y: 1.6, w: 3.6, h: 3.2, fontSize: 12, fontFace: "Calibri", valign: "top" });

// ======= Slide 3: Core Formula =======
let s3 = pres.addSlide();
s3.background = { color: WHITE };
s3.addText("核心公式：组合收益与风险", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s3.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// Left card: Return
s3.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 2.0,
  fill: { color: LIGHTBG }, shadow: makeShadow()
});
s3.addText("组合预期收益", {
  x: 0.8, y: 1.3, w: 3.8, h: 0.4,
  fontSize: 14, color: NAVY, fontFace: "Calibri", bold: true
});
s3.addText("E(Rp) = w'μ", {
  x: 0.8, y: 1.7, w: 3.8, h: 0.5,
  fontSize: 22, color: ACCENT, fontFace: "Calibri", bold: true
});
s3.addText("= w₁μ₁ + w₂μ₂ + ... + wₙμₙ", {
  x: 0.8, y: 2.2, w: 3.8, h: 0.4,
  fontSize: 13, color: DARK, fontFace: "Calibri"
});
s3.addText("各资产收益率的加权平均", {
  x: 0.8, y: 2.6, w: 3.8, h: 0.4,
  fontSize: 10, color: MUTED, fontFace: "Calibri", italic: true
});

// Right card: Variance  
s3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 2.0,
  fill: { color: LIGHTBG }, shadow: makeShadow()
});
s3.addText("组合方差（风险）", {
  x: 5.4, y: 1.3, w: 3.8, h: 0.4,
  fontSize: 14, color: NAVY, fontFace: "Calibri", bold: true
});
s3.addText("σ²p = w'Σ w", {
  x: 5.4, y: 1.7, w: 3.8, h: 0.5,
  fontSize: 22, color: ACCENT, fontFace: "Calibri", bold: true
});
s3.addText("= ΣᵢΣⱼ wᵢwⱼσᵢⱼ", {
  x: 5.4, y: 2.2, w: 3.8, h: 0.4,
  fontSize: 13, color: DARK, fontFace: "Calibri"
});
s3.addText("二次型，权重以平方和交叉项出现", {
  x: 5.4, y: 2.6, w: 3.8, h: 0.4,
  fontSize: 10, color: MUTED, fontFace: "Calibri", italic: true
});

// Bottom insight
s3.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 3.5, w: 8.8, h: 1.8,
  fill: { color: NAVY }
});
s3.addText("关键洞察", {
  x: 0.8, y: 3.6, w: 8.4, h: 0.4,
  fontSize: 14, color: ICE, fontFace: "Calibri", bold: true
});
s3.addText([
  { text: "若资产间相关性低（ρ ≈ 0），组合风险可小于单个资产风险的加权平均", options: { breakLine: true, color: WHITE } },
  { text: "这就是\"分散化\"的数学来源——不需要预测涨跌，只需要管理相关性", options: { color: ICE } },
], { x: 0.8, y: 4.1, w: 8.4, h: 1.0, fontSize: 12, fontFace: "Calibri" });

// ======= Slide 4: Efficient Frontier =======
let s4 = pres.addSlide();
s4.background = { color: WHITE };
s4.addText("有效前沿与最小方差组合", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s4.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// Chart area
s4.addChart(pres.charts.SCATTER, [
  { name: "前沿", labels: Array.from({length: 100}, (_,i) => ""+i),
    values: Array.from({length: 100}, (_,i) => {
      const w = i/99;
      const s1=0.20,s2=0.15,r=0.25;
      const risk = Math.sqrt(w*w*s1*s1+(1-w)*(1-w)*s2*s2+2*w*(1-w)*r*s1*s2);
      const ret = w*0.12+(1-w)*0.08;
      return {x: risk*100, y: ret*100};
    })
  },
], {
  x: 0.6, y: 1.0, w: 4.5, h: 3.2,
  chartColors: [NAVY],
  lineSize: 2.5,
  showLegend: false,
  catAxisLabelColor: MUTED,
  valAxisLabelColor: MUTED,
  catGridLine: { color: "E2E8F0", size: 0.5 },
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catAxisTitle: "Risk (Std Dev %)",
  valAxisTitle: "Return %",
  catAxisTitleColor: MUTED,
  valAxisTitleColor: MUTED,
  chartArea: { fill: { color: WHITE } },
});

// Text on right
s4.addShape(pres.shapes.RECTANGLE, {
  x: 5.4, y: 1.0, w: 4.0, h: 1.6,
  fill: { color: LIGHTBG }, shadow: makeShadow()
});
s4.addText("有效前沿", { x: 5.6, y: 1.1, w: 3.6, h: 0.35, fontSize: 14, color: NAVY, fontFace: "Calibri", bold: true });
s4.addText([
  { text: "给定收益，最小化风险", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "前沿上的点 = 帕累托最优", options: { bullet: true, breakLine: true, color: DARK } },
  { text: "前沿以下的点 = 可被改进", options: { bullet: true, color: DARK } },
], { x: 5.6, y: 1.5, w: 3.6, h: 1.0, fontSize: 11, fontFace: "Calibri" });

s4.addShape(pres.shapes.RECTANGLE, {
  x: 5.4, y: 2.8, w: 4.0, h: 1.4,
  fill: { color: NAVY }
});
s4.addText("分散化效果", { x: 5.6, y: 2.9, w: 3.6, h: 0.35, fontSize: 14, color: ICE, fontFace: "Calibri", bold: true });
s4.addText("ρ 越低 → 有效前沿越向左弯曲\n→ 分散化收益越大", {
  x: 5.6, y: 3.3, w: 3.6, h: 0.7,
  fontSize: 11, color: WHITE, fontFace: "Calibri"
});

// Bottom bar
s4.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 4.5, w: 8.8, h: 0.7,
  fill: { color: LIGHTBG }
});
s4.addText("目标函数：min w'Σ w    约束：w'1 = 1, w'μ = R_target", {
  x: 0.6, y: 4.5, w: 8.8, h: 0.7,
  fontSize: 13, color: NAVY, fontFace: "Calibri", bold: true, align: "center", valign: "middle"
});

// ======= Slide 5: Tangent Portfolio =======
let s5 = pres.addSlide();
s5.background = { color: WHITE };
s5.addText("切线组合 T — 最大夏普比率", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s5.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// Formula card
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.1, w: 5.0, h: 1.2,
  fill: { color: LIGHTBG }, shadow: makeShadow()
});
s5.addText("Sharpe Ratio = (E(Rp) − rf) / σp", {
  x: 0.8, y: 1.2, w: 4.6, h: 0.5,
  fontSize: 20, color: ACCENT, fontFace: "Calibri", bold: true
});
s5.addText("切线组合 T = 夏普比率最大的组合", {
  x: 0.8, y: 1.75, w: 4.6, h: 0.35,
  fontSize: 13, color: DARK, fontFace: "Calibri"
});
s5.addText("由rf向有效前沿画切线 → 切点即为T", {
  x: 0.8, y: 2.1, w: 4.6, h: 0.3,
  fontSize: 11, color: MUTED, fontFace: "Calibri", italic: true
});

// Key insight cards
const insights = [
  { title: "仅与资产属性有关", desc: "T 的权重只取决于 μ 和 Σ\n与你的风险偏好无关" },
  { title: "风险偏好单独决定", desc: "保守 → 多配 rf\n激进 → 借钱放大 T" },
  { title: "分离定理", desc: "最优风险组合 + 资金分配\n两个问题独立求解" },
];
insights.forEach((ins, i) => {
  const x = 0.6 + i * 3.1;
  s5.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 2.6, w: 2.8, h: 1.5,
    fill: { color: i === 0 ? NAVY : i === 1 ? ACCENT : LIGHTBG },
    shadow: makeShadow()
  });
  const titleColor = i === 2 ? NAVY : WHITE;
  const descColor = i === 2 ? MUTED : ICE;
  s5.addText(ins.title, {
    x: x + 0.15, y: 2.7, w: 2.5, h: 0.35,
    fontSize: 12, color: titleColor, fontFace: "Calibri", bold: true
  });
  s5.addText(ins.desc, {
    x: x + 0.15, y: 3.1, w: 2.5, h: 0.8,
    fontSize: 10, color: descColor, fontFace: "Calibri"
  });
});

// Bottom example
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 4.3, w: 8.8, h: 1.0,
  fill: { color: NAVY }
});
s5.addText("数值示例", { x: 0.8, y: 4.35, w: 8.4, h: 0.3, fontSize: 12, color: ICE, fontFace: "Calibri", bold: true });
s5.addText("资产A (μ=12%, σ=20%) + 资产B (μ=8%, σ=15%) + ρ=0.25 + rf=4%", {
  x: 0.8, y: 4.65, w: 6, h: 0.25, fontSize: 11, color: WHITE, fontFace: "Calibri" });
s5.addText("→ T = 60% A + 40% B, 夏普 = 0.435", {
  x: 0.8, y: 4.9, w: 6, h: 0.25, fontSize: 11, color: ICE, fontFace: "Calibri", bold: true });

// ======= Slide 6: Tangent Math =======
let s6 = pres.addSlide();
s6.background = { color: WHITE };
s6.addText("切线组合数学推导", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s6.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

const steps = [
  { label: "Step 1", formula: "max SR(w) = (w'μ − rf) / √(w'Σ w)", sub: "subject to w'1 = 1" },
  { label: "Step 2", formula: "∂SR/∂w = 0 → μ(w'Σ w) = (w'μ − rf)Σ w", sub: "一阶条件：边际夏普=0" },
  { label: "Step 3", formula: "w ∝ Σ⁻¹ μ", sub: "整理得：权重与 Σ⁻¹μ 成比例" },
  { label: "Step 4", formula: "w_T = Σ⁻¹(μ − rf) / [1'Σ⁻¹(μ − rf)]", sub: "归一化：权重之和=1" },
];

steps.forEach((step, i) => {
  const y = 1.1 + i * 1.1;
  s6.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: y, w: 0.6, h: 0.75,
    fill: { color: i < 2 ? NAVY : ACCENT }
  });
  s6.addText(step.label, {
    x: 0.6, y: y, w: 0.6, h: 0.75,
    fontSize: 10, color: WHITE, fontFace: "Calibri", bold: true,
    align: "center", valign: "middle", margin: 0
  });
  s6.addText(step.formula, {
    x: 1.4, y: y + 0.05, w: 8.0, h: 0.4,
    fontSize: 14, color: DARK, fontFace: "Consolas", bold: true, margin: 0
  });
  s6.addText(step.sub, {
    x: 1.4, y: y + 0.4, w: 8.0, h: 0.3,
    fontSize: 10, color: MUTED, fontFace: "Calibri", italic: true, margin: 0
  });
});

// ======= Slide 7: Black-Litterman =======
let s7 = pres.addSlide();
s7.background = { color: WHITE };
s7.addText("Black-Litterman 模型", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s7.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// Problem
s7.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.1, w: 8.8, h: 0.7,
  fill: { color: "FCEBEB" }
});
s7.addText("痛点：马克维茨对 μ 的输入极其敏感 — μ 变动 1%，权重可能变动 50%", {
  x: 0.8, y: 1.1, w: 8.4, h: 0.7,
  fontSize: 12, color: "A32D2D", fontFace: "Calibri", valign: "middle"
});

// Solution flow
const blSteps = [
  { title: "Step 1: 逆向优化", detail: "从市值权重反推隐含收益\nπ = λ · Σ · w_mkt" },
  { title: "Step 2: 表达观点", detail: "P · μ = Q + ε\n置信度由 Ω 编码" },
  { title: "Step 3: 贝叶斯更新", detail: "先验精度 + 观点精度\n→ 加权平均 → 后验" },
  { title: "Step 4: 代入马克维茨", detail: "用 μ_BL 代替直接估计的 μ\n权重更稳定、更合理" },
];

blSteps.forEach((step, i) => {
  const x = 0.6 + i * 2.35;
  s7.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 2.1, w: 2.15, h: 2.2,
    fill: { color: LIGHTBG }, shadow: makeShadow()
  });
  s7.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 2.1, w: 2.15, h: 0.45,
    fill: { color: NAVY }
  });
  s7.addText(step.title, {
    x: x + 0.1, y: 2.1, w: 1.95, h: 0.45,
    fontSize: 11, color: WHITE, fontFace: "Calibri", bold: true,
    valign: "middle", margin: 0
  });
  s7.addText(step.detail, {
    x: x + 0.1, y: 2.65, w: 1.95, h: 1.5,
    fontSize: 10, color: DARK, fontFace: "Calibri"
  });
  if (i < blSteps.length - 1) {
    s7.addText("→", {
      x: x + 2.0, y: 2.8, w: 0.4, h: 0.4,
      fontSize: 18, color: ACCENT, fontFace: "Calibri", bold: true, margin: 0
    });
  }
});

// ======= Slide 8: Risk Parity =======
let s8 = pres.addSlide();
s8.background = { color: WHITE };
s8.addText("风险平价", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s8.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// Problem statement
s8.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.1, w: 8.8, h: 0.7,
  fill: { color: "FCEBEB" }
});
s8.addText("传统 60/40 组合 → 股票贡献 90% 的风险，债券仅 10%", {
  x: 0.8, y: 1.1, w: 8.4, h: 0.7,
  fontSize: 13, color: "A32D2D", fontFace: "Calibri", bold: true, valign: "middle"
});

// Core formula
s8.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 2.0, w: 4.5, h: 1.8,
  fill: { color: LIGHTBG }, shadow: makeShadow()
});
s8.addText("边际风险贡献：MCRᵢ = (Σw)ᵢ / σp", {
  x: 0.8, y: 2.1, w: 4.1, h: 0.4,
  fontSize: 13, color: DARK, fontFace: "Calibri"
});
s8.addText("总风险贡献：RCᵢ = wᵢ × MCRᵢ", {
  x: 0.8, y: 2.5, w: 4.1, h: 0.4,
  fontSize: 13, color: DARK, fontFace: "Calibri"
});
s8.addText("目标：RC₁ = RC₂ = ... = RCₙ", {
  x: 0.8, y: 2.9, w: 4.1, h: 0.4,
  fontSize: 14, color: ACCENT, fontFace: "Calibri", bold: true
});
s8.addText("(ρ=0 时简化：w₁/w₂ = σ₂/σ₁)", {
  x: 0.8, y: 3.3, w: 4.1, h: 0.3,
  fontSize: 10, color: MUTED, fontFace: "Calibri", italic: true
});

// Key insight
s8.addShape(pres.shapes.RECTANGLE, {
  x: 5.4, y: 2.0, w: 4.0, h: 1.8,
  fill: { color: NAVY }
});
s8.addText("核心优势", { x: 5.6, y: 2.1, w: 3.6, h: 0.35, fontSize: 14, color: ICE, fontFace: "Calibri", bold: true });
s8.addText([
  { text: "不需要 μ（预期收益）作为输入", options: { breakLine: true, color: WHITE } },
  { text: "只依赖协方差矩阵 Σ", options: { breakLine: true, color: WHITE } },
  { text: "权重与波动率成反比", options: { breakLine: true, color: WHITE } },
  { text: "桥水全天候策略的理论基础", options: { color: ICE } },
], { x: 5.6, y: 2.5, w: 3.6, h: 1.2, fontSize: 11, fontFace: "Calibri" });

// ======= Slide 9: Constraints =======
let s9 = pres.addSlide();
s9.background = { color: WHITE };
s9.addText("四大实际约束", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s9.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

const constraints = [
  { icon: "1", title: "交易成本", bg: "FCEBEB", detail: "优化器倾向高换手\n加正则惩罚：min w'Σw + λ||w−w_old||" },
  { icon: "2", title: "卖空限制", bg: "EEEDFE", detail: "A股不能裸卖空\n约束：wᵢ ≥ 0 (bounds=[(0,1)])" },
  { icon: "3", title: "头寸集中度", bg: "FAEEDA", detail: "单标的不超过 20%\n约束：wᵢ ≤ 0.2" },
  { icon: "4", title: "流动性门槛", bg: "E6F1FB", detail: "大单有冲击成本\n经验：单笔 ≤ 日均成交量 5%" },
];
constraints.forEach((c, i) => {
  const x = 0.6 + i * 2.35;
  s9.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.1, w: 2.15, h: 2.5,
    fill: { color: LIGHTBG }, shadow: makeShadow()
  });
  s9.addShape(pres.shapes.OVAL, {
    x: x + 0.75, y: 1.2, w: 0.55, h: 0.55,
    fill: { color: ACCENT }
  });
  s9.addText(c.icon, {
    x: x + 0.75, y: 1.2, w: 0.55, h: 0.55,
    fontSize: 16, color: WHITE, fontFace: "Calibri", bold: true,
    align: "center", valign: "middle", margin: 0
  });
  s9.addText(c.title, {
    x: x + 0.1, y: 1.85, w: 1.95, h: 0.3,
    fontSize: 14, color: DARK, fontFace: "Calibri", bold: true,
    align: "center", margin: 0
  });
  s9.addText(c.detail, {
    x: x + 0.1, y: 2.2, w: 1.95, h: 1.2,
    fontSize: 10, color: MUTED, fontFace: "Calibri", align: "center"
  });
});

// ======= Slide 10: Python Demo =======
let s10 = pres.addSlide();
s10.background = { color: WHITE };
s10.addText("Python 实现 — Demo 结果", { x: 0.6, y: 0.3, w: 8, h: 0.6, fontSize: 26, color: NAVY, fontFace: "Calibri", bold: true });
s10.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.03, fill: { color: ACCENT } });

// Table
const headerOpts = { fill: { color: NAVY }, color: WHITE, bold: true, fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle" };
const cellOpts = { fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle", border: { pt: 0.5, color: "DDDDDD" } };
const highlightOpts = { fill: { color: "F5F7FA" }, fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle", border: { pt: 0.5, color: "DDDDDD" } };

s10.addTable([
  [{ text: "策略", options: { ...headerOpts } },
   { text: "收益", options: { ...headerOpts } },
   { text: "风险", options: { ...headerOpts } },
   { text: "夏普", options: { ...headerOpts } },
   { text: "AI权重", options: { ...headerOpts } },
   { text: "债券权重", options: { ...headerOpts } }],
  [{ text: "等权组合", options: { ...cellOpts } },
   { text: "10.0%", options: { ...cellOpts } },
   { text: "12.0%", options: { ...cellOpts } },
   { text: "0.499", options: { ...cellOpts } },
   { text: "33.3%", options: { ...cellOpts } },
   { text: "33.3%", options: { ...cellOpts } }],
  [{ text: "最小方差", options: { ...cellOpts } },
   { text: "5.6%", options: { ...cellOpts } },
   { text: "5.8%", options: { ...cellOpts, color: "1D9E75", bold: true } },
   { text: "0.268", options: { ...cellOpts } },
   { text: "3.4%", options: { ...cellOpts } },
   { text: "92.1%", options: { ...cellOpts, color: "1D9E75", bold: true } }],
  [{ text: "切线组合 T", options: { ...highlightOpts, bold: true, color: "1E2761" } },
   { text: "9.5%", options: { ...highlightOpts } },
   { text: "11.0%", options: { ...highlightOpts } },
   { text: "0.502", options: { ...highlightOpts, color: "F96167", bold: true } },
   { text: "32.6%", options: { ...highlightOpts } },
   { text: "42.7%", options: { ...highlightOpts } }],
  [{ text: "风险平价", options: { ...cellOpts } },
   { text: "7.5%", options: { ...cellOpts } },
   { text: "7.4%", options: { ...cellOpts } },
   { text: "0.466", options: { ...cellOpts } },
   { text: "14.8%", options: { ...cellOpts } },
   { text: "65.7%", options: { ...cellOpts } }],
  [{ text: "限集中度", options: { ...cellOpts } },
   { text: "9.5%", options: { ...cellOpts } },
   { text: "11.0%", options: { ...cellOpts } },
   { text: "0.502", options: { ...cellOpts } },
   { text: "32.6%", options: { ...cellOpts } },
   { text: "42.7%", options: { ...cellOpts } }],
], {
  x: 0.6, y: 1.1, w: 8.8,
  colW: [1.5, 1.2, 1.2, 1.2, 1.5, 1.5],
  rowH: [0.4, 0.35, 0.35, 0.4, 0.35, 0.35],
  border: { pt: 0.5, color: "DDDDDD" },
});

// Code note
s10.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 4.0, w: 8.8, h: 1.2,
  fill: { color: LIGHTBG }, shadow: makeShadow()
});
s10.addText("代码框架", { x: 0.8, y: 4.05, w: 8.4, h: 0.3, fontSize: 13, color: NAVY, fontFace: "Calibri", bold: true });
s10.addText("核心求解器：scipy.optimize.minimize(method='SLSQP')", {
  x: 0.8, y: 4.35, w: 8.4, h: 0.25, fontSize: 11, color: DARK, fontFace: "Consolas" });
s10.addText("文件：asset_allocator.py — 可直接修改 mu / sigma / corr 参数重新运行", {
  x: 0.8, y: 4.65, w: 8.4, h: 0.25, fontSize: 11, color: MUTED, fontFace: "Calibri" });
s10.addText("TradingAgents（选股）→ AssetAllocator（配资）→ 执行决策", {
  x: 0.8, y: 4.9, w: 8.4, h: 0.25, fontSize: 11, color: ACCENT, fontFace: "Calibri", bold: true });

// ======= Slide 11: Summary =======
let s11 = pres.addSlide();
s11.background = { color: NAVY };
s11.addText("总  结", { x: 0.5, y: 0.5, w: 9, h: 0.6, fontSize: 30, color: WHITE, fontFace: "Calibri", bold: true });
s11.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.05, w: 1.5, h: 0.03, fill: { color: ACCENT } });

// Chain
const chainItems = ["马克维茨", "切线组合", "Black-Litterman", "风险平价", "实际约束", "Python"];
chainItems.forEach((item, i) => {
  const x = 0.5 + i * 1.6;
  s11.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.5, w: 1.3, h: 0.7,
    fill: { color: i < 3 ? ICE : ACCENT }
  });
  s11.addText(item, {
    x: x, y: 1.5, w: 1.3, h: 0.7,
    fontSize: 12, color: NAVY, fontFace: "Calibri", bold: true,
    align: "center", valign: "middle", margin: 0
  });
  if (i < chainItems.length - 1) {
    s11.addText("→", {
      x: x + 1.25, y: 1.5, w: 0.4, h: 0.7,
      fontSize: 18, color: WHITE, fontFace: "Calibri", bold: true,
      valign: "middle", margin: 0
    });
  }
});

// Final insight box
s11.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 2.6, w: 9.0, h: 1.6,
  fill: { color: ACCENT }
});
s11.addText("完整交易系统", { x: 0.7, y: 2.7, w: 8.6, h: 0.4, fontSize: 16, color: WHITE, fontFace: "Calibri", bold: true });
s11.addText([
  { text: "TradingAgents", options: { bold: true, color: NAVY } },
  { text: "（LLM 多智能体选股分析）", options: { color: WHITE } },
  { text: "  +  ", options: { color: ICE } },
  { text: "AssetAllocator", options: { bold: true, color: NAVY } },
  { text: "（量化凸优化配资）", options: { color: WHITE } },
  { text: "  =  从选股到组合的全链路决策系统", options: { color: WHITE } },
], { x: 0.7, y: 3.2, w: 8.6, h: 0.8, fontSize: 14, fontFace: "Calibri" });

s11.addText("《量化交易》第4章 · 行者 · 2026-05", {
  x: 0.5, y: 4.8, w: 9, h: 0.4,
  fontSize: 10, color: ICE, fontFace: "Calibri", align: "center"
});

// Save
const outputPath = "C:\\Users\\user\\WorkBuddy\\Claw\\assets\\第4章_资产配置与风险管理.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("PPTX saved to: " + outputPath);
}).catch(err => {
  console.error("Error:", err);
});
