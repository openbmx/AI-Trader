# 📦 AI-Trader 部署教程

本文档提供 AI-Trader 加密货币交易系统的完整部署指南。

## 📋 目录

- [系统要求](#系统要求)
- [快速部署](#快速部署)
- [详细配置](#详细配置)
- [OKX API配置](#okx-api配置)
- [服务启动](#服务启动)
- [常见问题](#常见问题)
- [安全注意事项](#安全注意事项)

---

## 系统要求

### 硬件要求
- **CPU**: 2核心以上
- **内存**: 4GB RAM以上
- **存储**: 10GB可用空间
- **网络**: 稳定的互联网连接

### 软件要求
- **操作系统**: Linux / macOS / Windows (推荐 Linux)
- **Python**: 3.8 或更高版本
- **pip**: Python包管理器
- **git**: 版本控制工具

---

## 快速部署

### 步骤 1: 克隆项目

```bash
git clone https://github.com/openbmx/AI-Trader.git
cd AI-Trader
```

### 步骤 2: 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 4: 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入必要的配置
nano .env  # 或使用其他文本编辑器
```

### 步骤 5: 启动服务

```bash
# 启动 MCP 服务
cd agent_tools
python start_mcp_services.py &
cd ..

# 等待服务启动
sleep 5

# 运行交易系统
python main.py
```

---

## 详细配置

### 环境变量配置

在 `.env` 文件中配置以下变量：

#### 1. AI 模型 API 配置

```bash
# OpenAI API 配置
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=your_openai_api_key_here

# 支持多种 AI 模型提供商，根据需要配置
```

#### 2. OKX 交易所 API 配置

```bash
# OKX API 密钥
OKX_API_KEY=your_okx_api_key
OKX_API_SECRET=your_okx_api_secret
OKX_PASSPHRASE=your_okx_passphrase

# 测试网络设置 (true: 使用测试网, false: 使用正式网)
OKX_TESTNET=true

# OKX 服务端口
TRADE_OKX_HTTP_PORT=8004
GETPRICE_OKX_HTTP_PORT=8005

# 初始 USDT 资金 (仅用于本地模拟)
INITIAL_CASH_USDT=10000.0
```

#### 3. Jina AI 搜索配置

```bash
# Jina AI API 密钥 (用于市场信息搜索)
JINA_API_KEY=your_jina_api_key
```

#### 4. 系统配置

```bash
# 运行时环境配置文件路径 (推荐使用绝对路径)
RUNTIME_ENV_PATH=./runtime_env.json

# MCP 服务端口配置
MATH_HTTP_PORT=8000
SEARCH_HTTP_PORT=8001

# AI 代理配置
AGENT_MAX_STEP=30  # AI 最大推理步数
```

---

## OKX API配置

### 获取 OKX API 密钥

1. **注册 OKX 账户**
   - 访问 [OKX官网](https://www.okx.com)
   - 完成注册和身份验证

2. **创建 API 密钥**
   - 登录 OKX 账户
   - 进入 **个人中心** -> **API管理**
   - 点击 **创建 API**
   - 设置 API 名称和权限

3. **配置 API 权限**
   - ✅ **读取权限**: 必需
   - ✅ **交易权限**: 必需（现货和合约）
   - ❌ **提币权限**: 不建议开启
   - 设置 IP 白名单（强烈推荐）

4. **保存密钥信息**
   - **API Key**: 复制并保存
   - **Secret Key**: 复制并保存
   - **Passphrase**: 复制并保存
   - ⚠️ **注意**: Secret Key 只会显示一次，请妥善保存

### 测试网络配置

**强烈建议先在测试网络上进行测试！**

1. 访问 [OKX 测试网](https://www.okx.com/testnet)
2. 注册测试网账户
3. 创建测试网 API 密钥
4. 在 `.env` 中设置 `OKX_TESTNET=true`
5. 测试网提供模拟资金，可以安全测试

---

## 服务启动

### 方式 1: 使用启动脚本（推荐）

```bash
# 赋予执行权限
chmod +x main.sh

# 运行启动脚本
./main.sh
```

### 方式 2: 手动启动

#### 1. 启动 MCP 服务

```bash
cd agent_tools
python start_mcp_services.py
```

这将启动以下服务：
- ✅ Math Service (端口 8000)
- ✅ Search Service (端口 8001)
- ✅ OKX Trade Service (端口 8004)
- ✅ OKX Price Service (端口 8005)

#### 2. 运行交易代理

在新的终端窗口中：

```bash
python main.py
# 或指定配置文件
python main.py configs/okx_crypto_config.json
```

### 方式 3: 后台运行

```bash
# 启动 MCP 服务（后台）
cd agent_tools
nohup python start_mcp_services.py > ../logs/mcp_services.log 2>&1 &
cd ..

# 启动交易代理（后台）
nohup python main.py > logs/trading.log 2>&1 &
```

---

## 常见问题

### Q1: 安装依赖失败

**问题**: `pip install` 报错

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者使用清华源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### Q2: OKX API 连接失败

**问题**: 提示 "OKX API credentials not set" 或连接超时

**解决方案**:
1. 检查 `.env` 文件中的 API 密钥是否正确
2. 确认 API 密钥具有交易权限
3. 检查网络连接，确保能访问 OKX API
4. 如果在中国大陆，可能需要使用代理

### Q3: 服务端口被占用

**问题**: 提示端口已被使用

**解决方案**:
```bash
# 查看占用端口的进程
lsof -i :8000  # 替换为被占用的端口号

# 杀死占用端口的进程
kill -9 <PID>

# 或者修改 .env 中的端口配置
```

### Q4: AI 模型调用失败

**问题**: OpenAI API 调用超时或失败

**解决方案**:
1. 检查 API Key 是否有效
2. 确认账户余额充足
3. 检查 API Base URL 是否正确
4. 如果使用代理，确保代理配置正确

### Q5: 权限错误

**问题**: Permission denied 错误

**解决方案**:
```bash
# 给脚本添加执行权限
chmod +x main.sh

# 检查文件夹权限
ls -la

# 如果需要，修改所有权
sudo chown -R $USER:$USER .
```

---

## 安全注意事项

### ⚠️ 重要提醒

1. **API 密钥安全**
   - ❌ 不要将 API 密钥提交到 Git 仓库
   - ❌ 不要在公开场合分享 API 密钥
   - ✅ 使用环境变量管理敏感信息
   - ✅ 定期轮换 API 密钥

2. **测试先行**
   - ✅ **务必先在测试网络上测试**
   - ✅ 从小额资金开始
   - ✅ 充分理解系统行为后再使用真实资金

3. **权限限制**
   - ✅ API 密钥只授予必要的权限
   - ✅ 设置 IP 白名单
   - ✅ 禁用提币权限

4. **风险控制**
   - ⚠️ 加密货币交易具有高风险
   - ⚠️ 仅投入可承受损失的资金
   - ⚠️ 本系统仅供学习和研究使用

5. **监控和日志**
   - ✅ 定期检查日志文件
   - ✅ 监控交易记录
   - ✅ 及时发现异常行为

6. **备份重要数据**
   - ✅ 定期备份配置文件
   - ✅ 备份交易记录
   - ✅ 保存重要的日志

---

## 生产环境部署建议

### 1. 使用 Docker 部署（推荐）

```bash
# 构建 Docker 镜像
docker build -t ai-trader .

# 运行容器
docker run -d \
  --name ai-trader \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  ai-trader
```

### 2. 使用 systemd 服务

创建服务文件 `/etc/systemd/system/ai-trader.service`:

```ini
[Unit]
Description=AI-Trader Cryptocurrency Trading System
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/AI-Trader
ExecStart=/path/to/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-trader
sudo systemctl start ai-trader
sudo systemctl status ai-trader
```

### 3. 日志管理

```bash
# 使用 logrotate 管理日志
sudo nano /etc/logrotate.d/ai-trader

# 添加配置
/path/to/AI-Trader/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 username username
}
```

---

## 监控和维护

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/health  # Math Service
curl http://localhost:8001/health  # Search Service
curl http://localhost:8004/health  # OKX Trade Service
curl http://localhost:8005/health  # OKX Price Service
```

### 查看日志

```bash
# 查看 MCP 服务日志
tail -f logs/mcp_services.log

# 查看交易日志
tail -f logs/trading.log

# 查看特定日期的交易记录
ls -la data/agent_data/*/position/
```

### 性能监控

```bash
# 检查系统资源使用
htop

# 检查 Python 进程
ps aux | grep python

# 检查网络连接
netstat -tulpn | grep python
```

---

## 更新和升级

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 重启服务
./restart.sh  # 或手动重启
```

---

## 技术支持

如果遇到问题，请：

1. 查看本文档的[常见问题](#常见问题)部分
2. 检查项目的 [GitHub Issues](https://github.com/openbmx/AI-Trader/issues)
3. 参考 [OKX集成指南](docs/OKX_INTEGRATION_GUIDE.md)
4. 在 GitHub 上提交新的 Issue

---

## 免责声明

⚠️ **重要提醒**:

- 本系统仅供学习和研究使用
- 加密货币交易具有极高风险
- 不构成任何投资建议
- 使用者需自行承担所有风险
- 开发团队不对任何损失负责

---

**祝您使用愉快！Happy Trading! 🚀**
