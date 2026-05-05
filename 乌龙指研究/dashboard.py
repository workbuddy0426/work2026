#!/usr/bin/env python3
"""
量化交易系统 - Web管理面板后端
实时展示：价差套利 + 可转债乌龙指 的状态/持仓/交易记录
"""
from flask import Flask, jsonify, render_template_string, send_from_directory
import json, os, csv, glob
from datetime import datetime
from collections import deque

app = Flask(__name__)

BASE = r"C:\Users\user\WorkBuddy\Claw\乌龙指研究"

# ─── API: 概览数据 ───
@app.route("/api/overview")
def overview():
    crypto = get_crypto_status()
    cb = get_cb_status()
    trades = get_trade_history()
    return jsonify({
        "crypto": crypto,
        "cb": cb,
        "trades": trades[-20:],  # 最近20笔
        "time": datetime.now().strftime("%H:%M:%S"),
    })

# ─── API: 价差历史 ───
@app.route("/api/spreads")
def spreads():
    data = get_spread_history()
    return jsonify(data[-120:])  # 最近120条

# ─── API: 最近信号 ───
@app.route("/api/signals")
def signals():
    crypto_log = os.path.join(BASE, "results/arbitrage_monitor.log")
    cb_log = os.path.join(BASE, "results/cb_monitor.log")
    sigs = []
    for fname, src in [(crypto_log, "价差"), (cb_log, "可转债")]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "信号" in line or "开仓" in line or "平仓" in line or "乌龙指" in line:
                        sigs.append({"source": src, "msg": line.strip()[:120]})
    return jsonify(sigs[-30:])

# ─── API: 可转债回测结果 ───
@app.route("/api/cb-backtest")
def cb_backtest():
    f = os.path.join(BASE, "results/cb_backtest.json")
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as fp:
            return jsonify(json.load(fp))
    return jsonify({"error": "回测未运行"})

# ─── API: 多因子选股 ───
@app.route("/api/factors")
def multi_factor():
    f = os.path.join(BASE, "results/multi_factor_picks.json")
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as fp:
            return jsonify(json.load(fp))
    return jsonify([])

# ─── 数据读取函数 ───
def get_crypto_status():
    log = os.path.join(BASE, "results/arbitrage_monitor.log")
    csv_f = os.path.join(BASE, "results/arbitrage_log.csv")
    trades_f = os.path.join(BASE, "results/arbitrage_trades.json")
    
    status = {"running": False, "btc": 0, "okx": 0, "spread": 0, "signals": 0, "pnl": 0, "trades": 0}
    
    # 从日志取最后一条价差
    if os.path.exists(log):
        with open(log, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "B:$" in line:
                    parts = line.split()
                    for p in parts:
                        if p.startswith("B:$"):
                            try: status["btc"] = float(p.replace("B:$","").replace(",",""))
                            except: pass
                        if p.startswith("价差:"):
                            try: status["spread"] = float(p.replace("价差:","").replace("bps",""))
                            except: pass
                    status["running"] = True
                    break
    
    # 交易统计
    if os.path.exists(trades_f):
        try:
            with open(trades_f, "r", encoding="utf-8") as f:
                ts = json.load(f)
            status["trades"] = len(ts)
            status["pnl"] = round(sum(t.get("pnl", 0) for t in ts), 2)
            status["signals"] = len([t for t in ts if t.get("pnl") != 0])
        except: pass
    
    # CSV价差记录数
    if os.path.exists(csv_f):
        try:
            with open(csv_f, "r") as f:
                status["data_points"] = sum(1 for _ in f) - 1
        except: pass
    
    return status

def get_cb_status():
    log = os.path.join(BASE, "results/cb_monitor.log")
    status = {"running": False, "bonds": 0, "signals": 0}
    if os.path.exists(log):
        with open(log, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "监控:" in line and "只" in line:
                    try: status["bonds"] = int(line.split("监控:")[1].split("只")[0])
                    except: pass
                if "信号" in line:
                    try: status["signals"] = int(line.split("信号")[1].split(")")[0]) if ")" in line else 0
                    except: pass
                if "只 |" in line:
                    status["running"] = True
    return status

def get_spread_history():
    csv_f = os.path.join(BASE, "results/arbitrage_log.csv")
    data = []
    if os.path.exists(csv_f):
        with open(csv_f, "r") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0: continue
                if len(row) >= 5:
                    try:
                        data.append({
                            "t": row[0], "b": float(row[1]), "o": float(row[2]),
                            "s": float(row[3])
                        })
                    except: pass
    return data

def get_trade_history():
    f = os.path.join(BASE, "results/arbitrage_trades.json")
    if os.path.exists(f):
        try:
            with open(f, "r") as fp:
                return json.load(fp)
        except: return []
    return []

# ─── HTML 管理界面 ───
INDEX_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>量化交易监控</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, sans-serif; background: #0f0f0f; color: #e0e0e0; padding: 20px; }
h1 { font-size: 20px; margin-bottom: 16px; color: #fff; }
h2 { font-size: 15px; margin: 16px 0 8px; color: #aaa; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 16px; }
.card { background: #1a1a2e; border-radius: 10px; padding: 16px; border: 1px solid #2a2a4a; }
.card .label { font-size: 12px; color: #888; }
.card .value { font-size: 24px; font-weight: 600; margin-top: 4px; }
.card .sub { font-size: 13px; color: #888; margin-top: 4px; }
.green { color: #4caf50; }
.red { color: #f44336; }
.blue { color: #42a5f5; }
.yellow { color: #ffa726; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { text-align: left; padding: 8px 6px; border-bottom: 1px solid #2a2a4a; color: #888; font-weight: 500; }
td { padding: 6px; border-bottom: 1px solid #1a1a2e; }
.log-box { background: #111; padding: 12px; border-radius: 8px; max-height: 300px; overflow-y: auto; font-size: 12px; font-family: monospace; line-height: 1.6; }
.log-box div { padding: 2px 0; }
.tag { display: inline-block; padding: 1px 6px; border-radius: 4px; font-size: 11px; margin-right: 4px; }
.tag-crypto { background: #1a3a2e; color: #4caf50; }
.tag-cb { background: #2a1a3e; color: #ce93d8; }
canvas { max-height: 200px; }
</style>
</head>
<body>
<h1>小乌量化交易系统</h1>

<div class="cards">
  <div class="card">
    <div class="label">币安价差套利</div>
    <div class="value" id="crypto-status"><span class="yellow">检查中...</span></div>
    <div class="sub" id="crypto-detail"></div>
  </div>
  <div class="card">
    <div class="label">可转债乌龙指</div>
    <div class="value" id="cb-status"><span class="yellow">检查中...</span></div>
    <div class="sub" id="cb-detail"></div>
  </div>
  <div class="card">
    <div class="label">累计交易</div>
    <div class="value" id="total-trades">-</div>
    <div class="sub" id="total-pnl"></div>
  </div>
  <div class="card">
    <div class="label">最近价差 (bps)</div>
    <div class="value" id="last-spread">-</div>
    <div class="sub" id="update-time"></div>
  </div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
<div>
  <h2>价差走势</h2>
  <canvas id="spreadChart"></canvas>
</div>
<div>
  <h2>实时信号</h2>
  <div class="log-box" id="signal-log">等待数据...</div>
</div>
</div>

<h2>可转债乌龙指模型</h2>
<div class="cards">
  <div class="card">
    <div class="label">原理</div>
    <div class="sub">可转债市场流动性低于股票，偶尔出现大单错误定价（乌龙指），价格瞬间偏离后快速回归。利用高频轮询捕捉该瞬间，顺势做多/做空。</div>
  </div>
  <div class="card">
    <div class="label">检测逻辑</div>
    <div class="sub">1. 每10秒扫描256只可转债<br>2. 价格波动>8%触发信号<br>3. 价格>50元过滤低价债<br>4. 后续回归则平仓获利</div>
  </div>
  <div class="card">
    <div class="label">优势</div>
    <div class="sub">T+0交易 · 无需判断方向 · 风险可控 · 回归速度快</div>
  </div>
</div>

<h2>回测结果（一个月模拟数据）</h2>
<div class="cards" id="backtest-cards">
  <div class="card"><div class="label">加载中...</div></div>
</div>
<table id="backtest-table"><thead><tr>
  <th>债券</th><th>真实乌龙指</th><th>检测到</th><th>命中</th><th>误报</th><th>精准率</th><th>召回率</th><th>收益</th>
</tr></thead><tbody></tbody></table></div>

<h2>交易记录</h2>
<div style="max-height: 300px; overflow-y: auto;">
<table><thead><tr>
  <th>时间</th><th>类型</th><th>方向</th><th>入场价差</th><th>盈亏</th><th>原因</th>
</tr></thead><tbody id="trade-table"></tbody></table>
</div>

<h2>多因子选股</h2>
<div style="max-height: 400px; overflow-y: auto;">
<table><thead><tr>
  <th>排名</th><th>代码</th><th>名称</th><th>价格</th><th>总分</th><th>PE</th><th>PB</th><th>市值</th><th>涨幅%</th><th>换手%</th>
</tr></thead><tbody id="factor-table"></tbody></table>
</div>

<script>
function update() {
  fetch('/api/overview').then(r=>r.json()).then(d=>{
    // 币安状态
    const c = d.crypto;
    document.getElementById('crypto-status').innerHTML = c.running
      ? '<span class="green">运行中</span>'
      : '<span class="red">离线</span>';
    document.getElementById('crypto-detail').textContent = 
      'BTC $' + c.btc.toLocaleString() + ' | 信号 ' + c.signals + '次';
    
    // 可转债
    const cb = d.cb;
    document.getElementById('cb-status').innerHTML = cb.running
      ? '<span class="green">运行中</span>'
      : '<span class="red">离线</span>';
    document.getElementById('cb-detail').textContent = 
      cb.bonds + '只监控 | 信号 ' + cb.signals + '次';
    
    // 交易统计
    document.getElementById('total-trades').textContent = c.trades + '笔';
    const pnlColor = c.pnl >= 0 ? 'green' : 'red';
    document.getElementById('total-pnl').innerHTML = 
      '总盈亏 <span class="'+pnlColor+'">$' + c.pnl.toFixed(2) + '</span>';
    
    // 价差
    document.getElementById('last-spread').textContent = c.spread.toFixed(1) + ' bps';
    document.getElementById('update-time').textContent = d.time;
    
    // 交易表
    let html = '';
    d.trades.slice().reverse().forEach(t => {
      const pnlCls = (t.pnl || 0) >= 0 ? 'green' : 'red';
      html += '<tr><td>'+(t.exit_time||t.entry_time||'').slice(0,16)+
        '</td><td>'+(t.side||t.type||'-')+
        '</td><td>'+(t.side||'-')+
        '</td><td>'+(t.entry_spread||'')+'bps'+
        '</td><td class="'+pnlCls+'">$'+(t.pnl||0).toFixed(2)+
        '</td><td>'+(t.exit_reason||t.reason||'-')+'</td></tr>';
    });
    document.getElementById('trade-table').innerHTML = html || '<tr><td colspan="6">暂无交易</td></tr>';
  });
  
  // 信号日志
  fetch('/api/signals').then(r=>r.json()).then(sigs => {
    let html = '';
    sigs.slice().reverse().forEach(s => {
      const tag = s.source === '价差' ? 'tag-crypto' : 'tag-cb';
      html += '<div><span class="tag '+tag+'">'+s.source+'</span>'+s.msg+'</div>';
    });
    document.getElementById('signal-log').innerHTML = html || '暂无信号';
  });
  
  // 可转债回测数据
  fetch('/api/cb-backtest').then(r=>r.json()).then(d => {
    if (d.error) return;
    const t = d.total;
    document.getElementById('backtest-cards').innerHTML = 
      '<div class="card"><div class="label">总信号</div><div class="value">'+t.signals+'次</div></div>' +
      '<div class="card"><div class="label">精准率</div><div class="value '+(t.precision>50?'green':'yellow')+'">'+t.precision+'%</div></div>' +
      '<div class="card"><div class="label">召回率</div><div class="value green">'+t.recall+'%</div></div>' +
      '<div class="card"><div class="label">模拟收益</div><div class="value '+(t.pnl>0?'green':'red')+'">$'+t.pnl.toFixed(2)+'</div></div>';
    
    let html = '';
    d.results.forEach(r => {
      html += '<tr><td>'+r.name+'</td><td>'+r.real_fatfingers+'</td><td>'+r.signals+'</td><td>'+r.hits+
        '</td><td>'+r.false_alarms+'</td><td>'+r.precision+'%</td><td>'+r.recall+'%</td><td class="'+(r.pnl>0?'green':'red')+'">$'+r.pnl.toFixed(2)+'</td></tr>';
    });
    html += '<tr style="font-weight:600;border-top:2px solid #555"><td>合计</td><td>'+t.real+'</td><td>'+t.signals+'</td><td>'+t.hits+
      '</td><td>'+t.false+'</td><td>'+t.precision+'%</td><td>'+t.recall+'%</td><td class="'+(t.pnl>0?'green':'red')+'">$'+t.pnl.toFixed(2)+'</td></tr>';
    document.querySelector('#backtest-table tbody').innerHTML = html;
  });
  
  // 多因子选股
  fetch('/api/factors').then(r=>r.json()).then(data => {
    let html = '';
    data.slice(0, 20).forEach((s, i) => {
      const bg = i % 2 === 0 ? 'rgba(255,255,255,0.02)' : '';
      html += '<tr style="background:'+bg+'"><td>'+(i+1)+'</td><td>'+s.code+'</td><td>'+s.name+
        '</td><td>$'+(s.price||'-')+'</td><td>'+s.score+
        '</td><td>'+(s.pe||'-')+'</td><td>'+(s.pb||'-')+
        '</td><td>'+(s.mcap||'-')+'</td><td>'+(s.chg||'-')+'</td><td>'+(s.turnover||'-')+'</td></tr>';
    });
    document.getElementById('factor-table').innerHTML = html || '<tr><td colspan="10">暂无数据</td></tr>';
  });
  
  // 价差图表
  fetch('/api/spreads').then(r=>r.json()).then(data => {
    if (window.spreadChart) window.spreadChart.destroy();
    const ctx = document.getElementById('spreadChart');
    if (data.length < 2) { ctx.style.display='none'; return; }
    ctx.style.display='block';
    window.spreadChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.map(d => d.t),
        datasets: [{
          label: '价差(bps)',
          data: data.map(d => d.s),
          borderColor: '#42a5f5',
          borderWidth: 1,
          fill: true,
          backgroundColor: 'rgba(66,165,245,0.1)',
          pointRadius: 0,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { 
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#888', font: {size: 10} }
          }
        }
      }
    });
  });
}
setInterval(update, 3000);
update();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

if __name__ == "__main__":
    print(f" 量化交易监控面板")
    print(f" http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
