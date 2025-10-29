# 更新日志

## 2025-10-29 - v2.1.0 - 多AI提供商支持与生产环境增强

### 🤖 新增功能

#### 多AI模型提供商支持
- ✅ **OpenAI**: GPT-4, GPT-3.5, GPT-4 Turbo等
- ✅ **Ollama**: 本地自建模型 (Llama3, Mistral, Qwen等)
- ✅ **DeepSeek**: 高性价比中国AI服务
- ✅ **Anthropic Claude**: Claude 3.5 Sonnet, Claude 3 Opus
- ✅ **GitHub Copilot**: 企业用户支持
- ✅ **Google Gemini**: Gemini Pro, Gemini Ultra

#### 统一AI提供商接口
```python
# 自动识别提供商
basemodel = "ollama/llama3"      # Ollama
basemodel = "openai/gpt-4"       # OpenAI
basemodel = "deepseek/deepseek-chat"  # DeepSeek
basemodel = "anthropic/claude-3-5-sonnet-20241022"  # Claude
```

#### 配置验证系统
- ✅ 环境变量完整性检查
- ✅ API密钥有效性验证
- ✅ 配置文件格式验证
- ✅ 系统资源检查
- ✅ 安全配置审计

#### 生产环境工具
- ✅ 预部署检查脚本
- ✅ 安全审计工具
- ✅ 配置验证命令行工具

### 📖 新增文档

#### 完整的生产环境指南
- 📖 **AI Providers Guide** (`docs/AI_PROVIDERS_GUIDE.md`)
  - 6种AI提供商详细配置
  - 使用场景和最佳实践
  - 成本对比和选择建议
  - 故障排除指南

- 📖 **Production Guide** (`docs/PRODUCTION_GUIDE.md`)
  - 生产环境部署清单
  - 安全配置最佳实践
  - 系统监控和告警
  - 错误处理和恢复
  - 备份策略
  - 合规性建议

### 🛠️ 示例配置

#### 新增配置模板
- `configs/ollama_config.json` - Ollama本地模型配置
- `configs/deepseek_config.json` - DeepSeek配置
- `configs/anthropic_config.json` - Anthropic Claude配置

### 🔧 技术改进

#### BaseAgent增强
- 使用新的AI提供商工厂模式
- 支持多种AI后端自动切换
- 改进错误处理和日志记录

#### 命令行工具增强
```bash
# 验证配置
python main.py --validate-only

# 跳过验证（不推荐）
python main.py --skip-validation

# 使用指定配置文件
python main.py configs/ollama_config.json
```

### 🔐 安全增强

#### 配置验证工具
- 自动检查API密钥配置
- 验证文件权限（.env应为600）
- 检查敏感文件访问权限
- OKX测试网/正式网环境确认

#### 安全审计工具
- 扫描代码中的硬编码密钥
- 检测潜在的安全漏洞
- 文件权限审计
- 生成详细安全报告

#### 预部署检查脚本
```bash
./scripts/pre_deployment_check.sh
```
- 9项全面检查
- Python版本验证
- 依赖完整性检查
- 网络连接测试
- 安全审计执行

### 📝 环境变量更新

#### 新增环境变量
```bash
# Ollama (本地模型)
OLLAMA_API_BASE="http://localhost:11434/v1"

# DeepSeek
DEEPSEEK_API_BASE="https://api.deepseek.com/v1"
DEEPSEEK_API_KEY="your_key"

# Anthropic
ANTHROPIC_API_KEY="your_key"

# GitHub Copilot
GITHUB_COPILOT_API_BASE="https://api.githubcopilot.com/v1"
GITHUB_COPILOT_API_KEY="your_key"

# Google Gemini
GOOGLE_GEMINI_API_BASE="https://generativelanguage.googleapis.com/v1"
GOOGLE_GEMINI_API_KEY="your_key"
```

### 📦 依赖更新
- 新增 `python-dotenv>=1.0.0` 用于环境变量管理
- 可选依赖: `langchain-anthropic` (用于Claude支持)

### 🎯 使用场景推荐

| 场景 | 推荐AI提供商 | 理由 |
|------|-------------|------|
| 高质量决策 | OpenAI GPT-4, Claude 3.5 | 最佳推理能力 |
| 成本敏感 | DeepSeek, Ollama | 价格低廉或免费 |
| 离线部署 | Ollama | 无需外网连接 |
| 国内用户 | DeepSeek | 访问速度快 |
| 企业用户 | GitHub Copilot | 已有订阅 |

### 🔄 迁移指南

#### 从单一AI提供商迁移
如果您之前只使用OpenAI：

1. **保持现有配置**：现有配置完全兼容
2. **可选添加新提供商**：在 `.env` 中添加其他提供商密钥
3. **更新配置文件**：在models中添加新模型

示例：
```json
{
  "models": [
    {
      "name": "gpt-4",
      "basemodel": "openai/gpt-4",
      "signature": "gpt-4-okx",
      "enabled": true
    },
    {
      "name": "ollama-llama3",
      "basemodel": "ollama/llama3",
      "signature": "llama3-okx",
      "enabled": true
    }
  ]
}
```

### ⚡ 性能优化

#### 本地部署优势
- Ollama可完全离线运行
- 无API调用成本
- 更低的延迟（本地网络）
- 无速率限制

#### 成本优化
- DeepSeek价格约为OpenAI的1/10
- Ollama完全免费（需要本地GPU）
- 多模型并行可提高决策质量

### 🐛 Bug修复
- 修复API密钥验证逻辑
- 改进错误信息提示
- 优化日志输出格式

### 📊 统计数据
- **新增文件**: 8
- **修改文件**: 5
- **新增代码**: 约2000行
- **新增文档**: 约13000字

### 🚀 后续计划
- [ ] 添加更多AI提供商（Cohere, Mistral AI等）
- [ ] 实现AI模型性能对比功能
- [ ] 添加自动故障转移（一个模型失败时切换到备用）
- [ ] 实现成本追踪和预算控制
- [ ] 添加模型响应质量评分

### 📖 相关文档
- [AI Providers Guide](docs/AI_PROVIDERS_GUIDE.md) - AI提供商配置详解
- [Production Guide](docs/PRODUCTION_GUIDE.md) - 生产环境部署指南
- [DEPLOYMENT.md](DEPLOYMENT.md) - 基础部署教程

---

**版本**: v2.1.0  
**发布日期**: 2025-10-29  
**重要性**: 🟢 重要更新 - 向后兼容

---

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
