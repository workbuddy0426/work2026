#!/usr/bin/env python3
"""
A股多因子选股系统
因子：估值(PE/PB)、质量(ROE)、动量、小市值、低波
数据源：腾讯行情API + Sina
"""
import urllib.request, json, csv, os, math
from datetime import datetime, timedelta

BASE = r"C:\Users\user\WorkBuddy\Claw\乌龙指研究"
RESULT_DIR = os.path.join(BASE, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

# ─── 数据获取 ───
def get_stock_list():
    """获取A股列表"""
    import akshare as ak
    for k in ['http_proxy','https_proxy','HTTP_PROXY','HTTPS_PROXY']:
        os.environ.pop(k, None)
    df = ak.stock_info_a_code_name()
    stocks = []
    for _, row in df.iterrows():
        code = str(row['code']).strip()
        name = str(row['name']).strip()
        # 过滤ST和B股
        if name.startswith('*ST') or name.startswith('ST') or code.startswith('9'):
            continue
        # 代码转交易所前缀
        if code.startswith('6'):
            prefix = 'sh'
        elif code.startswith('0') or code.startswith('3'):
            prefix = 'sz'
        else:
            continue  # 北交所或其他
        stocks.append({'code': code, 'name': name, 'prefix': prefix})
    print(f"  股票池: {len(stocks)}只")
    return stocks

def fetch_quotes(stocks):
    """批量获取行情（腾讯API），最多查200只一批"""
    results = {}
    batch_size = 100
    for i in range(0, len(stocks), batch_size):
        batch = stocks[i:i+batch_size]
        query = ','.join(f"{s['prefix']}{s['code']}" for s in batch)
        url = f'https://qt.gtimg.cn/q={query}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            raw = resp.read().decode('gbk')
            for line in raw.strip().split(';'):
                if not line: continue
                parts = line.split('~')
                if len(parts) < 45: continue
                code = parts[2]
                try:
                    results[code] = {
                        'name': parts[1],
                        'price': float(parts[3]) if parts[3] else 0,
                        'open': float(parts[5]) if parts[5] else 0,
                        'high': float(parts[8]) if parts[8] else 0,
                        'low': float(parts[9]) if parts[9] else 0,
                        'volume': int(parts[6]) if parts[6] else 0,
                        'amount': float(parts[7]) if parts[7] else 0,
                        'pe': float(parts[39]) if parts[39] and parts[39] != '0.0' else 0,
                        'pb': float(parts[43]) if parts[43] and parts[43] != '0.0' else 0,
                        'mcap': float(parts[44]) if parts[44] else 0,
                        'chg_pct': float(parts[32]) if parts[32] else 0,
                    }
                except:
                    continue
        except:
            continue
    return results

# ─── 因子计算 ───
def calc_factors(quotes):
    """计算多因子得分"""
    results = []
    
    for code, q in quotes.items():
        price = q['price']
        if price <= 0: continue
        
        scores = {}
        details = {}
        
        # 1. 估值因子：PE低分高（低估值好）
        if q['pe'] > 0 and q['pe'] < 200:
            pe_score = max(0, 100 - q['pe'] / 2)  # PE=0得100分，PE=200得0分
            scores['pe'] = pe_score
            details['pe'] = round(q['pe'], 2)
        
        # 2. 市净率因子：PB低分高
        if q['pb'] > 0 and q['pb'] < 20:
            pb_score = max(0, 100 - q['pb'] * 5)
            scores['pb'] = pb_score
            details['pb'] = round(q['pb'], 2)
        
        # 3. 小市值因子：市值小分高
        if q['mcap'] > 0:
            mcap_score = max(0, 100 - math.log2(q['mcap'] / 1e8) * 8)
            scores['mcap'] = mcap_score
            details['mcap'] = f"{round(q['mcap']/1e8, 1)}亿"
        
        # 4. 价格动量（涨跌幅）
        if 'chg_pct' in q:
            chg = q['chg_pct']
            if -2 < chg < -0.5:
                mom_score = 70
            elif -0.5 <= chg <= 1:
                mom_score = 80
            elif 1 < chg <= 3:
                mom_score = 60
            else:
                mom_score = 40
            scores['momentum'] = mom_score
            details['chg'] = round(chg, 2)
        
        # 5. 成交量因子（量比适中）
        if q['amount'] > 0 and q['mcap'] > 0:
            turnover_rate = q['amount'] / q['mcap'] * 100
            if 0.5 < turnover_rate < 3:
                vol_score = 80
            elif turnover_rate <= 0.5:
                vol_score = 50
            else:
                vol_score = 30
            scores['volume'] = vol_score
            details['turnover'] = round(turnover_rate, 2)
        
        # 加权总分
        weights = {'pe': 0.25, 'pb': 0.15, 'mcap': 0.25, 'momentum': 0.20, 'volume': 0.15}
        total = 0
        weight_sum = 0
        for k, w in weights.items():
            if k in scores:
                total += scores[k] * w
                weight_sum += w
        
        final_score = round(total / weight_sum, 1) if weight_sum > 0 else 0
        
        results.append({
            'code': code,
            'name': q['name'],
            'price': round(price, 2),
            'score': final_score,
            **details,
        })
    
    # 排序
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# ─── 保存与展示 ───
def save_and_show(results, top_n=30):
    """保存结果并展示"""
    filepath = os.path.join(RESULT_DIR, "multi_factor_picks.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results[:100], f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f" 多因子选股结果（前{top_n}）")
    print(f"{'='*70}")
    print(f" {'排名':>4} {'代码':>6} {'名称':<8} {'价格':>8} {'总分':>6} {'PE':>8} {'PB':>6} {'市值':>10} {'涨幅':>7} {'换手%':>6}")
    print("-" * 70)
    for i, r in enumerate(results[:top_n]):
        print(f" {i+1:>4} {r['code']:>6} {r['name']:<8} {r['price']:>8.2f} "
              f"{r['score']:>5.1f} {r.get('pe','-'):>8} {r.get('pb','-'):>6} "
              f"{r.get('mcap','-'):>10} {r.get('chg','-'):>7} {r.get('turnover','-'):>6}")
    
    print(f"\n结果已保存: results/multi_factor_picks.json")

def main():
    print("多因子选股系统")
    print("=" * 30)
    
    print("\n1. 获取股票列表...")
    stocks = get_stock_list()
    
    print("\n2. 获取实时行情...")
    quotes = fetch_quotes(stocks)
    print(f"  获取 {len(quotes)} 只行情")
    
    print("\n3. 计算因子得分...")
    results = calc_factors(quotes)
    print(f"  评分 {len(results)} 只")
    
    print("\n4. 保存结果...")
    save_and_show(results)

if __name__ == "__main__":
    main()
