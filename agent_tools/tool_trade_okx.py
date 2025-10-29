"""
OKX Trading Tool
Provides buy and sell functionality for cryptocurrency trading on OKX exchange
"""
from fastmcp import FastMCP
import sys
import os
from typing import Dict, List, Optional, Any
import ccxt

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tools.general_tools import get_config_value, write_config_value
import json

mcp = FastMCP("OKXTradeTools")


def get_okx_client(trading_type: str = "spot"):
    """
    Get OKX exchange client instance
    
    Args:
        trading_type: Trading type - "spot" for spot trading, "swap" for perpetual futures,
                     "future" for delivery futures, "option" for options
    
    Returns:
        ccxt.okx: OKX exchange client
        
    Raises:
        ValueError: If OKX API credentials are not set
    """
    api_key = os.getenv("OKX_API_KEY")
    api_secret = os.getenv("OKX_API_SECRET")
    passphrase = os.getenv("OKX_PASSPHRASE")
    
    if not all([api_key, api_secret, passphrase]):
        raise ValueError("OKX API credentials not set. Please set OKX_API_KEY, OKX_API_SECRET, and OKX_PASSPHRASE environment variables")
    
    # Initialize OKX exchange client
    exchange = ccxt.okx({
        'apiKey': api_key,
        'secret': api_secret,
        'password': passphrase,
        'enableRateLimit': True,
        'options': {
            'defaultType': trading_type,  # 支持 spot, swap, future, option
        }
    })
    
    # Use testnet for testing if configured
    if os.getenv("OKX_TESTNET", "false").lower() == "true":
        exchange.set_sandbox_mode(True)
    
    return exchange


def get_current_price(symbol: str, trading_type: str = "spot") -> float:
    """
    Get current market price for a trading pair
    
    Args:
        symbol: Trading pair symbol (e.g., "BTC/USDT" for spot, "BTC/USDT:USDT" for swap)
        trading_type: Trading type - "spot", "swap", "future", "option"
        
    Returns:
        Current market price
    """
    try:
        exchange = get_okx_client(trading_type)
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        raise


@mcp.tool()
def buy_okx(symbol: str, amount: float, order_type: str = "market", trading_type: str = "spot") -> Dict[str, Any]:
    """
    Buy cryptocurrency on OKX exchange
    
    This function executes buy orders for cryptocurrency trading pairs.
    Supports both market and limit orders, and both spot and futures trading.
    
    Args:
        symbol: Trading pair symbol 
                - For spot: "BTC/USDT", "ETH/USDT"
                - For perpetual swap: "BTC/USDT:USDT", "ETH/USDT:USDT"
                - For delivery futures: "BTC/USDT:USDT-240329" (with expiry date)
        amount: Amount of base currency to buy (e.g., 0.001 BTC)
        order_type: Order type - "market" or "limit" (default: "market")
        trading_type: Trading type - "spot" for spot trading, "swap" for perpetual futures,
                     "future" for delivery futures (default: "spot")
        
    Returns:
        Dict[str, Any]:
          - Success: Returns order details and updated position
          - Failure: Returns {"error": error message, ...}
        
    Example:
        >>> # Spot trading
        >>> result = buy_okx("BTC/USDT", 0.001, trading_type="spot")
        >>> # Perpetual swap (futures)
        >>> result = buy_okx("BTC/USDT:USDT", 1, trading_type="swap")
    """
    signature = get_config_value("SIGNATURE")
    if signature is None:
        raise ValueError("SIGNATURE environment variable is not set")
    
    today_date = get_config_value("TODAY_DATE")
    
    try:
        # Get current position and action ID
        current_position, current_action_id = get_latest_position_okx(today_date, signature)
        
        # Get current price
        current_price = get_current_price(symbol, trading_type)
        
        # Calculate cost
        cost = current_price * amount
        cash_left = current_position.get("USDT", 0) - cost
        
        # Check if sufficient funds
        if cash_left < 0:
            return {
                "error": "Insufficient USDT balance",
                "required": cost,
                "available": current_position.get("USDT", 0),
                "symbol": symbol,
                "date": today_date
            }
        
        # Execute order on OKX (commented out for simulation mode)
        # exchange = get_okx_client()
        # order = exchange.create_market_buy_order(symbol, amount)
        
        # Simulate order for now
        order = {
            "id": f"simulated_{current_action_id + 1}",
            "symbol": symbol,
            "type": order_type,
            "side": "buy",
            "amount": amount,
            "price": current_price,
            "cost": cost,
            "status": "closed"
        }
        
        # Update position
        new_position = current_position.copy()
        new_position["USDT"] = cash_left
        
        # Extract base currency from symbol (e.g., "BTC" from "BTC/USDT")
        base_currency = symbol.split("/")[0]
        new_position[base_currency] = new_position.get(base_currency, 0) + amount
        
        # Save position record
        position_file_path = os.path.join(project_root, "data", "agent_data", signature, "position", "position_okx.jsonl")
        os.makedirs(os.path.dirname(position_file_path), exist_ok=True)
        
        with open(position_file_path, "a") as f:
            record = {
                "date": today_date,
                "id": current_action_id + 1,
                "this_action": {
                    "action": "buy",
                    "symbol": symbol,
                    "amount": amount,
                    "price": current_price,
                    "cost": cost,
                    "trading_type": trading_type
                },
                "positions": new_position,
                "order_info": order
            }
            f.write(json.dumps(record) + "\n")
        
        write_config_value("IF_TRADE", True)
        
        return {
            "success": True,
            "order_id": order["id"],
            "symbol": symbol,
            "amount": amount,
            "price": current_price,
            "cost": cost,
            "new_position": new_position
        }
        
    except Exception as e:
        return {
            "error": f"Failed to execute buy order: {str(e)}",
            "symbol": symbol,
            "date": today_date
        }


@mcp.tool()
def sell_okx(symbol: str, amount: float, order_type: str = "market", trading_type: str = "spot") -> Dict[str, Any]:
    """
    Sell cryptocurrency on OKX exchange
    
    This function executes sell orders for cryptocurrency trading pairs.
    Supports both market and limit orders, and both spot and futures trading.
    
    Args:
        symbol: Trading pair symbol
                - For spot: "BTC/USDT", "ETH/USDT"
                - For perpetual swap: "BTC/USDT:USDT", "ETH/USDT:USDT"
                - For delivery futures: "BTC/USDT:USDT-240329" (with expiry date)
        amount: Amount of base currency to sell (e.g., 0.001 BTC)
        order_type: Order type - "market" or "limit" (default: "market")
        trading_type: Trading type - "spot" for spot trading, "swap" for perpetual futures,
                     "future" for delivery futures (default: "spot")
        
    Returns:
        Dict[str, Any]:
          - Success: Returns order details and updated position
          - Failure: Returns {"error": error message, ...}
        
    Example:
        >>> # Spot trading
        >>> result = sell_okx("BTC/USDT", 0.001, trading_type="spot")
        >>> # Perpetual swap (futures)
        >>> result = sell_okx("BTC/USDT:USDT", 1, trading_type="swap")
    """
    signature = get_config_value("SIGNATURE")
    if signature is None:
        raise ValueError("SIGNATURE environment variable is not set")
    
    today_date = get_config_value("TODAY_DATE")
    
    try:
        # Get current position and action ID
        current_position, current_action_id = get_latest_position_okx(today_date, signature)
        
        # Extract base currency from symbol
        base_currency = symbol.split("/")[0]
        
        # Check if holding this currency
        if base_currency not in current_position or current_position[base_currency] < amount:
            return {
                "error": f"Insufficient {base_currency} balance",
                "have": current_position.get(base_currency, 0),
                "want_to_sell": amount,
                "symbol": symbol,
                "date": today_date
            }
        
        # Get current price
        current_price = get_current_price(symbol, trading_type)
        
        # Calculate proceeds
        proceeds = current_price * amount
        
        # Execute order on OKX (commented out for simulation mode)
        # exchange = get_okx_client()
        # order = exchange.create_market_sell_order(symbol, amount)
        
        # Simulate order for now
        order = {
            "id": f"simulated_{current_action_id + 1}",
            "symbol": symbol,
            "type": order_type,
            "side": "sell",
            "amount": amount,
            "price": current_price,
            "cost": proceeds,
            "status": "closed"
        }
        
        # Update position
        new_position = current_position.copy()
        new_position[base_currency] -= amount
        new_position["USDT"] = new_position.get("USDT", 0) + proceeds
        
        # Save position record
        position_file_path = os.path.join(project_root, "data", "agent_data", signature, "position", "position_okx.jsonl")
        os.makedirs(os.path.dirname(position_file_path), exist_ok=True)
        
        with open(position_file_path, "a") as f:
            record = {
                "date": today_date,
                "id": current_action_id + 1,
                "this_action": {
                    "action": "sell",
                    "symbol": symbol,
                    "amount": amount,
                    "price": current_price,
                    "proceeds": proceeds,
                    "trading_type": trading_type
                },
                "positions": new_position,
                "order_info": order
            }
            f.write(json.dumps(record) + "\n")
        
        write_config_value("IF_TRADE", True)
        
        return {
            "success": True,
            "order_id": order["id"],
            "symbol": symbol,
            "amount": amount,
            "price": current_price,
            "proceeds": proceeds,
            "new_position": new_position
        }
        
    except Exception as e:
        return {
            "error": f"Failed to execute sell order: {str(e)}",
            "symbol": symbol,
            "date": today_date
        }


def get_latest_position_okx(today_date: str, modelname: str) -> tuple:
    """
    Get latest OKX position
    
    Args:
        today_date: Date string in YYYY-MM-DD format
        modelname: Model name for file path construction
        
    Returns:
        (positions, max_id): Position dictionary and max action ID
    """
    from pathlib import Path
    
    base_dir = Path(__file__).resolve().parents[1]
    position_file = base_dir / "data" / "agent_data" / modelname / "position" / "position_okx.jsonl"
    
    if not position_file.exists():
        # Initialize with default USDT balance
        initial_cash = float(os.getenv("INITIAL_CASH_USDT", "10000.0"))
        return {"USDT": initial_cash}, -1
    
    # Try to read today's record first
    max_id_today = -1
    latest_positions_today = {}
    
    with position_file.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                doc = json.loads(line)
                if doc.get("date") == today_date:
                    current_id = doc.get("id", -1)
                    if current_id > max_id_today:
                        max_id_today = current_id
                        latest_positions_today = doc.get("positions", {})
            except Exception:
                continue
    
    if max_id_today >= 0:
        return latest_positions_today, max_id_today
    
    # If no record for today, get the latest record
    max_id_all = -1
    latest_positions_all = {}
    
    with position_file.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                doc = json.loads(line)
                current_id = doc.get("id", -1)
                if current_id > max_id_all:
                    max_id_all = current_id
                    latest_positions_all = doc.get("positions", {})
            except Exception:
                continue
    
    if max_id_all >= 0:
        return latest_positions_all, max_id_all
    
    # No records found, return initial balance
    initial_cash = float(os.getenv("INITIAL_CASH_USDT", "10000.0"))
    return {"USDT": initial_cash}, -1


if __name__ == "__main__":
    port = int(os.getenv("TRADE_OKX_HTTP_PORT", "8004"))
    mcp.run(transport="streamable-http", port=port)
