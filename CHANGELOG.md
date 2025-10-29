# 更新日志

## 2025-10-29 - 重大更新：专注加密货币交易

### 🚀 重大变更

#### 移除股票交易功能
- ❌ 移除所有 NASDAQ 100 股票交易相关代码
- ❌ 删除 Alpha Vantage API 集成
- ❌ 删除 100+ 个股票价格数据文件
- ❌ 移除股票交易工具 (tool_trade.py, tool_get_price_local.py)
- ❌ 移除股票数据收集脚本

#### 完善 OKX 交易功能
- ✅ **现货交易支持**: 完整的现货买卖功能
- ✅ **永续合约支持**: 支持永续合约交易 (swap)
- ✅ **交割合约支持**: 支持交割合约交易 (future)
- ✅ **资金费率查询**: 新增合约资金费率查询 API
- ✅ **多市场类型**: 支持按交易类型查询市场
- ✅ **交易类型参数**: 所有交易和价格查询函数支持 trading_type 参数

#### 文档更新
- 📖 **新增 DEPLOYMENT.md**: 详细的部署教程文档
- 📖 **精简 README.md**: 专注加密货币交易的简洁文档
- 📖 **更新 configs/README.md**: 配置文件说明更新
- 📖 **移除多语言 README**: 仅保留中文版本

### 📦 新增功能

#### OKX 交易工具增强
```python
# 现货交易
buy_okx("BTC/USDT", 0.001, trading_type="spot")
sell_okx("BTC/USDT", 0.001, trading_type="spot")

# 永续合约交易
buy_okx("BTC/USDT:USDT", 1, trading_type="swap")
sell_okx("BTC/USDT:USDT", 1, trading_type="swap")

# 资金费率查询
get_funding_rate_okx("BTC/USDT:USDT")

# 市场查询
list_okx_markets(trading_type="spot")   # 现货市场
list_okx_markets(trading_type="swap")   # 合约市场
```

### 🔧 技术改进

#### 代码结构优化
- 简化 MCP 服务配置
- 优化端口配置
- 移除冗余依赖
- 更新默认配置为 OKX

#### BaseAgent 更新
- 使用加密货币交易对作为默认符号
- 移除 stock_local MCP 服务配置
- 添加 okx_trade 和 okx_price MCP 服务
- 移除 price_tools 依赖

### 📝 配置变更

#### 环境变量更新
```bash
# 移除
ALPHAADVANTAGE_API_KEY  # 已删除
TRADE_HTTP_PORT         # 已删除
GETPRICE_HTTP_PORT      # 已删除

# 保留/新增
OKX_API_KEY            # OKX API 密钥
OKX_API_SECRET         # OKX API 密钥
OKX_PASSPHRASE         # OKX 密码短语
OKX_TESTNET            # 测试网开关
TRADE_OKX_HTTP_PORT    # OKX 交易服务端口
GETPRICE_OKX_HTTP_PORT # OKX 价格服务端口
```

#### 默认配置更新
- 默认配置文件: `configs/okx_crypto_config.json`
- 默认交易对: 加密货币 (BTC, ETH, SOL等)
- 默认资金单位: USDT

### 🗑️ 已删除文件

#### 工具文件
- `agent_tools/tool_trade.py`
- `agent_tools/tool_get_price_local.py`

#### 数据文件
- `data/daily_prices_*.json` (100+ 文件)
- `data/merged.jsonl`
- `data/get_daily_price.py`
- `data/get_interdaily_price.py`
- `data/merge_jsonl.py`

#### 配置和工具
- `configs/default_config.json`
- `tools/price_tools.py`
- `tools/result_tools.py`
- `configs/README_zh.md`

#### 文档
- `README_CN.md` (已合并到 README.md)

### 📊 统计数据

- **删除文件**: 110+
- **修改文件**: 15+
- **新增文件**: 2
- **代码行数减少**: 约 5000+ 行
- **文件大小减少**: 约 50+ MB

### ⚠️ 破坏性变更

1. **不再支持股票交易**: 所有股票交易相关功能已移除
2. **默认配置变更**: 系统默认使用 OKX 加密货币配置
3. **MCP 服务变更**: 股票相关 MCP 服务已移除
4. **数据格式变更**: 不再支持股票价格数据格式

### 🔄 迁移指南

如果您之前使用股票交易功能，请注意：

1. **不支持股票交易**: 本系统现在专注于加密货币交易
2. **配置文件需更新**: 使用 `okx_crypto_config.json` 作为模板
3. **API 密钥需更换**: 从 Alpha Vantage 切换到 OKX
4. **交易符号格式**: 从 "AAPL" 改为 "BTC/USDT"

### 🚀 后续计划

- [ ] 添加更多加密货币交易对支持
- [ ] 实现高级订单类型 (限价单、止损单等)
- [ ] 添加回测系统
- [ ] 实现实时性能监控
- [ ] 添加策略回测功能
- [ ] 支持更多交易所

### 📖 文档资源

- [README.md](README.md) - 项目简介和快速开始
- [DEPLOYMENT.md](DEPLOYMENT.md) - 详细部署教程
- [docs/OKX_INTEGRATION_GUIDE.md](docs/OKX_INTEGRATION_GUIDE.md) - OKX 集成指南

---

**版本**: v2.0.0-crypto  
**发布日期**: 2025-10-29  
**重要性**: 🔴 重大更新
