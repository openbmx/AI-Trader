# 配置文件说明

本目录包含 AI-Trader 系统的配置文件。

## 配置文件

### okx_crypto_config.json

OKX 加密货币交易配置文件（默认配置）

```json
{
  "agent_type": "BaseAgent",
  "trading_mode": "crypto_okx",
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
    }
  ],
  "agent_config": {
    "max_steps": 30,
    "max_retries": 3,
    "base_delay": 1.0,
    "initial_cash": 10000.0
  },
  "log_config": {
    "log_path": "./data/agent_data"
  }
}
```

## 配置参数说明

### 基础配置

- **agent_type**: AI 代理类型，默认 "BaseAgent"
- **trading_mode**: 交易模式，设置为 "crypto_okx" 表示使用 OKX 加密货币交易

### 日期范围 (date_range)

- **init_date**: 开始日期 (YYYY-MM-DD 格式)
- **end_date**: 结束日期 (YYYY-MM-DD 格式)

### 模型配置 (models)

每个模型包含：
- **name**: 模型显示名称
- **basemodel**: 模型路径（例如 "openai/gpt-5"）
- **signature**: 模型签名，用于标识交易记录
- **enabled**: 是否启用该模型

### AI代理配置 (agent_config)

- **max_steps**: AI 最大推理步数（默认 30）
- **max_retries**: 最大重试次数（默认 3）
- **base_delay**: 操作延迟秒数（默认 1.0）
- **initial_cash**: 初始资金，USDT（默认 10000.0）

### 日志配置 (log_config)

- **log_path**: 日志和交易记录保存路径

## 创建自定义配置

可以复制 `okx_crypto_config.json` 并修改以创建自定义配置：

```bash
cp okx_crypto_config.json my_config.json
# 编辑 my_config.json
nano my_config.json
```

然后使用自定义配置运行：

```bash
python main.py configs/my_config.json
```

## 支持的交易对

### 现货交易
- BTC/USDT, ETH/USDT, SOL/USDT
- BNB/USDT, XRP/USDT, ADA/USDT
- DOGE/USDT, DOT/USDT, MATIC/USDT
- 等更多交易对

### 永续合约
- BTC/USDT:USDT, ETH/USDT:USDT
- SOL/USDT:USDT, BNB/USDT:USDT
- 等更多合约交易对

## 注意事项

1. 配置文件必须是有效的 JSON 格式
2. 日期格式必须为 YYYY-MM-DD
3. initial_cash 单位为 USDT
4. 建议先在测试网络上测试配置
