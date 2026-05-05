#!/usr/bin/env python3
"""测试各数据源连通性"""
import urllib.request
import json
import time

ENDPOINTS = [
    ("OKX REST", "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"),
    ("Bybit REST", "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT"),
    ("KuCoin REST", "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT"),
    ("MEXC REST", "https://api.mexc.com/api/v3/ticker/price?symbol=BTCUSDT"),
    ("CoinGecko REST", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"),
    ("Gate.io REST", "https://api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT"),
    ("HTX (Huobi) REST", "https://api.huobi.pro/market/detail/merged?symbol=btcusdt"),
]

# WebSocket endpoints (just test TCP connectivity)
WS_ENDPOINTS = [
    ("Binance WSS", "wss://stream.binance.com:9443/ws/btcusdt@trade"),
    ("Bybit WSS", "wss://stream.bybit.com/v5/public/spot"),
    ("OKX WSS", "wss://ws.okx.com:8443/ws/v5/public"),
]

if __name__ == "__main__":
    print("=== REST API 连通性测试 ===\n")
    for name, url in ENDPOINTS:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            start = time.time()
            resp = urllib.request.urlopen(req, timeout=5)
            elapsed = time.time() - start
            data = json.loads(resp.read().decode())
            print(f"✅ {name}: {elapsed:.1f}s - {json.dumps(data)[:100]}")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:60]}")
        time.sleep(0.5)
    
    print("\n=== WebSocket 连通性测试 ===\n")
    import socket
    import ssl
    
    for name, url in WS_ENDPOINTS:
        try:
            # parse wss://host:port/path
            hostport = url.replace("wss://", "").split("/")[0]
            host, port = hostport.split(":")
            start = time.time()
            ctx = ssl.create_default_context()
            sock = socket.create_connection((host, int(port)), timeout=5)
            ssock = ctx.wrap_socket(sock, server_hostname=host)
            elapsed = time.time() - start
            ssock.close()
            print(f"✅ {name}: TCP+SSL 连接成功 ({elapsed:.1f}s)")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:80]}")
