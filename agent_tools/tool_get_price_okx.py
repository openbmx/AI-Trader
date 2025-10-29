"""
OKX Price Query Tool
Provides real-time and historical cryptocurrency price data from OKX exchange
"""
from fastmcp import FastMCP
import sys
import os
from typing import Dict, List, Optional, Any
import ccxt
from datetime import datetime, timedelta

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tools.general_tools import get_config_value

mcp = FastMCP("OKXPriceTools")


def get_okx_client():
    """
    Get OKX exchange client instance
    
    Returns:
        ccxt.okx: OKX exchange client
    """
    # For price queries, we don't need API credentials
    exchange = ccxt.okx({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
        }
    })
    
    # Use testnet if configured
    if os.getenv("OKX_TESTNET", "false").lower() == "true":
        exchange.set_sandbox_mode(True)
    
    return exchange


@mcp.tool()
def get_current_price_okx(symbol: str) -> Dict[str, Any]:
    """
    Get current market price for a cryptocurrency trading pair on OKX
    
    Args:
        symbol: Trading pair symbol (e.g., "BTC/USDT", "ETH/USDT")
        
    Returns:
        Dict containing price information:
          - symbol: Trading pair symbol
          - price: Current price
          - bid: Current bid price
          - ask: Current ask price
          - timestamp: Timestamp of the price
          - datetime: Human-readable datetime
        
    Example:
        >>> result = get_current_price_okx("BTC/USDT")
        >>> print(result)  # {"symbol": "BTC/USDT", "price": 45000.0, ...}
    """
    try:
        exchange = get_okx_client()
        ticker = exchange.fetch_ticker(symbol)
        
        return {
            "symbol": symbol,
            "price": ticker.get('last'),
            "bid": ticker.get('bid'),
            "ask": ticker.get('ask'),
            "high": ticker.get('high'),
            "low": ticker.get('low'),
            "volume": ticker.get('baseVolume'),
            "timestamp": ticker.get('timestamp'),
            "datetime": ticker.get('datetime')
        }
    except Exception as e:
        return {
            "error": f"Failed to fetch price for {symbol}: {str(e)}",
            "symbol": symbol
        }


@mcp.tool()
def get_multiple_prices_okx(symbols: List[str]) -> Dict[str, Any]:
    """
    Get current market prices for multiple cryptocurrency trading pairs on OKX
    
    Args:
        symbols: List of trading pair symbols (e.g., ["BTC/USDT", "ETH/USDT"])
        
    Returns:
        Dict mapping symbols to their price information
        
    Example:
        >>> result = get_multiple_prices_okx(["BTC/USDT", "ETH/USDT"])
        >>> print(result)  # {"BTC/USDT": {...}, "ETH/USDT": {...}}
    """
    results = {}
    
    try:
        exchange = get_okx_client()
        
        for symbol in symbols:
            try:
                ticker = exchange.fetch_ticker(symbol)
                results[symbol] = {
                    "price": ticker.get('last'),
                    "bid": ticker.get('bid'),
                    "ask": ticker.get('ask'),
                    "high": ticker.get('high'),
                    "low": ticker.get('low'),
                    "volume": ticker.get('baseVolume'),
                    "timestamp": ticker.get('timestamp'),
                    "datetime": ticker.get('datetime')
                }
            except Exception as e:
                results[symbol] = {
                    "error": f"Failed to fetch price: {str(e)}"
                }
        
        return results
    except Exception as e:
        return {
            "error": f"Failed to fetch prices: {str(e)}"
        }


@mcp.tool()
def get_historical_ohlcv_okx(symbol: str, timeframe: str = "1d", limit: int = 100) -> Dict[str, Any]:
    """
    Get historical OHLCV (Open, High, Low, Close, Volume) data for a trading pair on OKX
    
    Args:
        symbol: Trading pair symbol (e.g., "BTC/USDT")
        timeframe: Timeframe for candles (e.g., "1m", "5m", "1h", "1d")
        limit: Number of candles to fetch (default: 100)
        
    Returns:
        Dict containing historical OHLCV data
        
    Example:
        >>> result = get_historical_ohlcv_okx("BTC/USDT", "1d", 30)
        >>> print(result)  # {"symbol": "BTC/USDT", "timeframe": "1d", "data": [...]}
    """
    try:
        exchange = get_okx_client()
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        # Format OHLCV data
        formatted_data = []
        for candle in ohlcv:
            formatted_data.append({
                "timestamp": candle[0],
                "datetime": datetime.fromtimestamp(candle[0] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5]
            })
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "count": len(formatted_data),
            "data": formatted_data
        }
    except Exception as e:
        return {
            "error": f"Failed to fetch OHLCV data for {symbol}: {str(e)}",
            "symbol": symbol
        }


@mcp.tool()
def get_24h_stats_okx(symbol: str) -> Dict[str, Any]:
    """
    Get 24-hour statistics for a trading pair on OKX
    
    Args:
        symbol: Trading pair symbol (e.g., "BTC/USDT")
        
    Returns:
        Dict containing 24-hour statistics including price change, volume, etc.
        
    Example:
        >>> result = get_24h_stats_okx("BTC/USDT")
        >>> print(result)  # {"symbol": "BTC/USDT", "change": 2.5, ...}
    """
    try:
        exchange = get_okx_client()
        ticker = exchange.fetch_ticker(symbol)
        
        return {
            "symbol": symbol,
            "last_price": ticker.get('last'),
            "high_24h": ticker.get('high'),
            "low_24h": ticker.get('low'),
            "volume_24h": ticker.get('baseVolume'),
            "quote_volume_24h": ticker.get('quoteVolume'),
            "price_change": ticker.get('change'),
            "price_change_percent": ticker.get('percentage'),
            "timestamp": ticker.get('timestamp'),
            "datetime": ticker.get('datetime')
        }
    except Exception as e:
        return {
            "error": f"Failed to fetch 24h stats for {symbol}: {str(e)}",
            "symbol": symbol
        }


@mcp.tool()
def get_orderbook_okx(symbol: str, limit: int = 20) -> Dict[str, Any]:
    """
    Get current order book (bids and asks) for a trading pair on OKX
    
    Args:
        symbol: Trading pair symbol (e.g., "BTC/USDT")
        limit: Number of price levels to fetch (default: 20)
        
    Returns:
        Dict containing order book data with bids and asks
        
    Example:
        >>> result = get_orderbook_okx("BTC/USDT", 10)
        >>> print(result)  # {"symbol": "BTC/USDT", "bids": [...], "asks": [...]}
    """
    try:
        exchange = get_okx_client()
        orderbook = exchange.fetch_order_book(symbol, limit)
        
        return {
            "symbol": symbol,
            "timestamp": orderbook.get('timestamp'),
            "datetime": orderbook.get('datetime'),
            "bids": orderbook.get('bids', [])[:limit],
            "asks": orderbook.get('asks', [])[:limit],
            "bid_count": len(orderbook.get('bids', [])),
            "ask_count": len(orderbook.get('asks', []))
        }
    except Exception as e:
        return {
            "error": f"Failed to fetch orderbook for {symbol}: {str(e)}",
            "symbol": symbol
        }


@mcp.tool()
def list_okx_markets() -> Dict[str, Any]:
    """
    List available trading markets on OKX
    
    Returns:
        Dict containing list of available markets and trading pairs
        
    Example:
        >>> result = list_okx_markets()
        >>> print(result)  # {"markets": ["BTC/USDT", "ETH/USDT", ...]}
    """
    try:
        exchange = get_okx_client()
        markets = exchange.load_markets()
        
        # Filter to show only spot markets
        spot_markets = [
            symbol for symbol, market in markets.items()
            if market.get('spot', False) and market.get('active', False)
        ]
        
        # Get popular USDT pairs
        usdt_pairs = [m for m in spot_markets if m.endswith('/USDT')]
        
        return {
            "total_markets": len(spot_markets),
            "usdt_pairs_count": len(usdt_pairs),
            "popular_usdt_pairs": sorted(usdt_pairs)[:50],  # Top 50 USDT pairs
            "sample_markets": sorted(spot_markets)[:100]  # Sample of all markets
        }
    except Exception as e:
        return {
            "error": f"Failed to list markets: {str(e)}"
        }


if __name__ == "__main__":
    port = int(os.getenv("GETPRICE_OKX_HTTP_PORT", "8005"))
    mcp.run(transport="streamable-http", port=port)
