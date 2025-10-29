<div align="center">

# 🚀 AI-Trader: AI驱动的加密货币交易系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**让多个AI模型在加密货币市场中完全自主决策、同台竞技！**

[🚀 快速开始](#-快速开始) • [📖 部署教程](DEPLOYMENT.md) • [🛠️ 配置指南](#-配置指南) • [💡 功能特性](#-核心特性)

</div>

---

## 🌟 项目介绍

AI-Trader 是一个完全自主的AI加密货币交易系统，让多个大语言模型在OKX交易所进行7x24小时的自主交易竞赛。

### ✨ 核心特性

- 🤖 **完全自主决策**: AI代理100%独立分析、决策、执行，零人工干预
- 💱 **OKX交易所支持**: 完整支持现货和永续合约交易
- 🛠️ **纯工具驱动**: 基于MCP工具链的标准化工具调用架构
- 🏆 **多模型竞技**: 支持多个AI模型（GPT、Claude、Qwen等）同时交易
- 📊 **实时监控**: 完整的交易记录、持仓管理和性能分析
- 🔍 **智能资讯**: 集成Jina AI搜索，获取实时市场新闻
- 🌐 **7x24交易**: 全天候加密货币市场交易

---

## 🎮 交易环境

- 💰 **初始资金**: 10,000 USDT
- 📈 **交易标的**: 主流加密货币（BTC、ETH、SOL等）
- ⏰ **交易时间**: 7x24小时全天候
- 💹 **交易类型**: 支持现货和永续合约
- 📊 **数据来源**: OKX交易所实时数据

---

## 🚀 快速开始

### 📋 前置要求

- Python 3.8+
- OKX 交易所账户和 API 密钥
- AI 模型 API 密钥（支持多种选择）:
  - OpenAI (GPT-4, GPT-3.5)
  - Ollama (本地部署，免费)
  - DeepSeek (高性价比)
  - Anthropic Claude
  - GitHub Copilot (企业版)
  - Google Gemini

### ⚡ 一键安装

```bash
# 1. 克隆项目
git clone https://github.com/openbmx/AI-Trader.git
cd AI-Trader

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥

# 4. 验证配置（可选但推荐）
python main.py --validate-only

# 5. 启动服务
./main.sh
```

**详细部署教程请查看：[📖 DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 🔑 环境配置

在 `.env` 文件中配置以下变量：

```bash
# AI 模型 API (选择一个或多个)
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=your_openai_key

# Ollama 本地模型（可选）
OLLAMA_API_BASE=http://localhost:11434/v1

# DeepSeek API（可选）
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
DEEPSEEK_API_KEY=your_deepseek_key

# OKX 交易所 API
OKX_API_KEY=your_okx_api_key
OKX_API_SECRET=your_okx_secret
OKX_PASSPHRASE=your_okx_passphrase
OKX_TESTNET=true  # 建议先使用测试网

# Jina AI 搜索
JINA_API_KEY=your_jina_key

# 其他配置
INITIAL_CASH_USDT=10000.0
AGENT_MAX_STEP=30
```

**更多 AI 提供商配置请查看：[🤖 AI Providers Guide](docs/AI_PROVIDERS_GUIDE.md)**

---

## 🛠️ 配置指南

### 配置文件结构

```json
{
  "agent_type": "BaseAgent",
  "date_range": {
    "init_date": "2025-01-01",
    "end_date": "2025-01-31"
  },
  "models": [
    {
      "name": "gpt-5-crypto",
      "basemodel": "openai/gpt-5",
      "signature": "gpt-5-okx-crypto",
      "enabled": true
    },
    {
      "name": "ollama-llama3",
      "basemodel": "ollama/llama3",
      "signature": "llama3-okx-crypto",
      "enabled": false
    }
  ],
  "agent_config": {
    "max_steps": 30,
    "initial_cash": 10000.0
  }
}
```

### 支持的交易对

#### 现货交易
- BTC/USDT、ETH/USDT、SOL/USDT
- BNB/USDT、XRP/USDT、ADA/USDT
- 以及更多主流币种

#### 永续合约
- BTC/USDT:USDT、ETH/USDT:USDT
- SOL/USDT:USDT、BNB/USDT:USDT
- 以及更多合约交易对

---

## 📁 项目架构

```
AI-Trader/
├── 🤖 核心系统
│   ├── main.py                     # 主程序入口
│   ├── agent/base_agent/           # AI 代理核心
│   └── configs/                    # 配置文件
│
├── 🛠️ MCP 工具链
│   ├── agent_tools/
│   │   ├── tool_trade_okx.py       # OKX 交易执行
│   │   ├── tool_get_price_okx.py   # OKX 价格查询
│   │   ├── tool_jina_search.py     # 信息搜索
│   │   └── tool_math.py            # 数学计算
│   └── tools/                      # 辅助工具
│
├── 📊 数据系统
│   └── data/agent_data/            # AI 交易记录
│
└── 📋 文档
    ├── README.md                   # 本文档
    ├── DEPLOYMENT.md               # 详细部署教程
    └── docs/                       # 其他文档
```

---

## 🔧 功能说明

### MCP 工具链

| 工具 | 功能 | 说明 |
|------|------|------|
| **OKX交易工具** | 买入/卖出加密货币 | 支持现货和合约交易 |
| **OKX价格工具** | 实时价格查询 | 支持多种交易对和市场类型 |
| **搜索工具** | 市场信息搜索 | 获取新闻和市场动态 |
| **数学工具** | 财务计算 | 支持基础数学运算 |

### 交易功能

#### 现货交易
```python
# 买入现货
buy_okx(symbol="BTC/USDT", amount=0.001, trading_type="spot")

# 卖出现货
sell_okx(symbol="BTC/USDT", amount=0.001, trading_type="spot")
```

#### 永续合约交易
```python
# 开多单
buy_okx(symbol="BTC/USDT:USDT", amount=1, trading_type="swap")

# 平仓
sell_okx(symbol="BTC/USDT:USDT", amount=1, trading_type="swap")
```

#### 价格查询
```python
# 查询现货价格
get_current_price_okx(symbol="BTC/USDT", trading_type="spot")

# 查询合约价格和资金费率
get_current_price_okx(symbol="BTC/USDT:USDT", trading_type="swap")
get_funding_rate_okx(symbol="BTC/USDT:USDT")
```

---

## 📊 交易记录

交易记录保存在 `data/agent_data/{signature}/position/position_okx.jsonl`：

```json
{
  "date": "2025-10-29",
  "id": 1,
  "this_action": {
    "action": "buy",
    "symbol": "BTC/USDT",
    "amount": 0.001,
    "price": 45000.0,
    "cost": 45.0,
    "trading_type": "spot"
  },
  "positions": {
    "USDT": 9955.0,
    "BTC": 0.001
  }
}
```

---

## ⚠️ 安全注意事项

### 重要提醒

1. **测试先行**
   - ✅ **务必先在测试网络测试**
   - ✅ 从小额资金开始
   - ⚠️ 充分理解系统后再使用真实资金

2. **API 密钥安全**
   - ❌ 不要将密钥提交到代码仓库
   - ✅ 使用环境变量管理
   - ✅ 设置 IP 白名单
   - ✅ 限制 API 权限（禁用提币）

3. **风险控制**
   - ⚠️ 加密货币交易具有极高风险
   - ⚠️ 仅投入可承受损失的资金
   - ⚠️ 本系统仅供学习研究

---

## 🚀 高级功能

### 合约交易策略

支持多种合约交易类型：
- **永续合约 (swap)**: 无到期日的期货合约
- **交割合约 (future)**: 有固定到期日的期货合约

### 资金费率监控

```python
# 获取合约资金费率
get_funding_rate_okx("BTC/USDT:USDT")
```

### 多市场查询

```python
# 列出所有现货市场
list_okx_markets(trading_type="spot")

# 列出所有永续合约
list_okx_markets(trading_type="swap")
```

---

## 📖 文档

- [📦 详细部署教程](DEPLOYMENT.md) - 完整的部署和配置指南
- [🤖 AI Providers Guide](docs/AI_PROVIDERS_GUIDE.md) - AI 提供商配置指南
- [🚀 Production Guide](docs/PRODUCTION_GUIDE.md) - 生产环境部署指南
- [🔧 OKX 集成指南](docs/OKX_INTEGRATION_GUIDE.md) - OKX API 使用说明
- [💬 社区交流](Communication.md) - 加入我们的社区

---

## 🤝 贡献指南

欢迎贡献代码、提出建议或报告问题！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 免责声明

⚠️ **重要声明**:

- 本系统仅供学习和研究使用
- 不构成任何投资建议
- 加密货币交易具有极高风险
- 使用者需自行承担所有风险和损失
- 开发团队不对任何交易损失负责

---

<div align="center">

**🌟 如果这个项目对你有帮助，请给我们一个 Star！**

[![GitHub stars](https://img.shields.io/github/stars/openbmx/AI-Trader?style=social)](https://github.com/openbmx/AI-Trader)

**🤖 让 AI 在加密货币市场中完全自主决策！** 🚀

</div>

---

## ⭐ 项目统计

<div align="center">
  <img src="https://visitor-badge.laobi.icu/badge?page_id=openbmx.AI-Trader&style=for-the-badge&color=00d4ff" alt="访问量">
</div>
