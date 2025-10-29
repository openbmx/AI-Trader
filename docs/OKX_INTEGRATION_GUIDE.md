# OKX 交易所集成指南 / OKX Exchange Integration Guide

[English](#english) | [中文](#中文)

---

## 中文

### 概述

本项目现已支持OKX加密货币交易所集成，可以进行加密货币的自动交易。这是对原有股票交易功能的扩展，两种交易模式可以独立运行。

### 重要说明

**原项目不支持币安交易所**。本次更新是**新增OKX交易所支持**，而非从币安迁移到OKX。

### 主要特性

- ✅ 支持OKX现货交易
- ✅ 实时加密货币价格查询
- ✅ 市价单和限价单支持
- ✅ 支持多个交易对（BTC/USDT, ETH/USDT等）
- ✅ 测试网络支持（安全测试）
- ✅ 完整的持仓管理和交易记录

### 快速开始

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

新增的依赖：
- `ccxt>=4.0.0` - 加密货币交易所统一API库

#### 2. 配置OKX API密钥

在 `.env` 文件中添加OKX API凭证：

```bash
# OKX Exchange API Configuration
OKX_API_KEY="your_api_key_here"
OKX_API_SECRET="your_api_secret_here"
OKX_PASSPHRASE="your_passphrase_here"
OKX_TESTNET="true"  # 使用测试网络（推荐先测试）

# OKX服务端口
TRADE_OKX_HTTP_PORT=8004
GETPRICE_OKX_HTTP_PORT=8005

# 初始USDT资金
INITIAL_CASH_USDT=10000.0
```

#### 3. 获取OKX API密钥

1. 访问 [OKX官网](https://www.okx.com)
2. 注册/登录账户
3. 进入 API管理页面
4. 创建新的API密钥
5. 保存API Key, Secret Key和Passphrase

**安全建议：**
- 首先使用测试网络（`OKX_TESTNET=true`）
- 为API密钥设置IP白名单
- 限制API权限（只需要现货交易权限）
- 妥善保管API凭证

#### 4. 启动OKX服务

```bash
cd agent_tools
python start_mcp_services.py
```

这将启动所有服务，包括新的OKX交易和价格查询服务。

#### 5. 运行OKX交易Agent

使用OKX专用配置文件：

```bash
python main.py configs/okx_crypto_config.json
```

### 配置文件说明

`configs/okx_crypto_config.json` 示例：

```json
{
  "agent_type": "BaseAgent",
  "trading_mode": "crypto_okx",
  "models": [
    {
      "name": "gpt-5-crypto",
      "basemodel": "openai/gpt-5",
      "signature": "gpt-5-okx-crypto",
      "enabled": true
    }
  ],
  "agent_config": {
    "initial_cash": 10000.0
  },
  "okx_config": {
    "enabled": true,
    "trading_pairs": [
      "BTC/USDT",
      "ETH/USDT",
      "SOL/USDT"
    ],
    "default_order_type": "market",
    "use_testnet": true
  }
}
```

### 可用的交易对

常见的USDT交易对：
- BTC/USDT - 比特币
- ETH/USDT - 以太坊
- SOL/USDT - Solana
- BNB/USDT - Binance Coin
- XRP/USDT - Ripple
- ADA/USDT - Cardano
- DOGE/USDT - Dogecoin
- DOT/USDT - Polkadot
- MATIC/USDT - Polygon
- LINK/USDT - Chainlink

### 新增的工具函数

#### 交易工具 (tool_trade_okx.py)

```python
# 买入加密货币
buy_okx(symbol="BTC/USDT", amount=0.001)

# 卖出加密货币
sell_okx(symbol="BTC/USDT", amount=0.001)
```

#### 价格查询工具 (tool_get_price_okx.py)

```python
# 获取当前价格
get_current_price_okx(symbol="BTC/USDT")

# 获取多个价格
get_multiple_prices_okx(symbols=["BTC/USDT", "ETH/USDT"])

# 获取历史K线数据
get_historical_ohlcv_okx(symbol="BTC/USDT", timeframe="1d", limit=30)

# 获取24小时统计
get_24h_stats_okx(symbol="BTC/USDT")

# 获取订单簿
get_orderbook_okx(symbol="BTC/USDT", limit=20)

# 列出可用市场
list_okx_markets()
```

### 数据存储

OKX交易记录存储在：
```
data/agent_data/{signature}/position/position_okx.jsonl
```

格式示例：
```json
{
  "date": "2025-10-29",
  "id": 1,
  "this_action": {
    "action": "buy",
    "symbol": "BTC/USDT",
    "amount": 0.001,
    "price": 45000.0,
    "cost": 45.0
  },
  "positions": {
    "USDT": 9955.0,
    "BTC": 0.001
  }
}
```

### 架构设计

```
AI-Trader/
├── agent_tools/
│   ├── tool_trade.py           # 原有股票交易工具
│   ├── tool_trade_okx.py       # 新增：OKX交易工具 ✨
│   ├── tool_get_price_local.py # 原有股票价格工具
│   ├── tool_get_price_okx.py   # 新增：OKX价格工具 ✨
│   └── start_mcp_services.py   # 更新：支持OKX服务
├── configs/
│   ├── default_config.json     # 股票交易配置
│   └── okx_crypto_config.json  # 新增：OKX加密货币配置 ✨
└── requirements.txt            # 更新：添加ccxt依赖
```

### 与股票交易的区别

| 特性 | 股票交易 | OKX加密货币交易 |
|------|---------|----------------|
| 交易标的 | NASDAQ 100股票 | 加密货币交易对 |
| 数据源 | Alpha Vantage | OKX交易所API |
| 交易时间 | 工作日市场时间 | 24/7全天候 |
| 最小单位 | 整股 | 小数（如0.001 BTC） |
| 基础货币 | USD现金 | USDT稳定币 |
| 持仓文件 | position.jsonl | position_okx.jsonl |

### 测试建议

1. **使用测试网络**：设置 `OKX_TESTNET=true`
2. **小额测试**：先用小金额测试交易流程
3. **监控日志**：查看 `logs/` 目录中的服务日志
4. **验证持仓**：检查 `position_okx.jsonl` 文件

### 安全注意事项

⚠️ **重要警告**：
- 加密货币交易具有高风险
- 本项目仅供研究和学习使用
- 不构成投资建议
- 请充分了解风险后再使用
- 妥善保管API密钥，不要泄露

### 故障排除

#### 问题：无法连接到OKX
- 检查API密钥配置是否正确
- 确认网络连接正常
- 检查OKX服务是否正常运行

#### 问题：交易失败
- 检查账户余额是否足够
- 验证交易对是否正确（如 "BTC/USDT"）
- 查看日志文件获取详细错误信息

#### 问题：价格查询失败
- OKX价格查询不需要API密钥
- 检查交易对名称格式是否正确
- 确认该交易对在OKX上存在

---

## English

### Overview

This project now supports OKX cryptocurrency exchange integration for automated crypto trading. This is an extension to the original stock trading functionality, and both trading modes can run independently.

### Important Note

**The original project does not support Binance exchange**. This update **adds OKX exchange support** rather than migrating from Binance to OKX.

### Key Features

- ✅ OKX spot trading support
- ✅ Real-time cryptocurrency price queries
- ✅ Market and limit order support
- ✅ Multiple trading pairs support (BTC/USDT, ETH/USDT, etc.)
- ✅ Testnet support (for safe testing)
- ✅ Complete position management and trading records

### Quick Start

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New dependency:
- `ccxt>=4.0.0` - Unified cryptocurrency exchange API library

#### 2. Configure OKX API Keys

Add OKX API credentials to `.env` file:

```bash
# OKX Exchange API Configuration
OKX_API_KEY="your_api_key_here"
OKX_API_SECRET="your_api_secret_here"
OKX_PASSPHRASE="your_passphrase_here"
OKX_TESTNET="true"  # Use testnet (recommended for testing first)

# OKX service ports
TRADE_OKX_HTTP_PORT=8004
GETPRICE_OKX_HTTP_PORT=8005

# Initial USDT balance
INITIAL_CASH_USDT=10000.0
```

#### 3. Get OKX API Keys

1. Visit [OKX website](https://www.okx.com)
2. Register/login to your account
3. Go to API Management page
4. Create new API key
5. Save API Key, Secret Key, and Passphrase

**Security Recommendations:**
- Use testnet first (`OKX_TESTNET=true`)
- Set IP whitelist for API keys
- Limit API permissions (only need spot trading)
- Keep API credentials secure

#### 4. Start OKX Services

```bash
cd agent_tools
python start_mcp_services.py
```

This will start all services including the new OKX trading and price query services.

#### 5. Run OKX Trading Agent

Use OKX-specific configuration file:

```bash
python main.py configs/okx_crypto_config.json
```

### Configuration File

Example `configs/okx_crypto_config.json`:

```json
{
  "agent_type": "BaseAgent",
  "trading_mode": "crypto_okx",
  "models": [
    {
      "name": "gpt-5-crypto",
      "basemodel": "openai/gpt-5",
      "signature": "gpt-5-okx-crypto",
      "enabled": true
    }
  ],
  "agent_config": {
    "initial_cash": 10000.0
  },
  "okx_config": {
    "enabled": true,
    "trading_pairs": [
      "BTC/USDT",
      "ETH/USDT",
      "SOL/USDT"
    ],
    "default_order_type": "market",
    "use_testnet": true
  }
}
```

### Available Trading Pairs

Common USDT pairs:
- BTC/USDT - Bitcoin
- ETH/USDT - Ethereum
- SOL/USDT - Solana
- BNB/USDT - Binance Coin
- XRP/USDT - Ripple
- ADA/USDT - Cardano
- DOGE/USDT - Dogecoin
- DOT/USDT - Polkadot
- MATIC/USDT - Polygon
- LINK/USDT - Chainlink

### New Tool Functions

#### Trading Tools (tool_trade_okx.py)

```python
# Buy cryptocurrency
buy_okx(symbol="BTC/USDT", amount=0.001)

# Sell cryptocurrency
sell_okx(symbol="BTC/USDT", amount=0.001)
```

#### Price Query Tools (tool_get_price_okx.py)

```python
# Get current price
get_current_price_okx(symbol="BTC/USDT")

# Get multiple prices
get_multiple_prices_okx(symbols=["BTC/USDT", "ETH/USDT"])

# Get historical OHLCV data
get_historical_ohlcv_okx(symbol="BTC/USDT", timeframe="1d", limit=30)

# Get 24-hour statistics
get_24h_stats_okx(symbol="BTC/USDT")

# Get order book
get_orderbook_okx(symbol="BTC/USDT", limit=20)

# List available markets
list_okx_markets()
```

### Data Storage

OKX trading records are stored in:
```
data/agent_data/{signature}/position/position_okx.jsonl
```

Format example:
```json
{
  "date": "2025-10-29",
  "id": 1,
  "this_action": {
    "action": "buy",
    "symbol": "BTC/USDT",
    "amount": 0.001,
    "price": 45000.0,
    "cost": 45.0
  },
  "positions": {
    "USDT": 9955.0,
    "BTC": 0.001
  }
}
```

### Architecture

```
AI-Trader/
├── agent_tools/
│   ├── tool_trade.py           # Original stock trading tool
│   ├── tool_trade_okx.py       # New: OKX trading tool ✨
│   ├── tool_get_price_local.py # Original stock price tool
│   ├── tool_get_price_okx.py   # New: OKX price tool ✨
│   └── start_mcp_services.py   # Updated: OKX service support
├── configs/
│   ├── default_config.json     # Stock trading config
│   └── okx_crypto_config.json  # New: OKX crypto config ✨
└── requirements.txt            # Updated: added ccxt dependency
```

### Differences from Stock Trading

| Feature | Stock Trading | OKX Crypto Trading |
|---------|--------------|-------------------|
| Assets | NASDAQ 100 stocks | Cryptocurrency pairs |
| Data Source | Alpha Vantage | OKX Exchange API |
| Trading Hours | Market hours (weekdays) | 24/7 |
| Minimum Unit | Whole shares | Decimals (e.g., 0.001 BTC) |
| Base Currency | USD cash | USDT stablecoin |
| Position File | position.jsonl | position_okx.jsonl |

### Testing Recommendations

1. **Use Testnet**: Set `OKX_TESTNET=true`
2. **Small Amounts**: Test with small amounts first
3. **Monitor Logs**: Check service logs in `logs/` directory
4. **Verify Positions**: Check `position_okx.jsonl` file

### Security Warnings

⚠️ **Important Warnings**:
- Cryptocurrency trading involves high risks
- This project is for research and learning purposes only
- Does not constitute investment advice
- Understand the risks before using
- Keep API keys secure and never share them

### Troubleshooting

#### Issue: Cannot connect to OKX
- Check if API key configuration is correct
- Verify network connection
- Check if OKX service is running

#### Issue: Trading failed
- Check if account balance is sufficient
- Verify trading pair format (e.g., "BTC/USDT")
- Check log files for detailed error messages

#### Issue: Price query failed
- OKX price queries don't require API keys
- Check trading pair name format
- Verify the trading pair exists on OKX

---

## 贡献 / Contributing

欢迎提交Issue和Pull Request！
Welcome to submit Issues and Pull Requests!

## 许可证 / License

MIT License
