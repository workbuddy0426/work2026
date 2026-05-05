const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "运营";
pres.title = "第1章 概论 - 量化交易：算法、分析、数据、模型和优化";

const C = {
  primary: "1E2761",     // navy
  secondary: "3B82F6",   // blue
  accent: "F59E0B",      // amber
  dark: "0F172A",        // dark bg
  white: "FFFFFF",
  light: "F1F5F9",
  text: "1E293B",
  muted: "64748B",
  cardBg: "F8FAFC",
  border: "E2E8F0",
  purple: "7C3AED",
  teal: "0D9488",
  red: "EF4444",
  green: "10B981",
};
const FT = "Arial Black";
const FB = "Calibri";
const FM = "Consolas";

const mkShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });
const mkBlue = (n) => ({ type: "outer", color: C.primary, blur: n||3, offset: 1, angle: 135, opacity: 0.08 });

// ============================================================
// SLIDE 1: TITLE
// ============================================================
let s1 = pres.addSlide();
s1.background = { color: C.dark };
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s1.addText("第1章 概论", {
  x: 0.8, y: 0.8, w: 8.4, h: 0.6,
  fontSize: 18, fontFace: FB, color: C.accent, margin: 0
});
s1.addText("量化交易：算法、分析、数据、模型和优化", {
  x: 0.8, y: 1.4, w: 8.4, h: 1.2,
  fontSize: 30, fontFace: FT, color: C.white, margin: 0
});
s1.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 2.7, w: 1.8, h: 0.04, fill: { color: C.accent } });
s1.addText([
  { text: "原作：Xin Guo, Tze Leung Lai, Howard Shek, Samuel Wong", options: { breakLine: true } },
  { text: "视觉讲解 · 基于高等教育出版社2020年第1版", options: { fontSize: 11, color: C.muted } }
], {
  x: 0.8, y: 3.0, w: 8.4, h: 1.0,
  fontSize: 13, fontFace: FB, color: C.white, margin: 0
});
s1.addText("Quantitative Trading: Algorithms, Analytics, Data, Models, Optimization", {
  x: 0.8, y: 4.5, w: 8.4, h: 0.5,
  fontSize: 11, fontFace: FM, color: C.muted, italic: true, margin: 0
});

// ============================================================
// SLIDE 2: CHAPTER OVERVIEW
// ============================================================
let s2 = pres.addSlide();
s2.background = { color: C.white };
s2.addText("本章内容一览", {
  x: 0.6, y: 0.3, w: 8.8, h: 0.6,
  fontSize: 28, fontFace: FT, color: C.text, margin: 0
});
s2.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.85, w: 1.2, h: 0.04, fill: { color: C.primary } });

const sections = [
  { num: "1.1", title: "交易基础结构的演变", desc: "从手势喊价到电子交易平台", color: C.primary },
  { num: "1.2", title: "量化交易策略分类", desc: "基本面/宏观/统计套利 三足鼎立", color: C.secondary },
  { num: "1.3", title: "有效市场假说", desc: "EMH vs 统计套利的核心争论", color: C.purple },
  { num: "1.4", title: "基金类型", desc: "量化基金/公募/对冲基金", color: C.teal },
  { num: "1.5", title: "五大主题流程", desc: "数据→分析→模型→优化→算法", color: C.accent },
  { num: "1.6", title: "跨学科性", desc: "计算机·金融·数学·法律", color: C.red },
];

sections.forEach((s, i) => {
  const row = Math.floor(i / 3);
  const col = i % 3;
  const x = 0.5 + col * 3.1;
  const y = 1.3 + row * 1.8;
  
  s2.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 2.9, h: 1.45,
    fill: { color: C.cardBg },
    shadow: mkShadow(),
    line: { color: C.border, width: 0.5 }
  });
  s2.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h: 1.45, fill: { color: s.color } });
  s2.addText(s.num, {
    x: x + 0.2, y: y + 0.15, w: 2.5, h: 0.35,
    fontSize: 11, fontFace: FB, color: s.color, bold: true, margin: 0
  });
  s2.addText(s.title, {
    x: x + 0.2, y: y + 0.5, w: 2.5, h: 0.4,
    fontSize: 13, fontFace: FB, color: C.text, bold: true, margin: 0
  });
  s2.addText(s.desc, {
    x: x + 0.2, y: y + 0.95, w: 2.5, h: 0.4,
    fontSize: 10, fontFace: FB, color: C.muted, margin: 0
  });
});

// ============================================================
// SLIDE 3: 1.1 交易基础结构演变
// ============================================================
let s3 = pres.addSlide();
s3.background = { color: C.white };
s3.addText("1.1 交易基础结构的演变", {
  x: 0.6, y: 0.2, w: 8.8, h: 0.5,
  fontSize: 22, fontFace: FT, color: C.text, margin: 0
});
s3.addText("摘自原书p.1-4 · 从公开喊价到算法交易", {
  x: 0.6, y: 0.7, w: 8.8, h: 0.3,
  fontSize: 11, fontFace: FB, color: C.muted, margin: 0
});
s3.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.0, w: 1.0, h: 0.03, fill: { color: C.primary } });

const stages = [
  { num: "1", title: "公开喊价", years: "1792-1970s", desc: "手势+口头报价\n场内交易\n人工撮合", color: "DC2626" },
  { num: "2", title: "证券报价机", years: "1870s-1980s", desc: "西联电报机\n价格+公司缩写\n纸质卡片清算", color: "2563EB" },
  { num: "3", title: "电子交易", years: "1971-2000s", desc: "1971纳斯达克\n1992CME Globex\n直通式处理STP", color: "059669" },
  { num: "4", title: "算法交易", years: "2000s-至今", desc: "AI自动下单\n高频交易HFT\n微秒级撮合", color: "7C3AED" },
];

stages.forEach((st, i) => {
  const x = 0.3 + i * 2.4;
  s3.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.4, w: 2.15, h: 2.6,
    fill: { color: C.cardBg },
    shadow: mkShadow(),
    line: { color: C.border, width: 0.5 }
  });
  s3.addShape(pres.shapes.RECTANGLE, { x, y: 1.4, w: 2.15, h: 0.45, fill: { color: st.color } });
  s3.addText(`${st.num}`, {
    x: x + 0.1, y: 1.45, w: 0.4, h: 0.35,
    fontSize: 14, fontFace: FT, color: C.white, margin: 0
  });
  s3.addText(st.title, {
    x: x + 0.5, y: 1.45, w: 1.5, h: 0.35,
    fontSize: 13, fontFace: FB, color: C.white, bold: true, margin: 0
  });
  s3.addText(st.years, {
    x: x + 0.15, y: 2.0, w: 1.85, h: 0.3,
    fontSize: 10, fontFace: FB, color: st.color, bold: true, margin: 0
  });
  s3.addText(st.desc, {
    x: x + 0.15, y: 2.35, w: 1.85, h: 1.3,
    fontSize: 10, fontFace: FB, color: C.text, margin: 0, lineSpacingMultiple: 1.5
  });
  
  // Arrow between stages
  if (i < 3) {
    s3.addText("→", {
      x: x + 2.15, y: 2.4, w: 0.25, h: 0.4,
      fontSize: 14, color: C.muted, align: "center", margin: 0
    });
  }
});

s3.addText("原书引用：Powers(1996)\"旧世界的交易池\" — 手势喊价时代的交易细节", {
  x: 0.6, y: 4.2, w: 8.8, h: 0.3,
  fontSize: 9, fontFace: FB, color: C.muted, italic: true, margin: 0
});
s3.addText("核心趋势：交易从\"人与人\"变成\"机器与机器\"，速度从秒级降到微秒级", {
  x: 0.6, y: 4.8, w: 8.8, h: 0.4,
  fontSize: 12, fontFace: FB, color: C.primary, bold: true, margin: 0
});

// ============================================================
// SLIDE 4: 1.1 关键里程碑
// ============================================================
let s4 = pres.addSlide();
s4.background = { color: C.white };
s4.addText("1.1 关键里程碑", {
  x: 0.6, y: 0.2, w: 8.8, h: 0.5,
  fontSize: 22, fontFace: FT, color: C.text, margin: 0
});
s4.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.7, w: 1.0, h: 0.03, fill: { color: C.primary } });

const milestones = [
  { year: "1969", event: "Instinet成立 — 第一家电子通信网络公司(ECN)" },
  { year: "1971", event: "纳斯达克成立 — 第一个电子证券交易市场" },
  { year: "1986", event: "伦敦证券交易所引入电子交易系统" },
  { year: "1992", event: "CME Globex上线 — 首个跨市场电子交易平台" },
  { year: "2006", event: "纽交所(NYSE)引入电子交易系统" },
];

milestones.forEach((m, i) => {
  const y = 1.1 + i * 0.8;
  s4.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: y, w: 1.0, h: 0.5,
    fill: { color: C.primary }
  });
  s4.addText(m.year, {
    x: 0.8, y: y, w: 1.0, h: 0.5,
    fontSize: 13, fontFace: FT, color: C.white, align: "center", valign: "middle", margin: 0
  });
  s4.addShape(pres.shapes.RECTANGLE, {
    x: 1.8, y: y + 0.2, w: 7.4, h: 0.5,
    fill: { color: C.cardBg },
    line: { color: C.border, width: 0.5 }
  });
  s4.addText(m.event, {
    x: 2.0, y: y + 0.2, w: 7.0, h: 0.5,
    fontSize: 12, fontFace: FB, color: C.text, valign: "middle", margin: 0
  });
});

s4.addText("电子交易的核心优势：① 降低交易成本 ② 直通式处理(STP) ③ 全球范围信息传播", {
  x: 0.6, y: 5.0, w: 8.8, h: 0.4,
  fontSize: 11, fontFace: FB, color: C.primary, bold: true, margin: 0
});

// ============================================================
// SLIDE 5: 1.2 量化策略分类
// ============================================================
let s5 = pres.addSlide();
s5.background = { color: C.white };
s5.addText("1.2 量化交易策略分类与时间跨度", {
  x: 0.6, y: 0.2, w: 8.8, h: 0.5,
  fontSize: 22, fontFace: FT, color: C.text, margin: 0
});
s5.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.7, w: 1.0, h: 0.03, fill: { color: C.primary } });

const sTypes = [
  { 
    title: "基本面量化 (FMQ)", en: "Fundamental Quant", 
    span: "时间跨度：一个季度", color: C.primary,
    points: ["按季度财报驱动", "价值低估→买入", "高估→卖出", "指标：收益质量、公司价值、投资者情绪"],
    sources: "摘自原书p.6"
  },
  { 
    title: "全球宏观策略", en: "Global Macro", 
    span: "时间跨度：一个月", color: C.teal,
    points: ["利用宏观事件和趋势", "酌情型 vs 系统型", "如美元上涨→买入美元", "29天国债周期驱动"],
    sources: "摘自原书p.6-7"
  },
  { 
    title: "收敛/统计套利", en: "Stat Arb / Convergence", 
    span: "时间跨度：分钟~天", color: C.accent,
    points: ["相似资产价格趋向收敛", "配对交易策略", "做多低估+做空高估", "允许负收益，期望收益为正"],
    sources: "摘自原书p.7"
  },
];

sTypes.forEach((t, i) => {
  const x = 0.3 + i * 3.2;
  s5.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.0, w: 3.0, h: 3.5,
    fill: { color: C.cardBg },
    shadow: mkShadow(),
    line: { color: C.border, width: 0.5 }
  });
  s5.addShape(pres.shapes.RECTANGLE, { x, y: 1.0, w: 3.0, h: 0.06, fill: { color: t.color } });
  s5.addText(t.title, {
    x: x + 0.2, y: 1.25, w: 2.6, h: 0.35,
    fontSize: 12, fontFace: FB, color: t.color, bold: true, margin: 0
  });
  s5.addText(t.en, {
    x: x + 0.2, y: 1.6, w: 2.6, h: 0.25,
    fontSize: 9, fontFace: FB, color: C.muted, italic: true, margin: 0
  });
  s5.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.2, y: 2.0, w: 2.6, h: 0.35,
    fill: { color: t.color, transparency: 90 }
  });
  s5.addText(t.span, {
    x: x + 0.3, y: 2.0, w: 2.4, h: 0.35,
    fontSize: 10, fontFace: FB, color: t.color, bold: true, valign: "middle", margin: 0
  });
  
  const pts = t.points.map((p, j) => ({
    text: p,
    options: { bullet: true, breakLine: j < t.points.length - 1, fontSize: 10, color: C.text, paraSpaceAfter: 4 }
  }));
  s5.addText(pts, {
    x: x + 0.2, y: 2.55, w: 2.6, h: 1.7,
    fontFace: FB, valign: "top", margin: 0
  });
  
  s5.addText(t.sources, {
    x: x + 0.2, y: 4.2, w: 2.6, h: 0.2,
    fontSize: 8, fontFace: FB, color: C.muted, italic: true, margin: 0
  });
});

// ============================================================
// SLIDE 6: 1.3 有效市场假说 vs 统计套利
// ============================================================
let s6 = pres.addSlide();
s6.background = { color: C.white };
s6.addText("1.3 有效市场假说(EMH) vs 统计套利(StatArb)", {
  x: 0.6, y: 0.2, w: 8.8, h: 0.5,
  fontSize: 20, fontFace: FT, color: C.text, margin: 0
});
s6.addText("本书最核心的学术争论", {
  x: 0.6, y: 0.7, w: 8.8, h: 0.3,
  fontSize: 11, fontFace: FB, color: C.muted, margin: 0
});
s6.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.0, w: 1.0, h: 0.03, fill: { color: C.primary } });

// Left: EMH
s6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.3, w: 4.2, h: 3.0,
  fill: { color: "FEF2F2" },
  shadow: mkShadow(),
  line: { color: C.red, width: 0.5 }
});
s6.addText("有效市场假说", {
  x: 0.7, y: 1.4, w: 3.8, h: 0.4,
  fontSize: 14, fontFace: FB, color: C.red, bold: true, margin: 0
});
s6.addText("Eugene Fama (1970)", {
  x: 0.7, y: 1.8, w: 3.8, h: 0.3,
  fontSize: 10, fontFace: FB, color: C.muted, italic: true, margin: 0
});
s6.addText([
  { text: "市场价格反映所有可获得的信息", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "个体对市场预期是随机的", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "无法通过分析获得超额收益", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "三类：弱/半强式/强式有效", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "实证检验结果纷杂，无统一结论", options: { bullet: true, fontSize: 10, color: C.muted } }
], {
  x: 0.7, y: 2.2, w: 3.8, h: 2.0,
  fontFace: FB, valign: "top", margin: 0, lineSpacingMultiple: 1.6
});

// VS
s6.addText("⚡", {
  x: 4.7, y: 2.5, w: 0.6, h: 0.6,
  fontSize: 24, align: "center", valign: "middle", margin: 0
});

// Right: StatArb
s6.addShape(pres.shapes.RECTANGLE, {
  x: 5.3, y: 1.3, w: 4.2, h: 3.0,
  fill: { color: "ECFDF5" },
  shadow: mkShadow(),
  line: { color: C.green, width: 0.5 }
});
s6.addText("统计套利", {
  x: 5.5, y: 1.4, w: 3.8, h: 0.4,
  fontSize: 14, fontFace: FB, color: C.green, bold: true, margin: 0
});
s6.addText("Bondarenko (2003)", {
  x: 5.5, y: 1.8, w: 3.8, h: 0.3,
  fontSize: 10, fontFace: FB, color: C.muted, italic: true, margin: 0
});
s6.addText([
  { text: "市场中存在统计套利机会(SAO)", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "金融资产存在错误定价", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "利用统计方法获利（期望收益为正）", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "允许单次负收益，但长期为正", options: { bullet: true, breakLine: true, fontSize: 11 } },
  { text: "排除SAO会对价格产生鞅式影响", options: { bullet: true, fontSize: 10, color: C.muted } }
], {
  x: 5.5, y: 2.2, w: 3.8, h: 2.0,
  fontFace: FB, valign: "top", margin: 0, lineSpacingMultiple: 1.6
});

s6.addText("原书p.8: Cowles(1933,1944)实证研究表明专业投资者很难获得高于市场的收益", {
  x: 0.6, y: 4.5, w: 8.8, h: 0.3,
  fontSize: 9, fontFace: FB, color: C.muted, italic: true, margin: 0
});
s6.addText("核心问题：市场到底有没有免费午餐？ → 这就是量化交易存在的理由", {
  x: 0.6, y: 4.9, w: 8.8, h: 0.4,
  fontSize: 12, fontFace: FB, color: C.primary, bold: true, margin: 0
});

// ============================================================
// SLIDE 7: 1.5 五大主题
// ============================================================
let s7 = pres.addSlide();
s7.background = { color: C.white };
s7.addText("1.5 量化交易的五大主题（本书副标题）", {
  x: 0.6, y: 0.2, w: 8.8, h: 0.5,
  fontSize: 20, fontFace: FT, color: C.text, margin: 0
});
s7.addText("封面排序 = 量化交易流程顺序", {
  x: 0.6, y: 0.65, w: 8.8, h: 0.25,
  fontSize: 10, fontFace: FB, color: C.muted, margin: 0
});
s7.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.9, w: 1.0, h: 0.03, fill: { color: C.primary } });

const pillars = [
  { num: "①", title: "数据", en: "Data", color: "1E2761", items: "行情数据\nLOB数据\nTAQ数据\n财报数据\n另类数据" },
  { num: "②", title: "分析", en: "Analytics", color: "2563EB", items: "时间序列分析\n因子分析\n波动率估计\n统计推断\nEpps效应" },
  { num: "③", title: "模型", en: "Models", color: "059669", items: "定价模型\n风险模型\n预测模型\n行为模型\n机器学习" },
  { num: "④", title: "优化", en: "Optimization", color: "D97706", items: "组合优化\n执行优化\n参数调优\n在线学习\n随机控制" },
  { num: "⑤", title: "算法", en: "Algorithms", color: "DC2626", items: "订单执行\n做市算法\n套利算法\n订单拆分\nHFT算法" },
];

pillars.forEach((p, i) => {
  const x = 0.2 + i * 1.95;
  s7.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.2, w: 1.8, h: 3.0,
    fill: { color: C.cardBg },
    shadow: mkShadow(),
    line: { color: C.border, width: 0.5 }
  });
  s7.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 1.8, h: 0.5, fill: { color: p.color } });
  s7.addText(`${p.num} ${p.title}`, {
    x: x + 0.1, y: 1.25, w: 1.6, h: 0.4,
    fontSize: 13, fontFace: FB, color: C.white, bold: true, margin: 0
  });
  s7.addText(p.en, {
    x: x + 0.1, y: 1.85, w: 1.6, h: 0.25,
    fontSize: 9, fontFace: FB, color: p.color, italic: true, margin: 0
  });
  s7.addText(p.items, {
    x: x + 0.1, y: 2.15, w: 1.6, h: 1.8,
    fontSize: 9, fontFace: FB, color: C.text, margin: 0, lineSpacingMultiple: 1.5
  });
  
  // Arrow
  if (i < 4) {
    s7.addText("→", {
      x: x + 1.8, y: 2.3, w: 0.15, h: 0.4,
      fontSize: 12, color: C.muted, align: "center", margin: 0
    });
  }
});

s7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.45, w: 9.0, h: 0.8,
  fill: { color: "F1F5F9" },
  line: { color: C.border, width: 0.5 }
});
s7.addText([
  { text: "\"用于分析的机器首先需要导入数据，然后利用模型和优化程序来开发量化交易策略。算法交易是指利用算法在电子化交易平台上执行包含交易时间、价格、数量等信息的策略。\"", options: { fontSize: 9, italic: true } },
  { text: " — 原书p.10-11", options: { fontSize: 8, color: C.muted } }
], {
  x: 0.7, y: 4.5, w: 8.6, h: 0.7,
  fontFace: FB, color: C.text, valign: "middle", margin: 0
});

// ============================================================
// SLIDE 8: 1.4+1.6 补充
// ============================================================
let s8 = pres.addSlide();
s8.background = { color: C.white };
s8.addText("1.4 基金类型  ·  1.6 跨学科性", {
  x: 0.6, y: 0.2, w: 8.8, h: 0.5,
  fontSize: 22, fontFace: FT, color: C.text, margin: 0
});
s8.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.7, w: 1.0, h: 0.03, fill: { color: C.primary } });

// Fund types
s8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 4.5, h: 2.0,
  fill: { color: C.cardBg },
  shadow: mkShadow(),
  line: { color: C.border, width: 0.5 }
});
s8.addText("基金类型（原书p.8-10）", {
  x: 0.7, y: 1.15, w: 4.1, h: 0.35,
  fontSize: 12, fontFace: FB, color: C.primary, bold: true, margin: 0
});
s8.addText([
  { text: "量化基金 — 使用量化策略的投资基金", options: { bullet: true, breakLine: true, fontSize: 10 } },
  { text: "公募基金 — 向公众出售，开放型/封闭型", options: { bullet: true, breakLine: true, fontSize: 10 } },
  { text: "ETF — 交易所交易基金，净值紧密跟踪", options: { bullet: true, breakLine: true, fontSize: 10 } },
  { text: "对冲基金 — 私人合伙制，开放式", options: { bullet: true, fontSize: 10 } }
], {
  x: 0.7, y: 1.55, w: 4.1, h: 1.5,
  fontFace: FB, valign: "top", margin: 0, lineSpacingMultiple: 1.5
});

// Cross-disciplinarity
s8.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 2.0,
  fill: { color: C.cardBg },
  shadow: mkShadow(),
  line: { color: C.border, width: 0.5 }
});
s8.addText("跨学科性（原书p.11）", {
  x: 5.4, y: 1.15, w: 3.9, h: 0.35,
  fontSize: 12, fontFace: FB, color: C.primary, bold: true, margin: 0
});
s8.addText([
  { text: "计算机科学与工程 — 编程+算力", options: { bullet: true, breakLine: true, fontSize: 10 } },
  { text: "金融与经济 — 资产定价+风险管理", options: { bullet: true, breakLine: true, fontSize: 10 } },
  { text: "数学与统计 — 建模+推断+优化", options: { bullet: true, breakLine: true, fontSize: 10 } },
  { text: "法律 — 监管+合规+市场规则", options: { bullet: true, fontSize: 10 } }
], {
  x: 5.4, y: 1.55, w: 3.9, h: 1.5,
  fontFace: FB, valign: "top", margin: 0, lineSpacingMultiple: 1.5
});

// Performance metrics
s8.addText("基金业绩评估指标（原书p.9-10）", {
  x: 0.6, y: 3.3, w: 8.8, h: 0.35,
  fontSize: 12, fontFace: FB, color: C.primary, bold: true, margin: 0
});

const metrics = [
  { name: "Sharpe比率", formula: "(μ - rf) / σ", desc: "单位总风险的超额回报" },
  { name: "信息比率IR", formula: "(μ - μB) / σ(r-rB)", desc: "相对基准的超额回报" },
  { name: "Jensen指数", formula: "r - rf = α + β(μM-rf)", desc: "CAPM回归中的截距α" },
  { name: "Sortino比率", formula: "(μ - τ) / στ-", desc: "只考虑下行风险" },
];

metrics.forEach((m, i) => {
  const x = 0.3 + i * 2.4;
  s8.addShape(pres.shapes.RECTANGLE, {
    x, y: 3.8, w: 2.2, h: 1.3,
    fill: { color: C.cardBg },
    line: { color: C.border, width: 0.5 }
  });
  s8.addText(m.name, {
    x: x + 0.1, y: 3.85, w: 2.0, h: 0.3,
    fontSize: 11, fontFace: FB, color: C.primary, bold: true, margin: 0
  });
  s8.addText(m.formula, {
    x: x + 0.1, y: 4.15, w: 2.0, h: 0.3,
    fontSize: 9, fontFace: FM, color: C.text, margin: 0
  });
  s8.addText(m.desc, {
    x: x + 0.1, y: 4.45, w: 2.0, h: 0.3,
    fontSize: 9, fontFace: FB, color: C.muted, margin: 0
  });
});

// ============================================================
// SLIDE 9: 原书引用+核心框架
// ============================================================
let s9 = pres.addSlide();
s9.background = { color: C.dark };
s9.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });

s9.addText("第1章 核心框架", {
  x: 0.8, y: 0.6, w: 8.4, h: 0.6,
  fontSize: 26, fontFace: FT, color: C.white, margin: 0
});
s9.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 1.2, w: 1.5, h: 0.04, fill: { color: C.accent } });

s9.addText([
  { text: "交易模式的演变", options: { breakLine: true, fontSize: 13, bold: true, color: C.accent } },
  { text: "公开喊价 → 报价机 → 电子交易 → 算法交易", options: { breakLine: true, fontSize: 11, color: C.white, paraSpaceAfter: 8 } },
  { text: "策略的时间维度", options: { breakLine: true, fontSize: 13, bold: true, color: C.accent } },
  { text: "基本面(季度) · 宏观(月度) · 统计套利(分钟~天)", options: { breakLine: true, fontSize: 11, color: C.white, paraSpaceAfter: 8 } },
  { text: "核心学术争论", options: { breakLine: true, fontSize: 13, bold: true, color: C.accent } },
  { text: "有效市场(EMH) vs 统计套利(StatArb)", options: { breakLine: true, fontSize: 11, color: C.white, paraSpaceAfter: 8 } },
  { text: "五大主题流程", options: { breakLine: true, fontSize: 13, bold: true, color: C.accent } },
  { text: "数据 → 分析 → 模型 → 优化 → 算法", options: { fontSize: 11, color: C.white } }
], {
  x: 0.8, y: 1.5, w: 8.4, h: 3.5,
  fontFace: FB, margin: 0, lineSpacingMultiple: 1.2
});

s9.addText("原书网址：http://lait.web.stanford.edu/quantstratbook/", {
  x: 0.8, y: 4.9, w: 8.4, h: 0.3,
  fontSize: 10, fontFace: FB, color: C.muted, margin: 0
});

// ============================================================
// SLIDE 10: THANK YOU
// ============================================================
let s10 = pres.addSlide();
s10.background = { color: C.dark };
s10.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s10.addText("第1章 · 完", {
  x: 1, y: 1.5, w: 8, h: 1.0,
  fontSize: 36, fontFace: FT, color: C.white, align: "center", margin: 0
});
s10.addShape(pres.shapes.RECTANGLE, { x: 4.2, y: 2.5, w: 1.6, h: 0.04, fill: { color: C.accent } });
s10.addText("量化交易必须先从理解交易本身开始", {
  x: 1, y: 2.8, w: 8, h: 0.5,
  fontSize: 16, fontFace: FB, color: C.accent, align: "center", margin: 0
});
s10.addText("下一章：量化交易中的统计模型与方法", {
  x: 1, y: 3.5, w: 8, h: 0.5,
  fontSize: 13, fontFace: FB, color: C.muted, align: "center", margin: 0
});

// ============================================================
// WRITE
// ============================================================
const outPath = "C:/Users/user/WorkBuddy/Claw/乌龙指研究/第1章_概论_视觉讲解.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("✅ 已生成: " + outPath));
