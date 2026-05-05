import urllib.request, json, time

proxy = 'http://127.0.0.1:6864'
handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
opener = urllib.request.build_opener(handler)

# 币安24小时成交量排行
req = urllib.request.Request(
    'https://api.binance.com/api/v3/ticker/24hr',
    headers={'User-Agent': 'Mozilla/5.0'})
resp = opener.open(req, timeout=10)
data = json.loads(resp.read().decode())

usdt_pairs = [t for t in data if t['symbol'].endswith('USDT') and t['symbol'] != 'USDTUSDT']
usdt_pairs.sort(key=lambda x: float(x['quoteVolume']), reverse=True)

skip = {'USDC','BUSD','TUSD','DAI','FDUSD','PAX','USDP','GUSD','EUR','GBP'}

print(f"{'排名':>4} {'币种':>10} {'24h成交额':>16} {'现价':>12} {'24h涨跌':>10} {'价差(bps)':>12}")
print('=' * 68)

count = 0
for t in usdt_pairs:
    name = t['symbol'].replace('USDT', '')
    if name in skip or name.startswith('1000'):
        continue
    
    vol = float(t['quoteVolume'])
    price_b = float(t['lastPrice'])
    
    try:
        req_o = urllib.request.Request(
            f'https://www.okx.com/api/v5/market/ticker?instId={name}-USDT',
            headers={'User-Agent': 'Mozilla/5.0'})
        resp_o = opener.open(req_o, timeout=5)
        price_o = float(json.loads(resp_o.read().decode())['data'][0]['last'])
        spread = (price_b - price_o) / price_o * 10000
        chg = float(t['priceChangePercent'])
        
        count += 1
        vol_str = f"{vol/1e8:.1f}亿" if vol > 1e8 else f"{vol/1e6:.0f}M"
        print(f"{count:>4} {name:>10} {vol_str:>16} ${price_b:>9.4f} {chg:>+9.2f}% {spread:>+10.1f}")
    except:
        continue
    
    if count >= 25:
        break
    time.sleep(0.1)

print(f"\n注: 价差绝对值>20bps的值得关注")
