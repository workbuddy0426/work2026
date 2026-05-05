const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "运营";
pres.title = "第3章 积极型投资组合管理和投资策略";

const C = {
  primary: "1E2761", secondary: "3B82F6", accent: "F59E0B",
  dark: "0F172A", white: "FFFFFF", light: "F1F5F9",
  text: "1E293B", muted: "64748B", cardBg: "F8FAFC",
  border: "E2E8F0", purple: "7C3AED", teal: "0D9488",
  red: "EF4444", green: "10B981", amber: "D97706",
};
const FT = "Arial Black"; const FB = "Calibri";
const mkShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });
function addHeader(s, t, sub) {
  s.background = { color: C.white };
  s.addText(t, { x: 0.6, y: 0.2, w: 8.8, h: 0.5, fontSize: 20, fontFace: FT, color: C.text, margin: 0 });
  if (sub) s.addText(sub, { x: 0.6, y: 0.65, w: 8.8, h: 0.25, fontSize: 10, fontFace: FB, color: C.muted, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.9, w: 1.0, h: 0.03, fill: { color: C.primary } });
}
function addCard(s, x, y, w, h, color, items, title, opts) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.cardBg }, shadow: mkShadow(), line: { color: C.border, width: 0.5 } });
  if (color) s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.06, fill: { color } });
  if (title) s.addText(title, { x: x + 0.1, y: y + 0.15, w: w - 0.2, h: 0.35, fontSize: 11, fontFace: FB, color: C.text, bold: true, margin: 0 });
  if (items) {
    const txt = items.map((t, j) => ({ text: t, options: { bullet: !opts?.noBullet, breakLine: j < items.length - 1, fontSize: opts?.fs || 10, color: C.text, paraSpaceAfter: 3 } }));
    s.addText(txt, { x: x + 0.1, y: y + (title ? 0.55 : 0.15), w: w - 0.2, h: h - (title ? 0.7 : 0.3), fontFace: FB, valign: "top", margin: 0 });
  }
}

// S1: Title
let s1 = pres.addSlide(); s1.background = { color: C.dark };
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s1.addText("第3章", { x: 0.8, y: 0.8, w: 8.4, h: 0.5, fontSize: 16, fontFace: FB, color: C.accent, margin: 0 });
s1.addText("积极型投资组合管理\n和投资策略", { x: 0.8, y: 1.3, w: 8.4, h: 1.2, fontSize: 26, fontFace: FT, color: C.white, margin: 0 });
s1.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 2.6, w: 1.8, h: 0.04, fill: { color: C.accent } });
s1.addText("α和β · 奇异β · 交易成本\n多期投资组合 · Samuelson-Merton · 波动率脉动", {
  x: 0.8, y: 2.9, w: 8.4, h: 1.2, fontSize: 12, fontFace: FB, color: C.white, margin: 0, lineSpacingMultiple: 1.5
});

// S2: Alpha Beta
let s2 = pres.addSlide();
addHeader(s2, "3.1 α（阿尔法）和 β（贝塔）", "原书p.58-60 · 积极型投资组合管理的基础");
addCard(s2, 0.3, 1.1, 9.0, 0.6, "D97706", ["来自线性回归：收益 = α + β×市场 + 误差。α=截距(超越市场的本事)，β=斜率(跟大盘的同步程度)"], "📜 名称来源", { fs: 10 });
s2.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.9, w: 9.0, h: 0.5, fill: { color: "EEEDFE" }, line: { color: C.primary, width: 0.5 } });
s2.addText("核心公式：Rᵢ - R_f = α + β × (R_m - R_f) + ε", { x: 0.7, y: 1.95, w: 8.6, h: 0.4, fontSize: 13, fontFace: "Consolas", color: C.red, align: "center", valign: "middle", margin: 0 });
addCard(s2, 0.3, 2.6, 4.3, 1.2, "3B82F6", ["和市场一起波动的部分","β=1.2→大盘涨1%你涨1.2%","β=0.8→大盘跌1%你跌0.8%","公式中的斜率"], "β（贝塔）——随大流", { fs: 10 });
addCard(s2, 4.8, 2.6, 4.9, 1.2, "10B981", ["市场解释不了的超额收益","α>0→选股能力强","α<0→不如买指数","公式中的截距"], "α（阿尔法）——真本事", { fs: 10 });
addCard(s2, 0.3, 4.0, 9.0, 0.7, "D97706", ["①信息优势(比别人早知道) ②分析优势(解读更深) ③执行优势(更快交易——你的quant_monitor)"], "3.1.1 α的三个来源", { fs: 10 });

// S3: Exotic Beta
let s3 = pres.addSlide();
addHeader(s3, "3.1.2 奇异β + 3.1.3 积极型优化新方法", "原书p.59-61");
addCard(s3, 0.3, 1.1, 9.0, 0.5, "D97706", ["传统β只跟大盘有关，但现实中还有别的风险也在影响收益——这些非传统风险暴露叫奇异β(Exotic Beta)"], "📜 为什么叫奇异β？", { fs: 10 });
addCard(s3, 0.3, 1.8, 2.2, 1.2, "3B82F6", ["持有高波动股票的","额外风险回报","低波动异象"], "波动率β", { fs: 10 });
addCard(s3, 2.6, 1.8, 2.2, 1.2, "10B981", ["流动性差的股票有","流动性溢价","小盘股的一部分解释"], "流动性β", { fs: 10 });
addCard(s3, 4.9, 1.8, 2.2, 1.2, "D97706", ["高风险债券的","信用风险溢价","公司债收益来源"], "信用β", { fs: 10 });
addCard(s3, 7.2, 1.8, 2.5, 1.2, "7C3AED", ["行为金融偏差","过度反应/反应不足","系统性错误定价"], "偏差β", { fs: 10 });
addCard(s3, 0.3, 3.2, 9.0, 0.7, "1E2761", ["3.1.3 核心转变：从找Alpha到管理Beta暴露——控制你能控制的风险,而不是盲目追逐超额收益"], "积极型优化新方法", { fs: 10 });
addCard(s3, 0.3, 4.1, 9.0, 0.6, "1E293B", ["你的stock_scorer.py其实就是在找奇异Beta——ROE分是质量Beta，PE分是价值Beta，动量分是趋势Beta"], "📎 和你系统的关系", { fs: 9, noBullet: true });

// S4: Transaction Costs
let s4 = pres.addSlide();
addHeader(s4, "3.2 交易成本和买卖限制", "原书p.62-64");
addCard(s4, 0.3, 1.1, 9.0, 0.45, "D97706", ["经典理论假设交易免费，但现实中交易成本会吃掉利润——尤其是套利策略"], "📜 为什么要专门讲交易成本？", { fs: 10 });
addCard(s4, 0.3, 1.8, 4.3, 1.3, "3B82F6", ["佣金——券商手续费","印花税——政府税","过户费——登记结算费用","这些都是明码标价"], "显性交易成本", { fs: 10 });
addCard(s4, 4.8, 1.8, 4.9, 1.3, "EF4444", ["买卖价差——买价和卖价的差","市场冲击——大单推动价格变动","延迟成本——等待时价格变化","这些看不见但更致命"], "隐性交易成本", { fs: 10 });
addCard(s4, 0.3, 3.3, 9.0, 1.2, "1E293B", ["为什么币安和OKX价差0.5bps你也赚不到？","价差利润：$0.04（0.5bps）","交易成本：$0.08（1bp手续费+价差）","结论：价差利润 ＜ 交易成本 → 倒亏！"], "📊 用你的价差监控来理解", { fs: 10, noBullet: true });

// S5: Multi-period
let s5 = pres.addSlide();
addHeader(s5, "3.3 多期投资组合管理", "原书p.64-73");
addCard(s5, 0.3, 1.1, 4.3, 1.0, "D97706", ["前面所有模型都是单期的——决定今天怎么买就不管了。但实际交易是连续的：今天买了,明天还要调整。"], "📜 为什么从单期到多期？", { fs: 10 });
addCard(s5, 0.3, 2.3, 4.3, 1.3, "3B82F6", ["一次决策，永不再动","不考虑未来的变化","Markowitz就是单期的"], "单期模型", { fs: 10 });
addCard(s5, 4.8, 2.3, 4.9, 1.3, "10B981", ["持续调整组合","考虑未来各种可能性","随机控制理论"], "多期模型", { fs: 10 });
addCard(s5, 0.3, 3.8, 4.3, 0.8, "6366F1", ["1969 Samuelson终身投资组合","1971 Merton连续时间扩展"], "3.3.1 Samuelson-Merton", { fs: 10 });
addCard(s5, 4.8, 3.8, 4.9, 0.8, "D97706", ["频繁调整→成本太高","最优：不频繁再平衡"], "3.3.2 含成本的Merton问题", { fs: 10 });

// S6: Formula 3.3.4
let s6f = pres.addSlide();
addHeader(s6f, "3.3.4 多期均值-方差再平衡——公式详解", "原书p.88 · Markowitz和van Dijk(2003)");
s6f.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 9.0, h: 0.5, fill: { color: "FEF2F2" }, line: { color: C.red, width: 0.5 } });
s6f.addText("核心问题：什么时候该调整？单期Markowitz今天决定最优组合然后不管了，但多期需要持续调整", { x: 0.7, y: 1.15, w: 8.6, h: 0.4, fontSize: 10, fontFace: FB, color: C.red, margin: 0 });
addCard(s6f, 0.3, 1.8, 4.3, 1.3, "6366F1", ["U ≈ E[R] − λ × Var[R]","U=满足感/效用, E[R]=预期收益","Var[R]=风险(方差), λ=风险厌恶系数","翻译：投资满足感=期望收益−怕亏程度×风险"], "公式① 均值-方差替代法", { fs: 10 });
addCard(s6f, 4.8, 1.8, 4.9, 1.3, "D97706", ["Vₜ(xₜ)=max{ cₜ(xₜ,uₜ) + E[Vₜ₊₁(xₜ₊₁)] }","Vₜ=价值函数, xₜ=当前状态","uₜ=决策, cₜ=即时收益","E[Vₜ₊₁]=未来价值期望(只能估)"], "公式② 近似动态规划ADP", { fs: 10 });
addCard(s6f, 0.3, 3.3, 9.0, 0.6, "1E293B", ["Kritzman实证约束：wᵢ≥κᵢ(最低持仓) + Σwᵢ=1 + wᵢ≥0(不能做空)"], "实证约束", { fs: 9, noBullet: true });

// S7: Formula 3.3.5
let s7f = pres.addSlide();
addHeader(s7f, "3.3.5 含交易成本的动态优化——公式详解", "原书p.89 · Gârleanu和Pedersen(2013)");
addCard(s7f, 0.3, 1.1, 4.3, 0.8, "3B82F6", ["˜Rₜ₊₁ = Bfₜ + εₜ₊₁ — 超额收益的因子分解","˜Rₜ₊₁=下期超额收益, B=因子载荷, fₜ=当前因子值, ε=随机误差","fₜ₊₁=(I−Φ)fₜ + wₜ₊₁ — 因子自回归(VAR模型)","因子缓慢回归均值, w是新冲击"], "公式③④ 收益分解+因子自回归", { fs: 9 });
addCard(s7f, 4.8, 1.1, 4.9, 0.8, "D97706", ["uₜ=持仓向量, Δuₜ=调整量(买/卖多少)","Λ=交易成本矩阵, Σ=协方差矩阵(风险)","γ=风险厌恶系数, ρ=折现因子(<1)","Λ=λΣ 关键假设→使问题有解析解"], "符号说明", { fs: 9 });
addCard(s7f, 0.3, 2.1, 9.0, 1.5, "1E2761", ["max E[ Σ ρᵗ ( uₜᵀ˜Rₜ₊₁ − γ uₜᵀΣ uₜ − (Δuₜ)ᵀΛ Δuₜ ) ]","三项拆解：","① uₜᵀ˜Rₜ₊₁ = 持仓×收益 = 预期收益(越大越好)","② γ uₜᵀΣ uₜ = 风险厌恶×组合风险 = 风险惩罚(越小越好)","③ (Δuₜ)ᵀΛΔuₜ = 调整量×成本×调整量 = 交易成本惩罚(越小越好)"], "公式⑤ 总优化目标", { fs: 10 });
addCard(s7f, 0.3, 3.9, 9.0, 0.6, "1E293B", ["用你的系统理解：价差12bps, 买$200 BTC → 预期收益+$0.24, 风险惩罚−$20(因BTC波动±5%), 交易成本−$0.10 = −$19.86 → 不做"], "📊 算账实例", { fs: 9, noBullet: true });

// S8: Formula 3.3.6
let s8f = pres.addSlide();
addHeader(s8f, "3.3.6 参数不确定性——公式详解", "原书p.90-92 · Brennan(1998) · Kalman-Bucy滤波");
addCard(s8f, 0.3, 1.1, 4.3, 1.0, "3B82F6", ["dPₜ/Pₜ = μ dt + σ dBₜ — Brennan模型设定","μ=未知的预期收益(关键!), σ=已知的波动率","μ的先验: N(m₀, v₀) — 先猜一个范围"], "公式⑦ 模型设定", { fs: 10 });
addCard(s8f, 4.8, 1.1, 4.9, 1.0, "10B981", ["dmₜ = (vₜ/σ²)(dPₜ/Pₜ − mₜdt) — Kalman-Bucy滤波","新估计 = 旧估计 + Kalman增益×(实际−预测)","vₜ越大(越不确定)→更新幅度越大"], "公式⑧ 参数更新", { fs: 10 });
addCard(s8f, 0.3, 2.4, 4.3, 1.0, "D97706", ["µᵢ−r = αᵢ + βᵢ(µ₀−r) — Cvitanić多资产扩展","每个资产的超额收益 = αᵢ + βᵢ×市场超额收益","θ的先验→后验通过Kalman-Bucy滤波更新"], "公式⑨ 多资产扩展", { fs: 10 });
addCard(s8f, 4.8, 2.4, 4.9, 1.0, "7C3AED", ["实证: 1926-1994年69年S&P 500数据","考虑了参数不确定性后","最优配置在时间上可能增、减或非单调变化"], "实证结果", { fs: 10 });
addCard(s8f, 0.3, 3.7, 9.0, 0.7, "1E293B", ["三条公式递进：3.3.4(无成本)→3.3.5(加交易成本Λ)→3.3.6(加参数不确定μ未知)"], "完整递进关系", { fs: 9, noBullet: true });

// S9: Timeline
let s6 = pres.addSlide(); s6.background = { color: C.dark };
s6.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s6.addText("第3章 完整时间线", { x: 0.6, y: 0.3, w: 8.8, h: 0.5, fontSize: 20, fontFace: FT, color: C.white, margin: 0 });
s6.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.8, w: 1.5, h: 0.04, fill: { color: C.accent } });
const timeline = [
  { year: "1964", event: "CAPM α和β — Sharpe提出", note: "收益分解为α+β" },
  { year: "1969", event: "Samuelson终身投资组合选择", note: "离散时间多期模型" },
  { year: "1971", event: "Merton连续时间—随机控制HJB", note: "连续时间多期优化" },
  { year: "1990s", event: "带交易成本的动态优化", note: "再平衡策略优化" },
  { year: "2000s", event: "参数不确定+动态", note: "多期+贝叶斯+近似动态规划" },
];
timeline.forEach((item, i) => {
  const y = 1.2 + i * 0.8;
  s6.addShape(pres.shapes.RECTANGLE, { x: 0.6, y, w: 1.0, h: 0.4, fill: { color: "3B82F6" } });
  s6.addText(item.year, { x: 0.6, y, w: 1.0, h: 0.4, fontSize: 10, fontFace: FB, color: C.white, align: "center", valign: "middle", margin: 0 });
  s6.addShape(pres.shapes.RECTANGLE, { x: 1.8, y: y + 0.05, w: 7.4, h: 0.4, fill: { color: "1E293B" }, line: { color: "334155", width: 0.5 } });
  s6.addText(item.event, { x: 2.0, y: y + 0.05, w: 5.5, h: 0.4, fontSize: 10, fontFace: FB, color: C.white, valign: "middle", margin: 0 });
  s6.addText(item.note, { x: 7.5, y: y + 0.05, w: 2.0, h: 0.4, fontSize: 9, fontFace: FB, color: "94A3B8", valign: "middle", margin: 0 });
  if (i < timeline.length - 1) {
    s6.addShape(pres.shapes.LINE, { x: 1.1, y: y + 0.45, w: 0, h: 0.35, line: { color: "475569", width: 1 } });
  }
});
s6.addText("核心概念：α(真本事) + β(随大流) + 交易成本(吃掉利润) + 多期(持续调整)", {
  x: 0.6, y: 5.0, w: 8.8, h: 0.3, fontSize: 10, fontFace: FB, color: C.accent, margin: 0
});

// S7: End
let s7 = pres.addSlide(); s7.background = { color: C.dark };
s7.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.dark } });
s7.addText("第3章 · 完", { x: 1, y: 2.0, w: 8, h: 1.0, fontSize: 36, fontFace: FT, color: C.white, align: "center", margin: 0 });
s7.addShape(pres.shapes.RECTANGLE, { x: 4.2, y: 3.0, w: 1.6, h: 0.04, fill: { color: C.accent } });
s7.addText("下一章：电子交易中的计量经济学", { x: 1, y: 3.3, w: 8, h: 0.5, fontSize: 14, fontFace: FB, color: C.muted, align: "center", margin: 0 });

const outPath = "C:/Users/user/WorkBuddy/Claw/乌龙指研究/第3章_积极型投资组合管理_视觉讲解.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("✅ 已生成: " + outPath));
