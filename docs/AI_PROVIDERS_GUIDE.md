# 🤖 AI Provider Integration Guide

本文档详细介绍了 AI-Trader 支持的所有 AI 模型提供商及其配置方法。

## 📋 目录

- [支持的 AI 提供商](#支持的-ai-提供商)
- [配置方法](#配置方法)
- [使用示例](#使用示例)
- [故障排除](#故障排除)

---

## 支持的 AI 提供商

AI-Trader 现在支持以下 AI 模型提供商：

### 1. OpenAI (官方)

- **模型**: GPT-4, GPT-3.5, GPT-4 Turbo 等
- **适用场景**: 生产环境，高质量决策
- **费用**: 按使用量付费
- **配置前缀**: `openai/`

### 2. Ollama (本地自建)

- **模型**: Llama 3, Mistral, Qwen, 等开源模型
- **适用场景**: 本地部署，无需外网，成本优化
- **费用**: 免费（需要本地GPU资源）
- **配置前缀**: `ollama/`

### 3. DeepSeek (中国)

- **模型**: DeepSeek Chat, DeepSeek Coder
- **适用场景**: 国内用户，高性价比
- **费用**: 按使用量付费（相对便宜）
- **配置前缀**: `deepseek/`

### 4. Anthropic Claude

- **模型**: Claude 3.5 Sonnet, Claude 3 Opus
- **适用场景**: 需要高级推理能力
- **费用**: 按使用量付费
- **配置前缀**: `anthropic/`

### 5. GitHub Copilot (企业)

- **模型**: GitHub Copilot 模型
- **适用场景**: 已有 GitHub 企业订阅
- **费用**: 企业订阅包含
- **配置前缀**: `github_copilot/`
- **注意**: 需要 GitHub 企业账户

### 6. Google Gemini

- **模型**: Gemini Pro, Gemini Ultra
- **适用场景**: Google Cloud 用户
- **费用**: 按使用量付费
- **配置前缀**: `google_gemini/`

---

## 配置方法

### 通用配置步骤

1. **在 `.env` 文件中设置 API 密钥**
2. **在配置文件中指定模型**
3. **运行系统**

### 详细配置

#### 1. OpenAI 配置

**环境变量** (`.env`):
```bash
OPENAI_API_BASE="https://api.openai.com/v1"
OPENAI_API_KEY="sk-your-api-key-here"
```

**配置文件** (`configs/okx_crypto_config.json`):
```json
{
  "models": [
    {
      "name": "gpt-4-trader",
      "basemodel": "openai/gpt-4",
      "signature": "gpt-4-okx-crypto",
      "enabled": true
    }
  ]
}
```

#### 2. Ollama 配置 (本地)

**前置要求**:
- 安装 Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
- 下载模型: `ollama pull llama3`
- 启动服务: `ollama serve`

**环境变量** (`.env`):
```bash
OLLAMA_API_BASE="http://localhost:11434/v1"
# Ollama 不需要 API 密钥
```

**配置文件** (`configs/ollama_config.json`):
```json
{
  "models": [
    {
      "name": "llama3-trader",
      "basemodel": "ollama/llama3",
      "signature": "llama3-okx-crypto",
      "enabled": true
    }
  ]
}
```

**支持的 Ollama 模型**:
- `llama3` - Meta Llama 3
- `llama3.1` - Meta Llama 3.1
- `mistral` - Mistral 7B
- `qwen` - Alibaba Qwen
- `mixtral` - Mixtral 8x7B
- 更多模型见: https://ollama.com/library

#### 3. DeepSeek 配置

**获取 API 密钥**: https://platform.deepseek.com/

**环境变量** (`.env`):
```bash
DEEPSEEK_API_BASE="https://api.deepseek.com/v1"
DEEPSEEK_API_KEY="sk-your-deepseek-key"
```

**配置文件** (`configs/deepseek_config.json`):
```json
{
  "models": [
    {
      "name": "deepseek-chat",
      "basemodel": "deepseek/deepseek-chat",
      "signature": "deepseek-okx-crypto",
      "enabled": true
    }
  ]
}
```

**优势**:
- 价格低廉（相比 OpenAI）
- 支持中文
- 国内访问速度快

#### 4. Anthropic Claude 配置

**获取 API 密钥**: https://console.anthropic.com/

**环境变量** (`.env`):
```bash
ANTHROPIC_API_KEY="sk-ant-your-api-key"
```

**配置文件** (`configs/anthropic_config.json`):
```json
{
  "models": [
    {
      "name": "claude-sonnet",
      "basemodel": "anthropic/claude-3-5-sonnet-20241022",
      "signature": "claude-okx-crypto",
      "enabled": true
    }
  ]
}
```

**注意**: 需要安装额外依赖:
```bash
pip install langchain-anthropic
```

#### 5. GitHub Copilot 配置 (企业)

**前置要求**: GitHub 企业订阅

**环境变量** (`.env`):
```bash
GITHUB_COPILOT_API_BASE="https://api.githubcopilot.com/v1"
GITHUB_COPILOT_API_KEY="your-github-token"
```

**配置文件**:
```json
{
  "models": [
    {
      "name": "copilot-trader",
      "basemodel": "github_copilot/gpt-4",
      "signature": "copilot-okx-crypto",
      "enabled": true
    }
  ]
}
```

#### 6. Google Gemini 配置

**获取 API 密钥**: https://makersuite.google.com/app/apikey

**环境变量** (`.env`):
```bash
GOOGLE_GEMINI_API_BASE="https://generativelanguage.googleapis.com/v1"
GOOGLE_GEMINI_API_KEY="your-gemini-api-key"
```

**配置文件**:
```json
{
  "models": [
    {
      "name": "gemini-trader",
      "basemodel": "google_gemini/gemini-pro",
      "signature": "gemini-okx-crypto",
      "enabled": true
    }
  ]
}
```

---

## 使用示例

### 单模型运行

```bash
# 使用 OpenAI GPT-4
python main.py configs/okx_crypto_config.json

# 使用本地 Ollama
python main.py configs/ollama_config.json

# 使用 DeepSeek
python main.py configs/deepseek_config.json
```

### 多模型竞技

可以在一个配置文件中同时启用多个模型：

```json
{
  "models": [
    {
      "name": "gpt-4",
      "basemodel": "openai/gpt-4",
      "signature": "gpt-4-okx-crypto",
      "enabled": true
    },
    {
      "name": "claude-sonnet",
      "basemodel": "anthropic/claude-3-5-sonnet-20241022",
      "signature": "claude-okx-crypto",
      "enabled": true
    },
    {
      "name": "deepseek",
      "basemodel": "deepseek/deepseek-chat",
      "signature": "deepseek-okx-crypto",
      "enabled": true
    }
  ]
}
```

### 在配置文件中覆盖 API 配置

可以在模型配置中直接指定 API 密钥：

```json
{
  "models": [
    {
      "name": "custom-model",
      "basemodel": "openai/gpt-4",
      "signature": "custom-okx-crypto",
      "enabled": true,
      "openai_base_url": "https://custom-api.example.com/v1",
      "openai_api_key": "custom-key-here"
    }
  ]
}
```

---

## 故障排除

### Ollama 相关问题

**问题**: 连接失败
```
解决方案:
1. 确认 Ollama 服务运行: `ollama list`
2. 检查端口: `curl http://localhost:11434/api/tags`
3. 确保模型已下载: `ollama pull llama3`
```

**问题**: 响应速度慢
```
解决方案:
1. 使用更小的模型 (如 llama3:8b 而非 llama3:70b)
2. 增加 GPU 内存分配
3. 调整 timeout 参数
```

### API 密钥问题

**问题**: API 密钥无效
```
解决方案:
1. 检查 .env 文件是否正确加载
2. 确认密钥格式正确（无多余空格）
3. 验证密钥权限和额度
```

### 网络连接问题

**问题**: 无法连接到 API
```
解决方案:
1. 检查网络连接
2. 验证代理设置（如需要）
3. 确认 API 端点 URL 正确
4. 检查防火墙设置
```

### 模型兼容性

**问题**: 模型响应格式不兼容
```
解决方案:
1. 确保使用正确的模型名称
2. 查看模型文档确认支持的功能
3. 调整 agent_config 中的参数
```

---

## 最佳实践

### 1. 成本优化

- **开发/测试**: 使用 Ollama 本地模型
- **生产环境**: 使用 OpenAI 或 Claude
- **高性价比**: 使用 DeepSeek

### 2. 性能优化

- 本地模型: 需要 GPU 支持
- 云端 API: 注意网络延迟
- 批量请求: 使用多模型并行

### 3. 安全建议

- ✅ 使用环境变量存储密钥
- ✅ 定期轮换 API 密钥
- ✅ 设置 API 使用限额
- ❌ 不要将密钥提交到代码仓库
- ❌ 不要在配置文件中硬编码密钥

### 4. 选择建议

| 场景 | 推荐提供商 | 原因 |
|------|-----------|------|
| 高质量决策 | OpenAI GPT-4, Claude 3.5 | 最佳推理能力 |
| 成本敏感 | DeepSeek, Ollama | 价格低廉或免费 |
| 离线部署 | Ollama | 无需外网连接 |
| 国内用户 | DeepSeek | 访问速度快 |
| 企业用户 | GitHub Copilot | 已有订阅 |

---

## 技术支持

如有问题，请：
1. 查看本文档的故障排除部分
2. 查看各提供商的官方文档
3. 提交 Issue 到 GitHub 仓库

---

## 更新日志

- **2025-10-29**: 添加多 AI 提供商支持
  - 新增 Ollama 本地模型支持
  - 新增 DeepSeek API 支持
  - 新增 Anthropic Claude 支持
  - 新增 GitHub Copilot 支持
  - 新增 Google Gemini 支持
