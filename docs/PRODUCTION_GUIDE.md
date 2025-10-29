# 🚀 Production Deployment Guide

生产环境部署完整指南，确保系统安全、稳定运行。

## 📋 目录

- [生产环境检查清单](#生产环境检查清单)
- [安全配置](#安全配置)
- [系统监控](#系统监控)
- [错误处理](#错误处理)
- [性能优化](#性能优化)
- [备份与恢复](#备份与恢复)

---

## 生产环境检查清单

### ✅ 部署前检查

#### 1. 环境配置

- [ ] 所有必需的环境变量已设置
- [ ] API 密钥已验证且有效
- [ ] 使用生产级 API 密钥（非测试密钥）
- [ ] `.env` 文件权限设置为 600 (`chmod 600 .env`)
- [ ] 密钥未被提交到代码仓库
- [ ] 已设置 API 速率限制和使用配额

#### 2. OKX 交易配置

- [ ] **重要**: 已在测试网充分测试
- [ ] OKX API 权限仅限必要权限（禁用提币）
- [ ] 设置了 IP 白名单
- [ ] `OKX_TESTNET` 设置正确（生产环境为 `false`）
- [ ] 初始资金设置合理
- [ ] 交易限额设置适当
- [ ] 风控参数已配置

#### 3. AI 模型配置

- [ ] 选择了适合生产环境的模型
- [ ] API 配额足够支撑预期使用量
- [ ] 超时和重试参数设置合理
- [ ] 已测试模型响应质量
- [ ] 备用模型已配置（可选）

#### 4. 系统资源

- [ ] 服务器资源充足（CPU、内存、磁盘）
- [ ] 网络连接稳定可靠
- [ ] 磁盘空间足够（日志、数据）
- [ ] 已设置日志轮转
- [ ] 监控工具已部署

#### 5. 依赖和版本

- [ ] Python 版本 >= 3.8
- [ ] 所有依赖已安装 (`pip install -r requirements.txt`)
- [ ] 依赖版本已锁定
- [ ] 虚拟环境已创建和激活

---

## 安全配置

### 🔒 API 密钥管理

#### 最佳实践

1. **使用环境变量**
   ```bash
   # 好的做法 ✅
   export OPENAI_API_KEY="sk-..."
   
   # 不好的做法 ❌
   # 直接在代码中硬编码
   ```

2. **文件权限**
   ```bash
   # 限制 .env 文件访问权限
   chmod 600 .env
   
   # 确保日志文件安全
   chmod 644 data/agent_data/*/log/*.jsonl
   ```

3. **密钥轮换**
   - 定期更换 API 密钥（建议每 90 天）
   - 立即撤销泄露的密钥
   - 使用密钥管理服务（如 AWS Secrets Manager）

4. **访问控制**
   ```bash
   # OKX API 设置
   # 1. 只授予必要权限（读取、交易，禁用提币）
   # 2. 设置 IP 白名单
   # 3. 限制 API 密钥使用范围
   ```

### 🛡️ 网络安全

1. **防火墙配置**
   ```bash
   # 只开放必要端口
   ufw allow 8000/tcp  # MCP 服务端口
   ufw allow 8001/tcp
   ufw allow 8004/tcp
   ufw allow 8005/tcp
   ufw enable
   ```

2. **HTTPS/TLS**
   - 使用 HTTPS 连接外部 API
   - 验证 SSL 证书
   - 使用最新的 TLS 版本

3. **DDoS 防护**
   - 使用反向代理（如 Nginx）
   - 配置速率限制
   - 监控异常流量

### 🔐 数据安全

1. **敏感数据加密**
   ```bash
   # 加密存储的交易记录
   # 考虑使用数据库加密
   ```

2. **日志安全**
   - 不在日志中记录密钥
   - 脱敏敏感信息
   - 定期清理旧日志

3. **备份加密**
   ```bash
   # 加密备份文件
   tar -czf backup.tar.gz data/
   gpg --encrypt backup.tar.gz
   ```

---

## 系统监控

### 📊 监控指标

#### 1. 系统健康

创建健康检查脚本 `health_check.sh`:
```bash
#!/bin/bash

# 检查 MCP 服务
for port in 8000 8001 8004 8005; do
  if ! curl -s http://localhost:$port/health > /dev/null; then
    echo "❌ Port $port is down"
    exit 1
  fi
done

# 检查磁盘空间
disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $disk_usage -gt 80 ]; then
  echo "⚠️  Disk usage is high: ${disk_usage}%"
fi

# 检查内存使用
mem_usage=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
if [ $mem_usage -gt 80 ]; then
  echo "⚠️  Memory usage is high: ${mem_usage}%"
fi

echo "✅ System health check passed"
```

#### 2. 交易监控

监控指标：
- 交易执行成功率
- 平均响应时间
- API 调用次数和失败率
- 持仓变化
- 资金余额

#### 3. 错误监控

```python
# 在代码中添加错误追踪
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)
```

### 📈 性能指标

1. **AI 模型响应时间**
2. **MCP 工具调用延迟**
3. **OKX API 响应时间**
4. **交易执行延迟**

---

## 错误处理

### 🔄 重试机制

系统已内置重试机制，可通过配置调整：

```json
{
  "agent_config": {
    "max_retries": 3,
    "base_delay": 1.0
  }
}
```

### 📝 错误日志

所有错误会记录在：
- `data/agent_data/{signature}/log/{date}/log.jsonl`
- 系统标准输出/错误输出

### 🚨 告警配置

建议配置告警：
1. API 调用失败
2. 交易执行失败
3. 资金余额低于阈值
4. 系统资源不足
5. 服务异常停止

---

## 性能优化

### ⚡ 配置优化

1. **调整 max_steps**
   ```json
   {
     "agent_config": {
       "max_steps": 20  // 减少以提高速度
     }
   }
   ```

2. **使用更快的模型**
   - 开发: Ollama 本地模型
   - 生产: GPT-3.5-turbo (比 GPT-4 快)
   - 高性价比: DeepSeek

3. **并行处理**
   - 多模型可并行运行
   - 使用异步 I/O

### 💾 资源管理

1. **内存管理**
   ```python
   # 定期清理不需要的数据
   # 限制日志文件大小
   ```

2. **磁盘管理**
   ```bash
   # 定期清理旧日志
   find data/agent_data/*/log -type f -mtime +30 -delete
   
   # 日志轮转
   logrotate /etc/logrotate.d/ai-trader
   ```

---

## 备份与恢复

### 💾 备份策略

#### 1. 数据备份

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backup/ai-trader"

# 备份配置和数据
tar -czf "$BACKUP_DIR/backup-$DATE.tar.gz" \
  configs/ \
  data/agent_data/ \
  .env

# 保留最近 7 天的备份
find $BACKUP_DIR -type f -mtime +7 -delete

echo "✅ Backup completed: backup-$DATE.tar.gz"
```

#### 2. 自动备份

```bash
# 添加到 crontab
crontab -e

# 每天凌晨 2 点备份
0 2 * * * /path/to/backup.sh
```

### 🔄 恢复流程

```bash
# 1. 解压备份
tar -xzf backup-20251029.tar.gz

# 2. 恢复配置
cp -r configs/ /path/to/ai-trader/
cp .env /path/to/ai-trader/

# 3. 恢复数据
cp -r data/agent_data/ /path/to/ai-trader/data/

# 4. 验证恢复
python main.py --dry-run
```

---

## 运行时管理

### 🚀 启动服务

使用 systemd 管理服务（推荐）：

```ini
# /etc/systemd/system/ai-trader.service
[Unit]
Description=AI-Trader Crypto Trading System
After=network.target

[Service]
Type=simple
User=trader
WorkingDirectory=/opt/ai-trader
Environment="PATH=/opt/ai-trader/venv/bin"
ExecStart=/opt/ai-trader/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动和管理：
```bash
# 启动服务
sudo systemctl start ai-trader

# 设置开机自启
sudo systemctl enable ai-trader

# 查看状态
sudo systemctl status ai-trader

# 查看日志
sudo journalctl -u ai-trader -f
```

### 🛑 优雅停止

```bash
# 发送停止信号
sudo systemctl stop ai-trader

# 等待当前交易完成
# 系统会自动保存状态
```

---

## 维护计划

### 📅 日常维护

- [ ] 检查系统运行状态
- [ ] 查看错误日志
- [ ] 监控资金余额和持仓
- [ ] 验证 API 配额使用情况

### 📅 周度维护

- [ ] 审查交易记录
- [ ] 分析性能指标
- [ ] 更新依赖包
- [ ] 备份验证

### 📅 月度维护

- [ ] 安全审计
- [ ] 密钥轮换
- [ ] 系统更新
- [ ] 容量规划

---

## 故障处理

### 🔧 常见问题

#### 问题 1: MCP 服务无法启动

```bash
# 检查端口占用
netstat -tulpn | grep 8000

# 杀死占用进程
kill -9 <PID>

# 重新启动
python agent_tools/start_mcp_services.py
```

#### 问题 2: API 调用失败

```bash
# 检查网络连接
curl -I https://api.openai.com

# 验证 API 密钥
# 查看日志获取详细错误信息
```

#### 问题 3: 交易执行失败

```bash
# 检查 OKX API 状态
# 验证账户余额
# 确认交易对是否可用
```

---

## 合规性

### ⚖️ 法律合规

1. **了解当地法规**
   - 加密货币交易的合法性
   - 自动交易的合规要求
   - 税务申报义务

2. **风险披露**
   - 向用户明确风险
   - 保留完整交易记录
   - 遵守 KYC/AML 要求

3. **数据保护**
   - 遵守 GDPR/数据保护法
   - 用户数据加密
   - 数据保留政策

---

## 应急响应

### 🚨 应急预案

#### 1. 系统故障

```bash
# 立即停止交易
sudo systemctl stop ai-trader

# 评估损失
python scripts/analyze_positions.py

# 手动平仓（如需要）
# 通过 OKX 网页或 API
```

#### 2. API 密钥泄露

```bash
# 立即撤销密钥
# 在提供商控制台操作

# 生成新密钥
# 更新 .env 配置

# 审查访问日志
# 查找异常活动
```

#### 3. 异常交易

```bash
# 查看交易记录
cat data/agent_data/*/position/position_okx.jsonl

# 暂停系统
sudo systemctl stop ai-trader

# 调查原因
# 查看 AI 决策日志
```

---

## 联系支持

如遇到问题：
1. 查看本文档
2. 查看项目 GitHub Issues
3. 联系技术支持

---

## 附录

### 环境变量完整清单

```bash
# AI 模型
OPENAI_API_BASE=
OPENAI_API_KEY=
OLLAMA_API_BASE=
DEEPSEEK_API_BASE=
DEEPSEEK_API_KEY=
ANTHROPIC_API_KEY=

# 搜索服务
JINA_API_KEY=

# 交易所
OKX_API_KEY=
OKX_API_SECRET=
OKX_PASSPHRASE=
OKX_TESTNET=

# 服务端口
MATH_HTTP_PORT=
SEARCH_HTTP_PORT=
TRADE_OKX_HTTP_PORT=
GETPRICE_OKX_HTTP_PORT=

# 代理配置
AGENT_MAX_STEP=
INITIAL_CASH_USDT=
```

### 权限检查脚本

```bash
#!/bin/bash
# check_permissions.sh

echo "Checking file permissions..."

# 检查 .env 文件
if [ -f .env ]; then
  perm=$(stat -c %a .env)
  if [ "$perm" != "600" ]; then
    echo "⚠️  .env permissions: $perm (should be 600)"
  else
    echo "✅ .env permissions: OK"
  fi
fi

# 检查数据目录
if [ -d data/agent_data ]; then
  echo "✅ Data directory exists"
else
  echo "⚠️  Data directory not found"
fi

echo "Permission check completed"
```

---

**最后更新**: 2025-10-29
