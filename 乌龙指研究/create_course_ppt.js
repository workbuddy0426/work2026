const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "运营";
pres.title = "量化交易入门 - 12课课程";

// === Color Palette ===
const C = {
  primary: "028090",   // teal
  secondary: "00A896", // seafoam  
  accent: "02C39A",    // mint
  dark: "1A1A2E",      // dark bg
  white: "FFFFFF",
  light: "F0FDFA",     // very light teal
  text: "1E293B",      // dark text
  muted: "64748B",     // gray text
  cardBg: "F8FAFC",
  border: "E2E8F0",
  red: "EF4444",
  green: "10B981",
  amber: "F59E0B",
  purple: "8B5CF6",
  blue: "3B82F6",
};

const FONT_TITLE = "Arial Black";
const FONT_BODY = "Calibri";
const FONT_MONO = "Consolas";

// === Helper: makeShadow ===
const mkShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });

// ============================================================
// SLIDE 1: TITLE
// ============================================================
let s1 = pres.addSlide();
s1.background = { color: C.dark };
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: C.dark }
});
s1.addText("量化交易入门", {
  x: 0.8, y: 1.2, w: 8.4, h: 1.2,
  fontSize: 44, fontFace: FONT_TITLE, color: C.white, bold: true, margin: 0
});
s1.addText("初中生也能听懂 · 12课从零到实战", {
  x: 0.8, y: 2.5, w: 8.4, h: 0.6,
  fontSize: 20, fontFace: FONT_BODY, color: C.accent, margin: 0
});
s1.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 3.3, w: 2, h: 0.04, fill: { color: C.accent } });
s1.addText([
  { text: "Python抓价格 · 套利监控 · 多因子选股 · 风控系统", options: { breakLine: true } },
  { text: "", options: { breakLine: true, fontSize: 12 } },
  { text: "基于《量化交易：算法、分析、数据、模型和优化》", options: { fontSize: 11, color: C.muted } }
], {
  x: 0.8, y: 3.6, w: 8.4, h: 1.0,
  fontSize: 14, fontFace: FONT_BODY, color: C.white, margin: 0
});

// ============================================================
// SLIDE 2: COURSE OVERVIEW
// ============================================================
let s2 = pres.addSlide();
s2.background = { color: C.white };
s2.addText("课程总览", {
  x: 0.6, y: 0.3, w: 8.8, h: 0.7,
  fontSize: 32, fontFace: FONT_TITLE, color: C.dark, margin: 0
});
s2.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.95, w: 1.5, h: 0.04, fill: { color: C.primary } });

const phases = [
  { title: "阶段一：认识市场", lessons: "第1课 交易是什么\n第2课 价格怎么来的\n第3课  Python抓行情", color: C.primary },
  { title: "阶段二：套利基础", lessons: "第4课 价差和套利\n第5课 均值回归\n第6课 价差监控器", color: C.blue },
  { title: "阶段三：选股系统", lessons: "第7课 PE/PB/ROE\n第8课 多因子打分\n第9课 选股打分器", color: C.purple },
  { title: "阶段四：完整系统", lessons: "第10课 回测\n第11课 风控\n第12课 毕业设计", color: C.amber },
];

phases.forEach((p, i) => {
  const x = 0.4 + i * 2.35;
  s2.addShape(pres.shapes.RECTANGLE, { 
    x, y: 1.3, w: 2.15, h: 3.4, 
    fill: { color: C.cardBg }, 
    shadow: mkShadow(),
    line: { color: C.border, width: 0.5 }
  });
  s2.addShape(pres.shapes.RECTANGLE, { x, y: 1.3, w: 2.15, h: 0.06, fill: { color: p.color } });
  s2.addText(p.title, {
    x: x + 0.15, y: 1.55, w: 1.85, h: 0.5,
    fontSize: 13, fontFace: FONT_BODY, color: p.color, bold: true, margin: 0
  });
  s2.addText(p.lessons, {
    x: x + 0.15, y: 2.2, w: 1.85, h: 2.2,
    fontSize: 11, fontFace: FONT_BODY, color: C.text, margin: 0, lineSpacingMultiple: 1.5
  });
});

s2.addText("🎓 从零到跑通第一个量化监控系统", {
  x: 0.6, y: 4.9, w: 8.8, h: 0.5,
  fontSize: 14, fontFace: FONT_BODY, color: C.muted, italic: true, margin: 0
});

// ============================================================
// LESSON SLIDES (3-14)
// ============================================================
const lessons = [
  {
    num: "01", title: "交易是什么？",
    subtitle: "从菜市场到股票交易所",
    points: [
      "交易本质：一个人想卖，一个人想买，价格谈拢 → 成交",
      "菜市场：你问价 → 老板报价 → 砍价 → 成交",
      "交易所：你下单 → 系统查价 → 匹配 → 成交",
      "限价单：\"我只出这个价，爱卖不卖\" → 挂单排队",
      "市价单：\"现在就要！\" → 立刻吃掉最便宜的卖单",
      "价格优先 + 时间优先 = 排队规则"
    ],
    keyConcept: "价格优先 · 时间优先",
    emoji: "🤝"
  },
  {
    num: "02", title: "价格是怎么来的",
    subtitle: "供需关系 + K线图",
    points: [
      "想买的人 > 想卖的人 → 价格涨 (供不应求)",
      "想卖的人 > 想买的人 → 价格跌 (供过于求)",
      "K线 = 一个时间段的\"体温计\"",
      "一根K线包含：开盘价 / 收盘价 / 最高价 / 最低价",
      "红色 = 收盘 > 开盘 (涨了)",
      "量化交易者写代码直接连行情源，比看手机快几百倍"
    ],
    keyConcept: "供需决定价格 · K线四价",
    emoji: "📈"
  },
  {
    num: "03", title: "动手抓第一个行情",
    subtitle: "Python脚本获取实时比特币价格",
    points: [
      "API = 程序问服务器要数据的\"接口\"",
      "HTTP请求 → 服务器返回JSON → 提取价格",
      "只用20行代码：从3个数据源同时抓价格",
      "CoinGecko / 币安 / OKX 三源对比",
      "bps (基点) = 万分之一，金融圈常用单位",
      "第一次让电脑代替人眼看价格！"
    ],
    keyConcept: "API · JSON · 多源比价",
    emoji: "🐍",
    code: "get_price.py"
  },
  {
    num: "04", title: "套利和价差",
    subtitle: "低买高卖的数学原理",
    points: [
      "套利 = 同一个东西在不同地方价格不同 → 白赚差价",
      "价差 = 贵的 - 便宜的 (绝对价差)",
      "bps = 价差 ÷ 均价 × 10000 (相对价差)",
      "币安 vs OKX 价差通常 < 1 bps (被机器搬平了)",
      "市场剧烈波动时价差会\"裂开\"——窗口出现",
      "谁最快发现价差，谁就赚钱 (速度竞赛)"
    ],
    keyConcept: "价差 · bps · 套利窗口",
    emoji: "💰"
  },
  {
    num: "05", title: "均值回归",
    subtitle: "物极必反的数学原理",
    points: [
      "皮筋理论：拉得越远，弹回来的力气越大",
      "价格总是在均值上下晃荡",
      "涨太多 → 想卖的人增多 → 价格跌回来",
      "跌太多 → 想买的人增多 → 价格涨回去",
      "移动平均线(MA) = 过去N天的平均价格",
      "上轨卖出，下轨买入，等价格回到均值平仓"
    ],
    keyConcept: "均值回归 · 布林带 · 移动平均",
    emoji: "🎯"
  },
  {
    num: "06", title: "价差监控器",
    subtitle: "自动扫描，异常报警",
    points: [
      "把第3课的脚本升级：加循环 → 自动反复查",
      "每10秒扫描一次，发现价差过大就报警",
      "设置报警阈值 (如10 bps以上标记\"⚠️ 警报\")",
      "三个数据源同时对比 (CoinGecko/币安/OKX)",
      "在后台24小时自动运行，异常自动发现",
      "这就是量化自动化的第一步！"
    ],
    keyConcept: "自动循环 · 阈值报警 · 多源对比",
    emoji: "🔁",
    code: "spread_monitor.py"
  },
  {
    num: "07", title: "PE / PB / ROE",
    subtitle: "三个指标看懂一家公司",
    points: [
      "PE (市盈率) = 股价 ÷ 每股利润 = 回本需要多少年",
      "PB (市净率) = 股价 ÷ 每股净资产 = 溢价了几倍",
      "ROE (净资产收益率) = 净利润 ÷ 净资产 = 赚钱效率",
      "ROE是三个指标中最重要的！巴菲特最爱看它",
      "好公司画像：ROE > 15% + PE合理 + PB正常",
      "便宜的股票 ≠ 好股票 (小心\"价值陷阱\")"
    ],
    keyConcept: "PE(回本) · PB(溢价) · ROE(赚钱能力)",
    emoji: "📊"
  },
  {
    num: "08", title: "多因子打分",
    subtitle: "像考试一样给股票排名",
    points: [
      "多因子打分 = 给股票\"期末考试\"，多个科目分别打分",
      "ROE 40分 + PE 30分 + PB 15分 + 动量 15分 = 100分",
      "权重设计：ROE最高(40分) 因为最能体现公司质量",
      "打分规则：if-else 条件判断，初中数学水平",
      "专业量化基金用几十到上百个因子",
      "可回测验证：过去按这个打分选的股票涨没涨？"
    ],
    keyConcept: "因子权重 · 总分排名 · 量化选股",
    emoji: "📋"
  },
  {
    num: "09", title: "选股打分器",
    subtitle: "Python自动排名",
    points: [
      "代码 = 股票池 → 逐项打分 → 算总分 → 排名输出",
      "score_roe / score_pe / score_pb 等判断函数",
      "用真实数据：茅台ROE满分，招行PE便宜提分",
      "小米三项均衡后来居上，腾讯差1分惜败",
      "排序算法：results.sort(reverse=True) 一行搞定",
      "可以加入任意股票，一键排名！"
    ],
    keyConcept: "评分函数 · 排序算法 · 实时排名",
    emoji: "💻",
    code: "stock_scorer.py"
  },
  {
    num: "10", title: "回测",
    subtitle: "先模拟再实战",
    points: [
      "回测 = 用历史数据\"假装交易\"，看策略赚不赚钱",
      "和模拟考试一样：做往年真题→估分→调整",
      "过拟合(Overfitting)：背答案式调参数→实战亏光",
      "回测三谎言：只看上涨行情 / 反复调参 / 忽略手续费",
      "解决方法：样本外测试(80%调参+20%验证)",
      "公式：回测年化 = (每次收益率之和) ÷ 交易次数"
    ],
    keyConcept: "历史模拟 · 过拟合 · 样本外测试",
    emoji: "🎲"
  },
  {
    num: "11", title: "风险控制",
    subtitle: "先想好怎么亏钱",
    points: [
      "交易第一原则：不是谁赚得多，而是谁活得久",
      "止损：每笔交易设最大亏损 (如8%) → 到了就割肉",
      "仓位：单只股票不超过总资金20% → 分散风险",
      "回撤控制：总账户亏到15% → 停手反思",
      "亏50%需要涨100%才能回本 → 别大亏",
      "每次都执行：先定止损→再想仓位→最后算收益"
    ],
    keyConcept: "止损 · 仓位 · 回撤控制",
    emoji: "🛡️"
  },
  {
    num: "12", title: "毕业设计",
    subtitle: "跑通第一个量化监控系统",
    points: [
      "合体！行情采集 + 策略分析 + 风控 + 日志",
      "quant_monitor.py = 完整的自动化系统",
      "每30秒：抓3个源 → 算价差 → 风控检查 → 记录日志",
      "零错误运行！这是你的毕业成果 🎓",
      "下一步：接入微信通知 / 加更多品种 / 实盘",
      "你已经比90%的股民更懂交易背后的逻辑了！"
    ],
    keyConcept: "全系统整合 · 自动化运行",
    emoji: "🎓",
    code: "quant_monitor.py"
  }
];

lessons.forEach((l, idx) => {
  let slide = pres.addSlide();
  slide.background = { color: C.white };

  // Left accent bar
  slide.addShape(pres.shapes.RECTANGLE, { 
    x: 0, y: 0, w: 0.08, h: 5.625, fill: { color: C.primary } 
  });

  // Header
  slide.addText(`第${l.num}课`, {
    x: 0.4, y: 0.25, w: 1.5, h: 0.4,
    fontSize: 12, fontFace: FONT_BODY, color: C.primary, bold: true, margin: 0
  });
  slide.addText(l.title, {
    x: 0.4, y: 0.6, w: 6, h: 0.6,
    fontSize: 28, fontFace: FONT_TITLE, color: C.dark, margin: 0
  });
  slide.addText(l.subtitle, {
    x: 0.4, y: 1.15, w: 6, h: 0.35,
    fontSize: 14, fontFace: FONT_BODY, color: C.muted, margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, { 
    x: 0.4, y: 1.55, w: 1.2, h: 0.03, fill: { color: C.primary } 
  });

  // Content points
  const contentText = l.points.map((p, i) => ({
    text: `${i < 9 ? "0" + (i+1) : i+1}. ${p}`,
    options: { breakLine: true, fontSize: 12, color: C.text, paraSpaceAfter: 6 }
  }));

  slide.addText(contentText, {
    x: 0.4, y: 1.8, w: 6.5, h: 3.2,
    fontFace: FONT_BODY, valign: "top", margin: 0, lineSpacingMultiple: 1.3
  });

  // Right panel - Key Concept
  slide.addShape(pres.shapes.RECTANGLE, { 
    x: 7.2, y: 0.8, w: 2.5, h: 1.8, 
    fill: { color: C.light },
    line: { color: C.primary, width: 0.5 },
    shadow: mkShadow()
  });
  slide.addText("核心概念", {
    x: 7.4, y: 0.95, w: 2.1, h: 0.35,
    fontSize: 10, fontFace: FONT_BODY, color: C.primary, bold: true, margin: 0
  });
  slide.addText(l.keyConcept, {
    x: 7.4, y: 1.3, w: 2.1, h: 1.1,
    fontSize: 12, fontFace: FONT_BODY, color: C.dark, margin: 0, valign: "top"
  });

  // Right panel - File/Emoji
  if (l.code) {
    slide.addShape(pres.shapes.RECTANGLE, { 
      x: 7.2, y: 2.8, w: 2.5, h: 1.0, 
      fill: { color: "F1F5F9" },
      line: { color: C.border, width: 0.5 }
    });
    slide.addText("📁 对应文件", {
      x: 7.4, y: 2.9, w: 2.1, h: 0.3,
      fontSize: 10, fontFace: FONT_BODY, color: C.muted, bold: true, margin: 0
    });
    slide.addText(l.code, {
      x: 7.4, y: 3.2, w: 2.1, h: 0.4,
      fontSize: 11, fontFace: FONT_MONO, color: C.primary, margin: 0
    });
  }

  // Bottom emoji
  slide.addText(l.emoji, {
    x: 7.2, y: 4.6, w: 2.5, h: 0.6,
    fontSize: 32, align: "center", margin: 0
  });
});

// ============================================================
// FINAL SLIDE: GRADUATION
// ============================================================
let sf = pres.addSlide();
sf.background = { color: C.dark };
sf.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
sf.addText("🎓", {
  x: 3.5, y: 0.8, w: 3, h: 1.2,
  fontSize: 60, align: "center", margin: 0
});
sf.addText("恭喜毕业！", {
  x: 1, y: 2.0, w: 8, h: 0.8,
  fontSize: 36, fontFace: FONT_TITLE, color: C.white, align: "center", margin: 0
});
sf.addShape(pres.shapes.RECTANGLE, { x: 4, y: 2.8, w: 2, h: 0.04, fill: { color: C.accent } });
sf.addText("你已经完成了12课量化交易入门课程", {
  x: 1, y: 3.1, w: 8, h: 0.5,
  fontSize: 16, fontFace: FONT_BODY, color: C.accent, align: "center", margin: 0
});
sf.addText([
  { text: "✅ Python抓取实时行情", options: { breakLine: true } },
  { text: "✅ 价差套利分析", options: { breakLine: true } },
  { text: "✅ 多因子选股打分", options: { breakLine: true } },
  { text: "✅ 自动监控系统", options: { breakLine: true } },
  { text: "✅ 风险控制意识", options: {} }
], {
  x: 2.5, y: 3.7, w: 5, h: 1.6,
  fontSize: 13, fontFace: FONT_BODY, color: C.white, align: "center",
  lineSpacingMultiple: 1.6, margin: 0
});

// ============================================================
// WRITE FILE
// ============================================================
const outPath = "C:/Users/user/WorkBuddy/Claw/乌龙指研究/量化交易入门_12课课程.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("✅ PPT已生成: " + outPath));
