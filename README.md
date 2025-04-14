# China Stock MCP Server

## English

### Overview
China Stock MCP Server is a Multi-Call Protocol (MCP) server that provides comprehensive access to Chinese stock market data through a unified API. It leverages the AKShare library to fetch real-time and historical data from various Chinese stock exchanges including Shanghai (SSE), Shenzhen (SZSE), and Beijing (BSE).

### Features
- **Comprehensive Data Coverage**: Access to A-shares, B-shares, indices, ETFs, and more
- **Real-time Market Data**: Up-to-date quotes, bid-ask spreads, and market depth
- **Historical Data**: Daily, minute-level, and tick-level historical price data
- **Fundamental Data**: Company information, financial reports, and dividend history
- **Market Intelligence**: Sector analysis, concept boards, and institutional holdings
- **Technical Indicators**: Various technical analysis metrics and signals

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/china-stock-mcp.git
cd china-stock-mcp/china-stock-mcp-server

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### API Documentation
The server exposes numerous endpoints for accessing different types of stock market data. Each function is well-documented with parameter descriptions and return value formats. Some key functions include:

- `stock_zh_a_spot_em()`: Get real-time A-share market data
- `stock_zh_a_daily(symbol, start_date, end_date, adjust)`: Get historical daily data for a specific stock
- `stock_individual_info_em(symbol)`: Get detailed information for a specific stock
- `stock_financial_analysis_indicator(symbol)`: Get financial analysis indicators for a specific stock

### Dependencies
- AKShare: Chinese financial data interface package
- FastMCP: Multi-Call Protocol server framework

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 中文

### 概述
中国股票 MCP 服务器是一个多调用协议（MCP）服务器，通过统一的 API 提供对中国股票市场数据的全面访问。它利用 AKShare 库从上海证券交易所（SSE）、深圳证券交易所（SZSE）和北京证券交易所（BSE）等各种中国证券交易所获取实时和历史数据。

### 特点
- **全面的数据覆盖**：访问 A 股、B 股、指数、ETF 等
- **实时市场数据**：最新报价、买卖价差和市场深度
- **历史数据**：日线、分钟线和 tick 级别的历史价格数据
- **基本面数据**：公司信息、财务报告和股息历史
- **市场情报**：行业分析、概念板块和机构持股
- **技术指标**：各种技术分析指标和信号

### 安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/china-stock-mcp.git
cd china-stock-mcp/china-stock-mcp-server

# 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows 系统: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 使用方法
```bash
# 启动 MCP 服务器
python main.py
```

### API 文档
服务器暴露了许多用于访问不同类型股票市场数据的端点。每个函数都有详细的参数描述和返回值格式。一些关键功能包括：

- `stock_zh_a_spot_em()`：获取 A 股实时市场数据
- `stock_zh_a_daily(symbol, start_date, end_date, adjust)`：获取特定股票的历史日线数据
- `stock_individual_info_em(symbol)`：获取特定股票的详细信息
- `stock_financial_analysis_indicator(symbol)`：获取特定股票的财务分析指标

### 依赖
- AKShare：中文金融数据接口包
- FastMCP：多调用协议服务器框架

### 许可证
该项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件。

---

Last Updated: 2025-04-14