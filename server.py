from typing import Any, Dict, List, Optional, Union
import json
from mcp.server.fastmcp import FastMCP
import akshare as ak
from pandas import date_range

# Initialize FastMCP server
mcp = FastMCP("china-stock-mcp")

# Helper functions
def format_dataframe_to_json(df, max_rows=50):
    """Convert DataFrame to JSON string with max rows limit"""
    if df is None or df.empty:
        return json.dumps({"error": "No data available"})
    
    # Limit rows to prevent large responses
    if len(df) > max_rows:
        df = df.head(max_rows)
        truncated = True
    else:
        truncated = False
    
    # Convert to JSON
    result = {
        "data": json.loads(df.to_json(orient="records")),
        "columns": df.columns.tolist(),
        "truncated": truncated,
        "total_rows": len(df),
        "displayed_rows": min(max_rows, len(df))
    }
    
    return json.dumps(result)

# MCP Tools Implementation

# Shanghai Stock Exchange Summary
@mcp.tool()
def stock_sse_summary() -> str:
    """Get Shanghai Stock Exchange market overview data.
    
    Returns data in JSON format.
    
    Note: Data for the current trading day will only be available after the exchange closes.
    
    Returns:
    JSON formatted data including the following fields:
    - 项目: Item category
    - 股票: Stock data
    - 科创板: STAR Market (Science and Technology Innovation Board) data
    - 主板: Main Board data
    
    Each category contains detailed statistics about the market segment.
    
    
    中文: 上海证券交易所-股票数据总貌
    
    返回 JSON 格式的数据。
    
    注意：当前交易日的数据需要交易所收盘后才能获取。
    
    返回:
    JSON格式数据，包含以下字段：
    - 项目: 项目类别
    - 股票: 股票数据
    - 科创板: 科创板数据
    - 主板: 主板数据
    
    每个类别包含有关该市场组的详细统计数据。
    """
    try:
        df = ak.stock_sse_summary()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Shenzhen Stock Exchange Summary
@mcp.tool()
def stock_szse_summary(date: str) -> str:
    """Get Shenzhen Stock Exchange market overview data by security type.
    
    Returns data in JSON format.
    
    Parameters:
    date: str - Date in format YYYYMMDD (e.g., "20200619"). Note that data for the current trading day will only be available after the exchange closes.
    
    Returns:
    JSON formatted data including the following fields:
    - 证券类别: Security type
    - 数量: Quantity (unit: number of securities)
    - 成交金额: Transaction amount (unit: CNY)
    - 总市值: Total market value
    - 流通市值: Circulation market value
    
    
    中文: 深圳证券交易所-市场总貌-证券类别统计
    
    返回 JSON 格式的数据。
    
    参数:
    date: str - 日期，格式为 YYYYMMDD（例如："20200619"）。注意：当前交易日的数据需要交易所收盘后才能获取。
    
    返回:
    JSON格式数据，包含以下字段：
    - 证券类别: 证券类别
    - 数量: 数量（单位：只）
    - 成交金额: 成交金额（单位：元）
    - 总市值: 总市值
    - 流通市值: 流通市值
    """
    try:
        df = ak.stock_szse_summary(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-share Real-time Quotes
@mcp.tool()
def stock_zh_a_spot_em() -> str:
    """Get real-time quotes for all A-shares from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    This function does not require any parameters.
    
    Returns:
    JSON formatted data including the following fields for each stock:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount
    - 成交量: Trading volume (unit: lot)
    - 成交额: Trading amount (unit: CNY)
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Opening price
    - 昨收: Previous closing price
    - 量比: Volume ratio
    - 换手率: Turnover rate (%)
    - 市盈率-动态: PE ratio (dynamic)
    - 市净率: PB ratio
    - 总市值: Total market value (unit: CNY)
    - 流通市值: Circulation market value (unit: CNY)
    - 涨速: Rise speed
    - 5分钟涨跌: 5-minute change (%)
    - 60日涨跌幅: 60-day change (%)
    - 年初至今涨跌幅: Year-to-date change (%)
    
    Note: This function returns real-time data for all Shanghai, Shenzhen, and Beijing A-share listed companies.
    
    
    中文: 东方财富网-沪深京 A 股-实时行情数据
    
    返回 JSON 格式的数据。
    
    参数:
    该函数不需要任何参数。
    
    返回:
    JSON格式数据，包含每只股票的以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅 (%)
    - 涨跌额: 涨跌额
    - 成交量: 成交量 (单位: 手)
    - 成交额: 成交额 (单位: 元)
    - 振幅: 振幅 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 开盘价
    - 昨收: 昨日收盘价
    - 量比: 量比
    - 换手率: 换手率 (%)
    - 市盈率-动态: 市盈率(动态)
    - 市净率: 市净率
    - 总市值: 总市值 (单位: 元)
    - 流通市值: 流通市值 (单位: 元)
    - 涨速: 涨速
    - 5分钟涨跌: 5分钟涨跌 (%)
    - 60日涨跌幅: 60日涨跌幅 (%)
    - 年初至今涨跌幅: 年初至今涨跌幅 (%)
    
    注意：该函数返回所有沪深京 A 股上市公司的实时行情数据。
    """
    try:
        df = ak.stock_zh_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# MCP Tools Implementation

# Shanghai Stock Exchange Summary

# Shenzhen Stock Exchange Summary

# Shenzhen Stock Exchange Area Summary
@mcp.tool()
def stock_szse_area_summary(date: str) -> str:
    """Get Shenzhen Stock Exchange regional trading ranking data.
    
    Returns data in JSON format.
    
    Parameters:
    date: str - Date in format YYYYMM (e.g., "202203")
    
    Returns:
    JSON formatted data including the following fields:
    - 序号: Rank
    - 地区: Region
    - 总交易额: Total transaction amount (unit: CNY)
    - 占市场: Market share percentage (%)
    - 股票交易额: Stock transaction amount (unit: CNY)
    - 基金交易额: Fund transaction amount (unit: CNY)
    - 债券交易额: Bond transaction amount (unit: CNY)
    
    
    中文: 深圳证券交易所-市场总貌-地区交易排序
    
    返回 JSON 格式的数据。
    
    参数:
    date: str - 日期，格式为 YYYYMM（例如："202203"）
    
    返回:
    JSON格式数据，包含以下字段：
    - 序号: 排名
    - 地区: 地区
    - 总交易额: 总交易额 (单位: 元)
    - 占市场: 占市场比例 (%)
    - 股票交易额: 股票交易额 (单位: 元)
    - 基金交易额: 基金交易额 (单位: 元)
    - 债券交易额: 债券交易额 (单位: 元)
    """
    try:
        df = ak.stock_szse_area_summary(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-Share Individual Stock Data
@mcp.tool()
def stock_zh_a_daily(symbol: str, start_date: str, end_date: str, adjust: str = "") -> str:
    """Get A-share individual stock historical daily data from Sina Finance.
    
    Returns data in JSON format.
    
    Note: It is recommended to use stock_zh_a_hist instead as it provides higher quality data and has no access restrictions.
    For CDR stocks (e.g., sh689009), please use the stock_zh_a_cdr_daily interface.
    
    Parameters:
    symbol: str - Stock code with market prefix, e.g., "sh600000". Stock codes can be obtained from stock_zh_a_spot_em().
    start_date: str - Start date in format YYYYMMDD, e.g., "20201103".
    end_date: str - End date in format YYYYMMDD, e.g., "20201116".
    adjust: str - Price adjustment method. Options: 
           '' (no adjustment, default), 
           'qfq' (forward adjustment), 
           'hfq' (backward adjustment), 
           'qfq-factor' (forward adjustment factor), 
           'hfq-factor' (backward adjustment factor).
    
    Returns:
    JSON formatted data including the following fields:
    - date: Trading date
    - open: Opening price
    - high: Highest price
    - low: Lowest price
    - close: Closing price
    - volume: Trading volume (unit: shares)
    - amount: Trading amount (unit: CNY)
    - outstanding_share: Outstanding shares (unit: shares)
    - turnover: Turnover rate (volume/outstanding shares)
    
    Warning: Multiple requests may result in IP blocking.
    
    
    中文: 新浪财经-沪深京 A 股的数据, 历史数据按日频率更新
    
    返回 JSON 格式的数据。
    
    注意：建议使用 stock_zh_a_hist 接口，因为该接口数据质量更高，访问无限制。
    对于 CDR 股票（例如 sh689009），请使用 stock_zh_a_cdr_daily 接口。
    
    参数:
    symbol: str - 股票代码，需要带市场标识，例如 "sh600000"。股票代码可以从 stock_zh_a_spot_em() 中获取。
    start_date: str - 开始查询的日期，格式为 YYYYMMDD，例如 "20201103"。
    end_date: str - 结束查询的日期，格式为 YYYYMMDD，例如 "20201116"。
    adjust: str - 复权调整方式。可选值：
           '' (不复权，默认值), 
           'qfq' (前复权), 
           'hfq' (后复权), 
           'qfq-factor' (前复权因子), 
           'hfq-factor' (后复权因子)。
    
    返回:
    JSON格式数据，包含以下字段：
    - date: 交易日
    - open: 开盘价
    - high: 最高价
    - low: 最低价
    - close: 收盘价
    - volume: 成交量 (单位: 股)
    - amount: 成交额 (单位: 元)
    - outstanding_share: 流动股本 (单位: 股)
    - turnover: 换手率 (成交量/流动股本)
    
    警告：多次获取容易封禁 IP。
    """
    try:
        df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, end_date=end_date, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-Share Index Data

# A-Share Real-time Quotes

# A-Share Individual Stock Real-time Quote
@mcp.tool()
def stock_zh_a_spot(symbol: str) -> str:
    """Get real-time quote for a specific A-share stock.
    
    Args:
    symbol: Stock symbol (e.g., sh000001 for SSE, sz399001 for SZSE)
    
    Returns real-time data for the specified stock.
    
    
    中文: 新浪财经-沪深京 A 股数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
    
    Args:
    symbol: Stock symbol (e.g., sh000001 for SSE, sz399001 for SZSE)
    
    Returns real-time data for the specified stock.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_a_spot(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-Share Top Gainers

# A-Share Top Losers

# Beijing Stock Exchange Real-time Quotes
@mcp.tool()
def stock_bj_a_spot_em() -> str:
    """Get Beijing Stock Exchange real-time quotes for all stocks.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each stock:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount
    - 成交量: Trading volume (unit: lot)
    - 成交额: Trading amount (unit: yuan)
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Opening price
    - 昨收: Previous closing price
    - 量比: Volume ratio
    - 换手率: Turnover rate (%)
    - 市盈率-动态: P/E ratio (dynamic)
    - 市净率: P/B ratio
    - 总市值: Total market value (unit: yuan)
    - 流通市值: Circulating market value (unit: yuan)
    - 涨速: Rise speed
    - 5分钟涨跌: 5-minute change (%)
    - 60日涨跌幅: 60-day change (%)
    - 年初至今涨跌幅: Year-to-date change (%)
    
    
    中文: 东方财富网-京 A 股-实时行情数据
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每只股票的以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格
    - 涨跌幅: 涨跌幅 (%)
    - 涨跌额: 涨跌额
    - 成交量: 成交量 (单位: 手)
    - 成交额: 成交额 (单位: 元)
    - 振幅: 振幅 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 开盘价
    - 昨收: 昨日收盘价
    - 量比: 量比
    - 换手率: 换手率 (%)
    - 市盈率-动态: 市盈率(动态)
    - 市净率: 市净率
    - 总市值: 总市值 (单位: 元)
    - 流通市值: 流通市值 (单位: 元)
    - 涨速: 涨速
    - 5分钟涨跌: 5分钟涨跌 (%)
    - 60日涨跌幅: 60日涨跌幅 (%)
    - 年初至今涨跌幅: 年初至今涨跌幅 (%)
    """
    try:
        df = ak.stock_bj_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Individual Stock Information
@mcp.tool()
def stock_individual_info_em(symbol: str) -> str:
    """Get detailed information for a specific stock from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock symbol (e.g., '000001' for Ping An Bank)
    
    Returns:
    JSON formatted data including detailed information about the stock with the following fields:
    - item: Information item name
    - value: Information item value
    
    The information items typically include:
    - Stock name
    - Industry
    - Main business
    - Company profile
    - And other fundamental information
    
    
    中文: 东方财富-个股-股票信息
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码（例如：'000001'代表平安银行）
    
    返回:
    JSON格式数据，包含关于股票的详细信息，具有以下字段：
    - item: 信息项名称
    - value: 信息项值
    
    信息项通常包括：
    - 股票名称
    - 行业
    - 主营业务
    - 公司简介
    - 以及其他基本信息
    """
    try:
        df = ak.stock_individual_info_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Bid-Ask Data
@mcp.tool()
def stock_bid_ask_em(symbol: str) -> str:
    """Get real-time bid-ask data for a specific stock from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock symbol (e.g., '000001' for Ping An Bank)
    
    Returns:
    JSON formatted data including bid-ask information with the following fields:
    - item: Information item name
    - value: Information item value
    
    The information typically includes:
    - Bid prices and volumes (multiple levels)
    - Ask prices and volumes (multiple levels)
    - Spread information
    - Latest transaction data
    
    
    中文: 东方财富-行情报价
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码（例如：'000001'代表平安银行）
    
    返回:
    JSON格式数据，包含买卖盘信息，具有以下字段：
    - item: 信息项名称
    - value: 信息项值
    
    信息通常包括：
    - 买入价格和数量（多个档位）
    - 卖出价格和数量（多个档位）
    - 价差信息
    - 最新交易数据
    """
    try:
        df = ak.stock_bid_ask_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Sector Summary
@mcp.tool()
def stock_szse_sector_summary(symbol: str, date: str) -> str:
    """Get Shenzhen Stock Exchange sector transaction data.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Period type, must be one of {"当月", "当年"} ("current month" or "current year")
    date: str - Date in format YYYYMM (e.g., "202501")
    
    Returns:
    JSON formatted data including sector transaction statistics with the following fields:
    - 项目名称: Project name
    - 项目名称-英文: Project name in English
    - 交易天数: Trading days
    - 成交金额-人民币元: Transaction amount in RMB
    - 成交金额-占总计: Transaction amount percentage of total (%)
    - 成交股数-股数: Number of shares traded
    - 成交股数-占总计: Share volume percentage of total (%)
    - 成交笔数-笔: Number of transactions
    - 成交笔数-占总计: Transaction count percentage of total (%)
    
    
    中文: 深圳证券交易所-统计资料-股票行业成交数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 时间周期类型，必须是 {"当月", "当年"} 之一
    date: str - 日期，格式为 YYYYMM（例如："202501"）
    
    返回:
    JSON格式数据，包含行业成交统计信息，具有以下字段：
    - 项目名称: 项目名称
    - 项目名称-英文: 项目英文名称
    - 交易天数: 交易天数
    - 成交金额-人民币元: 人民币成交金额
    - 成交金额-占总计: 成交金额占总计百分比 (%)
    - 成交股数-股数: 成交股数
    - 成交股数-占总计: 成交股数占总计百分比 (%)
    - 成交笔数-笔: 成交笔数
    - 成交笔数-占总计: 成交笔数占总计百分比 (%)
    """
    try:
        df = ak.stock_szse_sector_summary(symbol=symbol, date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Shanghai Stock Exchange Daily Trading Data
@mcp.tool()
def stock_sse_deal_daily(date: str = None) -> str:
    """Get Shanghai Stock Exchange daily trading data.
    
    Returns data in JSON format.
    
    Parameters:
    date: str - Date in format YYYYMMDD (e.g., "20250221"), default is None for the latest data.
           Note: Only data after 20211227 (inclusive) is supported.
    
    Returns:
    JSON formatted data including daily trading statistics with the following fields:
    - 单日情况: Daily situation (contains all fields from the webpage)
    - 股票: Stocks
    - 主板A: Main Board A
    - 主板B: Main Board B
    - 科创板: STAR Market
    - 股票回购: Stock repurchase
    
    
    中文: 上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况
    
    返回 JSON 格式的数据。
    
    参数:
    date: str - 日期，格式为 YYYYMMDD（例如："20250221"），默认为 None 表示最新数据。
           注意：仅支持获取 20211227（包含）之后的数据。
    
    返回:
    JSON格式数据，包含每日交易统计信息，具有以下字段：
    - 单日情况: 单日情况（包含网页所有字段）
    - 股票: 股票
    - 主板A: 主板 A 股
    - 主板B: 主板 B 股
    - 科创板: 科创板
    - 股票回购: 股票回购
    """
    try:
        df = ak.stock_sse_deal_daily(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Minute-level Data
@mcp.tool()
def stock_zh_a_minute(symbol: str, period: str, adjust: str = "") -> str:
    """Get minute-level data for a specific A-share stock.
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock symbol with market identifier (e.g., 'sh600751' for Shanghai, 'sz000001' for Shenzhen)
    period: str - Time period, can be one of '1', '5', '15', '30', '60' minutes
    adjust: str - Price adjustment method: '' for no adjustment, 'qfq' for forward adjustment, 'hfq' for backward adjustment, default is ''
    
    Returns:
    JSON formatted data with fields including day (time), open, high, low, close, and volume
    
    参数:
    symbol: str - 股票代码，需要带市场标识，例如 'sh600751' 表示上海市场，'sz000001' 表示深圳市场
    period: str - 时间周期，可选值为 '1', '5', '15', '30', '60' 分钟
    adjust: str - 复权调整，可选值为 {'', 'qfq', 'hfq'}，'': 不复权, 'qfq': 前复权, 'hfq': 后复权，默认为 ''
    
    返回:
    JSON格式数据，包含日期时间、开盘价、最高价、最低价、收盘价、成交量等字段
    """
    try:
        df = ak.stock_zh_a_minute(symbol=symbol, period=period, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Minute-level Data (Eastmoney)
@mcp.tool()
def stock_zh_a_hist_min_em(symbol: str, start_date: str, end_date: str, period: str = "1", adjust: str = "") -> str:
    """Get minute-level historical data for a specific A-share stock from Eastmoney.
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情首页-沪深京 A 股-每日分时行情; 该接口只能获取近期的分时数据，注意时间周期的设置
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票代码，例如 "000001"
    start_date: str - 开始日期时间，格式为 YYYY-MM-DD HH:MM:SS，例如 "2024-03-01 09:30:00"
    end_date: str - 结束日期时间，格式为 YYYY-MM-DD HH:MM:SS，例如 "2024-03-05 15:00:00"
    period: str - 时间周期，可选值为 {'1', '5', '15', '30', '60'}，默认为 "1"
    adjust: str - 复权调整，可选值为 {'', 'qfq', 'hfq'}，'': 不复权, 'qfq': 前复权, 'hfq': 后复权，默认为 ""
    
    Returns:
    JSON formatted data with fields including time, open, close, high, low, volume, amount, and average price
    
    参数:
    symbol: str - 股票代码，例如 "000001"
    start_date: str - 开始日期时间，格式为 YYYY-MM-DD HH:MM:SS，例如 "2024-03-01 09:30:00"
    end_date: str - 结束日期时间，格式为 YYYY-MM-DD HH:MM:SS，例如 "2024-03-05 15:00:00"
    period: str - 时间周期，可选值为 {'1', '5', '15', '30', '60'}，默认为 "1"
    adjust: str - 复权调整，可选值为 {'', 'qfq', 'hfq'}，'': 不复权, 'qfq': 前复权, 'hfq': 后复权，默认为 ""
    
    返回:
    JSON格式数据，包含时间、开盘、收盘、最高、最低、成交量、成交额、均价等字段
    """
    try:
        df = ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Intraday Data
@mcp.tool()
def stock_intraday_em(symbol: str) -> str:
    """Get intraday data for a specific A-share stock from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock symbol (e.g., "000001")
    
    Returns:
    JSON formatted data including the following fields:
    - Time
    - Transaction price
    - Volume (in lots)
    - Buy/sell nature
    
    Note: Returns intraday data for the most recent trading day, including pre-market data.
    
    
    中文: 东财财富-分时数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码（例如："000001"）
    
    返回:
    JSON格式数据，包含以下字段：
    - 时间
    - 成交价
    - 手数
    - 买卖盘性质
    
    注意：返回最近一个交易日的分时数据，包含盘前数据。
    """
    try:
        df = ak.stock_intraday_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock New Listings
@mcp.tool()
def stock_zh_a_new() -> str:
    """Get information about newly listed A-share stocks from Sina Finance.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each newly listed stock:
    - symbol: Sina stock code
    - code: Stock code
    - name: Stock name
    - open: Opening price
    - high: Highest price
    - low: Lowest price
    - volume: Trading volume
    - amount: Trading amount
    - mktcap: Market capitalization
    - turnoverratio: Turnover ratio
    
    Note: Due to the changing nature of newly listed stocks, this only returns data for the most recent trading day.
    
    
    中文: 新浪财经-行情中心-沪深股市-次新股
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每只次新股的以下字段：
    - symbol: 新浪代码
    - code: 股票代码
    - name: 股票简称
    - open: 开盘价
    - high: 最高价
    - low: 最低价
    - volume: 成交量
    - amount: 成交额
    - mktcap: 市值
    - turnoverratio: 换手率
    
    注意：由于次新股名单随着交易日变化而变化，只能获取最近交易日的数据。
    """
    try:
        df = ak.stock_zh_a_new()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock ST Status
@mcp.tool()
def stock_zh_a_st_em() -> str:
    """Get information about A-share stocks with ST status (risk warning board) from Eastmoney.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each ST stock:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount
    - 成交量: Trading volume
    - 成交额: Trading amount
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Opening price
    - 昨收: Previous closing price
    - 量比: Volume ratio
    - 换手率: Turnover rate (%)
    - 市盈率-动态: P/E ratio (dynamic)
    - 市净率: P/B ratio
    
    Note: Returns data for all stocks on the risk warning board for the current trading day.
    
    
    中文: 东方财富网-行情中心-沪深个股-风险警示板
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每只风险警示板股票的以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格
    - 涨跌幅: 涨跌幅 (%)
    - 涨跌额: 涨跌额
    - 成交量: 成交量
    - 成交额: 成交额
    - 振幅: 振幅 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 开盘价
    - 昨收: 昨日收盘价
    - 量比: 量比
    - 换手率: 换手率 (%)
    - 市盈率-动态: 市盈率(动态)
    - 市净率: 市净率
    
    注意：返回当前交易日风险警示板的所有股票的行情数据。
    """
    try:
        df = ak.stock_zh_a_st_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Suspended
@mcp.tool()
def stock_zh_a_stop_em() -> str:
    """Get information about suspended A-share stocks.
    
    Returns data about suspended stocks including:
    - Stock code
    - Stock name
    - Suspension date
    - Suspension reason
    - Expected resumption date
    
    
    中文: 东方财富网-行情中心-沪深个股-两网及退市
    
    Returns data about suspended stocks including:
    - Stock code
    - Stock name
    - Suspension date
    - Suspension reason
    - Expected resumption date
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_a_stop_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-H Share Comparison
@mcp.tool()
def stock_zh_ah_spot_em() -> str:
    """Get real-time comparison data for stocks listed on both A-share and H-share markets from Eastmoney.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each A+H listed company:
    - 序号: Serial number
    - 名称: Stock name
    - H股代码: H-share stock code
    - 最新价-HKD: Latest H-share price (in HKD)
    - H股-涨跌幅: H-share change percentage (%)
    - A股代码: A-share stock code
    - 最新价-RMB: Latest A-share price (in RMB)
    - A股-涨跌幅: A-share change percentage (%)
    - 比价: Price ratio
    - 溢价: Premium percentage (%)
    
    Note: Data is delayed by 15 minutes.
    
    
    中文: 东方财富网-行情中心-沪深港通-AH股比价-实时行情, 延迟 15 分钟更新
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每个 A+H 上市公司的以下字段：
    - 序号: 序号
    - 名称: 股票名称
    - H股代码: H股股票代码
    - 最新价-HKD: H股最新价格（单位：HKD）
    - H股-涨跌幅: H股涨跌幅 (%)
    - A股代码: A股股票代码
    - 最新价-RMB: A股最新价格（单位：RMB）
    - A股-涨跌幅: A股涨跌幅 (%)
    - 比价: 价格比率
    - 溢价: 溢价百分比 (%)
    
    注意：数据延迟 15 分钟更新。
    """
    try:
        df = ak.stock_zh_ah_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# US Stock Quotes
@mcp.tool()
def stock_us_spot_em() -> str:
    """Get real-time quotes for US stocks.
    
    Returns real-time market data for US stocks including:
    - Stock code
    - Stock name
    - Latest price
    - Change amount
    - Change percentage
    - And other market metrics
    
    
    中文: 东方财富网-美股-实时行情
    
    Returns real-time market data for US stocks including:
    - Stock code
    - Stock name
    - Latest price
    - Change amount
    - Change percentage
    - And other market metrics
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_us_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# US Stock Historical Data
@mcp.tool()
def stock_us_hist(symbol: str, period: str = "daily", start_date: str = "", end_date: str = "", adjust: str = "") -> str:
    """Get historical data for a specific US stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - US stock symbol (e.g., "106.TTE"). You can get all available codes from the stock_us_spot_em function
    period: str - Data frequency, options: "daily", "weekly", "monthly", default is "daily"
    start_date: str - Start date in format YYYYMMDD (e.g., "20200101")
    end_date: str - End date in format YYYYMMDD (e.g., "20240214")
    adjust: str - Price adjustment method: "" for no adjustment, "qfq" for forward adjustment, "hfq" for backward adjustment, default is ""
    
    Returns:
    JSON formatted data including the following fields:
    - Date
    - Open (in USD)
    - Close (in USD)
    - High (in USD)
    - Low (in USD)
    - Volume (in shares)
    - Amount (in USD)
    - Amplitude (%)
    - Change percentage (%)
    - Change amount (in USD)
    - Turnover rate (%)
    
    Note: Returns all historical data for the specified company with the specified adjustment.
    
    
    中文: 东方财富网-行情-美股-每日行情
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 美股代码，例如 "106.TTE"。可以通过 stock_us_spot_em 函数获取所有可用代码
    period: str - 数据频率，可选值："daily"（日线）, "weekly"（周线）, "monthly"（月线），默认为 "daily"
    start_date: str - 开始日期，格式为 YYYYMMDD，例如 "20200101"
    end_date: str - 结束日期，格式为 YYYYMMDD，例如 "20240214"
    adjust: str - 复权调整，可选值为 {'', 'qfq', 'hfq'}，'': 不复权, 'qfq': 前复权, 'hfq': 后复权，默认为 ""
    
    返回:
    JSON格式数据，包含以下字段：
    - 日期
    - 开盘（美元）
    - 收盘（美元）
    - 最高（美元）
    - 最低（美元）
    - 成交量（股）
    - 成交额（美元）
    - 振幅（%）
    - 涨跌幅（%）
    - 涨跌额（美元）
    - 换手率（%）
    
    注意：返回指定公司的指定复权后的所有历史行情数据。
    """
    try:
        df = ak.stock_us_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Index List

# Stock Index Components

# Stock Industry Classification
@mcp.tool()
def stock_sector_spot(indicator: str = "新浪行业") -> str:
    """Get real-time data for stock industry sectors.
    
    Returns data in JSON format.
    
    Parameters:
    indicator: str - Indicator type, options: "新浪行业" (Sina Industry), "启明星行业" (Morningstar Industry), "概念" (Concept), "地域" (Region), "行业" (Industry), default is "新浪行业"
    
    Returns:
    JSON formatted data including the following fields:
    - label: Sector label/code
    - 板块: Sector name
    - 公司家数: Number of companies
    - 平均价格: Average price
    - 涨跌额: Change amount
    - 涨跌幅: Change percentage (%)
    - 总成交量: Total volume (in lots)
    - 总成交额: Total amount (in 10,000 CNY)
    - 股票代码: Leading stock code
    - 个股-涨跌幅: Leading stock change percentage (%)
    - 个股-当前价: Leading stock current price
    - 个股-涨跌额: Leading stock change amount
    - 股票名称: Leading stock name
    
    
    中文: 新浪行业-板块行情
    
    返回 JSON 格式的数据。
    
    参数:
    indicator: str - 指标类型，可选值："新浪行业"、"启明星行业"、"概念"、"地域"、"行业"，默认为 "新浪行业"
    
    返回:
    JSON格式数据，包含以下字段：
    - label: 板块标签/代码
    - 板块: 板块名称
    - 公司家数: 包含的公司数量
    - 平均价格: 平均价格
    - 涨跌额: 涨跌金额
    - 涨跌幅: 涨跌百分比 (%)
    - 总成交量: 总成交量（手）
    - 总成交额: 总成交额（万元）
    - 股票代码: 领涨股代码
    - 个股-涨跌幅: 领涨股涨跌百分比 (%)
    - 个股-当前价: 领涨股当前价格
    - 个股-涨跌额: 领涨股涨跌金额
    - 股票名称: 领涨股名称
    """
    try:
        df = ak.stock_sector_spot(indicator=indicator)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Sector Detail
@mcp.tool()
def stock_sector_detail(sector: str) -> str:
    """Get detailed data for stocks in a specific industry sector.
    
    Returns data in JSON format.
    
    Parameters:
    sector: str - Sector code (e.g., "hangye_ZL01"). You can get the sector code from the 'label' field in the stock_sector_spot function's return data
    
    Returns:
    JSON formatted data including the following fields:
    - symbol: Symbol
    - code: Stock code
    - name: Stock name
    - trade: Current price
    - pricechange: Price change amount
    - changepercent: Change percentage
    - buy: Buy price
    - sell: Sell price
    - settlement: Previous close price
    - open: Open price
    - high: High price
    - low: Low price
    - volume: Volume
    - amount: Transaction amount
    - ticktime: Time
    - per: Price-to-earnings ratio
    - pb: Price-to-book ratio
    - mktcap: Market capitalization
    - nmc: Circulation market value
    - turnoverratio: Turnover ratio
    
    Note: Due to errors in the statistics provided by the Sina webpage, the number of stocks in some sectors may be greater than the statistics.
    
    
    中文: 新浪行业-板块行情-成份详情, 由于新浪网页提供的统计数据有误, 部分行业数量大于统计数
    
    返回 JSON 格式的数据。
    
    参数:
    sector: str - 板块代码（例如："hangye_ZL01"）。可以通过 stock_sector_spot 函数返回数据中的 'label' 字段获取板块代码
    
    返回:
    JSON格式数据，包含以下字段：
    - symbol: 符号
    - code: 股票代码
    - name: 股票名称
    - trade: 当前价格
    - pricechange: 价格变化金额
    - changepercent: 变化百分比
    - buy: 买入价
    - sell: 卖出价
    - settlement: 前收盘价
    - open: 开盘价
    - high: 最高价
    - low: 最低价
    - volume: 成交量
    - amount: 成交金额
    - ticktime: 时间
    - per: 市盈率
    - pb: 市净率
    - mktcap: 总市值
    - nmc: 流通市值
    - turnoverratio: 换手率
    """
    try:
        df = ak.stock_sector_detail(sector=sector)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Fund Flow
@mcp.tool()
def stock_individual_fund_flow(stock: str, market: str = "sh") -> str:
    """Get fund flow data for a specific stock.
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-个股资金流向
    
    Returns data in JSON format.
    
    Parameters:
    stock: str - Stock code without market prefix (e.g., '600094')
    market: str - Market identifier: 'sh' for Shanghai, 'sz' for Shenzhen, 'bj' for Beijing, default is 'sh'
    
    Returns:
    JSON formatted data with fields including date, closing price, price change percentage, main capital net inflow (amount and percentage), 
    ultra-large order net inflow, large order net inflow, medium order net inflow, and small order net inflow
    
    参数:
    stock: str - 股票代码，不带市场前缀（例如：'600094'）
    market: str - 市场标识：'sh' 表示上海证券交易所，'sz' 表示深圳证券交易所，'bj' 表示北京证券交易所，默认为 'sh'
    
    返回:
    JSON格式数据，包含日期、收盘价、涨跌幅、主力净流入（净额和净占比）、超大单净流入、大单净流入、中单净流入、小单净流入等字段
    """
    try:
        df = ak.stock_individual_fund_flow(stock=stock, market=market)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market Fund Flow
@mcp.tool()
def stock_market_fund_flow() -> str:
    """Get overall market fund flow data.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields:
    - 日期 (Date)
    - 上证-收盘价 (SSE-Closing Price)
    - 上证-涨跌幅 (SSE-Change Percentage) (%)
    - 深证-收盘价 (SZSE-Closing Price)
    - 深证-涨跌幅 (SZSE-Change Percentage) (%)
    - 主力净流入-净额 (Main Capital Net Inflow-Amount)
    - 主力净流入-净占比 (Main Capital Net Inflow-Percentage) (%)
    - 超大单净流入-净额 (Ultra-large Order Net Inflow-Amount)
    - 超大单净流入-净占比 (Ultra-large Order Net Inflow-Percentage) (%)
    - 大单净流入-净额 (Large Order Net Inflow-Amount)
    - 大单净流入-净占比 (Large Order Net Inflow-Percentage) (%)
    - 中单净流入-净额 (Medium Order Net Inflow-Amount)
    - 中单净流入-净占比 (Medium Order Net Inflow-Percentage) (%)
    - 小单净流入-净额 (Small Order Net Inflow-Amount)
    - 小单净流入-净占比 (Small Order Net Inflow-Percentage) (%)
    
    
    中文: 东方财富网-数据中心-资金流向-大盘
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含以下字段：
    - 日期
    - 上证-收盘价
    - 上证-涨跌幅 (%)
    - 深证-收盘价
    - 深证-涨跌幅 (%)
    - 主力净流入-净额
    - 主力净流入-净占比 (%)
    - 超大单净流入-净额
    - 超大单净流入-净占比 (%)
    - 大单净流入-净额
    - 大单净流入-净占比 (%)
    - 中单净流入-净额
    - 中单净流入-净占比 (%)
    - 小单净流入-净额
    - 小单净流入-净占比 (%)
    """
    try:
        df = ak.stock_market_fund_flow()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Sector Fund Flow
@mcp.tool()
def stock_sector_fund_flow_rank(indicator: str = "今日", sector_type: str = "行业资金流") -> str:
    """Get fund flow ranking data for industry sectors.
    
    Returns data in JSON format.
    
    Parameters:
    indicator: str - Time period, options: "今日" (Today), "5日" (5 days), "10日" (10 days), default is "今日"
    sector_type: str - Sector type, options: "行业资金流" (Industry Fund Flow), "概念资金流" (Concept Fund Flow), "地域资金流" (Regional Fund Flow), default is "行业资金流"
    
    Returns:
    JSON formatted data including the following fields:
    - 序号: Rank
    - 名称: Sector name
    - 今日涨跌幅: Today's change percentage (%)
    - 主力净流入-净额: Main capital net inflow amount
    - 主力净流入-净占比: Main capital net inflow percentage (%)
    - 超大单净流入-净额: Ultra-large order net inflow amount
    - 超大单净流入-净占比: Ultra-large order net inflow percentage (%)
    - 大单净流入-净额: Large order net inflow amount
    - 大单净流入-净占比: Large order net inflow percentage (%)
    - 中单净流入-净额: Medium order net inflow amount
    - 中单净流入-净占比: Medium order net inflow percentage (%)
    - 小单净流入-净额: Small order net inflow amount
    - 小单净流入-净占比: Small order net inflow percentage (%)
    - 主力净流入最大股: Stock with largest main capital net inflow
    
    
    中文: 东方财富网-数据中心-资金流向-板块资金流-排名
    
    返回 JSON 格式的数据。
    
    参数:
    indicator: str - 时间周期，可选值："今日"、"5日"、"10日"，默认为 "今日"
    sector_type: str - 板块类型，可选值："行业资金流"、"概念资金流"、"地域资金流"，默认为 "行业资金流"
    
    返回:
    JSON格式数据，包含以下字段：
    - 序号: 排名
    - 名称: 板块名称
    - 今日涨跌幅: 今日涨跌百分比 (%)
    - 主力净流入-净额: 主力资金净流入金额
    - 主力净流入-净占比: 主力资金净流入百分比 (%)
    - 超大单净流入-净额: 超大单净流入金额
    - 超大单净流入-净占比: 超大单净流入百分比 (%)
    - 大单净流入-净额: 大单净流入金额
    - 大单净流入-净占比: 大单净流入百分比 (%)
    - 中单净流入-净额: 中单净流入金额
    - 中单净流入-净占比: 中单净流入百分比 (%)
    - 小单净流入-净额: 小单净流入金额
    - 小单净流入-净占比: 小单净流入百分比 (%)
    - 主力净流入最大股: 主力资金净流入最大的股票
    """
    try:
        df = ak.stock_sector_fund_flow_rank(indicator=indicator, sector_type=sector_type)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Concept Data
@mcp.tool()
def stock_board_concept_name_em() -> str:
    """Get a list of all stock concept boards from Eastmoney.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields:
    - 排名: Rank
    - 板块名称: Concept board name
    - 板块代码: Concept board code
    - 最新价: Latest price
    - 涨跌额: Price change amount
    - 涨跌幅: Price change percentage (%)
    - 总市值: Total market value
    - 换手率: Turnover rate (%)
    - 上涨家数: Number of stocks rising
    - 下跌家数: Number of stocks falling
    - 领涨股票: Leading stock
    - 领涨股票-涨跌幅: Leading stock price change percentage (%)
    
    Note: This data is useful for identifying concept boards and their codes, which can be used as inputs for other functions like stock_board_concept_cons_em.
    
    
    中文: 东方财富网-行情中心-沪深京板块-概念板块
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含以下字段：
    - 排名: 排名
    - 板块名称: 概念板块名称
    - 板块代码: 概念板块代码
    - 最新价: 最新价格
    - 涨跌额: 价格变化金额
    - 涨跌幅: 价格变化百分比 (%)
    - 总市值: 总市值
    - 换手率: 换手率 (%)
    - 上涨家数: 上涨股票数量
    - 下跌家数: 下跌股票数量
    - 领涨股票: 领涨股票
    - 领涨股票-涨跌幅: 领涨股票价格变化百分比 (%)
    
    注意：该数据对于识别概念板块及其代码非常有用，这些代码可以用作其他函数（如 stock_board_concept_cons_em）的输入。
    """
    try:
        df = ak.stock_board_concept_name_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Concept Detail
@mcp.tool()
def stock_board_concept_cons_em(symbol: str) -> str:
    """Get stocks in a specific concept board from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Concept board name (e.g., "融资融券") or code (e.g., "BK0655"). 
            You can use stock_board_concept_name_em() to get a list of all concept board names and codes.
    
    Returns:
    JSON formatted data including the following fields for each stock in the concept board:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount
    - 成交量: Trading volume (unit: lot)
    - 成交额: Trading amount
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Opening price
    - 昨收: Previous closing price
    - 换手率: Turnover rate (%)
    - 市盈率-动态: P/E ratio (dynamic)
    - 市净率: P/B ratio
    
    
    中文: 东方财富-沪深板块-概念板块-板块成份
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 概念板块名称（例如："融资融券"）或代码（例如："BK0655"）。
            可以使用 stock_board_concept_name_em() 获取所有概念板块名称和代码的列表。
    
    返回:
    JSON格式数据，包含概念板块中每只股票的以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格
    - 涨跌幅: 涨跌幅 (%)
    - 涨跌额: 涨跌额
    - 成交量: 成交量 (单位: 手)
    - 成交额: 成交额
    - 振幅: 振幅 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 开盘价
    - 昨收: 昨日收盘价
    - 换手率: 换手率 (%)
    - 市盈率-动态: 市盈率(动态)
    - 市净率: 市净率
    """
    try:
        df = ak.stock_board_concept_cons_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Industry Data
@mcp.tool()
def stock_board_industry_name_em() -> str:
    """Get a list of all stock industry boards from Eastmoney.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each industry board:
    - 排名: Ranking
    - 板块名称: Board name
    - 板块代码: Board code
    - 最新价: Latest price
    - 涨跌额: Change amount
    - 涨跌幅: Change percentage (%)
    - 总市值: Total market value
    - 换手率: Turnover rate (%)
    - 上涨家数: Number of rising stocks
    - 下跌家数: Number of falling stocks
    - 领涨股票: Leading stock
    - 领涨股票-涨跌幅: Leading stock change percentage (%)
    
    Note: This data is useful for identifying industry boards and their codes, which can be used as inputs for other functions like stock_board_industry_cons_em.
    
    
    中文: 东方财富-沪深京板块-行业板块
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每个行业板块的以下字段：
    - 排名: 排名
    - 板块名称: 板块名称
    - 板块代码: 板块代码
    - 最新价: 最新价格
    - 涨跌额: 涨跌额
    - 涨跌幅: 涨跌幅 (%)
    - 总市值: 总市值
    - 换手率: 换手率 (%)
    - 上涨家数: 上涨股票数量
    - 下跌家数: 下跌股票数量
    - 领涨股票: 领涨股票
    - 领涨股票-涨跌幅: 领涨股票涨跌幅 (%)
    
    注意：该数据对于识别行业板块及其代码非常有用，这些代码可以用作其他函数（如 stock_board_industry_cons_em）的输入。
    """
    try:
        df = ak.stock_board_industry_name_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Industry Detail
@mcp.tool()
def stock_board_industry_cons_em(symbol: str) -> str:
    """Get stocks in a specific industry board from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Industry board name (e.g., "小金属") or code (e.g., "BK1027"). 
            You can use stock_board_industry_name_em() to get a list of all industry board names and codes.
    
    Returns:
    JSON formatted data including the following fields for each stock in the industry board:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount
    - 成交量: Trading volume (unit: lot)
    - 成交额: Trading amount
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Opening price
    - 昨收: Previous closing price
    - 换手率: Turnover rate (%)
    - 市盈率-动态: P/E ratio (dynamic)
    - 市净率: P/B ratio
    
    
    中文: 东方财富-沪深板块-行业板块-板块成份
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 行业板块名称（例如："小金属"）或代码（例如："BK1027"）。
            可以使用 stock_board_industry_name_em() 获取所有行业板块名称和代码的列表。
    
    返回:
    JSON格式数据，包含行业板块中每只股票的以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格
    - 涨跌幅: 涨跌幅 (%)
    - 涨跌额: 涨跌额
    - 成交量: 成交量 (单位: 手)
    - 成交额: 成交额
    - 振幅: 振幅 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 开盘价
    - 昨收: 昨日收盘价
    - 换手率: 换手率 (%)
    - 市盈率-动态: 市盈率(动态)
    - 市净率: 市净率
    """
    try:
        df = ak.stock_board_industry_cons_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Financial Report

# Stock Financial Analysis
@mcp.tool()
def stock_financial_analysis_indicator(symbol: str, start_year: str = "2020") -> str:
    """Get financial analysis indicators for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock symbol (e.g., '600004')
    start_year: str - Starting year for the financial data query (e.g., '2020'), default is '2020'
    
    Returns:
    JSON formatted data including a comprehensive set of financial indicators such as:
    - Per share indicators (EPS, adjusted EPS, net assets per share, etc.)
    - Profitability indicators (profit margins, return on assets, return on equity, etc.)
    - Growth indicators (revenue growth rate, net profit growth rate, etc.)
    - Operational efficiency indicators (asset turnover, inventory turnover, etc.)
    - Liquidity indicators (current ratio, quick ratio, etc.)
    - Solvency indicators (debt ratio, equity ratio, etc.)
    - Cash flow indicators (cash flow to sales ratio, cash flow to debt ratio, etc.)
    
    
    中文: 新浪财经-财务分析-财务指标
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码（例如：'600004'）
    start_year: str - 开始查询的年份（例如：'2020'），默认为 '2020'
    
    返回:
    JSON格式数据，包含全面的财务指标，如：
    - 每股指标（每股收益、调整后每股收益、每股净资产等）
    - 盈利能力指标（利润率、资产收益率、股本收益率等）
    - 增长指标（营业收入增长率、净利润增长率等）
    - 运营效率指标（资产周转率、存货周转率等）
    - 流动性指标（流动比率、速动比率等）
    - 偿债能力指标（资产负债率、股东权益比率等）
    - 现金流量指标（现金流量与销售比率、现金流量与负债比率等）
    """
    try:
        df = ak.stock_financial_analysis_indicator(symbol=symbol, start_year=start_year)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Dividend
@mcp.tool()
def stock_dividend_cninfo(symbol: str) -> str:
    """Get dividend history for a specific stock from CNINFO.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock symbol (e.g., '600009')
    
    Returns:
    JSON formatted data including the following fields for each dividend record:
    - Implementation plan announcement date
    - Bonus share ratio (per 10 shares)
    - Conversion ratio (per 10 shares)
    - Dividend ratio (per 10 shares)
    - Registration date
    - Ex-dividend date
    - Dividend payment date
    - Share arrival date
    - Dividend plan description
    - Dividend type
    - Reporting time
    
    
    中文: 巨潮资讯-个股-历史分红
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码（例如：'600009'）
    
    返回:
    JSON格式数据，包含每条分红记录的以下字段：
    - 实施方案公告日期
    - 送股比例（每10股）
    - 转增比例（每10股）
    - 派息比例（每10股）
    - 股权登记日
    - 除权日
    - 派息日
    - 股份到账日
    - 实施方案分红说明
    - 分红类型
    - 报告时间
    """
    try:
        df = ak.stock_dividend_cninfo(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Margin Trading

# Stock Margin Trading Summary
@mcp.tool()
def stock_margin_sse(start_date: str = "20010106", end_date: str = "20210208") -> str:
    """Get margin trading summary for Shanghai Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    start_date: str - Start date in format "YYYYMMDD" (e.g., "20010106"), default is "20010106"
    end_date: str - End date in format "YYYYMMDD" (e.g., "20210208"), default is "20210208"
    
    Returns:
    JSON formatted data including the following fields:
    - Credit transaction date
    - Margin balance (in CNY)
    - Margin buying amount (in CNY)
    - Short selling volume
    - Short selling amount (in CNY)
    - Short selling volume sold
    - Margin trading balance (in CNY)
    
    
    中文: 上海证券交易所-融资融券数据-融资融券汇总数据
    
    返回 JSON 格式的数据。
    
    参数:
    start_date: str - 开始日期，格式为 "YYYYMMDD"（例如："20010106"），默认为 "20010106"
    end_date: str - 结束日期，格式为 "YYYYMMDD"（例如："20210208"），默认为 "20210208"
    
    返回:
    JSON格式数据，包含以下字段：
    - 信用交易日期
    - 融资余额（单位：元）
    - 融资买入额（单位：元）
    - 融券余量
    - 融券余量金额（单位：元）
    - 融券卖出量
    - 融资融券余额（单位：元）
    """
    try:
        df = ak.stock_margin_sse(start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Short Interest

# Stock Institutional Investors
@mcp.tool()
def stock_institute_hold(symbol: str = "20201") -> str:
    """Get institutional investors' holdings data.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Quarter and year code in format YYYYQ (e.g., "20201" for 2020Q1), default is "20201"
                  From 2005 onwards, where Q represents: 1=Q1, 2=Q2, 3=Q3, 4=Q4
                  For example, "20191" means 2019Q1, "20193" means 2019Q3
    
    Returns:
    JSON formatted data including the following fields:
    - Stock code
    - Stock name
    - Number of institutions
    - Change in number of institutions
    - Holding percentage (%)
    - Increase in holding percentage (%)
    - Percentage of tradable shares (%)
    - Increase in percentage of tradable shares (%)
    
    
    中文: 新浪财经-机构持股-机构持股一览表
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 年度和季度代码，格式为 YYYYQ（例如："20201" 表示 2020年第一季度），默认为 "20201"
                 从 2005 年开始，其中 Q 代表：1=第一季度，2=第二季度，3=第三季度，4=第四季度
                 例如，"20191" 表示 2019年第一季度，"20193" 表示 2019年第三季度
    
    返回:
    JSON格式数据，包含以下字段：
    - 证券代码
    - 证券简称
    - 机构数
    - 机构数变化
    - 持股比例 (%)
    - 持股比例增幅 (%)
    - 占流通股比例 (%)
    - 占流通股比例增幅 (%)
    """
    try:
        df = ak.stock_institute_hold(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Forecast

# Stock Analyst Rating

# Stock Analyst Detail
@mcp.tool()
def stock_analyst_detail_em(symbol: str) -> str:
    """Get detailed analyst reports for a specific stock from Eastmoney.
    
    Args:
    symbol: Stock symbol (e.g., 600000)
    
    Returns analyst report details including:
    - Report date
    - Institution name
    - Analyst name
    - Report title
    - Rating
    - Target price
    
    
    中文: 东方财富网-数据中心-研究报告-东方财富分析师指数-分析师详情
    
    Args:
    symbol: Stock symbol (e.g., 600000)
    
    Returns analyst report details including:
    - Report date
    - Institution name
    - Analyst name
    - Report title
    - Rating
    - Target price
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_analyst_detail_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock News
@mcp.tool()
def stock_news_em(symbol: str) -> str:
    """Get latest stock market news from Eastmoney for a specific stock or keyword.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code (e.g., "300059") or other keyword to search for news
    
    Returns:
    JSON formatted data including the following fields:
    - 关键词: Keyword
    - 新闻标题: News title
    - 新闻内容: News content
    - 发布时间: Publication time
    - 文章来源: News source
    - 新闻链接: News link
    
    Note: Returns the most recent 100 news items for the specified symbol on the current day.
    
    
    中文: 东方财富指定个股的新闻资讯数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码（例如："300059"）或其他要搜索的关键词
    
    返回:
    JSON格式数据，包含以下字段：
    - 关键词: 关键词
    - 新闻标题: 新闻标题
    - 新闻内容: 新闻内容
    - 发布时间: 发布时间
    - 文章来源: 新闻来源
    - 新闻链接: 新闻链接
    
    注意：返回当天指定股票最近的 100 条新闻资讯数据。
    """
    try:
        df = ak.stock_news_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Company News

# Stock Announcements
@mcp.tool()
def stock_notice_report(symbol: str = "全部", date: str = None) -> str:
    """Get stock announcements from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Announcement type, options: "全部" (All), "重大事项" (Major Events), "财务报告" (Financial Reports), "融资公告" (Financing Announcements), "风险提示" (Risk Warnings), "资产重组" (Asset Restructuring), "信息变更" (Information Changes), "持股变动" (Shareholding Changes), default is "全部"
    date: str - Specific date in format "YYYYMMDD" (e.g., "20240613"), default is current date
    
    Returns:
    JSON formatted data including the following fields:
    - 代码: Stock code
    - 名称: Stock name
    - 公告标题: Announcement title
    - 公告类型: Announcement type
    - 公告日期: Announcement date
    - 网址: Announcement URL
    
    
    中文: 东方财富网-数据中心-公告大全-沪深京 A 股公告
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 公告类型，可选值："全部"、"重大事项"、"财务报告"、"融资公告"、"风险提示"、"资产重组"、"信息变更"、"持股变动"，默认为 "全部"
    date: str - 指定日期，格式为 "YYYYMMDD"（例如："20240613"），默认为当前日期
    
    返回:
    JSON格式数据，包含以下字段：
    - 代码: 股票代码
    - 名称: 股票名称
    - 公告标题: 公告标题
    - 公告类型: 公告类型
    - 公告日期: 公告日期
    - 网址: 公告链接
    """
    try:
        if date is None:
            from datetime import datetime
            date = datetime.now().strftime("%Y%m%d")
        df = ak.stock_notice_report(symbol=symbol, date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Company Announcements

# Stock ETF List

# Stock ETF Daily

# Stock ETF Real-time

# Stock ETF Components

# Stock Options

# Stock Option Quote

# Stock Option Chain

# Stock Option Greeks

# Stock IPO Calendar

# Stock Delisting

# Stock Macro Data - GDP

# Stock Macro Data - CPI

# Stock Macro Data - PPI

# Stock Macro Data - PMI

# Stock Macro Data - M2

# Stock Macro Data - Interest Rate

# Stock Macro Data - Foreign Exchange Reserves

# Stock Macro Data - Foreign Investment

# Stock Macro Data - Industrial Production

# Stock Macro Data - Retail Sales

# Bond Market - Treasury Yield Curve

# Bond Market - China Government Bond

# Bond Market - Corporate Bond

# Bond Market - Convertible Bond

# Futures Market - China Futures List

# Futures Market - China Futures Quote

# Futures Market - China Futures Daily

# Futures Market - China Futures Holdings

# Stock Market - Index Constituents

# Stock Market - Index Daily

# Stock Market - Index Real-time

# Stock Market - Index Future

# Stock Market - Fund Flow

# Stock Market - Fund Flow Rank
@mcp.tool()
def stock_individual_fund_flow_rank() -> str:
    """Get fund flow ranking for all stocks.
    
    Returns fund flow ranking data including:
    - Stock code
    - Stock name
    - Latest price
    - Change percentage
    - Net inflow amount
    - Net inflow percentage
    - Main inflow
    - Retail inflow
    
    
    中文: 东方财富网-数据中心-资金流向-排名
    
    Returns fund flow ranking data including:
    - Stock code
    - Stock name
    - Latest price
    - Change percentage
    - Net inflow amount
    - Net inflow percentage
    - Main inflow
    - Retail inflow
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_individual_fund_flow_rank()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Sector Fund Flow

# Stock Market - Market Sentiment
@mcp.tool()
def stock_market_activity_legu() -> str:
    """Get market sentiment and activity data.
    
    Returns market sentiment data including:
    - Date
    - Market activity
    - Bullish sentiment
    - Bearish sentiment
    - Turnover rate
    
    
    中文: 乐咕乐股网-赚钱效应分析数据
    
    Returns market sentiment data including:
    - Date
    - Market activity
    - Bullish sentiment
    - Bearish sentiment
    - Turnover rate
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_market_activity_legu()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Market PE

# Stock Market - Market PB

# Stock Market - HK Stocks List
@mcp.tool()
def stock_hk_spot_em() -> str:
    """Get real-time quotes for all Hong Kong stocks.
    
    Returns HK stocks data including:
    - Stock code
    - Stock name
    - Latest price
    - Change amount
    - Change percentage
    - Volume
    - Amount
    
    
    中文: 所有港股的实时行情数据; 该数据有 15 分钟延时
    
    Returns HK stocks data including:
    - Stock code
    - Stock name
    - Latest price
    - Change amount
    - Change percentage
    - Volume
    - Amount
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - HK Stock Daily
@mcp.tool()
def stock_hk_daily() -> str:
    """Get historical daily data for a specific Hong Kong stock.
    
    Args:
        symbol: Stock symbol (e.g., 00700 for Tencent)
        
    Returns HK stock historical data including:
    - Date
    - Open
    - High
    - Low
    - Close
    - Volume
    - Amount
    
    中文: Get historical daily data for a specific Hong Kong stock.
    
    Args:
        symbol: Stock symbol (e.g., 00700 for Tencent)
        
    Returns HK stock historical data including:
    - Date
    - Open
    - High
    - Low
    - Close
    - Volume
    - Amount
    
    Returns:
        JSON formatted data
        
    返回:
        JSON格式数据
    """
    try:
        df = ak.stock_hk_daily(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - US Stocks List

# Stock Market - US Stock Daily
@mcp.tool()
def stock_us_daily(symbol: str) -> str:
    """Get historical daily data for a specific US stock.
    
    Args:
    symbol: Stock symbol (e.g., AAPL for Apple)
    
    Returns US stock historical data including:
    - Date
    - Open
    - High
    - Low
    - Close
    - Volume
    - Amount
    
    
    中文: 美股历史行情数据，设定 adjust="qfq" 则返回前复权后的数据，默认 adjust="", 则返回未复权的数据，历史数据按日频率更新
    
    Args:
    symbol: Stock symbol (e.g., AAPL for Apple)
    
    Returns US stock historical data including:
    - Date
    - Open
    - High
    - Low
    - Close
    - Volume
    - Amount
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_us_daily(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - US Stock Financials

# Stock Market - Global Indices

# Stock Market - Global Commodities

# Stock Market - Global Forex

# Stock Market - Stock Screening

# Stock Market - Stock Screening - New Stocks

# Stock Market - Stock Screening - Suspended Stocks

# Stock Market - Stock Screening - High Growth

# Stock Market - Stock Screening - Limit Up/Down

# Stock Market - AH Comparison

# Stock Market - Stock Repurchase
@mcp.tool()
def stock_repurchase_em() -> str:
    """Get stock repurchase data.
    
    Returns stock repurchase data including:
    - Stock code
    - Stock name
    - Announcement date
    - Repurchase amount
    - Repurchase price range
    - Repurchase period
    
    
    中文: 东方财富网-数据中心-股票回购-股票回购数据
    
    Returns stock repurchase data including:
    - Stock code
    - Stock name
    - Announcement date
    - Repurchase amount
    - Repurchase price range
    - Repurchase period
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_repurchase_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Restricted Shares

# Stock Market - Insider Trading

# Stock Market - Major Shareholders

# Technical Analysis - KDJ Indicator

# Technical Analysis - MACD Indicator

# Technical Analysis - RSI Indicator

# Technical Analysis - Bollinger Bands

# Stock Ranking - ROE Ranking

# Stock Ranking - Profit Growth Ranking

# Stock Ranking - Net Profit Ranking

# Stock Ranking - PE Ranking

# Stock Ranking - Market Cap Ranking

# Stock Industry Analysis

# Stock Industry Performance

# Stock Market - Northbound Capital Flow

# Stock Market - Southbound Capital Flow

# Stock Market - Northbound Holdings

# Stock Market - Southbound Holdings

# Stock Market - QFII Holdings

# Stock Market - QFII Holdings Detail

# Stock Market - MSCI Constituents

# Stock Market - FTSE Constituents

# Stock Financial Indicators

# Stock Dividend Data

# Stock Dividend History

# Stock Dividend Statistics

# Stock Market - Trading Calendar

# Stock Market - Margin Trading Data

# Stock Market - Margin Trading Summary

# Stock Market - Margin Trading Securities List
@mcp.tool()
def stock_margin_underlying_info_szse() -> str:
    """Get list of securities eligible for margin trading in Shenzhen Stock Exchange.
    
    Returns margin trading securities list including:
    - Stock code
    - Stock name
    - Inclusion date
    - Status
    
    
    中文: 深圳证券交易所-融资融券数据-标的证券信息
    
    Returns margin trading securities list including:
    - Stock code
    - Stock name
    - Inclusion date
    - Status
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_margin_underlying_info_szse()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Stock Account Statistics
@mcp.tool()
def stock_account_statistics_em() -> str:
    """Get statistics on stock trading accounts.
    
    Returns stock account statistics including:
    - Date
    - Number of new accounts
    - Total number of accounts
    - Active accounts
    - A-share accounts
    - B-share accounts
    
    
    中文: 东方财富网-数据中心-特色数据-股票账户统计
    
    Returns stock account statistics including:
    - Date
    - Number of new accounts
    - Total number of accounts
    - Active accounts
    - A-share accounts
    - B-share accounts
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_account_statistics_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Stock Account Opening

# Stock Market - Investor Structure

# Stock Market - Investor Sentiment Index

@mcp.tool()
def news_report_time_baidu(date: str = "20241107") -> str:
    """Get 百度股市通-财报发行
    
    Returns data in JSON format.
    
    
    中文: 百度股市通-财报发行
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.news_report_time_baidu(date="20241107")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def news_trade_notify_dividend_baidu(date: str = "20241107") -> str:
    """Get 百度股市通-交易提醒-分红派息
    
    Returns data in JSON format.
    
    
    中文: 百度股市通-交易提醒-分红派息
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.news_trade_notify_dividend_baidu(date="20241107")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def news_trade_notify_suspend_baidu(date: str = "20241107") -> str:
    """Get 百度股市通-交易提醒-停复牌
    
    Returns data in JSON format.
    
    
    中文: 百度股市通-交易提醒-停复牌
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.news_trade_notify_suspend_baidu(date="20241107")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_a_all_pb() -> str:
    """Get 乐咕乐股-A 股等权重与中位数市净率
    
    Returns data in JSON format.
    
    
    中文: 乐咕乐股-A 股等权重与中位数市净率
    
    Returns data in JSON format.
    
    Parameters:
    This function does not require any parameters.
    
    Returns:
    JSON formatted data with fields including date, middlePB, equalWeightAveragePB, close, and various quantile metrics
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含日期、全部A股市净率中位数、全部A股市净率等权平均、上证指数等字段
    """
    try:
        df = ak.stock_a_all_pb()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_a_below_net_asset_statistics(symbol: str = "全部A股") -> str:
    """Get 乐咕乐股-A 股破净股统计数据
    
    Returns data in JSON format.
    
    
    中文: 乐咕乐股-A 股破净股统计数据
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票指数类型，选项包括 {"全部A股", "沪深300", "上证50", "中证500"}
    
    Returns:
    JSON formatted data with fields including date, below_net_asset, total_company, below_net_asset_ratio
    
    参数:
    symbol: str - 股票指数类型，选项包括 {"全部A股", "沪深300", "上证50", "中证500"}
    
    返回:
    JSON格式数据，包含交易日、破净股家数、总公司数、破净股比率等字段
    """
    try:
        df = ak.stock_a_below_net_asset_statistics(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_a_congestion_lg() -> str:
    """Get 乐咕乐股-大盘拥挤度
    
    Returns data in JSON format.
    
    
    中文: 乐咕乐股-大盘拥挤度
    
    Returns data in JSON format.
    
    Parameters:
    This function does not require any parameters.
    
    Returns:
    JSON formatted data with fields including date, close, congestion
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含日期、收盘价、拥挤度等字段
    """
    try:
        df = ak.stock_a_congestion_lg()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_a_gxl_lg(symbol: str = "上证A股") -> str:
    """Get 乐咕乐股-股息率-A 股股息率
    
    Returns data in JSON format.
    
    
    中文: 乐咕乐股-股息率-A 股股息率
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_a_gxl_lg(symbol="上证A股")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_a_high_low_statistics(symbol: str = "all") -> str:
    """Get 不同市场的创新高和新低的股票数量
    
    Returns data in JSON format.
    
    
    中文: 不同市场的创新高和新低的股票数量
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票市场类型，选项包括 {"all": "全部A股", "sz50": "上证50", "hs300": "沪深300", "zz500": "中证500"}
    
    Returns:
    JSON formatted data with fields including date, close, high20, low20, high60, low60, high120, low120
    
    参数:
    symbol: str - 股票市场类型，选项包括 {"all": "全部A股", "sz50": "上证50", "hs300": "沪深300", "zz500": "中证500"}
    
    返回:
    JSON格式数据，包含交易日、相关指数收盘价、20日新高、20日新低、60日新高、60日新低、120日新高、120日新低等字段
    """
    try:
        df = ak.stock_a_high_low_statistics(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_a_indicator_lg(symbol: str = "000001") -> str:
    """Get 乐咕乐股-A 股个股指标: 市盈率, 市净率, 股息率
    
    Returns data in JSON format.
    
    
    中文: 乐咕乐股-A 股个股指标: 市盈率, 市净率, 股息率
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票代码，例如 "000001"，使用 ak.stock_a_indicator_lg(symbol="all") 获取所有股票代码
    
    Returns:
    JSON formatted data with fields including trade_date, pe, pe_ttm, pb, ps, ps_ttm, dv_ratio, dv_ttm, total_mv
    
    参数:
    symbol: str - 股票代码，例如 "000001"，使用 ak.stock_a_indicator_lg(symbol="all") 获取所有股票代码
    
    返回:
    JSON格式数据，包含交易日期、市盈率、市盈率TTM、市净率、市销率、市销率TTM、股息率、股息率TTM、总市值等字段
    """
    try:
        df = ak.stock_a_indicator_lg(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_a_ttm_lyr() -> str:
    """Get 乐咕乐股-A 股等权重市盈率与中位数市盈率
    
    Returns data in JSON format.
    
    
    中文: 乐咕乐股-A 股等权重市盈率与中位数市盈率
    
    Returns data in JSON format.
    
    Parameters:
    This function does not require any parameters.
    
    Returns:
    JSON formatted data with fields including date, middlePETTM, averagePETTM, middlePELYR, averagePELYR, and various quantile metrics
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含日期、全A股滚动市盈率中位数、全A股滚动市盈率等权平均、全A股静态市盈率中位数、全A股静态市盈率等权平均等字段
    """
    try:
        df = ak.stock_a_ttm_lyr()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_add_stock(symbol: str = "600004") -> str:
    """Get 新浪财经-发行与分配-增发
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-发行与分配-增发
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_add_stock(symbol="600004")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_allotment_cninfo(symbol: str = "600030", start_date: str = "19700101", end_date: str = "22220222") -> str:
    """Get 巨潮资讯-个股-配股实施方案
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-个股-配股实施方案
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票代码，例如 "600030"
    start_date: str - 开始日期，格式为 YYYYMMDD，例如 "19700101"
    end_date: str - 结束日期，格式为 YYYYMMDD，例如 "22220222"
    
    Returns:
    JSON formatted data with fields including record ID, stock name, suspension start date, listing announcement date, etc.
    
    参数:
    symbol: str - 股票代码，例如 "600030"
    start_date: str - 开始日期，格式为 YYYYMMDD，例如 "19700101"
    end_date: str - 结束日期，格式为 YYYYMMDD，例如 "22220222"
    
    返回:
    JSON格式数据，包含记录标识、证券简称、停牌起始日、上市公告日期等字段
    """
    try:
        df = ak.stock_allotment_cninfo(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_analyst_rank_em(year: str) -> str:
    """Get 东方财富网-数据中心-研究报告-东方财富分析师指数
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-研究报告-东方财富分析师指数
    
    Returns data in JSON format.
    
    Parameters:
    year: str - 年份，例如 '2024'，数据范围从 2013 年至今
    
    Returns:
    JSON formatted data with fields including analyst name, company, annual index, return rates, and stock ratings
    
    参数:
    year: str - 年份，例如 '2024'，数据范围从 2013 年至今
    
    返回:
    JSON格式数据，包含分析师名称、分析师单位、年度指数、收益率、成分股个数、股票评级等字段
    """
    try:
        df = ak.stock_analyst_rank_em(year=year)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_balance_sheet_by_report_delisted_em(symbol: str = "SZ000013") -> str:
    """Get 东方财富-股票-财务分析-资产负债表-已退市股票-按报告期
    
    Returns data in JSON format.
    
    
    中文: 东方财富-股票-财务分析-资产负债表-已退市股票-按报告期
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 带市场标识的已退市股票代码，例如 "SZ000013"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 带市场标识的已退市股票代码，例如 "SZ000013"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_balance_sheet_by_report_delisted_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_balance_sheet_by_report_em(symbol: str = "SH600519") -> str:
    """Get 东方财富-股票-财务分析-资产负债表-按报告期
    
    Returns data in JSON format.
    
    
    中文: 东方财富-股票-财务分析-资产负债表-按报告期
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票代码，例如 "SH600519"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 股票代码，例如 "SH600519"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_balance_sheet_by_yearly_em(symbol: str = "SH600519") -> str:
    """Get 东方财富-股票-财务分析-资产负债表-按年度
    
    Returns data in JSON format.
    
    
    中文: 东方财富-股票-财务分析-资产负债表-按年度
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票代码，例如 "SH600519"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 股票代码，例如 "SH600519"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_balance_sheet_by_yearly_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_change_em() -> str:
    """Get 东方财富-行情中心-当日板块异动详情
    
    Returns data in JSON format.
    
    
    中文: 东方财富-行情中心-当日板块异动详情
    
    Returns data in JSON format.
    
    Parameters:
    This function does not require any parameters.
    
    Returns:
    JSON formatted data with fields including 板块名称, 涨跌幅, 主力净流入, 板块异动总次数, etc.
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含板块名称, 涨跌幅, 主力净流入, 板块异动总次数等字段
    """
    try:
        df = ak.stock_board_change_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_concept_hist_em(symbol: str = "HS300", period: str = "daily", start_date: str = "20220101", end_date: str = "20220101", adjust: str = "") -> str:
    """Get 东方财富-沪深板块-概念板块-历史行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富-沪深板块-概念板块-历史行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_concept_hist_em(symbol="绿色电力", period="daily", start_date="20220101", end_date="20250227", adjust="")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_concept_hist_min_em(symbol: str = "长寿药", period: str = "1") -> str:
    """Get 东方财富-沪深板块-概念板块-分时历史行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富-沪深板块-概念板块-分时历史行情数据
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 概念板块名称，可以通过调用 stock_board_concept_name_em() 查看东方财富-概念板块的所有概念代码
    period: str - 分时周期，可选值为 {"1", "5", "15", "30", "60"}
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 概念板块名称，可以通过调用 stock_board_concept_name_em() 查看东方财富-概念板块的所有概念代码
    period: str - 分时周期，可选值为 {"1", "5", "15", "30", "60"}
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_concept_hist_min_em(symbol=symbol, period=period)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_concept_index_ths(symbol: str = "计算机概念", start_date: str = "20200101", end_date: str = "20250228") -> str:
    """Get 同花顺-板块-概念板块-指数日频率数据
    
    Returns data in JSON format.
    
    
    中文: 同花顺-板块-概念板块-指数日频率数据
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 概念板块名称，可以通过 stock_board_concept_name_ths() 查看所有概念名称
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 概念板块名称，可以通过 stock_board_concept_name_ths() 查看所有概念名称
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_concept_index_ths(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_concept_info_ths(symbol: str = "阿里巴巴概念") -> str:
    """Get 同花顺-板块-概念板块-板块简介
    
    Returns data in JSON format.
    
    
    中文: 同花顺-板块-概念板块-板块简介
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_concept_info_ths(symbol="阿里巴巴概念")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_concept_spot_em(symbol: str = "可燃冰") -> str:
    """Get 东方财富网-行情中心-沪深京板块-概念板块-实时行情
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-沪深京板块-概念板块-实时行情
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 概念板块名称，例如“可燃冰”
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 概念板块名称，例如“可燃冰”
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_concept_spot_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_industry_hist_em(symbol: str = "小金属", start_date: str = "20211201", end_date: str = "20240222", period: str = "日k", adjust: str = "") -> str:
    """Get 东方财富-沪深板块-行业板块-历史行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富-沪深板块-行业板块-历史行情数据
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 行业板块名称，可以通过调用 stock_board_industry_name_em() 查看东方财富-行业板块的所有行业代码
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    period: str - 周期，可选值为 {"日k", "周k", "月k"}
    adjust: str - 复权类型，可选值为 {'': 不复权, 默认; "qfq": 前复权, "hfq": 后复权}
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 行业板块名称，可以通过调用 stock_board_industry_name_em() 查看东方财富-行业板块的所有行业代码
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    period: str - 周期，可选值为 {"日k", "周k", "月k"}
    adjust: str - 复权类型，可选值为 {'': 不复权, 默认; "qfq": 前复权, "hfq": 后复权}
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_industry_hist_em(symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_industry_hist_min_em(symbol: str = "小金属", period: str = "1") -> str:
    """Get 东方财富-沪深板块-行业板块-分时历史行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富-沪深板块-行业板块-分时历史行情数据
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 行业板块名称，可以通过调用 stock_board_industry_name_em() 查看东方财富-行业板块的所有行业代码
    period: str - 分时周期，可选值为 {"1", "5", "15", "30", "60"}
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 行业板块名称，可以通过调用 stock_board_industry_name_em() 查看东方财富-行业板块的所有行业代码
    period: str - 分时周期，可选值为 {"1", "5", "15", "30", "60"}
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_industry_hist_min_em(symbol=symbol, period=period)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_industry_index_ths(symbol: str = "计算机行业", start_date: str = "20200101", end_date: str = "20211027") -> str:
    """Get 同花顺-板块-行业板块-指数日频率数据
    
    Returns data in JSON format.
    
    
    中文: 同花顺-板块-行业板块-指数日频率数据
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 行业板块名称，可以通过 stock_board_industry_name_ths() 查看所有行业名称
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 行业板块名称，可以通过 stock_board_industry_name_ths() 查看所有行业名称
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_industry_index_ths(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_industry_spot_em(symbol: str = "小金属") -> str:
    """Get 东方财富网-沪深板块-行业板块-实时行情
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-沪深板块-行业板块-实时行情
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 行业板块名称，例如“小金属”
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 行业板块名称，例如“小金属”
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_industry_spot_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_board_industry_summary_ths() -> str:
    """Get 同花顺-同花顺行业一览表
    
    Returns data in JSON format.
    
    
    中文: 同花顺-同花顺行业一览表
    
    Returns data in JSON format.
    
    Parameters:
    None - 此 API 不需要参数
    
    Returns:
    JSON formatted data
    
    参数:
    无 - 此 API 不需要参数
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_board_industry_summary_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_buffett_index_lg() -> str:
    """Get 乐估乐股-底部研究-巴菲特指标
    
    Returns data in JSON format.
    
    
    中文: 乐估乐股-底部研究-巴菲特指标
    
    Returns data in JSON format.
    
    Parameters:
    This function does not require any parameters.
    
    Returns:
    JSON formatted data with fields including 日期(交易日), 收盘价, 总市值, GDP, 近十年分位数, 总历史分位数
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含日期(交易日), 收盘价, 总市值, GDP, 近十年分位数, 总历史分位数等字段
    """
    try:
        df = ak.stock_buffett_index_lg()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cash_flow_sheet_by_quarterly_em(symbol: str = "SH600519") -> str:
    """Get cash flow statement by quarter from East Money for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code with market prefix, e.g., "SH600519" for Kweichow Moutai. Default is "SH600519".
    
    Returns:
    JSON formatted data containing the quarterly cash flow statement with approximately 315 different financial metrics.
    The data includes operating cash flows, investment cash flows, financing cash flows, and other related metrics.
    
    
    中文: 东方财富-股票-财务分析-现金流量表-按单季度
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，需要带市场标识，例如 "SH600519" 表示贵州茅台。默认值为 "SH600519"。
    
    返回:
    JSON格式数据，包含按季度的现金流量表，约有315个不同的财务指标。
    数据包括经营活动现金流量、投资活动现金流量、筹资活动现金流量等相关指标。
    """
    try:
        df = ak.stock_cash_flow_sheet_by_quarterly_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cash_flow_sheet_by_report_delisted_em(symbol: str = "SZ000013") -> str:
    """Get 东方财富-股票-财务分析-现金流量表-已退市股票-按报告期
    
    Returns data in JSON format.
    
    
    中文: 东方财富-股票-财务分析-现金流量表-已退市股票-按报告期
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 带市场标识的已退市股票代码，例如 "SZ000013"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 带市场标识的已退市股票代码，例如 "SZ000013"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_cash_flow_sheet_by_report_delisted_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cash_flow_sheet_by_report_em(symbol: str = "SH600519") -> str:
    """Get cash flow statement by reporting period from East Money for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code with market prefix, e.g., "SH600519" for Kweichow Moutai. Default is "SH600519".
    
    Returns:
    JSON formatted data containing the cash flow statement by reporting period with approximately 252 different financial metrics.
    The data includes operating cash flows, investment cash flows, financing cash flows, and other related metrics.
    
    
    中文: 东方财富-股票-财务分析-现金流量表-按报告期
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，需要带市场标识，例如 "SH600519" 表示贵州茅台。默认值为 "SH600519"。
    
    返回:
    JSON格式数据，包含按报告期的现金流量表，约有252个不同的财务指标。
    数据包括经营活动现金流量、投资活动现金流量、筹资活动现金流量等相关指标。
    """
    try:
        df = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cash_flow_sheet_by_yearly_em(symbol: str = "SH600519") -> str:
    """Get cash flow statement by year from East Money for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code with market prefix, e.g., "SH600519" for Kweichow Moutai. Default is "SH600519".
    
    Returns:
    JSON formatted data containing the yearly cash flow statement with approximately 314 different financial metrics.
    The data includes operating cash flows, investment cash flows, financing cash flows, and other related metrics.
    
    
    中文: 东方财富-股票-财务分析-现金流量表-按年度
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，需要带市场标识，例如 "SH600519" 表示贵州茅台。默认值为 "SH600519"。
    
    返回:
    JSON格式数据，包含按年度的现金流量表，约有314个不同的财务指标。
    数据包括经营活动现金流量、投资活动现金流量、筹资活动现金流量等相关指标。
    """
    try:
        df = ak.stock_cash_flow_sheet_by_yearly_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cg_equity_mortgage_cninfo(date: str = "20210930") -> str:
    """Get equity pledge data from CNINFO (China Securities Regulatory Commission Information Disclosure).
    
    Returns data in JSON format.
    
    Parameters:
    date: str - Query date in format "YYYYMMDD", e.g., "20210930". Default is "20210930".
    
    Returns:
    JSON formatted data containing equity pledge information with the following fields:
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 公告日期: Announcement date
    - 出质人: Pledgor
    - 质权人: Pledgee
    - 质押数量: Pledged amount (unit: 10,000 shares)
    - 占总股本比例: Percentage of total share capital (%)
    - 质押解除数量: Amount of pledge released (unit: 10,000 shares)
    - 质押事项: Pledge matters (unit: 10,000 yuan)
    - 累计质押占总股本比例: Cumulative pledge as percentage of total share capital (%)
    
    
    中文: 巨潮资讯-数据中心-专题统计-公司治理-股权质押
    
    返回 JSON 格式的数据。
    
    参数:
    date: str - 查询日期，格式为 "YYYYMMDD"，例如 "20210930"。默认值为 "20210930"。
    
    返回:
    JSON格式数据，包含股权质押信息，包含以下字段：
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 公告日期: 公告日期
    - 出质人: 出质人
    - 质权人: 质权人
    - 质押数量: 质押数量（单位：万股）
    - 占总股本比例: 占总股本比例（%）
    - 质押解除数量: 质押解除数量（单位：万股）
    - 质押事项: 质押事项（单位：万元）
    - 累计质押占总股本比例: 累计质押占总股本比例（%）
    """
    try:
        df = ak.stock_cg_equity_mortgage_cninfo(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cg_guarantee_cninfo(symbol: str = "全部", start_date: str = "20180630", end_date: str = "20210927") -> str:
    """Get 巨潮资讯-数据中心-专题统计-公司治理-对外担保
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-数据中心-专题统计-公司治理-对外担保
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 市场类型，可选值包括 {"全部", "深市主板", "沪市", "创业板", "科创板"}
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 市场类型，可选值包括 {"全部", "深市主板", "沪市", "创业板", "科创板"}
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_cg_guarantee_cninfo(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cg_lawsuit_cninfo(symbol: str = "全部", start_date: str = "20180630", end_date: str = "20210927") -> str:
    """Get 巨潮资讯-数据中心-专题统计-公司治理-公司诉讼
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-数据中心-专题统计-公司治理-公司诉讼
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 市场类型，可选值包括 {"全部", "深市主板", "沪市", "创业板", "科创板"}
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    Returns:
    JSON formatted data
    
    参数:
    symbol: str - 市场类型，可选值包括 {"全部", "深市主板", "沪市", "创业板", "科创板"}
    start_date: str - 开始日期，格式为 "YYYYMMDD"
    end_date: str - 结束日期，格式为 "YYYYMMDD"
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_cg_lawsuit_cninfo(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_changes_em(symbol: str = "大笔买入") -> str:
    """Get market anomaly data from East Money's market center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Type of market anomaly. Default is "大笔买入" (large buy orders).
      Available options include:
      - Upward trends: '火箭发射' (rocket launch), '快速反弹' (quick rebound), '大笔买入' (large buy orders),
        '封涨停板' (hit upper limit), '打开跌停板' (breaking lower limit), '有大买盘' (large buying),
        '竞价上涨' (auction rise), '高开5日线' (open above 5-day line), '向上缺口' (upward gap),
        '60日新高' (60-day high), '60日大幅上涨' (60-day significant rise)
      - Downward trends: '加速下跌' (accelerated decline), '高台跳水' (high diving), '大笔卖出' (large sell orders),
        '封跌停板' (hit lower limit), '打开涨停板' (breaking upper limit), '有大卖盘' (large selling),
        '竞价下跌' (auction decline), '低开5日线' (open below 5-day line), '向下缺口' (downward gap),
        '60日新低' (60-day low), '60日大幅下跌' (60-day significant decline)
    
    Returns:
    JSON formatted data containing the following fields:
    - 时间: Time of the anomaly
    - 代码: Stock code
    - 名称: Stock name
    - 板块: Sector/industry
    - 相关信息: Related information (note: units may vary depending on the anomaly type)
    
    
    中文: 东方财富-行情中心-盘口异动数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 盘口异动类型。默认值为 "大笔买入"。
      可选值包括：
      - 上涨趋势：'火箭发射', '快速反弹', '大笔买入', '封涨停板', '打开跌停板', 
        '有大买盘', '竞价上涨', '高开5日线', '向上缺口', '60日新高', '60日大幅上涨'
      - 下跌趋势：'加速下跌', '高台跳水', '大笔卖出', '封跌停板', '打开涨停板', 
        '有大卖盘', '竞价下跌', '低开5日线', '向下缺口', '60日新低', '60日大幅下跌'
    
    返回:
    JSON格式数据，包含以下字段：
    - 时间: 异动发生时间
    - 代码: 股票代码
    - 名称: 股票名称
    - 板块: 所属板块/行业
    - 相关信息: 相关信息（注意：不同类型的异动单位可能不同）
    """
    try:
        df = ak.stock_changes_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_circulate_stock_holder(symbol: str = "600000") -> str:
    """Get circulating shareholder data from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market prefix, e.g., "600000" for Bank of Shanghai. Default is "600000".
    
    Returns:
    JSON formatted data containing information about circulating shareholders with the following fields:
    - 截止日期: Cut-off date
    - 公告日期: Announcement date
    - 编号: Serial number
    - 股东名称: Shareholder name
    - 持股数量: Number of shares held (unit: shares)
    - 占流通股比例: Percentage of circulating shares (%)
    - 股本性质: Nature of shares
    
    
    中文: 新浪财经-股东股本-流通股东
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场前缀，例如 "600000" 表示上海银行。默认值为 "600000"。
    
    返回:
    JSON格式数据，包含流通股东信息，包含以下字段：
    - 截止日期: 截止日期
    - 公告日期: 公告日期
    - 编号: 序号
    - 股东名称: 股东名称
    - 持股数量: 持股数量（单位：股）
    - 占流通股比例: 占流通股比例（%）
    - 股本性质: 股本性质
    """
    try:
        df = ak.stock_circulate_stock_holder(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_comment_detail_scrd_cost_em(symbol: str = "600000") -> str:
    """Get market cost data from East Money's stock comment feature.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market prefix, e.g., "600000" for Bank of Shanghai. Default is "600000".
    
    Returns:
    JSON formatted data containing market cost information with the following fields:
    - 日期: Date
    - 市场成本: Market cost
    - 5日市场成本: 5-day market cost
    
    
    中文: 东方财富网-数据中心-特色数据-千股千评-市场热度-市场成本
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场前缀，例如 "600000" 表示上海银行。默认值为 "600000"。
    
    返回:
    JSON格式数据，包含市场成本信息，包含以下字段：
    - 日期: 日期
    - 市场成本: 市场成本
    - 5日市场成本: 5日市场成本
    """
    try:
        df = ak.stock_comment_detail_scrd_cost_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_comment_detail_scrd_desire_daily_em(symbol: str = "600000") -> str:
    """Get daily market participation willingness data from East Money's stock comment feature.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market prefix, e.g., "600000" for Bank of Shanghai. Default is "600000".
    
    Returns:
    JSON formatted data containing daily market participation willingness information with the following fields:
    - 交易日: Trading day
    - 当日意愿上升: Daily willingness rise
    - 5日平均参与意愿变化: 5-day average participation willingness change
    
    
    中文: 东方财富网-数据中心-特色数据-千股千评-市场热度-日度市场参与意愿
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场前缀，例如 "600000" 表示上海银行。默认值为 "600000"。
    
    返回:
    JSON格式数据，包含日度市场参与意愿信息，包含以下字段：
    - 交易日: 交易日
    - 当日意愿上升: 当日意愿上升
    - 5日平均参与意愿变化: 5日平均参与意愿变化
    """
    try:
        df = ak.stock_comment_detail_scrd_desire_daily_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_comment_detail_scrd_desire_em(symbol: str = "600000") -> str:
    """Get market participation willingness data from East Money's stock comment feature.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market prefix, e.g., "600000" for Bank of Shanghai. Default is "600000".
    
    Returns:
    JSON formatted data containing market participation willingness information with the following fields:
    - 日期时间: Date and time
    - 大户: Large investors
    - 全部: All investors
    - 散户: Retail investors
    
    
    中文: 东方财富网-数据中心-特色数据-千股千评-市场热度-市场参与意愿
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场前缀，例如 "600000" 表示上海银行。默认值为 "600000"。
    
    返回:
    JSON格式数据，包含市场参与意愿信息，包含以下字段：
    - 日期时间: 日期和时间
    - 大户: 大型投资者
    - 全部: 所有投资者
    - 散户: 散户投资者
    """
    try:
        df = ak.stock_comment_detail_scrd_desire_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_comment_detail_scrd_focus_em(symbol: str = "600000") -> str:
    """Get user focus index data from East Money's stock comment feature.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market prefix, e.g., "600000" for Bank of Shanghai. Default is "600000".
    
    Returns:
    JSON formatted data containing user focus index information with the following fields:
    - 交易日: Trading day
    - 用户关注指数: User focus index
    
    
    中文: 东方财富网-数据中心-特色数据-千股千评-市场热度-用户关注指数
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场前缀，例如 "600000" 表示上海银行。默认值为 "600000"。
    
    返回:
    JSON格式数据，包含用户关注指数信息，包含以下字段：
    - 交易日: 交易日
    - 用户关注指数: 用户关注指数
    """
    try:
        df = ak.stock_comment_detail_scrd_focus_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_comment_detail_zhpj_lspf_em(symbol: str = "600000") -> str:
    """Get historical score data from East Money's comprehensive stock evaluation.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market prefix, e.g., "600000" for Bank of Shanghai. Default is "600000".
    
    Returns:
    JSON formatted data containing historical score information with the following fields:
    - 日期: Date
    - 评分: Score
    
    
    中文: 东方财富网-数据中心-特色数据-千股千评-综合评价-历史评分
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场前缀，例如 "600000" 表示上海银行。默认值为 "600000"。
    
    返回:
    JSON格式数据，包含历史评分信息，包含以下字段：
    - 日期: 日期
    - 评分: 评分
    """
    try:
        df = ak.stock_comment_detail_zhpj_lspf_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_comment_detail_zlkp_jgcyd_em(symbol: str = "600000") -> str:
    """Get institutional participation data from East Money's main force control panel.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market prefix, e.g., "600000" for Bank of Shanghai. Default is "600000".
    
    Returns:
    JSON formatted data containing institutional participation information with the following fields:
    - 交易日: Trading day
    - 机构参与度: Institutional participation degree (unit: %)
    
    
    中文: 东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场前缀，例如 "600000" 表示上海银行。默认值为 "600000"。
    
    返回:
    JSON格式数据，包含机构参与度信息，包含以下字段：
    - 交易日: 交易日
    - 机构参与度: 机构参与度（单位: %）
    """
    try:
        df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_comment_em() -> str:
    """Get comprehensive stock evaluation data from East Money's data center.
    
    Returns data in JSON format.
    
    This function retrieves all stock evaluation data without any input parameters.
    
    Returns:
    JSON formatted data containing comprehensive stock evaluation information with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Price change percentage
    - 换手率: Turnover rate (unit: %)
    - 市盈率: Price-to-earnings ratio
    - 主力成本: Main force cost
    - 机构参与度: Institutional participation degree
    - 综合得分: Comprehensive score
    - 上升: Rising (note: positive/negative sign)
    - 目前排名: Current ranking
    - 关注指数: Focus index
    - 交易日: Trading day
    
    
    中文: 东方财富网-数据中心-特色数据-千股千评
    
    返回 JSON 格式的数据。
    
    此函数不需要任何输入参数，获取所有股票评价数据。
    
    返回:
    JSON格式数据，包含综合股票评价信息，包含以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅
    - 换手率: 换手率（单位: %）
    - 市盈率: 市盈率
    - 主力成本: 主力成本
    - 机构参与度: 机构参与度
    - 综合得分: 综合得分
    - 上升: 上升（注意: 正负号）
    - 目前排名: 目前排名
    - 关注指数: 关注指数
    - 交易日: 交易日
    """
    try:
        df = ak.stock_comment_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_concept_cons_futu(symbol: str = "特朗普概念股") -> str:
    """Get concept stock constituents from Futu Niuiu's thematic investment section.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Name of the concept board, e.g., "特朗普概念股" (Trump concept stocks). Default is "特朗普概念股".
                 Available options include: "巴菲特持仓" (Buffett holdings), "佩洛西持仓" (Pelosi holdings), "特朗普概念股" (Trump concept stocks).
    
    Returns:
    JSON formatted data containing concept stock constituent information with the following fields:
    - 代码: Stock code
    - 股票名称: Stock name
    - 最新价: Latest price
    - 涨跌额: Price change amount
    - 涨跌幅: Price change percentage
    - 成交量: Trading volume
    - 成交额: Trading amount
    
    
    中文: 富途牛牛-主题投资-概念板块-成分股
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 概念板块名称，例如 "特朗普概念股"。默认值为 "特朗普概念股"。
                 可选值包括："巴菲特持仓"，"佩洛西持仓"，"特朗普概念股"。
    
    返回:
    JSON格式数据，包含概念股票成分股信息，包含以下字段：
    - 代码: 股票代码
    - 股票名称: 股票名称
    - 最新价: 最新价
    - 涨跌额: 涨跌额
    - 涨跌幅: 涨跌幅
    - 成交量: 成交量
    - 成交额: 成交额
    """
    try:
        df = ak.stock_concept_cons_futu(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_concept_fund_flow_hist(symbol: str = "数据要素") -> str:
    """Get historical concept fund flow data from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Name of the concept, e.g., "数据要素" (Data Elements). Default is "数据要素".
    
    Returns:
    JSON formatted data containing historical concept fund flow information with the following fields:
    - 日期: Date
    - 主力净流入-净额: Main force net inflow - net amount
    - 主力净流入-净占比: Main force net inflow - net percentage (unit: %)
    - 超大单净流入-净额: Super large order net inflow - net amount
    - 超大单净流入-净占比: Super large order net inflow - net percentage (unit: %)
    - 大单净流入-净额: Large order net inflow - net amount
    - 大单净流入-净占比: Large order net inflow - net percentage (unit: %)
    - 中单净流入-净额: Medium order net inflow - net amount
    - 中单净流入-净占比: Medium order net inflow - net percentage (unit: %)
    - 小单净流入-净额: Small order net inflow - net amount
    - 小单净流入-净占比: Small order net inflow - net percentage (unit: %)
    
    
    中文: 东方财富网-数据中心-资金流向-概念资金流-概念历史资金流
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 概念名称，例如 "数据要素"。默认值为 "数据要素"。
    
    返回:
    JSON格式数据，包含概念历史资金流信息，包含以下字段：
    - 日期: 日期
    - 主力净流入-净额: 主力净流入-净额
    - 主力净流入-净占比: 主力净流入-净占比（单位: %）
    - 超大单净流入-净额: 超大单净流入-净额
    - 超大单净流入-净占比: 超大单净流入-净占比（单位: %）
    - 大单净流入-净额: 大单净流入-净额
    - 大单净流入-净占比: 大单净流入-净占比（单位: %）
    - 中单净流入-净额: 中单净流入-净额
    - 中单净流入-净占比: 中单净流入-净占比（单位: %）
    - 小单净流入-净额: 小单净流入-净额
    - 小单净流入-净占比: 小单净流入-净占比（单位: %）
    """
    try:
        df = ak.stock_concept_fund_flow_hist(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cy_a_spot_em() -> str:
    """Get real-time quotes for ChiNext (Growth Enterprise Market) stocks from East Money.
    
    Returns data in JSON format.
    
    This function retrieves real-time market data for all ChiNext stocks without any input parameters.
    
    Returns:
    JSON formatted data containing real-time market information for ChiNext stocks with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Price change percentage (unit: %)
    - 涨跌额: Price change amount
    - 成交量: Trading volume (unit: lots)
    - 成交额: Trading amount (unit: CNY)
    - 振幅: Amplitude (unit: %)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Today's opening price
    - 昨收: Yesterday's closing price
    - 量比: Volume ratio
    - 换手率: Turnover rate (unit: %)
    - 市盈率-动态: Price-to-earnings ratio - dynamic
    - 市净率: Price-to-book ratio
    - 总市值: Total market value (unit: CNY)
    - 流通市值: Circulating market value (unit: CNY)
    - 涨速: Rising speed
    - 5分钟涨跌: 5-minute price change (unit: %)
    - 60日涨跌幅: 60-day price change percentage (unit: %)
    - 年初至今涨跌幅: Year-to-date price change percentage (unit: %)
    
    
    中文: 东方财富网-创业板-实时行情
    
    返回 JSON 格式的数据。
    
    此函数不需要任何输入参数，获取所有创业板股票的实时行情数据。
    
    返回:
    JSON格式数据，包含创业板股票的实时行情信息，包含以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅（单位: %）
    - 涨跌额: 涨跌额
    - 成交量: 成交量（单位: 手）
    - 成交额: 成交额（单位: 元）
    - 振幅: 振幅（单位: %）
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 今日开盘价
    - 昨收: 昨日收盘价
    - 量比: 量比
    - 换手率: 换手率（单位: %）
    - 市盈率-动态: 市盈率-动态
    - 市净率: 市净率
    - 总市值: 总市值（单位: 元）
    - 流通市值: 流通市值（单位: 元）
    - 涨速: 涨速
    - 5分钟涨跌: 5分钟涨跌（单位: %）
    - 60日涨跌幅: 60日涨跌幅（单位: %）
    - 年初至今涨跌幅: 年初至今涨跌幅（单位: %）
    """
    try:
        df = ak.stock_cy_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_cyq_em(symbol: str = "000001", adjust: str = "") -> str:
    """Get chip distribution data from East Money's concept board market center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code, e.g., "000001". Default is "000001".
    adjust: str - Price adjustment method. Default is "" (no adjustment).
                  Available options include: "qfq" (forward adjustment), "hfq" (backward adjustment), "" (no adjustment).
    
    Returns:
    JSON formatted data containing chip distribution information with the following fields:
    - 日期: Date
    - 获利比例: Profit ratio
    - 平均成本: Average cost
    - 90成本-低: 90% cost - low
    - 90成本-高: 90% cost - high
    - 90集中度: 90% concentration
    - 70成本-低: 70% cost - low
    - 70成本-高: 70% cost - high
    - 70集中度: 70% concentration
    
    
    中文: 东方财富网-概念板-行情中心-日K-筹码分布
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，例如 "000001"。默认值为 "000001"。
    adjust: str - 价格调整方式。默认值为 ""(不复权)。
                  可选值包括："qfq"(前复权)，"hfq"(后复权)，""(不复权)。
    
    返回:
    JSON格式数据，包含筹码分布信息，包含以下字段：
    - 日期: 日期
    - 获利比例: 获利比例
    - 平均成本: 平均成本
    - 90成本-低: 90成本-低
    - 90成本-高: 90成本-高
    - 90集中度: 90集中度
    - 70成本-低: 70成本-低
    - 70成本-高: 70成本-高
    - 70集中度: 70集中度
    """
    try:
        df = ak.stock_cyq_em(symbol=symbol, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_dxsyl_em() -> str:
    """Get new stock subscription yield data from East Money's data center.
    
    Returns data in JSON format.
    
    This function retrieves new stock subscription yield data without any input parameters.
    
    Returns:
    JSON formatted data containing new stock subscription yield information with the following fields:
    - 股票代码: Stock code
    - 股票简称: Stock abbreviation
    - 发行价: Issue price
    - 最新价: Latest price
    - 网上发行中签率: Online issuance winning rate (unit: %)
    - 网上有效申购股数: Number of valid online subscription shares
    - 网上有效申购户数: Number of valid online subscription accounts (unit: accounts)
    - 网上超额认购倍数: Online oversubscription multiple
    - 网下配售中签率: Offline allocation winning rate (unit: %)
    - 网下有效申购股数: Number of valid offline subscription shares
    - 网下有效申购户数: Number of valid offline subscription accounts (unit: accounts)
    - 网下配售认购倍数: Offline allocation subscription multiple
    - 总发行数量: Total issuance quantity
    - 开盘溢价: Opening premium
    - 首日涨幅: First-day price increase
    - 上市日期: Listing date
    
    
    中文: 东方财富网-数据中心-新股申购-打新收益率
    
    返回 JSON 格式的数据。
    
    此函数不需要任何输入参数，获取所有打新收益率数据。
    
    返回:
    JSON格式数据，包含新股申购收益率信息，包含以下字段：
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 发行价: 发行价
    - 最新价: 最新价
    - 网上发行中签率: 网上发行中签率（单位: %）
    - 网上有效申购股数: 网上有效申购股数
    - 网上有效申购户数: 网上有效申购户数（单位: 户）
    - 网上超额认购倍数: 网上超额认购倍数
    - 网下配售中签率: 网下配售中签率（单位: %）
    - 网下有效申购股数: 网下有效申购股数
    - 网下有效申购户数: 网下有效申购户数（单位: 户）
    - 网下配售认购倍数: 网下配售认购倍数
    - 总发行数量: 总发行数量
    - 开盘溢价: 开盘溢价
    - 首日涨幅: 首日涨幅
    - 上市日期: 上市日期
    """
    try:
        df = ak.stock_dxsyl_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_dzjy_hygtj(symbol: str = "近三月") -> str:
    """Get active A-share statistics for block trades from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Time period for statistics, e.g., "近三月" (last three months). Default is "近三月".
                  Available options include: "近一月" (last month), "近三月" (last three months), 
                  "近六月" (last six months), "近一年" (last year).
    
    Returns:
    JSON formatted data containing active A-share statistics for block trades with the following fields:
    - 序号: Serial number
    - 证券代码: Security code
    - 证券简称: Security abbreviation
    - 最新价: Latest price
    - 涨跌幅: Price change percentage (unit: %)
    - 最近上榜日: Most recent listing date
    - 上榜次数-总计: Number of listings - total
    - 上榜次数-溢价: Number of listings - premium
    - 上榜次数-折价: Number of listings - discount
    - 总成交额: Total transaction amount (unit: 10,000 CNY)
    - 折溢率: Discount premium rate (unit: 10,000 CNY)
    - 成交总额/流通市值: Total transaction amount/circulating market value
    - 上榜日后平均涨跌幅-1日: Average price change after listing - 1 day (unit: %)
    - 上榜日后平均涨跌幅-5日: Average price change after listing - 5 days (unit: %)
    - 上榜日后平均涨跌幅-10日: Average price change after listing - 10 days (unit: %)
    - 上榜日后平均涨跌幅-20日: Average price change after listing - 20 days (unit: %)
    
    
    中文: 东方财富网-数据中心-大宗交易-活跃 A 股统计
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 统计时间周期，例如 "近三月"。默认值为 "近三月"。
                  可选值包括："近一月"，"近三月"，"近六月"，"近一年"。
    
    返回:
    JSON格式数据，包含大宗交易活跃A股统计信息，包含以下字段：
    - 序号: 序号
    - 证券代码: 证券代码
    - 证券简称: 证券简称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅（单位: %）
    - 最近上榜日: 最近上榜日
    - 上榜次数-总计: 上榜次数-总计
    - 上榜次数-溢价: 上榜次数-溢价
    - 上榜次数-折价: 上榜次数-折价
    - 总成交额: 总成交额（单位: 万元）
    - 折溢率: 折溢率（单位: 万元）
    - 成交总额/流通市值: 成交总额/流通市值
    - 上榜日后平均涨跌幅-1日: 上榜日后平均涨跌幅-1日（单位: %）
    - 上榜日后平均涨跌幅-5日: 上榜日后平均涨跌幅-5日（单位: %）
    - 上榜日后平均涨跌幅-10日: 上榜日后平均涨跌幅-10日（单位: %）
    - 上榜日后平均涨跌幅-20日: 上榜日后平均涨跌幅-20日（单位: %）
    """
    try:
        df = ak.stock_dzjy_hygtj(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_dzjy_hyyybtj(symbol: str = "近3日") -> str:
    """Get active brokerage statistics for block trades from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Time period for statistics, e.g., "近3日" (last 3 days). Default is "近3日".
                  Available options include: "当前交易日" (current trading day), "近3日" (last 3 days), 
                  "近5日" (last 5 days), "近10日" (last 10 days), "近30日" (last 30 days).
    
    Returns:
    JSON formatted data containing active brokerage statistics for block trades with the following fields:
    - 序号: Serial number
    - 营业部名称: Brokerage name
    - 最近上榜日: Most recent listing date
    - 次数总计-买入: Total number of times - buying
    - 次数总计-卖出: Total number of times - selling (unit: %)
    - 成交金额统计-买入: Transaction amount statistics - buying (unit: 10,000 CNY)
    - 成交金额统计-卖出: Transaction amount statistics - selling (unit: 10,000 CNY)
    - 成交金额统计-净买入额: Transaction amount statistics - net buying amount (unit: 10,000 CNY)
    - 买入的股票: Stocks bought
    
    
    中文: 东方财富网-数据中心-大宗交易-活跃营业部统计
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 统计时间周期，例如 "近3日"。默认值为 "近3日"。
                  可选值包括："当前交易日"，"近3日"，"近5日"，"近10日"，"近30日"。
    
    返回:
    JSON格式数据，包含大宗交易活跃营业部统计信息，包含以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 最近上榜日: 最近上榜日
    - 次数总计-买入: 次数总计-买入
    - 次数总计-卖出: 次数总计-卖出（单位: %）
    - 成交金额统计-买入: 成交金额统计-买入（单位: 万元）
    - 成交金额统计-卖出: 成交金额统计-卖出（单位: 万元）
    - 成交金额统计-净买入额: 成交金额统计-净买入额（单位: 万元）
    - 买入的股票: 买入的股票
    """
    try:
        df = ak.stock_dzjy_hyyybtj(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_dzjy_mrmx(symbol: str = "A股", start_date: str = "20220104", end_date: str = "20220104") -> str:
    """Get daily details of block trades from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Type of security, e.g., "A股" (A-shares). Default is "A股".
                  Available options include: "A股" (A-shares), "B股" (B-shares), 
                  "基金" (funds), "债券" (bonds).
    start_date: str - Start date for query in format 'YYYYMMDD', e.g., "20220104". Default is "20220104".
    end_date: str - End date for query in format 'YYYYMMDD', e.g., "20220104". Default is "20220104".
    
    Returns:
    JSON formatted data containing daily details of block trades with the following fields (for A-shares):
    - 序号: Serial number
    - 交易日期: Trading date
    - 证券代码: Security code
    - 证券简称: Security abbreviation
    - 涨跌幅: Price change percentage (unit: %)
    - 收盘价: Closing price
    - 成交价: Transaction price
    - 折溢率: Discount premium rate
    - 成交量: Transaction volume (unit: shares)
    - 成交额: Transaction amount (unit: CNY)
    - 成交额/流通市值: Transaction amount/circulating market value (unit: %)
    - 买方营业部: Buyer's brokerage
    - 卖方营业部: Seller's brokerage
    
    
    中文: 东方财富网-数据中心-大宗交易-每日明细
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 证券类型，例如 "A股"。默认值为 "A股"。
                  可选值包括："A股"，"B股"，"基金"，"债券"。
    start_date: str - 查询开始日期，格式为 'YYYYMMDD'，例如 "20220104"。默认值为 "20220104"。
    end_date: str - 查询结束日期，格式为 'YYYYMMDD'，例如 "20220104"。默认值为 "20220104"。
    
    返回:
    JSON格式数据，包含大宗交易每日明细信息（对于A股），包含以下字段：
    - 序号: 序号
    - 交易日期: 交易日期
    - 证券代码: 证券代码
    - 证券简称: 证券简称
    - 涨跌幅: 涨跌幅（单位: %）
    - 收盘价: 收盘价
    - 成交价: 成交价
    - 折溢率: 折溢率
    - 成交量: 成交量（单位: 股）
    - 成交额: 成交额（单位: 元）
    - 成交额/流通市值: 成交额/流通市值（单位: %）
    - 买方营业部: 买方营业部
    - 卖方营业部: 卖方营业部
    """
    try:
        df = ak.stock_dzjy_mrmx(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_dzjy_mrtj(start_date: str = "20220105", end_date: str = "20220105") -> str:
    """Get daily statistics of block trades from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    start_date: str - Start date for query in format 'YYYYMMDD', e.g., "20220105". Default is "20220105".
    end_date: str - End date for query in format 'YYYYMMDD', e.g., "20220105". Default is "20220105".
    
    Returns:
    JSON formatted data containing daily statistics of block trades with the following fields:
    - 序号: Serial number
    - 交易日期: Trading date
    - 证券代码: Security code
    - 证券简称: Security abbreviation
    - 涨跌幅: Price change percentage (unit: %)
    - 收盘价: Closing price
    - 成交均价: Average transaction price
    - 折溢率: Discount premium rate
    - 成交笔数: Number of transactions
    - 成交总量: Total transaction volume (unit: 10,000 shares)
    - 成交总额: Total transaction amount (unit: 10,000 CNY)
    - 成交总额/流通市值: Total transaction amount/circulating market value (unit: %)
    
    
    中文: 东方财富网-数据中心-大宗交易-每日统计
    
    返回 JSON 格式的数据。
    
    参数:
    start_date: str - 查询开始日期，格式为 'YYYYMMDD'，例如 "20220105"。默认值为 "20220105"。
    end_date: str - 查询结束日期，格式为 'YYYYMMDD'，例如 "20220105"。默认值为 "20220105"。
    
    返回:
    JSON格式数据，包含大宗交易每日统计信息，包含以下字段：
    - 序号: 序号
    - 交易日期: 交易日期
    - 证券代码: 证券代码
    - 证券简称: 证券简称
    - 涨跌幅: 涨跌幅（单位: %）
    - 收盘价: 收盘价
    - 成交均价: 成交均价
    - 折溢率: 折溢率
    - 成交笔数: 成交笔数
    - 成交总量: 成交总量（单位: 万股）
    - 成交总额: 成交总额（单位: 万元）
    - 成交总额/流通市值: 成交总额/流通市值（单位: %）
    """
    try:
        df = ak.stock_dzjy_mrtj(start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_dzjy_sctj() -> str:
    """Get market statistics of block trades from East Money's data center.
    
    Returns data in JSON format.
    
    This function does not require any input parameters and retrieves all historical market statistics data for block trades.
    
    Returns:
    JSON formatted data containing market statistics of block trades with the following fields:
    - 序号: Serial number
    - 交易日期: Trading date
    - 上证指数: Shanghai Stock Exchange Index
    - 上证指数涨跌幅: Shanghai Stock Exchange Index change percentage (unit: %)
    - 大宗交易成交总额: Total transaction amount of block trades (unit: CNY)
    - 溢价成交总额: Total premium transaction amount (unit: CNY)
    - 溢价成交总额占比: Percentage of premium transaction amount (unit: %)
    - 折价成交总额: Total discount transaction amount (unit: CNY)
    - 折价成交总额占比: Percentage of discount transaction amount (unit: %)
    
    
    中文: 东方财富网-数据中心-大宗交易-市场统计
    
    返回 JSON 格式的数据。
    
    此函数不需要任何输入参数，获取所有历史大宗交易市场统计数据。
    
    返回:
    JSON格式数据，包含大宗交易市场统计信息，包含以下字段：
    - 序号: 序号
    - 交易日期: 交易日期
    - 上证指数: 上证指数
    - 上证指数涨跌幅: 上证指数涨跌幅（单位: %）
    - 大宗交易成交总额: 大宗交易成交总额（单位: 元）
    - 溢价成交总额: 溢价成交总额（单位: 元）
    - 溢价成交总额占比: 溢价成交总额占比（单位: %）
    - 折价成交总额: 折价成交总额（单位: 元）
    - 折价成交总额占比: 折价成交总额占比（单位: %）
    """
    try:
        df = ak.stock_dzjy_sctj()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_dzjy_yybph(symbol: str = "近三月") -> str:
    """Get brokerage rankings for block trades from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Time period for statistics, e.g., "近三月" (last three months). Default is "近三月".
                  Available options include: "近一月" (last month), "近三月" (last three months), 
                  "近六月" (last six months), "近一年" (last year).
    
    Returns:
    JSON formatted data containing brokerage rankings for block trades with the following fields:
    - 序号: Serial number
    - 营业部名称: Brokerage name
    - 上榜后1天-买入次数: Number of purchases after listing - 1 day
    - 上榜后1天-平均涨幅: Average price increase after listing - 1 day (unit: %)
    - 上榜后1天-上涨概率: Probability of price increase after listing - 1 day
    - 上榜后5天-买入次数: Number of purchases after listing - 5 days
    - 上榜后5天-平均涨幅: Average price increase after listing - 5 days (unit: %)
    - 上榜后5天-上涨概率: Probability of price increase after listing - 5 days
    - 上榜后10天-买入次数: Number of purchases after listing - 10 days
    - 上榜后10天-平均涨幅: Average price increase after listing - 10 days (unit: %)
    - 上榜后10天-上涨概率: Probability of price increase after listing - 10 days
    - 上榜后20天-买入次数: Number of purchases after listing - 20 days
    - 上榜后20天-平均涨幅: Average price increase after listing - 20 days (unit: %)
    - 上榜后20天-上涨概率: Probability of price increase after listing - 20 days
    
    
    中文: 东方财富网-数据中心-大宗交易-营业部排行
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 统计时间周期，例如 "近三月"。默认值为 "近三月"。
                  可选值包括："近一月"，"近三月"，"近六月"，"近一年"。
    
    返回:
    JSON格式数据，包含大宗交易营业部排行信息，包含以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 上榜后1天-买入次数: 上榜后1天-买入次数
    - 上榜后1天-平均涨幅: 上榜后1天-平均涨幅（单位: %）
    - 上榜后1天-上涨概率: 上榜后1天-上涨概率
    - 上榜后5天-买入次数: 上榜后5天-买入次数
    - 上榜后5天-平均涨幅: 上榜后5天-平均涨幅（单位: %）
    - 上榜后5天-上涨概率: 上榜后5天-上涨概率
    - 上榜后10天-买入次数: 上榜后10天-买入次数
    - 上榜后10天-平均涨幅: 上榜后10天-平均涨幅（单位: %）
    - 上榜后10天-上涨概率: 上榜后10天-上涨概率
    - 上榜后20天-买入次数: 上榜后20天-买入次数
    - 上榜后20天-平均涨幅: 上榜后20天-平均涨幅（单位: %）
    - 上榜后20天-上涨概率: 上榜后20天-上涨概率
    """
    try:
        df = ak.stock_dzjy_yybph(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_ebs_lg() -> str:
    """Get equity-bond spread data from LeGuLeGu.
    
    Returns data in JSON format.
    
    This function retrieves historical equity-bond spread data. The equity-bond spread is the difference between the earnings yield of stocks and the yield of bonds, which is an important indicator for asset allocation between stocks and bonds.
    
    This function does not require any input parameters and retrieves all historical data.
    
    Returns:
    JSON formatted data containing equity-bond spread information with the following fields:
    - 日期: Date
    - 沪深300指数: CSI 300 Index
    - 股债利差: Equity-bond spread
    - 股债利差均线: Moving average of equity-bond spread
    
    
    中文: 乐咕乐股-股债利差
    
    返回 JSON 格式的数据。
    
    此函数获取历史股债利差数据。股债利差是股票收益率与债券收益率之间的差异，是股票与债券资产配置的重要指标。
    
    此函数不需要任何输入参数，获取所有历史数据。
    
    返回:
    JSON格式数据，包含股债利差信息，包含以下字段：
    - 日期: 日期
    - 沪深300指数: 沪深300指数
    - 股债利差: 股债利差
    - 股债利差均线: 股债利差均线
    """
    try:
        df = ak.stock_ebs_lg()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_esg_hz_sina() -> str:
    """Get ESG ratings from Sina Finance's ESG Rating Center - Huazheng Index.
    
    Returns data in JSON format.
    
    This function retrieves ESG (Environmental, Social, and Governance) ratings data from Sina Finance's ESG Rating Center, specifically the Huazheng Index ratings. ESG ratings evaluate companies based on their environmental impact, social responsibility, and corporate governance practices.
    
    This function does not require any input parameters and retrieves all available data.
    
    Returns:
    JSON formatted data containing ESG ratings with the following fields:
    - 日期: Date
    - 股票代码: Stock code
    - 交易市场: Trading market
    - 股票名称: Stock name
    - ESG评分: ESG score
    - ESG等级: ESG rating
    - 环境: Environmental score
    - 环境等级: Environmental rating
    - 社会: Social score
    - 社会等级: Social rating
    - 公司治理: Governance score
    - 公司治理等级: Governance rating
    
    
    中文: 新浪财经-ESG评级中心-ESG评级-华证指数
    
    返回 JSON 格式的数据。
    
    此函数获取新浪财经 ESG 评级中心的 ESG（环境、社会和公司治理）评级数据，特别是华证指数评级。ESG 评级基于公司的环境影响、社会责任和公司治理实践进行评估。
    
    此函数不需要任何输入参数，获取所有可用数据。
    
    返回:
    JSON格式数据，包含 ESG 评级信息，包含以下字段：
    - 日期: 日期
    - 股票代码: 股票代码
    - 交易市场: 交易市场
    - 股票名称: 股票名称
    - ESG评分: ESG评分
    - ESG等级: ESG等级
    - 环境: 环境评分
    - 环境等级: 环境等级
    - 社会: 社会评分
    - 社会等级: 社会等级
    - 公司治理: 公司治理评分
    - 公司治理等级: 公司治理等级
    """
    try:
        df = ak.stock_esg_hz_sina()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_esg_msci_sina() -> str:
    """Get 新浪财经-ESG评级中心-ESG评级-MSCI
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-ESG评级中心-ESG评级-MSCI
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_esg_msci_sina()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_esg_rate_sina() -> str:
    """Get 新浪财经-ESG评级中心-ESG评级-ESG评级数据
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-ESG评级中心-ESG评级-ESG评级数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_esg_rate_sina()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_esg_rft_sina() -> str:
    """Get 新浪财经-ESG评级中心-ESG评级-路孚特
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-ESG评级中心-ESG评级-路孚特
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_esg_rft_sina()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_esg_zd_sina() -> str:
    """Get 新浪财经-ESG评级中心-ESG评级-秩鼎
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-ESG评级中心-ESG评级-秩鼎
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_esg_zd_sina()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fhps_detail_em(symbol: str = "300073") -> str:
    """Get 东方财富网-数据中心-分红送配-分红送配详情
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-分红送配-分红送配详情
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_fhps_detail_em(symbol="300073")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fhps_detail_ths(symbol: str = "603444") -> str:
    """Get 同花顺-分红情况
    
    Returns data in JSON format.
    
    
    中文: 同花顺-分红情况
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_fhps_detail_ths(symbol="603444")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fhps_em(date: str = "20231231") -> str:
    """Get 东方财富-数据中心-年报季报-分红配送
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-分红配送
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_fhps_em(date="20231231")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_abstract(symbol: str = "600004") -> str:
    """Get 新浪财经-财务报表-关键指标
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-财务报表-关键指标
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_abstract(symbol="600004")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_abstract_ths(symbol: str = "000063", indicator: str = "按报告期") -> str:
    """Get 同花顺-财务指标-主要指标
    
    Returns data in JSON format.
    
    
    中文: 同花顺-财务指标-主要指标
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_abstract_ths(symbol="000063", indicator="按报告期")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_benefit_ths(symbol: str = "000063", indicator: str = "按报告期") -> str:
    """Get 同花顺-财务指标-利润表
    
    Returns data in JSON format.
    
    
    中文: 同花顺-财务指标-利润表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_benefit_ths(symbol="000063", indicator="按报告期")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_cash_ths(symbol: str = "000063", indicator: str = "按单季度") -> str:
    """Get 同花顺-财务指标-现金流量表
    
    Returns data in JSON format.
    
    
    中文: 同花顺-财务指标-现金流量表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_cash_ths(symbol="000063", indicator="按单季度")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_debt_ths(symbol: str = "000063", indicator: str = "按年度") -> str:
    """Get 同花顺-财务指标-资产负债表
    
    Returns data in JSON format.
    
    
    中文: 同花顺-财务指标-资产负债表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_debt_ths(symbol="000063", indicator="按年度")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_hk_analysis_indicator_em(symbol: str = "00700", indicator: str = "年度") -> str:
    """Get 东方财富-港股-财务分析-主要指标
    
    Returns data in JSON format.
    
    
    中文: 东方财富-港股-财务分析-主要指标
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_hk_analysis_indicator_em(symbol="00700", indicator="年度")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_hk_report_em(stock: str = "00700", symbol: str = "资产负债表", indicator: str = "年度") -> str:
    """Get 东方财富-港股-财务报表-三大报表
    
    Returns data in JSON format.
    
    
    中文: 东方财富-港股-财务报表-三大报表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_hk_report_em(stock="00700", symbol="资产负债表", indicator="年度")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_report_sina(stock: str = "sh600600", symbol: str = "资产负债表") -> str:
    """Get 新浪财经-财务报表-三大报表
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-财务报表-三大报表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_report_sina(stock="sh600600", symbol="资产负债表")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_us_analysis_indicator_em(symbol: str = "TSLA", indicator: str = "年报") -> str:
    """Get 东方财富-美股-财务分析-主要指标
    
    Returns data in JSON format.
    
    
    中文: 东方财富-美股-财务分析-主要指标
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_us_analysis_indicator_em(symbol="TSLA", indicator="年报")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_financial_us_report_em(stock: str = "TSLA", symbol: str = "资产负债表", indicator: str = "年报") -> str:
    """Get 东方财富-美股-财务分析-三大报表
    
    Returns data in JSON format.
    
    
    中文: 东方财富-美股-财务分析-三大报表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_financial_us_report_em(stock="TSLA", symbol="资产负债表", indicator="年报")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fund_flow_big_deal() -> str:
    """Get big deal tracking data from TongHuaShun data center.
    
    Returns data in JSON format.
    
    This function retrieves the current big deal tracking data from TongHuaShun data center.
    A big deal refers to a large volume transaction in the stock market.
    
    Returns:
    JSON formatted data containing big deal tracking information with the following fields:
    - 成交时间: Transaction time
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 成交价格: Transaction price
    - 成交量: Transaction volume (unit: shares)
    - 成交额: Transaction amount (unit: 10,000 CNY)
    - 大单性质: Big deal nature
    - 涨跌幅: Change percentage
    - 涨跌额: Change amount
    
    
    中文: 同花顺-数据中心-资金流向-大单追踪
    
    返回 JSON 格式的数据。
    
    此函数从同花顺数据中心获取当前的大单追踪数据。
    大单指的是股票市场中的大量交易。
    
    返回:
    JSON格式数据，包含大单追踪信息，具有以下字段：
    - 成交时间: 成交时间
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 成交价格: 成交价格
    - 成交量: 成交量（单位: 股）
    - 成交额: 成交额（单位: 万元）
    - 大单性质: 大单性质
    - 涨跌幅: 涨跌幅
    - 涨跌额: 涨跌额
    """
    try:
        df = ak.stock_fund_flow_big_deal()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fund_flow_concept(symbol: str = "即时") -> str:
    """Get concept fund flow data from TongHuaShun data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Time period for the fund flow data. Default is "即时" (real-time).
                  Available options include: "即时" (real-time), "3日排行" (3-day ranking), 
                  "5日排行" (5-day ranking), "10日排行" (10-day ranking), "20日排行" (20-day ranking).
    
    Returns:
    JSON formatted data containing concept fund flow information with different fields based on the selected time period:
    
    For "即时" (real-time):
    - 序号: Serial number
    - 行业: Industry/Concept
    - 行业指数: Industry index
    - 行业-涨跌幅: Industry change percentage (unit: %)
    - 流入资金: Capital inflow (unit: 100 million CNY)
    - 流出资金: Capital outflow (unit: 100 million CNY)
    - 净额: Net amount (unit: 100 million CNY)
    - 公司家数: Number of companies
    - 领涨股: Leading stock
    - 领涨股-涨跌幅: Leading stock change percentage (unit: %)
    - 当前价: Current price (unit: CNY)
    
    For "3日排行", "5日排行", "10日排行", and "20日排行":
    - 序号: Serial number
    - 行业: Industry/Concept
    - 公司家数: Number of companies
    - 行业指数: Industry index
    - 阶段涨跌幅: Period change percentage (unit: %)
    - 流入资金: Capital inflow (unit: 100 million CNY)
    - 流出资金: Capital outflow (unit: 100 million CNY)
    - 净额: Net amount (unit: 100 million CNY)
    
    
    中文: 同花顺-数据中心-资金流向-概念资金流
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 资金流向数据的时间周期。默认值为 "即时"。
                  可选值包括："即时"，"3日排行"，"5日排行"，"10日排行"，"20日排行"。
    
    返回:
    JSON格式数据，包含概念资金流向信息，根据选择的时间周期有不同的字段：
    
    对于 "即时":
    - 序号: 序号
    - 行业: 行业/概念
    - 行业指数: 行业指数
    - 行业-涨跌幅: 行业涨跌幅（单位: %）
    - 流入资金: 流入资金（单位: 亿）
    - 流出资金: 流出资金（单位: 亿）
    - 净额: 净额（单位: 亿）
    - 公司家数: 公司家数
    - 领涨股: 领涨股
    - 领涨股-涨跌幅: 领涨股涨跌幅（单位: %）
    - 当前价: 当前价（单位: 元）
    
    对于 "3日排行", "5日排行", "10日排行", 和 "20日排行":
    - 序号: 序号
    - 行业: 行业/概念
    - 公司家数: 公司家数
    - 行业指数: 行业指数
    - 阶段涨跌幅: 阶段涨跌幅（单位: %）
    - 流入资金: 流入资金（单位: 亿）
    - 流出资金: 流出资金（单位: 亿）
    - 净额: 净额（单位: 亿）
    """
    try:
        df = ak.stock_fund_flow_concept(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fund_flow_individual(symbol: str = "即时") -> str:
    """Get individual stock fund flow data from TongHuaShun data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Time period for the fund flow data. Default is "即时" (real-time).
                  Available options include: "即时" (real-time), "3日排行" (3-day ranking), 
                  "5日排行" (5-day ranking), "10日排行" (10-day ranking), "20日排行" (20-day ranking).
    
    Returns:
    JSON formatted data containing individual stock fund flow information with different fields based on the selected time period:
    
    For "即时" (real-time):
    - 序号: Serial number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (unit: %)
    - 换手率: Turnover rate
    - 流入资金: Capital inflow (unit: CNY)
    - 流出资金: Capital outflow (unit: CNY)
    - 净额: Net amount (unit: CNY)
    - 成交额: Transaction amount (unit: CNY)
    
    For "3日排行", "5日排行", "10日排行", and "20日排行":
    - 序号: Serial number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 最新价: Latest price
    - 阶段涨跌幅: Period change percentage (unit: %)
    - 连续换手率: Continuous turnover rate (unit: %)
    - 资金流入净额: Net capital inflow (unit: CNY)
    
    
    中文: 同花顺-数据中心-资金流向-个股资金流
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 资金流向数据的时间周期。默认值为 "即时"。
                  可选值包括："即时"，"3日排行"，"5日排行"，"10日排行"，"20日排行"。
    
    返回:
    JSON格式数据，包含个股资金流向信息，根据选择的时间周期有不同的字段：
    
    对于 "即时":
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅（单位: %）
    - 换手率: 换手率
    - 流入资金: 流入资金（单位: 元）
    - 流出资金: 流出资金（单位: 元）
    - 净额: 净额（单位: 元）
    - 成交额: 成交额（单位: 元）
    
    对于 "3日排行", "5日排行", "10日排行", 和 "20日排行":
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 最新价: 最新价
    - 阶段涨跌幅: 阶段涨跌幅（单位: %）
    - 连续换手率: 连续换手率（单位: %）
    - 资金流入净额: 资金流入净额（单位: 元）
    """
    try:
        df = ak.stock_fund_flow_individual(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fund_flow_industry(symbol: str = "即时") -> str:
    """Get industry fund flow data from TongHuaShun data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Time period for the fund flow data. Default is "即时" (real-time).
                  Available options include: "即时" (real-time), "3日排行" (3-day ranking), 
                  "5日排行" (5-day ranking), "10日排行" (10-day ranking), "20日排行" (20-day ranking).
    
    Returns:
    JSON formatted data containing industry fund flow information with different fields based on the selected time period:
    
    For "即时" (real-time):
    - 序号: Serial number
    - 行业: Industry
    - 行业指数: Industry index
    - 行业-涨跌幅: Industry change percentage (unit: %)
    - 流入资金: Capital inflow (unit: 100 million CNY)
    - 流出资金: Capital outflow (unit: 100 million CNY)
    - 净额: Net amount (unit: 100 million CNY)
    - 公司家数: Number of companies
    - 领涨股: Leading stock
    - 领涨股-涨跌幅: Leading stock change percentage (unit: %)
    - 当前价: Current price (unit: CNY)
    
    For "3日排行", "5日排行", "10日排行", and "20日排行":
    - 序号: Serial number
    - 行业: Industry
    - 公司家数: Number of companies
    - 行业指数: Industry index
    - 阶段涨跌幅: Period change percentage (unit: %)
    - 流入资金: Capital inflow (unit: 100 million CNY)
    - 流出资金: Capital outflow (unit: 100 million CNY)
    - 净额: Net amount (unit: 100 million CNY)
    
    
    中文: 同花顺-数据中心-资金流向-行业资金流
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 资金流向数据的时间周期。默认值为 "即时"。
                  可选值包括："即时"，"3日排行"，"5日排行"，"10日排行"，"20日排行"。
    
    返回:
    JSON格式数据，包含行业资金流向信息，根据选择的时间周期有不同的字段：
    
    对于 "即时":
    - 序号: 序号
    - 行业: 行业
    - 行业指数: 行业指数
    - 行业-涨跌幅: 行业涨跌幅（单位: %）
    - 流入资金: 流入资金（单位: 亿）
    - 流出资金: 流出资金（单位: 亿）
    - 净额: 净额（单位: 亿）
    - 公司家数: 公司家数
    - 领涨股: 领涨股
    - 领涨股-涨跌幅: 领涨股涨跌幅（单位: %）
    - 当前价: 当前价（单位: 元）
    
    对于 "3日排行", "5日排行", "10日排行", 和 "20日排行":
    - 序号: 序号
    - 行业: 行业
    - 公司家数: 公司家数
    - 行业指数: 行业指数
    - 阶段涨跌幅: 阶段涨跌幅（单位: %）
    - 流入资金: 流入资金（单位: 亿）
    - 流出资金: 流出资金（单位: 亿）
    - 净额: 净额（单位: 亿）
    """
    try:
        df = ak.stock_fund_flow_industry(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_fund_stock_holder(symbol: str = "601318") -> str:
    """Get 新浪财经-股本股东-基金持股
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-股本股东-基金持股
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_fund_stock_holder(symbol="601318")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gddh_em() -> str:
    """Get 东方财富网-数据中心-股东大会
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东大会
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gddh_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_free_holding_analyse_em(date: str = "20230930") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股分析-十大流通股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股分析-十大流通股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_free_holding_analyse_em(date="20230930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_free_holding_change_em(date: str = "20210930") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股变动统计-十大流通股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股变动统计-十大流通股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_free_holding_change_em(date="20210930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_free_holding_detail_em(date: str = "20210930") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股明细-十大流通股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股明细-十大流通股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_free_holding_detail_em(date="20210930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_free_holding_statistics_em(date: str = "20210930") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股统计-十大股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股统计-十大股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_free_holding_statistics_em(date="20210930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_free_holding_teamwork_em(symbol: str = "社保") -> str:
    """Get 东方财富网-数据中心-股东分析-股东协同-十大流通股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东协同-十大流通股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_free_holding_teamwork_em(symbol="社保")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_free_top_10_em(symbol: str = "sh688686", date: str = "20240930") -> str:
    """Get 东方财富网-个股-十大流通股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-个股-十大流通股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_free_top_10_em(symbol="sh688686", date="20240930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_holding_analyse_em(date: str = "20210930") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股分析-十大股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股分析-十大股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_holding_analyse_em(date="20210930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_holding_change_em(date: str = "20210930") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股变动统计-十大股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股变动统计-十大股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_holding_change_em(date="20210930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_holding_detail_em(date: str = "20230331", indicator: str = "个人", symbol: str = "新进") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股明细-十大股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股明细-十大股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_holding_detail_em(date="20230331", indicator="个人", symbol="新进")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_holding_statistics_em(date: str = "20210930") -> str:
    """Get 东方财富网-数据中心-股东分析-股东持股统计-十大股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东持股统计-十大股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_holding_statistics_em(date="20210930")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_holding_teamwork_em(symbol: str = "社保") -> str:
    """Get 东方财富网-数据中心-股东分析-股东协同-十大股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股东分析-股东协同-十大股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_holding_teamwork_em(symbol="社保")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gdfx_top_10_em(symbol: str = "sh688686", date: str = "20210630") -> str:
    """Get 东方财富网-个股-十大股东
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-个股-十大股东
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gdfx_top_10_em(symbol="sh688686", date="20210630")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_ggcg_em(symbol: str = "全部") -> str:
    """Get 东方财富网-数据中心-特色数据-高管持股
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-高管持股
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_ggcg_em(symbol="全部")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gpzy_distribute_statistics_bank_em() -> str:
    """Get 东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gpzy_distribute_statistics_bank_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gpzy_distribute_statistics_company_em() -> str:
    """Get 东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gpzy_distribute_statistics_company_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gpzy_industry_data_em() -> str:
    """Get 东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gpzy_industry_data_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gpzy_pledge_ratio_detail_em() -> str:
    """Get 东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gpzy_pledge_ratio_detail_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gpzy_pledge_ratio_em(date: str = "20241220") -> str:
    """Get 东方财富网-数据中心-特色数据-股权质押-上市公司质押比例
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股权质押-上市公司质押比例
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gpzy_pledge_ratio_em(date="20241220")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gpzy_profile_em() -> str:
    """Get 东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gpzy_profile_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_gsrl_gsdt_em(date: str = "20230808") -> str:
    """Get 东方财富网-数据中心-股市日历-公司动态
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-股市日历-公司动态
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_gsrl_gsdt_em(date="20230808")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_history_dividend() -> str:
    """Get 新浪财经-发行与分配-历史分红
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-发行与分配-历史分红
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_history_dividend()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_history_dividend_detail(symbol: str = "600012", indicator: str = "分红") -> str:
    """Get 新浪财经-发行与分配-分红配股
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-发行与分配-分红配股
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_history_dividend_detail(symbol="600012", indicator="分红")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_fhpx_detail_ths(symbol: str = "0700") -> str:
    """Get 同花顺-港股-分红派息
    
    Returns data in JSON format.
    
    
    中文: 同花顺-港股-分红派息
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_fhpx_detail_ths(symbol="0700")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_ggt_components_em() -> str:
    """Get 东方财富网-行情中心-港股市场-港股通成份股
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-港股市场-港股通成份股
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_ggt_components_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_gxl_lg() -> str:
    """Get 乐咕乐股-股息率-恒生指数股息率
    
    Returns data in JSON format.
    
    
    中文: 乐咕乐股-股息率-恒生指数股息率
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_gxl_lg()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_hist(symbol: str = "01611", period: str = "daily", adjust: str = "", start_date: str = "1979-09-01 09:32:00", end_date: str = "2222-01-01 09:32:00") -> str:
    """Get 东方财富网-行情首页-港股-每日分时行情
    
    Returns data in JSON format.
    
    
    中文: 港股-历史行情数据, 可以选择返回复权后数据, 更新频率为日频
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_hist()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_hist_min_em(symbol: str = "01611", period: str = "1", adjust: str = "", start_date: str = "1979-09-01 09:32:00", end_date: str = "2222-01-01 09:32:00") -> str:
    """Get 东方财富网-行情首页-港股-每日分时行情
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情首页-港股-每日分时行情
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_hist_min_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_hot_rank_detail_em(symbol: str = "00700") -> str:
    """Get 东方财富网-股票热度-历史趋势
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-股票热度-历史趋势
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_hot_rank_detail_em(symbol="00700")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_hot_rank_detail_realtime_em(symbol: str = "00700") -> str:
    """Get 东方财富网-个股人气榜-实时变动
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-个股人气榜-实时变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_hot_rank_detail_realtime_em(symbol="00700")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_hot_rank_em() -> str:
    """Get 东方财富-个股人气榜-人气榜-港股市场
    
    Returns data in JSON format.
    
    
    中文: 东方财富-个股人气榜-人气榜-港股市场
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_hot_rank_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_hot_rank_latest_em(symbol: str = "00700") -> str:
    """Get 东方财富-个股人气榜-最新排名
    
    Returns data in JSON format.
    
    
    中文: 东方财富-个股人气榜-最新排名
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_hot_rank_latest_em(symbol="00700")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_indicator_eniu(symbol: str = "hk01093", indicator: str = "市净率") -> str:
    """Get 亿牛网-港股个股指标: 市盈率, 市净率, 股息率, ROE, 市值
    
    Returns data in JSON format.
    
    
    中文: 亿牛网-港股个股指标: 市盈率, 市净率, 股息率, ROE, 市值
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_indicator_eniu(symbol="hk01093", indicator="市净率")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_main_board_spot_em() -> str:
    """Get 港股主板的实时行情数据; 该数据有 15 分钟延时
    
    Returns data in JSON format.
    
    
    中文: 港股主板的实时行情数据; 该数据有 15 分钟延时
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_main_board_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_profit_forecast_et(symbol: str = "00700") -> str:
    """Get 经济通-公司资料-盈利预测
    
    Returns data in JSON format.
    
    
    中文: 经济通-公司资料-盈利预测
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_profit_forecast_et(symbol="09999", indicator="盈利预测概览")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_spot() -> str:
    """Get 所有港股的实时行情数据; 该数据有 15 分钟延时
    
    Returns data in JSON format.
    
    
    中文: 获取所有港股的实时行情数据 15 分钟延时
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_spot()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hk_valuation_baidu(symbol: str = "06969", indicator: str = "总市值", period: str = "近一年") -> str:
    """Get 百度股市通-港股-财务报表-估值数据
    
    Returns data in JSON format.
    
    
    中文: 百度股市通-港股-财务报表-估值数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hk_valuation_baidu(symbol="06969", indicator="总市值", period="近一年")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hold_change_cninfo(symbol: str = "全部") -> str:
    """Get 巨潮资讯-数据中心-专题统计-股东股本-股本变动
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-数据中心-专题统计-股东股本-股本变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hold_change_cninfo(symbol="全部")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hold_control_cninfo(symbol: str = "全部") -> str:
    """Get 巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hold_control_cninfo(symbol="全部")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hold_management_detail_cninfo(symbol: str = "增持") -> str:
    """Get 巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hold_management_detail_cninfo(symbol="增持")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hold_management_detail_em() -> str:
    """Get 东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hold_management_detail_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hold_management_person_em(symbol: str = "001308", name: str = "孙建华") -> str:
    """Get 东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hold_management_person_em(symbol="001308", name="孙建华")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hold_num_cninfo(date: str = "20210630") -> str:
    """Get 巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hold_num_cninfo(date="20210630")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_deal_xq(symbol: str = "最热门") -> str:
    """Get 雪球-沪深股市-热度排行榜-交易排行榜
    
    Returns data in JSON format.
    
    
    中文: 雪球-沪深股市-热度排行榜-交易排行榜
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_deal_xq(symbol="最热门")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_follow_xq(symbol: str = "最热门") -> str:
    """Get 雪球-沪深股市-热度排行榜-关注排行榜
    
    Returns data in JSON format.
    
    
    中文: 雪球-沪深股市-热度排行榜-关注排行榜
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_follow_xq(symbol="最热门")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_keyword_em(symbol: str = "SZ000665") -> str:
    """Get 东方财富-个股人气榜-热门关键词
    
    Returns data in JSON format.
    
    
    中文: 东方财富-个股人气榜-热门关键词
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_keyword_em(symbol="SZ000665")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_rank_detail_em(symbol: str = "SZ000665") -> str:
    """Get 东方财富网-股票热度-历史趋势及粉丝特征
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-股票热度-历史趋势及粉丝特征
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_rank_detail_em(symbol="SZ000665")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_rank_detail_realtime_em(symbol: str = "SZ000665") -> str:
    """Get 东方财富网-个股人气榜-实时变动
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-个股人气榜-实时变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_rank_detail_realtime_em(symbol="SZ000665")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_rank_em() -> str:
    """Get 东方财富网站-股票热度
    
    Returns data in JSON format.
    
    
    中文: 东方财富网站-股票热度
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_rank_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_rank_latest_em(symbol: str = "SZ000665") -> str:
    """Get 东方财富-个股人气榜-最新排名
    
    Returns data in JSON format.
    
    
    中文: 东方财富-个股人气榜-最新排名
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_rank_latest_em(symbol="SZ000665")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_rank_relate_em(symbol: str = "SZ000665") -> str:
    """Get 东方财富-个股人气榜-相关股票
    
    Returns data in JSON format.
    
    
    中文: 东方财富-个股人气榜-相关股票
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_rank_relate_em(symbol="SZ000665")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_rank_wc(date: str = "20240920") -> str:
    """Get 问财-热门股票排名数据; 请注意访问的频率
    
    Returns data in JSON format.
    
    
    中文: 问财-热门股票排名数据; 请注意访问的频率
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_rank_wc(date="20240920")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_search_baidu(symbol: str = "A股", date: str = "20240929", time: str = "今日") -> str:
    """Get 百度股市通-热搜股票
    
    Returns data in JSON format.
    
    
    中文: 百度股市通-热搜股票
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_search_baidu(symbol="A股", date="20240929", time="今日")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_tweet_xq(symbol: str = "最热门") -> str:
    """Get 雪球-沪深股市-热度排行榜-讨论排行榜
    
    Returns data in JSON format.
    
    
    中文: 雪球-沪深股市-热度排行榜-讨论排行榜
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_tweet_xq(symbol="最热门")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hot_up_em() -> str:
    """Get 东方财富-个股人气榜-飙升榜
    
    Returns data in JSON format.
    
    
    中文: 东方财富-个股人气榜-飙升榜
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hot_up_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_board_rank_em(symbol: str = "北向资金增持行业板块排行", indicator: str = "今日") -> str:
    """Get sector ranking data for Shanghai-Shenzhen-Hong Kong Stock Connect holdings from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The type of sector ranking to query. Default is "北向资金增持行业板块排行" (Northbound funds increased industry sector ranking).
                  Available options include: "北向资金增持行业板块排行" (Northbound funds increased industry sector ranking),
                  "北向资金增持概念板块排行" (Northbound funds increased concept sector ranking),
                  "北向资金增持地域板块排行" (Northbound funds increased regional sector ranking).
    
    indicator: str - Time period for the ranking. Default is "今日" (Today).
                     Available options include: "今日" (Today), "3日" (3 days), "5日" (5 days),
                     "10日" (10 days), "1月" (1 month), "1季" (1 quarter), "1年" (1 year).
    
    Returns:
    JSON formatted data containing sector ranking information with the following fields:
    - 序号: Serial number
    - 名称: Sector name
    - 最新涨跌幅: Latest change percentage (unit: %)
    - 北向资金今日持股-股票只数: Number of stocks held by northbound funds today
    - 北向资金今日持股-市值: Market value of stocks held by northbound funds today (unit: CNY)
    - 北向资金今日持股-占板块比: Percentage of northbound funds holdings in the sector
    - 北向资金今日持股-占北向资金比: Percentage of sector holdings in total northbound funds
    - 北向资金今日增持估计-股票只数: Number of stocks estimated to be increased by northbound funds today
    - 北向资金今日增持估计-市值: Market value of stocks estimated to be increased by northbound funds today (unit: CNY)
    - 北向资金今日增持估计-市值增幅: Market value increase percentage of stocks estimated to be increased by northbound funds today
    - 北向资金今日增持估计-占板块比: Percentage of estimated increased holdings in the sector
    - 北向资金今日增持估计-占北向资金比: Percentage of estimated increased holdings in total northbound funds
    - 今日增持最大股-市值: Market value of the largest stock increased today
    - 今日增持最大股-占股本比: Percentage of the largest stock increased today in total shares
    - 今日减持最大股-占股本比: Percentage of the largest stock decreased today in total shares
    - 今日减持最大股-市值: Market value of the largest stock decreased today
    - 报告时间: Report time
    
    
    中文: 东方财富网-数据中心-沪深港通持股-板块排行
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的板块排行类型。默认值为 "北向资金增持行业板块排行"。
                  可选值包括："北向资金增持行业板块排行"，"北向资金增持概念板块排行"，
                  "北向资金增持地域板块排行"。
    
    indicator: str - 排行的时间周期。默认值为 "今日"。
                     可选值包括："今日"，"3日"，"5日"，"10日"，"1月"，"1季"，"1年"。
    
    返回:
    JSON格式数据，包含板块排行信息，具有以下字段：
    - 序号: 序号
    - 名称: 板块名称
    - 最新涨跌幅: 最新涨跌幅（单位: %）
    - 北向资金今日持股-股票只数: 北向资金今日持有的股票数量
    - 北向资金今日持股-市值: 北向资金今日持有的股票市值（单位: 元）
    - 北向资金今日持股-占板块比: 北向资金持股占板块的比例
    - 北向资金今日持股-占北向资金比: 板块持股占北向资金总量的比例
    - 北向资金今日增持估计-股票只数: 北向资金今日估计增持的股票数量
    - 北向资金今日增持估计-市值: 北向资金今日估计增持的股票市值（单位: 元）
    - 北向资金今日增持估计-市值增幅: 北向资金今日估计增持的股票市值增幅
    - 北向资金今日增持估计-占板块比: 估计增持占板块的比例
    - 北向资金今日增持估计-占北向资金比: 估计增持占北向资金总量的比例
    - 今日增持最大股-市值: 今日增持最大股票的市值
    - 今日增持最大股-占股本比: 今日增持最大股票占总股本的比例
    - 今日减持最大股-占股本比: 今日减持最大股票占总股本的比例
    - 今日减持最大股-市值: 今日减持最大股票的市值
    - 报告时间: 报告时间
    """
    try:
        df = ak.stock_hsgt_board_rank_em(symbol=symbol, indicator=indicator)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_fund_flow_summary_em() -> str:
    """Get 东方财富网-数据中心-资金流向-沪深港通资金流向
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-资金流向-沪深港通资金流向
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hsgt_fund_flow_summary_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_fund_min_em(symbol: str = "北向资金") -> str:
    """Get 东方财富-数据中心-沪深港通-市场概括-分时数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-沪深港通-市场概括-分时数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hsgt_fund_min_em(symbol="北向资金")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_hist_em(symbol: str = "北向资金") -> str:
    """Get historical data for Shanghai-Shenzhen-Hong Kong Stock Connect capital flows from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The type of capital flow to query. Default is "北向资金" (Northbound funds).
                  Available options include: "北向资金" (Northbound funds), "沪股通" (Shanghai Connect), 
                  "深股通" (Shenzhen Connect), "南向资金" (Southbound funds), 
                  "港股通沪" (Hong Kong Stock Connect - Shanghai), "港股通深" (Hong Kong Stock Connect - Shenzhen).
    
    Returns:
    JSON formatted data containing historical capital flow information with different fields based on the selected symbol:
    
    For "北向资金" (Northbound funds):
    - 日期: Date
    - 当日成交净买额: Net purchase amount for the day (unit: 100 million CNY)
    - 买入成交额: Purchase transaction amount (unit: 100 million CNY)
    - 卖出成交额: Sell transaction amount (unit: 100 million CNY)
    - 历史累计净买额: Historical cumulative net purchase amount (unit: trillion CNY)
    - 当日资金流入: Capital inflow for the day (unit: 100 million CNY)
    - 当日余额: Balance for the day (unit: 100 million CNY)
    - 持股市值: Holdings market value (unit: CNY)
    - 领涨股: Leading stock
    - 领涨股-涨跌幅: Leading stock change percentage (unit: %)
    - 沪深300: CSI 300 Index
    - 沪深300-涨跌幅: CSI 300 Index change percentage (unit: %)
    - 领涨股-代码: Leading stock code
    
    For "港股通沪" (Hong Kong Stock Connect - Shanghai) and similar:
    - 日期: Date
    - 当日成交净买额: Net purchase amount for the day (unit: 100 million HKD)
    - 买入成交额: Purchase transaction amount (unit: 100 million HKD)
    - 卖出成交额: Sell transaction amount (unit: 100 million HKD)
    - 历史累计净买额: Historical cumulative net purchase amount (unit: trillion CNY)
    - 当日资金流入: Capital inflow for the day (unit: 100 million CNY)
    - 当日余额: Balance for the day (unit: 100 million CNY)
    - 持股市值: Holdings market value (unit: CNY)
    - 领涨股: Leading stock
    - 领涨股-涨跌幅: Leading stock change percentage (unit: %)
    - 恒生指数: Hang Seng Index
    - 恒生指数-涨跌幅: Hang Seng Index change percentage (unit: %)
    - 领涨股-代码: Leading stock code
    
    
    中文: 东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的资金流向类型。默认值为 "北向资金"。
                  可选值包括："北向资金"，"沪股通"，"深股通"，"南向资金"，
                  "港股通沪"，"港股通深"。
    
    返回:
    JSON格式数据，包含历史资金流向信息，根据选择的符号有不同的字段：
    
    对于 "北向资金":
    - 日期: 日期
    - 当日成交净买额: 当日成交净买额（单位: 亿元）
    - 买入成交额: 买入成交额（单位: 亿元）
    - 卖出成交额: 卖出成交额（单位: 亿元）
    - 历史累计净买额: 历史累计净买额（单位: 万亿元）
    - 当日资金流入: 当日资金流入（单位: 亿元）
    - 当日余额: 当日余额（单位: 亿元）
    - 持股市值: 持股市值（单位: 元）
    - 领涨股: 领涨股
    - 领涨股-涨跌幅: 领涨股涨跌幅（单位: %）
    - 沪深300: 沪深300指数
    - 沪深300-涨跌幅: 沪深300指数涨跌幅（单位: %）
    - 领涨股-代码: 领涨股代码
    
    对于 "港股通沪" 等:
    - 日期: 日期
    - 当日成交净买额: 当日成交净买额（单位: 亿港元）
    - 买入成交额: 买入成交额（单位: 亿港元）
    - 卖出成交额: 卖出成交额（单位: 亿港元）
    - 历史累计净买额: 历史累计净买额（单位: 万亿元）
    - 当日资金流入: 当日资金流入（单位: 亿元）
    - 当日余额: 当日余额（单位: 亿元）
    - 持股市值: 持股市值（单位: 元）
    - 领涨股: 领涨股
    - 领涨股-涨跌幅: 领涨股涨跌幅（单位: %）
    - 恒生指数: 恒生指数
    - 恒生指数-涨跌幅: 恒生指数涨跌幅（单位: %）
    - 领涨股-代码: 领涨股代码
    """
    try:
        df = ak.stock_hsgt_hist_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_hold_stock_em(market: str = "北向", indicator: str = "今日排行") -> str:
    """Get individual stock ranking data for Shanghai-Shenzhen-Hong Kong Stock Connect holdings from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    market: str - Market direction for the stock connect. Default is "北向" (Northbound).
                  Available options include: "北向" (Northbound), "沪股通" (Shanghai Connect), "深股通" (Shenzhen Connect).
    
    indicator: str - Time period for the ranking. Default is "今日排行" (Today's ranking).
                     Available options include: "今日排行" (Today's ranking), "3日排行" (3-day ranking),
                     "5日排行" (5-day ranking), "10日排行" (10-day ranking), "月排行" (Monthly ranking),
                     "季排行" (Quarterly ranking), "年排行" (Yearly ranking).
    
    Returns:
    JSON formatted data containing individual stock ranking information with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 今日收盘价: Today's closing price
    - 今日涨跌幅: Today's change percentage (unit: %)
    - 今日持股-股数: Today's holdings - shares (unit: 10,000 shares)
    - 今日持股-市值: Today's holdings - market value (unit: 10,000 CNY)
    - 今日持股-占流通股比: Today's holdings - percentage of circulating shares (unit: %)
    - 今日持股-占总股本比: Today's holdings - percentage of total shares (unit: %)
    - 增持估计-股数: Estimated increase - shares (unit: 10,000 shares) [field name varies based on indicator]
    - 增持估计-市值: Estimated increase - market value (unit: 10,000 CNY) [field name varies based on indicator]
    - 增持估计-市值增幅: Estimated increase - market value growth (unit: %) [field name varies based on indicator]
    - 增持估计-占流通股比: Estimated increase - percentage of circulating shares (unit: ‰) [field name varies based on indicator]
    - 增持估计-占总股本比: Estimated increase - percentage of total shares (unit: ‰) [field name varies based on indicator]
    - 所属板块: Sector
    - 日期: Date
    
    
    中文: 东方财富网-数据中心-沪深港通持股-个股排行
    
    返回 JSON 格式的数据。
    
    参数:
    market: str - 股票互联互通的市场方向。默认值为 "北向"。
                  可选值包括："北向"，"沪股通"，"深股通"。
    
    indicator: str - 排行的时间周期。默认值为 "今日排行"。
                     可选值包括："今日排行"，"3日排行"，"5日排行"，"10日排行"，
                     "月排行"，"季排行"，"年排行"。
    
    返回:
    JSON格式数据，包含个股排行信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 今日收盘价: 今日收盘价
    - 今日涨跌幅: 今日涨跌幅（单位: %）
    - 今日持股-股数: 今日持股-股数（单位: 万）
    - 今日持股-市值: 今日持股-市值（单位: 万）
    - 今日持股-占流通股比: 今日持股-占流通股比（单位: %）
    - 今日持股-占总股本比: 今日持股-占总股本比（单位: %）
    - 增持估计-股数: 增持估计-股数（单位: 万）[字段名根据 indicator 变化]
    - 增持估计-市值: 增持估计-市值（单位: 万）[字段名根据 indicator 变化]
    - 增持估计-市值增幅: 增持估计-市值增幅（单位: %）[字段名根据 indicator 变化]
    - 增持估计-占流通股比: 增持估计-占流通股比（单位: ‰）[字段名根据 indicator 变化]
    - 增持估计-占总股本比: 增持估计-占总股本比（单位: ‰）[字段名根据 indicator 变化]
    - 所属板块: 所属板块
    - 日期: 日期
    """
    try:
        df = ak.stock_hsgt_hold_stock_em(market=market, indicator=indicator)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_individual_detail_em(symbol: str = "600519") -> str:
    """Get 东方财富网-数据中心-沪深港通-沪深港通持股-具体股票-个股详情
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-沪深港通-沪深港通持股-具体股票-个股详情
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_hsgt_individual_detail_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_individual_em(stock: str = "002008") -> str:
    """Get Shanghai-Shenzhen-Hong Kong Stock Connect holdings data for a specific stock from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    stock: str - The stock code to query. Default is "002008".
                 For Shenzhen Stock Exchange: Use the code directly (e.g., "002008").
                 For Shanghai Stock Exchange: Use the code directly (e.g., "600000").
    
    Returns:
    JSON formatted data containing the stock's holding information with the following fields:
    - 持股日期: Holding date
    - 当日收盘价: Closing price for the day (unit: CNY)
    - 当日涨跌幅: Price change percentage for the day (unit: %)
    - 持股数量: Number of shares held (unit: shares)
    - 持股市值: Market value of holdings (unit: CNY)
    - 持股数量占A股百分比: Percentage of holdings in A-shares (unit: %)
    - 持股市值变化-1日: Change in market value of holdings over 1 day (unit: CNY)
    - 持股市值变化-5日: Change in market value of holdings over 5 days (unit: CNY)
    - 持股市值变化-10日: Change in market value of holdings over 10 days (unit: CNY)
    
    
    中文: 东方财富网-数据中心-沪深港通-沪深港通持股-具体股票
    
    返回 JSON 格式的数据。
    
    参数:
    stock: str - 要查询的股票代码。默认值为 "002008"。
                 深圳证券交易所：直接使用代码（例如，"002008"）。
                 上海证券交易所：直接使用代码（例如，"600000"）。
    
    返回:
    JSON格式数据，包含股票的持股信息，具有以下字段：
    - 持股日期: 持股日期
    - 当日收盘价: 当日收盘价（单位: 元）
    - 当日涨跌幅: 当日涨跌幅（单位: %）
    - 持股数量: 持股数量（单位: 股）
    - 持股市值: 持股市值（单位: 元）
    - 持股数量占A股百分比: 持股数量占A股百分比（单位: %）
    - 持股市值变化-1日: 持股市值1日变化（单位: 元）
    - 持股市值变化-5日: 持股市值5日变化（单位: 元）
    - 持股市值变化-10日: 持股市值10日变化（单位: 元）
    """
    try:
        df = ak.stock_hsgt_individual_em(stock=stock)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_institution_statistics_em(market: str = "北向持股", start_date: str = "20201218", end_date: str = "20201218") -> str:
    """Get institutional ranking data for Shanghai-Shenzhen-Hong Kong Stock Connect holdings from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    market: str - The market type to query. Default is "北向持股" (Northbound holdings).
                  Available options include: "北向持股" (Northbound holdings), "沪股通持股" (Shanghai Connect holdings),
                  "深股通持股" (Shenzhen Connect holdings), "南向持股" (Southbound holdings).
    
    start_date: str - Start date for the query in format "YYYYMMDD". Default is "20201218".
                      Note: This interface can only obtain recent data.
    
    end_date: str - End date for the query in format "YYYYMMDD". Default is "20201218".
                    Note: This interface can only obtain recent data.
    
    Returns:
    JSON formatted data containing institutional ranking information with the following fields:
    - 持股日期: Holding date
    - 机构名称: Institution name
    - 持股只数: Number of stocks held (unit: stocks)
    - 持股市值: Market value of holdings (unit: CNY for Northbound, HKD for Southbound)
    - 持股市值变化-1日: Change in market value of holdings over 1 day (unit: CNY for Northbound, HKD for Southbound)
    - 持股市值变化-5日: Change in market value of holdings over 5 days (unit: CNY for Northbound, HKD for Southbound)
    - 持股市值变化-10日: Change in market value of holdings over 10 days (unit: CNY for Northbound, HKD for Southbound)
    
    
    中文: 东方财富网-数据中心-沪深港通-沪深港通持股-机构排行
    
    返回 JSON 格式的数据。
    
    参数:
    market: str - 要查询的市场类型。默认值为 "北向持股"。
                  可选值包括："北向持股"，"沪股通持股"，"深股通持股"，"南向持股"。
    
    start_date: str - 查询的开始日期，格式为 "YYYYMMDD"。默认值为 "20201218"。
                      注意：此接口只能获取近期的数据。
    
    end_date: str - 查询的结束日期，格式为 "YYYYMMDD"。默认值为 "20201218"。
                    注意：此接口只能获取近期的数据。
    
    返回:
    JSON格式数据，包含机构排行信息，具有以下字段：
    - 持股日期: 持股日期
    - 机构名称: 机构名称
    - 持股只数: 持股只数（单位: 只）
    - 持股市值: 持股市值（北向持股单位: 元，南向持股单位: 港元）
    - 持股市值变化-1日: 持股市值1日变化（北向持股单位: 元，南向持股单位: 港元）
    - 持股市值变化-5日: 持股市值5日变化（北向持股单位: 元，南向持股单位: 港元）
    - 持股市值变化-10日: 持股市值10日变化（北向持股单位: 元，南向持股单位: 港元）
    """
    try:
        df = ak.stock_hsgt_institution_statistics_em(market=market, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_sh_hk_spot_em() -> str:
    """Get real-time stock data for Shanghai-Hong Kong Stock Connect (Shanghai to Hong Kong) from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    This function does not take any parameters.
    
    Returns:
    JSON formatted data containing real-time stock information with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price (unit: HKD)
    - 涨跌额: Price change amount
    - 涨跌幅: Price change percentage (unit: %)
    - 今开: Opening price today
    - 最高: Highest price
    - 最低: Lowest price
    - 昨收: Yesterday's closing price
    - 成交量: Trading volume (unit: 100 million shares)
    - 成交额: Trading amount (unit: 100 million HKD)
    
    
    中文: 东方财富网-行情中心-沪深港通-港股通(沪>港)-股票
    
    返回 JSON 格式的数据。
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含实时股票信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格（单位: 港元）
    - 涨跌额: 价格变化金额
    - 涨跌幅: 价格变化百分比（单位: %）
    - 今开: 今日开盘价
    - 最高: 最高价
    - 最低: 最低价
    - 昨收: 昨日收盘价
    - 成交量: 成交量（单位: 亿股）
    - 成交额: 成交金额（单位: 亿港元）
    """
    try:
        df = ak.stock_hsgt_sh_hk_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_hsgt_stock_statistics_em(symbol: str = "北向持股", start_date: str = "20211027", end_date: str = "20211027") -> str:
    """Get daily stock statistics for Shanghai-Shenzhen-Hong Kong Stock Connect holdings from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The market type to query. Default is "北向持股" (Northbound holdings).
                  Available options include: "北向持股" (Northbound holdings), "沪股通持股" (Shanghai Connect holdings),
                  "深股通持股" (Shenzhen Connect holdings), "南向持股" (Southbound holdings).
    
    start_date: str - Start date for the query in format "YYYYMMDD". Default is "20211027".
                      Note: This interface can only obtain recent data.
    
    end_date: str - End date for the query in format "YYYYMMDD". Default is "20211027".
                    Note: This interface can only obtain recent data.
    
    Returns:
    JSON formatted data containing daily stock statistics with the following fields:
    - 持股日期: Holding date
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 当日收盘价: Closing price for the day (unit: CNY for Northbound, HKD for Southbound)
    - 当日涨跌幅: Price change percentage for the day (unit: %)
    - 持股数量: Number of shares held (unit: 10,000 shares)
    - 持股市值: Market value of holdings (unit: 10,000 CNY/HKD)
    - 持股数量占发行股百分比: Percentage of holdings in issued shares (unit: %)
    - 持股市值变化-1日: Change in market value of holdings over 1 day (unit: CNY/HKD)
    - 持股市值变化-5日: Change in market value of holdings over 5 days (unit: CNY/HKD)
    - 持股市值变化-10日: Change in market value of holdings over 10 days (unit: CNY/HKD)
    
    
    中文: 东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的市场类型。默认值为 "北向持股"。
                  可选值包括："北向持股"，"沪股通持股"，"深股通持股"，"南向持股"。
    
    start_date: str - 查询的开始日期，格式为 "YYYYMMDD"。默认值为 "20211027"。
                      注意：此接口只能获取近期的数据。
    
    end_date: str - 查询的结束日期，格式为 "YYYYMMDD"。默认值为 "20211027"。
                    注意：此接口只能获取近期的数据。
    
    返回:
    JSON格式数据，包含每日个股统计信息，具有以下字段：
    - 持股日期: 持股日期
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 当日收盘价: 当日收盘价（北向持股单位: 元，南向持股单位: 港元）
    - 当日涨跌幅: 当日涨跌幅（单位: %）
    - 持股数量: 持股数量（单位: 万股）
    - 持股市值: 持股市值（单位: 万元）
    - 持股数量占发行股百分比: 持股数量占发行股百分比（单位: %）
    - 持股市值变化-1日: 持股市值1日变化（单位: 元）
    - 持股市值变化-5日: 持股市值5日变化（单位: 元）
    - 持股市值变化-10日: 持股市值10日变化（单位: 元）
    """
    try:
        df = ak.stock_hsgt_stock_statistics_em(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_index_pb_lg(symbol: str = "上证50") -> str:
    """Get index price-to-book ratio data from LeGuLeGu.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The index to query. Default is "上证50" (SSE 50 Index).
                  Available options include: "上证50" (SSE 50), "沪深300" (CSI 300), "上证380" (SSE 380),
                  "创业板50" (ChiNext 50), "中证500" (CSI 500), "上证180" (SSE 180),
                  "深证红利" (SZSE Dividend), "深证100" (SZSE 100), "中证1000" (CSI 1000),
                  "上证红利" (SSE Dividend), "中证100" (CSI 100), "中证800" (CSI 800).
    
    Returns:
    JSON formatted data containing index price-to-book ratio information with the following fields:
    - 日期: Date
    - 指数: Index value
    - 市净率: Price-to-book ratio
    - 等权市净率: Equal-weighted price-to-book ratio
    - 市净率中位数: Median price-to-book ratio
    
    
    中文: 乐咕乐股-指数市净率
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的指数。默认值为 "上证50"。
                  可选值包括："上证50"，"沪深300"，"上证380"，"创业板50"，"中证500"，
                  "上证180"，"深证红利"，"深证100"，"中证1000"，"上证红利"，
                  "中证100"，"中证800"。
    
    返回:
    JSON格式数据，包含指数市净率信息，具有以下字段：
    - 日期: 日期
    - 指数: 指数值
    - 市净率: 市净率
    - 等权市净率: 等权市净率
    - 市净率中位数: 市净率中位数
    """
    try:
        df = ak.stock_index_pb_lg(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_index_pe_lg(symbol: str = "上证50") -> str:
    """Get index price-to-earnings ratio data from LeGuLeGu.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The index to query. Default is "上证50" (SSE 50 Index).
                  Available options include: "上证50" (SSE 50), "沪深300" (CSI 300), "上证380" (SSE 380),
                  "创业板50" (ChiNext 50), "中证500" (CSI 500), "上证180" (SSE 180),
                  "深证红利" (SZSE Dividend), "深证100" (SZSE 100), "中证1000" (CSI 1000),
                  "上证红利" (SSE Dividend), "中证100" (CSI 100), "中证800" (CSI 800).
    
    Returns:
    JSON formatted data containing index price-to-earnings ratio information with the following fields:
    - 日期: Date
    - 指数: Index value
    - 等权静态市盈率: Equal-weighted static price-to-earnings ratio
    - 静态市盈率: Static price-to-earnings ratio
    - 静态市盈率中位数: Median static price-to-earnings ratio
    - 等权滚动市盈率: Equal-weighted rolling price-to-earnings ratio
    - 滚动市盈率: Rolling price-to-earnings ratio
    - 滚动市盈率中位数: Median rolling price-to-earnings ratio
    
    
    中文: 乐咕乐股-指数市盈率
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的指数。默认值为 "上证50"。
                  可选值包括："上证50"，"沪深300"，"上证380"，"创业板50"，"中证500"，
                  "上证180"，"深证红利"，"深证100"，"中证1000"，"上证红利"，
                  "中证100"，"中证800"。
    
    返回:
    JSON格式数据，包含指数市盈率信息，具有以下字段：
    - 日期: 日期
    - 指数: 指数值
    - 等权静态市盈率: 等权静态市盈率
    - 静态市盈率: 静态市盈率
    - 静态市盈率中位数: 静态市盈率中位数
    - 等权滚动市盈率: 等权滚动市盈率
    - 滚动市盈率: 滚动市盈率
    - 滚动市盈率中位数: 滚动市盈率中位数
    """
    try:
        df = ak.stock_index_pe_lg(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_individual_spot_xq(symbol: str = "SPY", timeout: float = None, token: float = None) -> str:
    """Get real-time stock data for individual stocks from XueQiu.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The stock symbol to query. Default is "SPY".
                  Can be A-share stock code, A-share in-market fund code, A-share index, US stock code, or US index.
                  Example: "SH600000" for a Chinese A-share stock.
    
    timeout: float - Optional timeout parameter. Default is None (no timeout).
    
    token: float - Optional token parameter. Default is None (no token).
    
    Returns:
    JSON formatted data containing real-time stock information with the following fields:
    - item: Item name/description
    - value: Corresponding value for the item
    
    
    中文: 雪球-行情中心-个股
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的股票代码。默认值为 "SPY"。
                  可以是 A 股个股代码，A 股场内基金代码，A 股指数，美股代码或美股指数。
                  例如："SH600000" 表示中国 A 股股票。
    
    timeout: float - 可选的超时参数。默认值为 None（不设置超时）。
    
    token: float - 可选的令牌参数。默认值为 None（不设置令牌）。
    
    返回:
    JSON格式数据，包含实时股票信息，具有以下字段：
    - item: 项目名称/描述
    - value: 项目对应的值
    """
    try:
        df = ak.stock_individual_spot_xq(symbol=symbol, timeout=timeout, token=token)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_industry_category_cninfo(symbol: str = "巨潮行业分类标准") -> str:
    """Get industry classification data from CNINFO (China Securities Regulatory Commission)
    
    This function retrieves industry classification data from CNINFO based on the specified classification standard.
    Returns data in JSON format.
    
    Args:
        symbol: The industry classification standard to use. Default is "巨潮行业分类标准" (CNINFO Industry Classification Standard).
               Available options include: "证监会行业分类标准", "巨潮行业分类标准", "申银万国行业分类标准", 
               "新财富行业分类标准", "国资委行业分类标准", "巨潮产业细分标准", "天相行业分类标准", "全球行业分类标准".
    
    Returns:
        JSON formatted data containing industry classification information including category codes, 
        category names, end dates, industry types, industry type codes, English category names, 
        parent codes, and classification levels.
    
    中文: 巨潮资讯-数据-行业分类数据
    
    该函数从巨潮资讯网获取行业分类数据，基于指定的分类标准。
    返回JSON格式的数据。
    
    参数:
        symbol: 行业分类标准。默认为"巨潮行业分类标准"。
               可选值包括: "证监会行业分类标准", "巨潮行业分类标准", "申银万国行业分类标准", 
               "新财富行业分类标准", "国资委行业分类标准", "巨潮产业细分标准", "天相行业分类标准", "全球行业分类标准"。
    
    返回:
        JSON格式的数据，包含行业分类信息，如类目编码、类目名称、终止日期、行业类型、行业类型编码、类目名称英文、父类编码和分级等。
    """
    try:
        df = ak.stock_industry_category_cninfo(symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_industry_change_cninfo(symbol: str = "002594", start_date: str = "20091227", end_date: str = "20220708") -> str:
    """Get industry classification changes for listed companies from CNINFO.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The stock code to query. Default is "002594".
    
    start_date: str - Start date for the query in format "YYYYMMDD". Default is "20091227".
    
    end_date: str - End date for the query in format "YYYYMMDD". Default is "20220708".
    
    Returns:
    JSON formatted data containing industry classification changes with the following fields:
    - 新证券简称: New security abbreviation
    - 行业中类: Industry middle category
    - 行业大类: Industry major category
    - 行业次类: Industry sub-category
    - 行业门类: Industry sector
    - 机构名称: Institution name
    - 行业编码: Industry code
    - 分类标准: Classification standard
    - 分类标准编码: Classification standard code
    - 证券代码: Security code
    - 变更日期: Change date
    
    
    中文: 巨潮资讯-数据-上市公司行业归属的变动情况
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的股票代码。默认值为 "002594"。
    
    start_date: str - 查询的开始日期，格式为 "YYYYMMDD"。默认值为 "20091227"。
    
    end_date: str - 查询的结束日期，格式为 "YYYYMMDD"。默认值为 "20220708"。
    
    返回:
    JSON格式数据，包含行业分类变化信息，具有以下字段：
    - 新证券简称: 新证券简称
    - 行业中类: 行业中类
    - 行业大类: 行业大类
    - 行业次类: 行业次类
    - 行业门类: 行业门类
    - 机构名称: 机构名称
    - 行业编码: 行业编码
    - 分类标准: 分类标准
    - 分类标准编码: 分类标准编码
    - 证券代码: 证券代码
    - 变更日期: 变更日期
    """
    try:
        df = ak.stock_industry_change_cninfo(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_industry_clf_hist_sw() -> str:
    """Get historical industry classification data for all stocks from Shenwan Hongyuan Research.
    
    Returns data in JSON format.
    
    Parameters:
    This function does not take any parameters.
    
    Returns:
    JSON formatted data containing historical industry classification information with the following fields:
    - symbol: Stock code
    - start_date: Inclusion date
    - industry_code: Shenwan industry code
    - update_time: Update date
    
    
    中文: 申万宏源研究-行业分类-全部行业分类
    
    返回 JSON 格式的数据。
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含历史行业分类信息，具有以下字段：
    - symbol: 股票代码
    - start_date: 计入日期
    - industry_code: 申万行业代码
    - update_time: 更新日期
    """
    try:
        df = ak.stock_industry_clf_hist_sw()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_industry_pe_ratio_cninfo(symbol: str = "国证行业分类", date: str = "20240617") -> str:
    """Get industry price-to-earnings ratio data from CNINFO.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - The industry classification standard to query. Default is "国证行业分类" (CNINDEX Industry Classification).
                  Available options include: "证监会行业分类" (CSRC Industry Classification), "国证行业分类" (CNINDEX Industry Classification).
    
    date: str - Trading date for the query in format "YYYYMMDD". Default is "20240617".
                Note: This interface can only obtain recent data.
    
    Returns:
    JSON formatted data containing industry price-to-earnings ratio information with the following fields:
    - 变动日期: Change date
    - 行业分类: Industry classification
    - 行业层级: Industry level
    - 行业编码: Industry code
    - 行业名称: Industry name
    - 公司数量: Number of companies
    - 纳入计算公司数量: Number of companies included in calculation
    - 总市值-静态: Total market value - static (unit: 100 million yuan)
    - 净利润-静态: Net profit - static (unit: 100 million yuan)
    - 静态市盈率-加权平均: Static price-to-earnings ratio - weighted average
    - 静态市盈率-中位数: Static price-to-earnings ratio - median
    - 静态市盈率-算术平均: Static price-to-earnings ratio - arithmetic average
    
    
    中文: 巨潮资讯-数据中心-行业分析-行业市盈率
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的行业分类标准。默认值为 "国证行业分类"。
                  可选值包括："证监会行业分类"，"国证行业分类"。
    
    date: str - 查询的交易日期，格式为 "YYYYMMDD"。默认值为 "20240617"。
                注意：此接口只能获取近期的数据。
    
    返回:
    JSON格式数据，包含行业市盈率信息，具有以下字段：
    - 变动日期: 变动日期
    - 行业分类: 行业分类
    - 行业层级: 行业层级
    - 行业编码: 行业编码
    - 行业名称: 行业名称
    - 公司数量: 公司数量
    - 纳入计算公司数量: 纳入计算的公司数量
    - 总市值-静态: 总市值-静态（单位: 亿元）
    - 净利润-静态: 净利润-静态（单位: 亿元）
    - 静态市盈率-加权平均: 静态市盈率-加权平均
    - 静态市盈率-中位数: 静态市盈率-中位数
    - 静态市盈率-算术平均: 静态市盈率-算术平均
    """
    try:
        df = ak.stock_industry_pe_ratio_cninfo(symbol=symbol, date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_a_code_name() -> str:
    """Get stock codes and names for all A-shares listed on Shanghai, Shenzhen, and Beijing Stock Exchanges.
    
    Returns data in JSON format.
    
    Parameters:
    This function does not take any parameters.
    
    Returns:
    JSON formatted data containing stock codes and names with the following fields:
    - code: Stock code
    - name: Stock name
    
    
    中文: 沪深京 A 股股票代码和股票简称数据
    
    返回 JSON 格式的数据。
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含股票代码和名称，具有以下字段：
    - code: 股票代码
    - name: 股票名称
    """
    try:
        df = ak.stock_info_a_code_name()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_bj_name_code() -> str:
    """Get stock codes and names for all stocks listed on the Beijing Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    This function does not take any parameters.
    
    Returns:
    JSON formatted data containing stock information with the following fields:
    - 证券代码: Stock code
    - 证券简称: Stock name
    - 总股本: Total share capital (unit: shares)
    - 流通股本: Circulating share capital (unit: shares)
    - 上市日期: Listing date
    - 所属行业: Industry
    - 地区: Region
    - 报告日期: Report date
    
    
    中文: 北京证券交易所股票代码和简称数据
    
    返回 JSON 格式的数据。
    
    参数:
    此函数不需要任何参数。
    
    返回:
    JSON格式数据，包含股票信息，具有以下字段：
    - 证券代码: 股票代码
    - 证券简称: 股票名称
    - 总股本: 总股本（单位: 股）
    - 流通股本: 流通股本（单位: 股）
    - 上市日期: 上市日期
    - 所属行业: 所属行业
    - 地区: 地区
    - 报告日期: 报告日期
    """
    try:
        df = ak.stock_info_bj_name_code()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_change_name(symbol: str = "000503") -> str:
    """Get historical names (former names) of a stock from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code. Default is "000503".
    
    Returns:
    JSON formatted data containing historical names of the specified stock with the following fields:
    - index: Index number
    - name: Historical name of the stock
    
    
    中文: 新浪财经-股票曾用名
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码。默认值为 "000503"。
    
    返回:
    JSON格式数据，包含指定股票的历史名称，具有以下字段：
    - index: 索引号
    - name: 股票的历史名称
    """
    try:
        df = ak.stock_info_change_name(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_sh_delist(symbol: str = "全部") -> str:
    """Get suspended/delisted stocks information from the Shanghai Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Market segment to query. Default is "全部" (All).
                  Available options include: "全部" (All), "沪市" (Shanghai Main Board), "科创板" (STAR Market).
    
    Returns:
    JSON formatted data containing suspended/delisted stocks information with the following fields:
    - 公司代码: Company code
    - 公司简称: Company name
    - 上市日期: Listing date
    - 暂停上市日期: Suspension date
    
    
    中文: 上海证券交易所暂停/终止上市股票
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的市场版块。默认值为 "全部"。
                  可选值包括："全部"，"沪市"，"科创板"。
    
    返回:
    JSON格式数据，包含暂停/终止上市股票信息，具有以下字段：
    - 公司代码: 公司代码
    - 公司简称: 公司名称
    - 上市日期: 上市日期
    - 暂停上市日期: 暂停上市日期
    """
    try:
        df = ak.stock_info_sh_delist(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_sh_name_code(symbol: str = "主板A股") -> str:
    """Get stock codes and names for stocks listed on the Shanghai Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Market segment to query. Default is "主板A股" (Main Board A-shares).
                  Available options include: "主板A股" (Main Board A-shares), "主板B股" (Main Board B-shares), "科创板" (STAR Market).
    
    Returns:
    JSON formatted data containing stock information with the following fields:
    - 证券代码: Stock code
    - 证券简称: Stock name
    - 公司全称: Company full name
    - 上市日期: Listing date
    
    
    中文: 上海证券交易所股票代码和简称数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的市场版块。默认值为 "主板A股"。
                  可选值包括："主板A股"，"主板B股"，"科创板"。
    
    返回:
    JSON格式数据，包含证券代码、证券简称、公司全称、上市日期等字段
    """
    try:
        df = ak.stock_info_sh_name_code(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_sz_change_name(symbol: str = "全称变更") -> str:
    """Get company name change information from the Shenzhen Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Type of name change to query. Default is "全称变更" (Full Name Change).
                  Available options include: "全称变更" (Full Name Change), "简称变更" (Short Name Change).
    
    Returns:
    JSON formatted data containing company name change information with the following fields:
    - 变更日期: Change date
    - 证券代码: Stock code
    - 证券简称: Stock name
    - 变更前全称: Company full name before change
    - 变更后全称: Company full name after change
    
    
    中文: 深证证券交易所-市场数据-股票数据-名称变更
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的名称变更类型。默认值为 "全称变更"。
                  可选值包括："全称变更"，"简称变更"。
    
    返回:
    JSON格式数据，包含公司名称变更信息，具有以下字段：
    - 变更日期: 变更日期
    - 证券代码: 股票代码
    - 证券简称: 股票名称
    - 变更前全称: 变更前的公司全称
    - 变更后全称: 变更后的公司全称
    """
    try:
        df = ak.stock_info_sz_change_name(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_sz_delist(symbol: str = "终止上市公司") -> str:
    """Get suspended/delisted stocks information from the Shenzhen Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Type of delisted companies to query. Default is "终止上市公司" (Delisted Companies).
                  Available options include: "暂停上市公司" (Suspended Companies), "终止上市公司" (Delisted Companies).
    
    Returns:
    JSON formatted data containing suspended/delisted stocks information with the following fields:
    - 证券代码: Stock code
    - 证券简称: Stock name
    - 上市日期: Listing date
    - 终止上市日期: Delisting date
    
    
    中文: 深证证券交易所终止/暂停上市股票
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的退市公司类型。默认值为 "终止上市公司"。
                  可选值包括："暂停上市公司"，"终止上市公司"。
    
    返回:
    JSON格式数据，包含暂停/终止上市股票信息，具有以下字段：
    - 证券代码: 股票代码
    - 证券简称: 股票名称
    - 上市日期: 上市日期
    - 终止上市日期: 退市日期
    """
    try:
        df = ak.stock_info_sz_delist(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_info_sz_name_code(symbol: str = "A股列表") -> str:
    """Get stock codes and names for stocks listed on the Shenzhen Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Type of stock list to query. Default is "A股列表" (A-share List).
                  Available options include: "A股列表" (A-share List), "B股列表" (B-share List), 
                  "CDR列表" (CDR List), "AB股列表" (AB-share List).
    
    Returns:
    JSON formatted data containing stock information with the following fields (for A-share List):
    - 板块: Board
    - A股代码: A-share code
    - A股简称: A-share name
    - A股上市日期: A-share listing date
    - A股总股本: A-share total share capital
    - A股流通股本: A-share circulating share capital
    - 所属行业: Industry
    
    
    中文: 深证证券交易所股票代码和股票简称数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的股票列表类型。默认值为 "A股列表"。
                  可选值包括："A股列表"，"B股列表"，"CDR列表"，"AB股列表"。
    
    返回:
    JSON格式数据，包含板块、A股代码、A股简称、A股上市日期、A股总股本、A股流通股本、所属行业等字段
    """
    try:
        df = ak.stock_info_sz_name_code(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_inner_trade_xq() -> str:
    """Get insider trading information from Xueqiu for stocks in the Shanghai and Shenzhen markets.
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing insider trading information with the following fields:
    - 股票代码: Stock code
    - 股票名称: Stock name
    - 变动日期: Change date
    - 变动人: Person making the change
    - 变动股数: Number of shares changed
    - 成交均价: Average transaction price
    - 变动后持股数: Shares held after change
    - 与董监高关系: Relationship with directors/supervisors/executives
    - 董监高职务: Position of directors/supervisors/executives
    
    
    中文: 雪球-行情中心-沪深股市-内部交易
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含内部交易信息，具有以下字段：
    - 股票代码: 股票代码
    - 股票名称: 股票名称
    - 变动日期: 变动日期
    - 变动人: 变动人
    - 变动股数: 变动股数
    - 成交均价: 成交均价
    - 变动后持股数: 变动后持股数
    - 与董监高关系: 与董监高关系
    - 董监高职务: 董监高职务
    """
    try:
        df = ak.stock_inner_trade_xq()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_institute_hold_detail(stock: str = "300003", quarter: str = "20201") -> str:
    """Get detailed institutional shareholding information from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    stock: str - Stock code (e.g., '300003'), default is '300003'
    quarter: str - Financial quarter in format 'YYYYQ' where Q is quarter number (1-4), default is '20201'
                   For example: '20191' for Q1 2019, '20192' for Q2 2019, '20193' for Q3 2019, '20194' for Q4 2019
    
    Returns:
    JSON formatted data containing institutional shareholding details with the following fields:
    - 持股机构类型: Institution type
    - 持股机构代码: Institution code
    - 持股机构简称: Institution short name
    - 持股机构全称: Institution full name
    - 持股数: Number of shares held (in 10,000 shares)
    - 最新持股数: Latest number of shares held (in 10,000 shares)
    - 持股比例: Shareholding ratio (%)
    - 最新持股比例: Latest shareholding ratio (%)
    - 占流通股比例: Proportion of circulating shares (%)
    - 最新占流通股比例: Latest proportion of circulating shares (%)
    - 持股比例增幅: Increase in shareholding ratio (%)
    - 占流通股比例增幅: Increase in proportion of circulating shares (%)
    
    
    中文: 新浪财经-机构持股-机构持股详情
    
    返回 JSON 格式的数据。
    
    参数:
    stock: str - 股票代码（例如：'300003'），默认为 '300003'
    quarter: str - 财务季度，格式为 'YYYYQ'，Q 为季度号 (1-4)，默认为 '20201'
                   例如：'20191' 表示 2019 年一季度，'20192' 表示 2019 年二季度，
                   '20193' 表示 2019 年三季度，'20194' 表示 2019 年四季度
    
    返回:
    JSON格式数据，包含机构持股详情，具有以下字段：
    - 持股机构类型: 机构类型
    - 持股机构代码: 机构代码
    - 持股机构简称: 机构简称
    - 持股机构全称: 机构全称
    - 持股数: 持股数量（单位：万股）
    - 最新持股数: 最新持股数量（单位：万股）
    - 持股比例: 持股比例（%）
    - 最新持股比例: 最新持股比例（%）
    - 占流通股比例: 占流通股比例（%）
    - 最新占流通股比例: 最新占流通股比例（%）
    - 持股比例增幅: 持股比例增幅（%）
    - 占流通股比例增幅: 占流通股比例增幅（%）
    """
    try:
        df = ak.stock_institute_hold_detail(stock=stock, quarter=quarter)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_institute_recommend(symbol: str = "投资评级选股") -> str:
    """Get institutional recommendation pool data from Sina Finance based on specific indicators.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Indicator type to query. Default is "投资评级选股" (Investment Rating Stock Selection).
                  Available options include: 
                  "最新投资评级" (Latest Investment Ratings),
                  "上调评级股票" (Upgraded Rating Stocks),
                  "下调评级股票" (Downgraded Rating Stocks),
                  "股票综合评级" (Comprehensive Stock Ratings),
                  "首次评级股票" (First-time Rated Stocks),
                  "目标涨幅排名" (Target Increase Ranking),
                  "机构关注度" (Institutional Attention),
                  "行业关注度" (Industry Attention),
                  "投资评级选股" (Investment Rating Stock Selection).
    
    Returns:
    JSON formatted data with fields that vary depending on the selected indicator. The output fields will change
    based on the specific indicator selected in the symbol parameter.
    
    
    中文: 新浪财经-机构推荐池-具体指标的数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的指标类型。默认值为 "投资评级选股"。
                  可选值包括：
                  "最新投资评级"（最新投资评级），
                  "上调评级股票"（上调评级股票），
                  "下调评级股票"（下调评级股票），
                  "股票综合评级"（股票综合评级），
                  "首次评级股票"（首次评级股票），
                  "目标涨幅排名"（目标涨幅排名），
                  "机构关注度"（机构关注度），
                  "行业关注度"（行业关注度），
                  "投资评级选股"（投资评级选股）。
    
    返回:
    JSON格式数据，字段因所选指标而异。输出字段将根据在symbol参数中选择的特定指标而变化。
    """
    try:
        df = ak.stock_institute_recommend(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_institute_recommend_detail(symbol: str = "002709") -> str:
    """Get detailed stock rating records from the institutional recommendation pool on Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code to query. Default is "002709".
    
    Returns:
    JSON formatted data containing stock rating records with the following fields:
    - 股票代码: Stock code
    - 股票名称: Stock name
    - 目标价: Target price
    - 最新评级: Latest rating
    - 评级机构: Rating institution
    - 分析师: Analyst
    - 行业: Industry
    - 评级日期: Rating date
    
    
    中文: 新浪财经-机构推荐池-股票评级记录
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的股票代码。默认值为 "002709"。
    
    返回:
    JSON格式数据，包含股票评级记录，具有以下字段：
    - 股票代码: 股票代码
    - 股票名称: 股票名称
    - 目标价: 目标价格
    - 最新评级: 最新评级
    - 评级机构: 评级机构
    - 分析师: 分析师
    - 行业: 行业
    - 评级日期: 评级日期
    """
    try:
        df = ak.stock_institute_recommend_detail(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_intraday_sina(symbol: str = "sz000001", date: str = "20240321") -> str:
    """Get intraday time-series data from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code with market identifier. Default is "sz000001".
                  Example: "sz000001" for Shenzhen market, "sh600000" for Shanghai market.
    date: str - Trading date in format "YYYYMMDD". Default is "20240321".
                Note: Only recent data is available.
    
    Returns:
    JSON formatted data containing intraday time-series information with the following fields:
    - symbol: Stock code with market identifier
    - name: Stock name
    - ticktime: Time of the tick
    - price: Price at that time
    - volume: Trading volume (in shares)
    - prev_price: Previous price
    - kind: Type of order ("D" for sell order, "表示" for buy order)
    
    
    中文: 新浪财经-日内分时数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 带市场标识的股票代码。默认值为 "sz000001"。
                  例如："sz000001" 表示深圳市场，"sh600000" 表示上海市场。
    date: str - 交易日期，格式为 "YYYYMMDD"。默认值为 "20240321"。
              注意：只能获取近期的数据。
    
    返回:
    JSON格式数据，包含日内分时信息，具有以下字段：
    - symbol: 带市场标识的股票代码
    - name: 股票名称
    - ticktime: 时间点
    - price: 当时价格
    - volume: 交易量（单位：股）
    - prev_price: 前一价格
    - kind: 委托类型（"D" 表示卖盘，"表示" 表示买盘）
    """
    try:
        df = ak.stock_intraday_sina(symbol=symbol, date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_ipo_benefit_ths() -> str:
    """Get IPO beneficiary stocks data from TongHuaShun Data Center.
    
    Returns data in JSON format.
    
    This function retrieves data about stocks that benefit from IPOs. The data is updated weekly
    and returns the most recent week's data.
    
    Returns:
    JSON formatted data containing IPO beneficiary stocks with the following fields:
    - 序号: Serial number
    - 股票代码: Stock code
    - 股票简称: Stock abbreviation
    - 收盘价: Closing price (in CNY)
    - 涨跌幅: Price change percentage (%)
    - 市值: Market value (in CNY)
    - 参股家数: Number of invested companies
    - 投资总额: Total investment amount (in CNY)
    - 投资占市值比: Investment as percentage of market value (%)
    - 参股对象: Investment targets
    
    
    中文: 同花顺-数据中心-新股数据-IPO受益股
    
    返回 JSON 格式的数据。
    
    此函数检索有关从 IPO 中受益的股票数据。数据每周更新一次，
    返回最近一周的数据。
    
    返回:
    JSON格式数据，包含 IPO 受益股信息，具有以下字段：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 收盘价: 收盘价（单位：元）
    - 涨跌幅: 价格变化百分比（%）
    - 市值: 市值（单位：元）
    - 参股家数: 投资公司数量
    - 投资总额: 总投资金额（单位：元）
    - 投资占市值比: 投资占市值的百分比（%）
    - 参股对象: 投资目标
    """
    try:
        df = ak.stock_ipo_benefit_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_ipo_declare() -> str:
    """Get IPO declaration information from East Money Data Center.
    
    Returns data in JSON format.
    
    This function retrieves information about companies that have filed for initial public offerings (IPOs).
    It returns all historical data in a single request.
    
    Returns:
    JSON formatted data containing IPO declaration information with the following fields:
    - 序号: Serial number
    - 申报企业: Reporting company
    - 拟上市地: Intended listing location
    - 保荐机构: Sponsoring institution
    - 会计师事务所: Accounting firm
    - 律师事务所: Law firm
    - 备注: Remarks
    
    
    中文: 东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息
    
    返回 JSON 格式的数据。
    
    此函数检索有关已申请首次公开发行（IPO）的公司信息。
    它在单次请求中返回所有历史数据。
    
    返回:
    JSON格式数据，包含 IPO 申报信息，具有以下字段：
    - 序号: 序号
    - 申报企业: 申报公司
    - 拟上市地: 计划上市地点
    - 保荐机构: 保荐机构
    - 会计师事务所: 会计师事务所
    - 律师事务所: 律师事务所
    - 备注: 备注
    """
    try:
        df = ak.stock_ipo_declare()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_ipo_info(stock: str = "600004") -> str:
    """Get new stock issuance information from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    stock: str - Stock code to query. Default is "600004".
    
    Returns:
    JSON formatted data containing basic information about the IPO of the specified stock.
    The data is structured in a key-value format with the following fields:
    - item: The name of the information item
    - value: The corresponding value of the item
    
    Information items typically include details about the IPO such as issue price,
    issue date, listing date, number of shares issued, etc.
    
    
    中文: 新浪财经-发行与分配-新股发行
    
    返回 JSON 格式的数据。
    
    参数:
    stock: str - 要查询的股票代码。默认值为 "600004"。
    
    返回:
    JSON格式数据，包含指定股票的IPO基本信息。
    数据以键值对的形式结构，具有以下字段：
    - item: 信息项目名称
    - value: 相应的项目值
    
    信息项目通常包括有关IPO的详细信息，如发行价格、
    发行日期、上市日期、发行股数等。
    """
    try:
        df = ak.stock_ipo_info(stock=stock)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_ipo_summary_cninfo(symbol: str = "600030") -> str:
    """Get IPO-related information for a specific stock from CNINFO (China Securities Information).
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code to query. Default is "600030".
    
    Returns:
    JSON formatted data containing IPO-related information with the following fields:
    - 股票代码: Stock code
    - 招股公告日期: Prospectus announcement date
    - 中签率公告日: Winning rate announcement date
    - 每股面值: Par value per share (in CNY)
    - 总发行数量: Total issuance volume (in 10,000 shares)
    - 发行前每股净资产: Net assets per share before issuance (in CNY)
    - 折薄发行市盈率: Diluted issuance price-to-earnings ratio
    - 募集资金净额: Net amount of raised funds (in 10,000 CNY)
    - 上网发行日期: Online issuance date
    - 上市日期: Listing date
    - 发行价格: Issuance price (in CNY)
    - 发行费用总额: Total issuance expenses (in 10,000 CNY)
    - 发行后每股净资产: Net assets per share after issuance (in CNY)
    - 上网发行中签率: Online issuance winning rate (%)
    - 主承销商: Lead underwriter
    
    
    中文: 巨潮资讯-个股-上市相关
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的股票代码。默认值为 "600030"。
    
    返回:
    JSON格式数据，包含上市相关信息，具有以下字段：
    - 股票代码: 股票代码
    - 招股公告日期: 招股说明书公告日期
    - 中签率公告日: 中签率公告日
    - 每股面值: 每股面值（单位：元）
    - 总发行数量: 总发行量（单位：万股）
    - 发行前每股净资产: 发行前每股净资产（单位：元）
    - 折薄发行市盈率: 折薄发行市盈率
    - 募集资金净额: 募集资金净额（单位：万元）
    - 上网发行日期: 上网发行日期
    - 上市日期: 上市日期
    - 发行价格: 发行价格（单位：元）
    - 发行费用总额: 发行费用总额（单位：万元）
    - 发行后每股净资产: 发行后每股净资产（单位：元）
    - 上网发行中签率: 上网发行中签率（单位：%）
    - 主承销商: 主承销商
    """
    try:
        df = ak.stock_ipo_summary_cninfo(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_irm_ans_cninfo(symbol: str = "1495108801386602496") -> str:
    """Get answer data from the Interactive Easy platform (CNINFO).
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Question ID to query. Default is "1495108801386602496".
                  Note: Use ak.stock_irm_cninfo to get specific question IDs.
    
    Returns:
    JSON formatted data containing answer information with the following fields:
    - 股票代码: Stock code
    - 公司简称: Company abbreviation
    - 问题: Question
    - 回答内容: Answer content
    - 提问者: Questioner
    - 提问时间: Question time
    - 回答时间: Answer time
    
    
    中文: 互动易-回答
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的问题ID。默认值为 "1495108801386602496"。
                  注意：使用 ak.stock_irm_cninfo 获取特定的问题ID。
    
    返回:
    JSON格式数据，包含回答信息，具有以下字段：
    - 股票代码: 股票代码
    - 公司简称: 公司简称
    - 问题: 问题
    - 回答内容: 回答内容
    - 提问者: 提问者
    - 提问时间: 提问时间
    - 回答时间: 回答时间
    """
    try:
        df = ak.stock_irm_ans_cninfo(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_irm_cninfo(symbol: str = "002594") -> str:
    """Get question data from the Interactive Easy platform (CNINFO).
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code to query. Default is "002594".
    
    Returns:
    JSON formatted data containing question information with the following fields:
    - 股票代码: Stock code
    - 公司简称: Company abbreviation
    - 行业: Industry
    - 行业代码: Industry code
    - 问题: Question
    - 提问者: Questioner
    - 来源: Source
    - 提问时间: Question time
    - 更新时间: Update time
    - 提问者编号: Questioner ID
    - 问题编号: Question ID
    - 回答ID: Answer ID
    - 回答内容: Answer content
    - 回答者: Answerer
    
    
    中文: 互动易-提问
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 要查询的股票代码。默认值为 "002594"。
    
    返回:
    JSON格式数据，包含提问信息，具有以下字段：
    - 股票代码: 股票代码
    - 公司简称: 公司简称
    - 行业: 行业
    - 行业代码: 行业代码
    - 问题: 问题
    - 提问者: 提问者
    - 来源: 来源
    - 提问时间: 提问时间
    - 更新时间: 更新时间
    - 提问者编号: 提问者编号
    - 问题编号: 问题编号
    - 回答ID: 回答ID
    - 回答内容: 回答内容
    - 回答者: 回答者
    """
    try:
        df = ak.stock_irm_cninfo(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_jgdy_detail_em(date: str = "20241211") -> str:
    """Get detailed institutional research data from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    date: str - Start date for the query in format "YYYYMMDD". Default is "20241211".
    
    Returns:
    JSON formatted data containing detailed institutional research information with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Price change percentage (%)
    - 调研机构: Research institution
    - 机构类型: Institution type
    - 调研人员: Research personnel
    - 接待方式: Reception method
    - 接待人员: Reception personnel
    - 接待地点: Reception location
    - 调研日期: Research date
    - 公告日期: Announcement date
    
    
    中文: 东方财富网-数据中心-特色数据-机构调研-机构调研详细
    
    返回 JSON 格式的数据。
    
    参数:
    date: str - 查询的开始日期，格式为 "YYYYMMDD"。默认值为 "20241211"。
    
    返回:
    JSON格式数据，包含机构调研详细信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅百分比 (%)
    - 调研机构: 调研机构
    - 机构类型: 机构类型
    - 调研人员: 调研人员
    - 接待方式: 接待方式
    - 接待人员: 接待人员
    - 接待地点: 接待地点
    - 调研日期: 调研日期
    - 公告日期: 公告日期
    """
    try:
        df = ak.stock_jgdy_detail_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_jgdy_tj_em(date: str = "20210128") -> str:
    """Get institutional research statistics from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    date: str - Start date for the query in format "YYYYMMDD". Default is "20210128".
    
    Returns:
    JSON formatted data containing institutional research statistics with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Price change percentage (%)
    - 接待机构数量: Number of receiving institutions
    - 接待方式: Reception method
    - 接待人员: Reception personnel
    - 接待地点: Reception location
    - 接待日期: Reception date
    - 公告日期: Announcement date
    
    
    中文: 东方财富网-数据中心-特色数据-机构调研-机构调研统计
    
    返回 JSON 格式的数据。
    
    参数:
    date: str - 查询的开始日期，格式为 "YYYYMMDD"。默认值为 "20210128"。
    
    返回:
    JSON格式数据，包含机构调研统计信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅百分比 (%)
    - 接待机构数量: 接待机构数量
    - 接待方式: 接待方式
    - 接待人员: 接待人员
    - 接待地点: 接待地点
    - 接待日期: 接待日期
    - 公告日期: 公告日期
    """
    try:
        df = ak.stock_jgdy_tj_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_kc_a_spot_em() -> str:
    """Get real-time quotes for all stocks on the Science and Technology Innovation Board (STAR Market) from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing real-time market information with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Price change percentage (%)
    - 涨跌额: Price change amount
    - 成交量: Trading volume (in lots)
    - 成交额: Trading amount (in CNY)
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Today's opening price
    - 昨收: Yesterday's closing price
    - 量比: Volume ratio
    - 换手率: Turnover rate (%)
    - 市盈率-动态: Dynamic price-to-earnings ratio
    - 市净率: Price-to-book ratio
    - 总市值: Total market value (in CNY)
    - 流通市值: Circulating market value (in CNY)
    - 涨速: Price change speed
    - 5分钟涨跌: 5-minute price change (%)
    - 60日涨跌幅: 60-day price change percentage (%)
    - 年初至今涨跌幅: Year-to-date price change percentage (%)
    
    
    中文: 东方财富网-科创板-实时行情
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含实时行情信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价
    - 涨跌幅: 涨跌幅百分比 (%)
    - 涨跌额: 涨跌额
    - 成交量: 成交量（单位：手）
    - 成交额: 成交额（单位：元）
    - 振幅: 振幅百分比 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 今日开盘价
    - 昨收: 昨日收盘价
    - 量比: 量比
    - 换手率: 换手率百分比 (%)
    - 市盈率-动态: 动态市盈率
    - 市净率: 市净率
    - 总市值: 总市值（单位：元）
    - 流通市值: 流通市值（单位：元）
    - 涨速: 涨速
    - 5分钟涨跌: 5分钟涨跌百分比 (%)
    - 60日涨跌幅: 60日涨跌幅百分比 (%)
    - 年初至今涨跌幅: 年初至今涨跌幅百分比 (%)
    """
    try:
        df = ak.stock_kc_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lh_yyb_capital() -> str:
    """Get data on brokerage departments ranked by financial strength from the Dragon-Tiger List.
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing brokerage department rankings with the following fields:
    - 序号: Serial number
    - 营业部名称: Brokerage department name
    - 今日最高操作: Today's highest operation count
    - 今日最高金额: Today's highest amount
    - 今日最高买入金额: Today's highest purchase amount
    - 累计参与金额: Cumulative participation amount
    - 累计买入金额: Cumulative purchase amount
    
    
    中文: 龙虎榜-营业部排行-资金实力最强
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含营业部排行信息，具有以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 今日最高操作: 今日最高操作次数
    - 今日最高金额: 今日最高金额
    - 今日最高买入金额: 今日最高买入金额
    - 累计参与金额: 累计参与金额
    - 累计买入金额: 累计买入金额
    """
    try:
        df = ak.stock_lh_yyb_capital()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lh_yyb_control() -> str:
    """Get data on brokerage departments ranked by group operation strength from the Dragon-Tiger List.
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing brokerage department group operation rankings with the following fields:
    - 序号: Serial number
    - 营业部名称: Brokerage department name
    - 携手营业部家数: Number of partnered brokerage departments
    - 年内最佳携手对象: Best partner within the year
    - 年内最佳携手股票数: Number of best partnered stocks within the year
    - 年内最佳携手成功率: Success rate of best partnership within the year
    
    
    中文: 龙虎榜-营业部排行-抱团操作实力
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含营业部抱团操作排行信息，具有以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 携手营业部家数: 携手营业部家数
    - 年内最佳携手对象: 年内最佳携手对象
    - 年内最佳携手股票数: 年内最佳携手股票数
    - 年内最佳携手成功率: 年内最佳携手成功率
    """
    try:
        df = ak.stock_lh_yyb_control()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lh_yyb_most() -> str:
    """Get data on brokerage departments ranked by most appearances on the Dragon-Tiger List.
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing brokerage department rankings with the following fields:
    - 序号: Serial number
    - 营业部名称: Brokerage department name
    - 上榜次数: Number of appearances on the list
    - 合计动用资金: Total funds deployed
    - 年内上榜次数: Number of appearances on the list within the year
    - 年内买入股票只数: Number of stocks purchased within the year
    - 年内3日跟买成功率: Success rate of 3-day follow-up purchases within the year
    
    
    中文: 龙虎榜-营业部排行-上榜次数最多
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含营业部上榜次数排行信息，具有以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 上榜次数: 上榜次数
    - 合计动用资金: 合计动用资金
    - 年内上榜次数: 年内上榜次数
    - 年内买入股票只数: 年内买入股票只数
    - 年内3日跟买成功率: 年内3日跟买成功率
    """
    try:
        df = ak.stock_lh_yyb_most()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_detail_daily_sina(date: str = "20240222") -> str:
    """Get daily details from the Dragon-Tiger List from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    date: Trading date in the format "YYYYMMDD", default is "20240222"
    
    Returns:
    JSON formatted data containing daily Dragon-Tiger List details with the following fields:
    - 序号: Serial number
    - 股票代码: Stock code
    - 股票名称: Stock name
    - 收盘价: Closing price (in CNY)
    - 对应值: Corresponding value (%)
    - 成交量: Trading volume (in 10,000 shares)
    - 成交额: Trading amount (in 10,000 CNY)
    - 指标: Indicator (in 10,000 CNY)
    
    
    中文: 新浪财经-龙虎榜-每日详情
    
    返回 JSON 格式的数据。
    
    参数:
    date: 交易日期，格式为 "YYYYMMDD"，默认值为 "20240222"
    
    返回:
    JSON格式数据，包含龙虎榜每日详情，具有以下字段：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票名称: 股票名称
    - 收盘价: 收盘价（单位：元）
    - 对应值: 对应值（单位：%）
    - 成交量: 成交量（单位：万股）
    - 成交额: 成交额（单位：万元）
    - 指标: 指标（单位：万元）
    """
    try:
        df = ak.stock_lhb_detail_daily_sina(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_detail_em(start_date: str = "20230403", end_date: str = "20230417") -> str:
    """Get Dragon-Tiger List details from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    start_date: Start date in the format "YYYYMMDD", default is "20230403"
    end_date: End date in the format "YYYYMMDD", default is "20230417"
    
    Returns:
    JSON formatted data containing Dragon-Tiger List details with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 上榜日: Listing date
    - 解读: Interpretation
    - 收盘价: Closing price
    - 涨跌幅: Price change percentage (%)
    - 龙虎榜净买额: Net purchase amount on Dragon-Tiger List (in CNY)
    - 龙虎榜买入额: Purchase amount on Dragon-Tiger List (in CNY)
    - 龙虎榜卖出额: Sell amount on Dragon-Tiger List (in CNY)
    - 龙虎榜成交额: Transaction amount on Dragon-Tiger List (in CNY)
    - 市场总成交额: Total market transaction amount (in CNY)
    - 净买额占总成交比: Ratio of net purchase amount to total transaction (%)
    - 成交额占总成交比: Ratio of transaction amount to total transaction (%)
    - 换手率: Turnover rate (%)
    - 流通市值: Circulating market value (in CNY)
    - 上榜原因: Reason for listing
    - 上榜后1日: Price change 1 day after listing (%)
    - 上榜后2日: Price change 2 days after listing (%)
    - 上榜后5日: Price change 5 days after listing (%)
    - 上榜后10日: Price change 10 days after listing (%)
    
    
    中文: 东方财富网-数据中心-龙虎榜单-龙虎榜详情
    
    返回 JSON 格式的数据。
    
    参数:
    start_date: 开始日期，格式为 "YYYYMMDD"，默认值为 "20230403"
    end_date: 结束日期，格式为 "YYYYMMDD"，默认值为 "20230417"
    
    返回:
    JSON格式数据，包含龙虎榜详情，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 上榜日: 上榜日期
    - 解读: 解读
    - 收盘价: 收盘价
    - 涨跌幅: 涨跌幅（单位：%）
    - 龙虎榜净买额: 龙虎榜净买额（单位：元）
    - 龙虎榜买入额: 龙虎榜买入额（单位：元）
    - 龙虎榜卖出额: 龙虎榜卖出额（单位：元）
    - 龙虎榜成交额: 龙虎榜成交额（单位：元）
    - 市场总成交额: 市场总成交额（单位：元）
    - 净买额占总成交比: 净买额占总成交比（单位：%）
    - 成交额占总成交比: 成交额占总成交比（单位：%）
    - 换手率: 换手率（单位：%）
    - 流通市值: 流通市值（单位：元）
    - 上榜原因: 上榜原因
    - 上榜后1日: 上榜后1日涨跌幅（单位：%）
    - 上榜后2日: 上榜后2日涨跌幅（单位：%）
    - 上榜后5日: 上榜后5日涨跌幅（单位：%）
    - 上榜后10日: 上榜后10日涨跌幅（单位：%）
    """
    try:
        df = ak.stock_lhb_detail_em(start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_ggtj_sina(symbol: str = "5") -> str:
    """Get individual stock listing statistics from the Dragon-Tiger List from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Time period for statistics, default is "5"
           Options: "5": Last 5 days; "10": Last 10 days; "30": Last 30 days; "60": Last 60 days
    
    Returns:
    JSON formatted data containing individual stock listing statistics with the following fields:
    - 股票代码: Stock code
    - 股票名称: Stock name
    - 上榜次数: Number of times listed
    - 累积购买额: Accumulated purchase amount (in 10,000 CNY)
    - 累积卖出额: Accumulated sell amount (in 10,000 CNY)
    - 净额: Net amount (in 10,000 CNY)
    - 买入席位数: Number of buying seats
    - 卖出席位数: Number of selling seats
    
    
    中文: 新浪财经-龙虎榜-个股上榜统计
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 统计的时间周期，默认值为 "5"
           选项: "5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天
    
    返回:
    JSON格式数据，包含个股上榜统计信息，具有以下字段：
    - 股票代码: 股票代码
    - 股票名称: 股票名称
    - 上榜次数: 上榜次数
    - 累积购买额: 累积购买额（单位：万元）
    - 累积卖出额: 累积卖出额（单位：万元）
    - 净额: 净额（单位：万元）
    - 买入席位数: 买入席位数
    - 卖出席位数: 卖出席位数
    """
    try:
        df = ak.stock_lhb_ggtj_sina(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_hyyyb_em(start_date: str = "20220324", end_date: str = "20220324") -> str:
    """Get daily active brokerage departments from the Dragon-Tiger List from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    start_date: Start date in the format "YYYYMMDD", default is "20220324"
    end_date: End date in the format "YYYYMMDD", default is "20220324"
    
    Returns:
    JSON formatted data containing daily active brokerage department information with the following fields:
    - 序号: Serial number
    - 营业部名称: Brokerage department name
    - 上榜日: Listing date
    - 买入个股数: Number of stocks bought
    - 卖出个股数: Number of stocks sold
    - 买入总金额: Total purchase amount (in CNY)
    - 卖出总金额: Total sell amount (in CNY)
    - 总买卖净额: Total net buy-sell amount (in CNY)
    - 买入股票: Stocks purchased
    
    
    中文: 东方财富网-数据中心-龙虎榜单-每日活跃营业部
    
    返回 JSON 格式的数据。
    
    参数:
    start_date: 开始日期，格式为 "YYYYMMDD"，默认值为 "20220324"
    end_date: 结束日期，格式为 "YYYYMMDD"，默认值为 "20220324"
    
    返回:
    JSON格式数据，包含每日活跃营业部信息，具有以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 上榜日: 上榜日期
    - 买入个股数: 买入个股数
    - 卖出个股数: 卖出个股数
    - 买入总金额: 买入总金额（单位：元）
    - 卖出总金额: 卖出总金额（单位：元）
    - 总买卖净额: 总买卖净额（单位：元）
    - 买入股票: 买入的股票
    """
    try:
        df = ak.stock_lhb_hyyyb_em(start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_jgmmtj_em(start_date: str = "20240417", end_date: str = "20240430") -> str:
    """Get daily statistics of institutional buying and selling from the Dragon-Tiger List from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    start_date: Start date in the format "YYYYMMDD", default is "20240417"
    end_date: End date in the format "YYYYMMDD", default is "20240430"
    
    Returns:
    JSON formatted data containing daily statistics of institutional buying and selling with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 收盘价: Closing price
    - 涨跌幅: Price change percentage
    - 买方机构数: Number of buying institutions
    - 卖方机构数: Number of selling institutions
    - 机构买入总额: Total institutional purchase amount (in CNY)
    - 机构卖出总额: Total institutional sell amount (in CNY)
    - 机构买入净额: Net institutional purchase amount (in CNY)
    - 市场总成交额: Total market transaction amount (in CNY)
    - 机构净买额占总成交额比: Ratio of net institutional purchase to total transaction amount
    - 换手率: Turnover rate
    - 流通市值: Circulating market value (in 100 million CNY)
    - 上榜原因: Reason for listing
    - 上榜日期: Listing date
    
    
    中文: 东方财富网-数据中心-龙虎榜单-机构买卖每日统计
    
    返回 JSON 格式的数据。
    
    参数:
    start_date: 开始日期，格式为 "YYYYMMDD"，默认值为 "20240417"
    end_date: 结束日期，格式为 "YYYYMMDD"，默认值为 "20240430"
    
    返回:
    JSON格式数据，包含机构买卖每日统计信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 收盘价: 收盘价
    - 涨跌幅: 涨跌幅
    - 买方机构数: 买方机构数
    - 卖方机构数: 卖方机构数
    - 机构买入总额: 机构买入总额（单位：元）
    - 机构卖出总额: 机构卖出总额（单位：元）
    - 机构买入净额: 机构买入净额（单位：元）
    - 市场总成交额: 市场总成交额（单位：元）
    - 机构净买额占总成交额比: 机构净买额占总成交额比
    - 换手率: 换手率
    - 流通市值: 流通市值（单位：亿元）
    - 上榜原因: 上榜原因
    - 上榜日期: 上榜日期
    """
    try:
        df = ak.stock_lhb_jgmmtj_em(start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_jgmx_sina() -> str:
    """Get institutional seat transaction details from the Dragon-Tiger List from Sina Finance.
    
    Returns data in JSON format.
    
    This API retrieves detailed transaction information of institutional seats from Sina Finance's Dragon-Tiger List.
    No input parameters are required.
    
    Returns:
    JSON formatted data containing institutional seat transaction details with the following fields:
    - 股票代码: Stock code
    - 股票名称: Stock name
    - 交易日期: Trading date
    - 机构席位买入额: Institutional seat purchase amount (in 10,000 CNY)
    - 机构席位卖出额: Institutional seat sell amount (in 10,000 CNY)
    - 类型: Type
    
    
    中文: 新浪财经-龙虎榜-机构席位成交明细
    
    返回 JSON 格式的数据。
    
    该接口获取新浪财经龙虎榜中的机构席位成交详细信息。
    不需要输入参数。
    
    返回:
    JSON格式数据，包含机构席位成交明细信息，具有以下字段：
    - 股票代码: 股票代码
    - 股票名称: 股票名称
    - 交易日期: 交易日期
    - 机构席位买入额: 机构席位买入额（单位：万元）
    - 机构席位卖出额: 机构席位卖出额（单位：万元）
    - 类型: 类型
    """
    try:
        df = ak.stock_lhb_jgmx_sina()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_jgstatistic_em(symbol: str = "近一月") -> str:
    """Get institutional seat tracking from the Dragon-Tiger List from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Time period for statistics, default is "近一月" (last month)
           Options: "近一月" (last month), "近三月" (last three months), "近六月" (last six months), "近一年" (last year)
    
    Returns:
    JSON formatted data containing institutional seat tracking information with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 收盘价: Closing price
    - 涨跌幅: Price change percentage (%)
    - 龙虎榜成交金额: Dragon-Tiger List transaction amount (in CNY)
    - 上榜次数: Number of times listed
    - 机构买入额: Institutional purchase amount (in CNY)
    - 机构买入次数: Number of institutional purchases
    - 机构卖出额: Institutional sell amount (in CNY)
    - 机构卖出次数: Number of institutional sales
    - 机构净买额: Net institutional purchase amount (in CNY)
    - 近1个月涨跌幅: Price change percentage in the last month (%)
    - 近3个月涨跌幅: Price change percentage in the last 3 months (%)
    - 近6个月涨跌幅: Price change percentage in the last 6 months (%)
    - 近1年涨跌幅: Price change percentage in the last year (%)
    
    
    中文: 东方财富网-数据中心-龙虎榜单-机构席位追踪
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 统计的时间周期，默认值为 "近一月"
           选项: "近一月", "近三月", "近六月", "近一年"
    
    返回:
    JSON格式数据，包含机构席位追踪信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 收盘价: 收盘价
    - 涨跌幅: 涨跌幅（单位：%）
    - 龙虎榜成交金额: 龙虎榜成交金额（单位：元）
    - 上榜次数: 上榜次数
    - 机构买入额: 机构买入额（单位：元）
    - 机构买入次数: 机构买入次数
    - 机构卖出额: 机构卖出额（单位：元）
    - 机构卖出次数: 机构卖出次数
    - 机构净买额: 机构净买额（单位：元）
    - 近1个月涨跌幅: 近 1 个月涨跌幅（单位：%）
    - 近3个月涨跌幅: 近 3 个月涨跌幅（单位：%）
    - 近6个月涨跌幅: 近 6 个月涨跌幅（单位：%）
    - 近1年涨跌幅: 近 1 年涨跌幅（单位：%）
    """
    try:
        df = ak.stock_lhb_jgstatistic_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_jgzz_sina(symbol: str = "5") -> str:
    """Get institutional seat tracking from the Dragon-Tiger List from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Time period for statistics, default is "5"
           Options: "5": Last 5 days; "10": Last 10 days; "30": Last 30 days; "60": Last 60 days
    
    Returns:
    JSON formatted data containing institutional seat tracking information with the following fields:
    - 股票代码: Stock code
    - 股票名称: Stock name
    - 累积买入额: Accumulated purchase amount (in 10,000 CNY)
    - 买入次数: Number of purchases
    - 累积卖出额: Accumulated sell amount (in 10,000 CNY)
    - 卖出次数: Number of sales
    - 净额: Net amount (in 10,000 CNY)
    
    
    中文: 新浪财经-龙虎榜-机构席位追踪
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 统计的时间周期，默认值为 "5"
           选项: "5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天
    
    返回:
    JSON格式数据，包含机构席位追踪信息，具有以下字段：
    - 股票代码: 股票代码
    - 股票名称: 股票名称
    - 累积买入额: 累积买入额（单位：万元）
    - 买入次数: 买入次数
    - 累积卖出额: 累积卖出额（单位：万元）
    - 卖出次数: 卖出次数
    - 净额: 净额（单位：万元）
    """
    try:
        df = ak.stock_lhb_jgzz_sina(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_stock_detail_em(symbol: str = "600077", date: str = "20070416", flag: str = "买入") -> str:
    """Get individual stock Dragon-Tiger List details from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code, default is "600077"
    date: Date in the format "YYYYMMDD", default is "20070416"
          You need to get the available dates for a specific stock through the stock_lhb_stock_detail_date_em API
    flag: Type of transaction, default is "买入" (buy)
          Options: "买入" (buy), "卖出" (sell)
    
    Returns:
    JSON formatted data containing individual stock Dragon-Tiger List details with the following fields:
    - 序号: Serial number
    - 交易营业部名称: Trading branch name
    - 买入金额: Purchase amount
    - 买入金额-占总成交比例: Purchase amount - percentage of total transaction
    - 卖出金额-占总成交比例: Sell amount - percentage of total transaction
    - 净额: Net amount
    - 类型: Type (this field mainly deals with multiple Dragon-Tiger List standard issues)
    
    
    中文: 东方财富网-数据中心-龙虎榜单-个股龙虎榜详情
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 股票代码，默认值为 "600077"
    date: 日期，格式为 "YYYYMMDD"，默认值为 "20070416"
          需要通过 stock_lhb_stock_detail_date_em 接口获取相应股票的有龙虎榜详情数据的日期
    flag: 交易类型，默认值为 "买入"
          选项: "买入", "卖出"
    
    返回:
    JSON格式数据，包含个股龙虎榜详情信息，具有以下字段：
    - 序号: 序号
    - 交易营业部名称: 交易营业部名称
    - 买入金额: 买入金额
    - 买入金额-占总成交比例: 买入金额-占总成交比例
    - 卖出金额-占总成交比例: 卖出金额-占总成交比例
    - 净额: 净额
    - 类型: 类型（该字段主要处理多种龙虎榜标准问题）
    """
    try:
        df = ak.stock_lhb_stock_detail_em(symbol=symbol, date=date, flag=flag)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_stock_statistic_em(symbol: str = "近一月") -> str:
    """Get individual stock listing statistics from the Dragon-Tiger List from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Time period for statistics, default is "近一月" (last month)
           Options: "近一月" (last month), "近三月" (last three months), "近六月" (last six months), "近一年" (last year)
    
    Returns:
    JSON formatted data containing individual stock listing statistics with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最近上榜日: Most recent listing date
    - 收盘价: Closing price
    - 涨跌幅: Price change percentage
    - 上榜次数: Number of times listed
    - 龙虎榜净买额: Dragon-Tiger List net purchase amount
    - 龙虎榜买入额: Dragon-Tiger List purchase amount
    - 龙虎榜卖出额: Dragon-Tiger List sell amount
    - 龙虎榜总成交额: Dragon-Tiger List total transaction amount
    - 买方机构次数: Number of buying institutions
    - 卖方机构次数: Number of selling institutions
    - 机构买入净额: Net institutional purchase amount
    - 机构买入总额: Total institutional purchase amount
    - 机构卖出总额: Total institutional sell amount
    - 近1个月涨跌幅: Price change percentage in the last month
    - 近3个月涨跌幅: Price change percentage in the last 3 months
    - 近6个月涨跌幅: Price change percentage in the last 6 months
    - 近1年涨跌幅: Price change percentage in the last year
    
    
    中文: 东方财富网-数据中心-龙虎榜单-个股上榜统计
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 统计的时间周期，默认值为 "近一月"
           选项: "近一月", "近三月", "近六月", "近一年"
    
    返回:
    JSON格式数据，包含个股上榜统计信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最近上榜日: 最近上榜日期
    - 收盘价: 收盘价
    - 涨跌幅: 涨跌幅
    - 上榜次数: 上榜次数
    - 龙虎榜净买额: 龙虎榜净买额
    - 龙虎榜买入额: 龙虎榜买入额
    - 龙虎榜卖出额: 龙虎榜卖出额
    - 龙虎榜总成交额: 龙虎榜总成交额
    - 买方机构次数: 买方机构次数
    - 卖方机构次数: 卖方机构次数
    - 机构买入净额: 机构买入净额
    - 机构买入总额: 机构买入总额
    - 机构卖出总额: 机构卖出总额
    - 近1个月涨跌幅: 近 1 个月涨跌幅
    - 近3个月涨跌幅: 近 3 个月涨跌幅
    - 近6个月涨跌幅: 近 6 个月涨跌幅
    - 近1年涨跌幅: 近 1 年涨跌幅
    """
    try:
        df = ak.stock_lhb_stock_statistic_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_traderstatistic_em(symbol: str = "近一月") -> str:
    """Get trading department statistics from the Dragon-Tiger List from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Time period for statistics, default is "近一月" (last month)
           Options: "近一月" (last month), "近三月" (last three months), "近六月" (last six months), "近一年" (last year)
    
    Returns:
    JSON formatted data containing trading department statistics with the following fields:
    - 序号: Serial number
    - 营业部名称: Trading department name
    - 龙虎榜成交金额: Dragon-Tiger List transaction amount
    - 上榜次数: Number of times listed
    - 买入额: Purchase amount (unit: CNY)
    - 买入次数: Number of purchases
    - 卖出额: Sell amount (unit: CNY)
    - 卖出次数: Number of sales
    
    
    中文: 东方财富网-数据中心-龙虎榜单-营业部统计
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 统计的时间周期，默认值为 "近一月"
           选项: "近一月", "近三月", "近六月", "近一年"
    
    返回:
    JSON格式数据，包含营业部统计信息，具有以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 龙虎榜成交金额: 龙虎榜成交金额
    - 上榜次数: 上榜次数
    - 买入额: 买入额（单位：元）
    - 买入次数: 买入次数
    - 卖出额: 卖出额（单位：元）
    - 卖出次数: 卖出次数
    """
    try:
        df = ak.stock_lhb_traderstatistic_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_yybph_em(symbol: str = "近一月") -> str:
    """Get trading department rankings from the Dragon-Tiger List from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Time period for statistics, default is "近一月" (last month)
           Options: "近一月" (last month), "近三月" (last three months), "近六月" (last six months), "近一年" (last year)
    
    Returns:
    JSON formatted data containing trading department rankings with the following fields:
    - 序号: Serial number
    - 营业部名称: Trading department name
    - 上榜后1天-买入次数: Number of purchases after 1 day of listing
    - 上榜后1天-平均涨幅: Average price increase after 1 day of listing (unit: %)
    - 上榜后1天-上涨概率: Probability of price increase after 1 day of listing (unit: %)
    - 上榜后2天-买入次数: Number of purchases after 2 days of listing
    - 上榜后2天-平均涨幅: Average price increase after 2 days of listing (unit: %)
    - 上榜后2天-上涨概率: Probability of price increase after 2 days of listing (unit: %)
    - 上榜后3天-买入次数: Number of purchases after 3 days of listing
    - 上榜后3天-平均涨幅: Average price increase after 3 days of listing (unit: %)
    - 上榜后3天-上涨概率: Probability of price increase after 3 days of listing (unit: %)
    - 上榜后4天-买入次数: Number of purchases after 4 days of listing
    - 上榜后4天-平均涨幅: Average price increase after 4 days of listing (unit: %)
    - 上榜后4天-上涨概率: Probability of price increase after 4 days of listing (unit: %)
    - 上榜后10天-买入次数: Number of purchases after 10 days of listing
    - 上榜后10天-平均涨幅: Average price increase after 10 days of listing (unit: %)
    - 上榜后10天-上涨概率: Probability of price increase after 10 days of listing (unit: %)
    
    
    中文: 东方财富网-数据中心-龙虎榜单-营业部排行
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 统计的时间周期，默认值为 "近一月"
           选项: "近一月", "近三月", "近六月", "近一年"
    
    返回:
    JSON格式数据，包含营业部排行信息，具有以下字段：
    - 序号: 序号
    - 营业部名称: 营业部名称
    - 上榜后1天-买入次数: 上榜后 1 天买入次数
    - 上榜后1天-平均涨幅: 上榜后 1 天平均涨幅（单位：%）
    - 上榜后1天-上涨概率: 上榜后 1 天上涨概率（单位：%）
    - 上榜后2天-买入次数: 上榜后 2 天买入次数
    - 上榜后2天-平均涨幅: 上榜后 2 天平均涨幅（单位：%）
    - 上榜后2天-上涨概率: 上榜后 2 天上涨概率（单位：%）
    - 上榜后3天-买入次数: 上榜后 3 天买入次数
    - 上榜后3天-平均涨幅: 上榜后 3 天平均涨幅（单位：%）
    - 上榜后3天-上涨概率: 上榜后 3 天上涨概率（单位：%）
    - 上榜后4天-买入次数: 上榜后 4 天买入次数
    - 上榜后4天-平均涨幅: 上榜后 4 天平均涨幅（单位：%）
    - 上榜后4天-上涨概率: 上榜后 4 天上涨概率（单位：%）
    - 上榜后10天-买入次数: 上榜后 10 天买入次数
    - 上榜后10天-平均涨幅: 上榜后 10 天平均涨幅（单位：%）
    - 上榜后10天-上涨概率: 上榜后 10 天上涨概率（单位：%）
    """
    try:
        df = ak.stock_lhb_yybph_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lhb_yytj_sina(symbol: str = "5") -> str:
    """Get trading department listing statistics from the Dragon-Tiger List from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Time period for statistics, default is "5"
           Options: "5": Last 5 days; "10": Last 10 days; "30": Last 30 days; "60": Last 60 days
    
    Returns:
    JSON formatted data containing trading department listing statistics with the following fields:
    - 营业部名称: Trading department name
    - 上榜次数: Number of times listed
    - 累积购买额: Accumulated purchase amount (in 10,000 CNY)
    - 买入席位数: Number of buying seats
    - 累积卖出额: Accumulated sell amount (in 10,000 CNY)
    - 卖出席位数: Number of selling seats
    - 买入前三股票: Top three stocks purchased
    
    
    中文: 新浪财经-龙虎榜-营业上榜统计
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 统计的时间周期，默认值为 "5"
           选项: "5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天
    
    返回:
    JSON格式数据，包含营业上榜统计信息，具有以下字段：
    - 营业部名称: 营业部名称
    - 上榜次数: 上榜次数
    - 累积购买额: 累积购买额（单位：万元）
    - 买入席位数: 买入席位数
    - 累积卖出额: 累积卖出额（单位：万元）
    - 卖出席位数: 卖出席位数
    - 买入前三股票: 买入前三股票
    """
    try:
        df = ak.stock_lhb_yytj_sina(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_lrb_em(date: str = "20240331") -> str:
    """Get income statement data from East Money's data center for annual and quarterly reports.
    
    Returns data in JSON format.
    
    Parameters:
    date: Date in the format "YYYYMMDD", default is "20240331"
          Options: "XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"
          Available from 20120331 onwards
    
    Returns:
    JSON formatted data containing income statement information with the following fields:
    - 序号: Serial number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 净利润: Net profit (unit: CNY)
    - 净利润同比: Year-on-year change in net profit (unit: %)
    - 营业总收入: Total operating income (unit: CNY)
    - 营业总收入同比: Year-on-year change in total operating income (unit: %)
    - 营业总支出-营业支出: Total operating expenses - Operating expenses (unit: CNY)
    - 营业总支出-销售费用: Total operating expenses - Selling expenses (unit: CNY)
    - 营业总支出-管理费用: Total operating expenses - Administrative expenses (unit: CNY)
    - 营业总支出-财务费用: Total operating expenses - Financial expenses (unit: CNY)
    - 营业总支出-营业总支出: Total operating expenses - Total operating expenses (unit: CNY)
    - 营业利润: Operating profit (unit: CNY)
    - 利润总额: Total profit (unit: CNY)
    - 公告日期: Announcement date
    
    
    中文: 东方财富-数据中心-年报季报-业绩快报-利润表
    
    返回 JSON 格式的数据。
    
    参数:
    date: 日期，格式为 "YYYYMMDD"，默认值为 "20240331"
          选项: "XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"
          可用日期从 20120331 开始
    
    返回:
    JSON格式数据，包含利润表信息，具有以下字段：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 净利润: 净利润（单位：元）
    - 净利润同比: 净利润同比（单位：%）
    - 营业总收入: 营业总收入（单位：元）
    - 营业总收入同比: 营业总收入同比（单位：%）
    - 营业总支出-营业支出: 营业总支出-营业支出（单位：元）
    - 营业总支出-销售费用: 营业总支出-销售费用（单位：元）
    - 营业总支出-管理费用: 营业总支出-管理费用（单位：元）
    - 营业总支出-财务费用: 营业总支出-财务费用（单位：元）
    - 营业总支出-营业总支出: 营业总支出-营业总支出（单位：元）
    - 营业利润: 营业利润（单位：元）
    - 利润总额: 利润总额（单位：元）
    - 公告日期: 公告日期
    """
    try:
        df = ak.stock_lrb_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_main_fund_flow(symbol: str = "全部股票") -> str:
    """Get main capital inflow ranking data from East Money's data center.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock category, default is "全部股票" (All stocks)
           Options: "全部股票" (All stocks), "沪深A股" (Shanghai and Shenzhen A shares), "沪A股" (Shanghai A shares), 
                   "科创板" (STAR Market), "深市A股" (Shenzhen A shares), "创业板" (ChiNext), 
                   "沪B股" (Shanghai B shares), "深市B股" (Shenzhen B shares)
    
    Returns:
    JSON formatted data containing main capital inflow ranking with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 今日排行榜-主力净占比: Today's ranking - Main capital net proportion (unit: %)
    - 今日排行榜-今日排名: Today's ranking - Today's rank
    - 今日排行榜-今日涨跌: Today's ranking - Today's change (unit: %)
    - 5日排行榜-主力净占比: 5-day ranking - Main capital net proportion (unit: %)
    - 5日排行榜-5日排名: 5-day ranking - 5-day rank
    - 5日排行榜-5日涨跌: 5-day ranking - 5-day change (unit: %)
    - 10日排行榜-主力净占比: 10-day ranking - Main capital net proportion (unit: %)
    - 10日排行榜-10日排名: 10-day ranking - 10-day rank
    - 10日排行榜-10日涨跌: 10-day ranking - 10-day change (unit: %)
    - 所属板块: Sector
    
    
    中文: 东方财富网-数据中心-资金流向-主力净流入排名
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 股票类别，默认值为 "全部股票"
           选项: "全部股票", "沪深A股", "沪A股", "科创板", "深市A股", "创业板", "沪B股", "深市B股"
    
    返回:
    JSON格式数据，包含主力资金流入排名信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价
    - 今日排行榜-主力净占比: 今日排行榜-主力净占比（单位：%）
    - 今日排行榜-今日排名: 今日排行榜-今日排名
    - 今日排行榜-今日涨跌: 今日排行榜-今日涨跌（单位：%）
    - 5日排行榜-主力净占比: 5日排行榜-主力净占比（单位：%）
    - 5日排行榜-5日排名: 5日排行榜-5日排名
    - 5日排行榜-5日涨跌: 5日排行榜-5日涨跌（单位：%）
    - 10日排行榜-主力净占比: 10日排行榜-主力净占比（单位：%）
    - 10日排行榜-10日排名: 10日排行榜-10日排名
    - 10日排行榜-10日涨跌: 10日排行榜-10日涨跌（单位：%）
    - 所属板块: 所属板块
    """
    try:
        df = ak.stock_main_fund_flow(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_main_stock_holder(stock: str = "600004") -> str:
    """Get main shareholders data from Sina Finance.
    
    Returns data in JSON format.
    
    Parameters:
    stock: Stock code, default is "600004"
    
    Returns:
    JSON formatted data containing main shareholders information with the following fields:
    - 编号: Serial number
    - 股东名称: Shareholder name
    - 持股数量: Number of shares held (unit: shares)
    - 持股比例: Shareholding ratio (unit: %)
    - 股本性质: Nature of shares
    - 截至日期: Date as of
    - 公告日期: Announcement date
    - 股东说明: Shareholder description
    - 股东总数: Total number of shareholders
    - 平均持股数: Average number of shares held (calculated based on total share capital)
    
    
    中文: 新浪财经-股本股东-主要股东
    
    返回 JSON 格式的数据。
    
    参数:
    stock: 股票代码，默认值为 "600004"
    
    返回:
    JSON格式数据，包含主要股东信息，具有以下字段：
    - 编号: 编号
    - 股东名称: 股东名称
    - 持股数量: 持股数量（单位：股）
    - 持股比例: 持股比例（单位：%）
    - 股本性质: 股本性质
    - 截至日期: 截至日期
    - 公告日期: 公告日期
    - 股东说明: 股东说明
    - 股东总数: 股东总数
    - 平均持股数: 平均持股数（按总股本计算）
    """
    try:
        df = ak.stock_main_stock_holder(stock=stock)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_management_change_ths(symbol: str = "688981") -> str:
    """Get executive shareholding changes from TongHuaShun's company major events data.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code, default is "688981"
    
    Returns:
    JSON formatted data containing executive shareholding changes with the following fields:
    - 公告日期: Announcement date
    - 变动人: Person making the change
    - 与公司高管关系: Relationship with company executives
    - 变动数量: Change in number of shares (unit: shares)
    - 交易均价: Average transaction price (unit: CNY)
    - 剩余股数: Remaining number of shares (unit: shares)
    - 变动途径: Method of change
    
    
    中文: 同花顺-公司大事-高管持股变动
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 股票代码，默认值为 "688981"
    
    返回:
    JSON格式数据，包含高管持股变动信息，具有以下字段：
    - 公告日期: 公告日期
    - 变动人: 变动人
    - 与公司高管关系: 与公司高管关系
    - 变动数量: 变动数量（单位：股）
    - 交易均价: 交易均价（单位：元）
    - 剩余股数: 剩余股数（单位：股）
    - 变动途径: 变动途径
    """
    try:
        df = ak.stock_management_change_ths(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_margin_account_info() -> str:
    """Get margin trading account statistics from East Money's data center.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data containing margin trading account statistics with the following fields:
    - 日期: Date
    - 融资余额: Margin financing balance (unit: 100 million CNY)
    - 融券余额: Securities lending balance (unit: 100 million CNY)
    - 融资买入额: Margin financing purchase amount (unit: 100 million CNY)
    - 融券卖出额: Securities lending sales amount (unit: 100 million CNY)
    - 证券公司数量: Number of securities companies (unit: companies)
    - 营业部数量: Number of business departments (unit: departments)
    - 个人投资者数量: Number of individual investors (unit: 10,000 persons)
    - 机构投资者数量: Number of institutional investors (unit: institutions)
    - 参与交易的投资者数量: Number of investors participating in trading (unit: persons)
    - 有融资融券负债的投资者数量: Number of investors with margin trading debt (unit: persons)
    - 担保物总价值: Total value of collateral (unit: 100 million CNY)
    - 平均维持担保比例: Average maintenance margin ratio (unit: %)
    
    
    中文: 东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含融资融券账户统计信息，具有以下字段：
    - 日期: 日期
    - 融资余额: 融资余额（单位：亿元）
    - 融券余额: 融券余额（单位：亿元）
    - 融资买入额: 融资买入额（单位：亿元）
    - 融券卖出额: 融券卖出额（单位：亿元）
    - 证券公司数量: 证券公司数量（单位：家）
    - 营业部数量: 营业部数量（单位：家）
    - 个人投资者数量: 个人投资者数量（单位：万名）
    - 机构投资者数量: 机构投资者数量（单位：家）
    - 参与交易的投资者数量: 参与交易的投资者数量（单位：名）
    - 有融资融券负债的投资者数量: 有融资融券负债的投资者数量（单位：名）
    - 担保物总价值: 担保物总价值（单位：亿元）
    - 平均维持担保比例: 平均维持担保比例（单位：%）
    """
    try:
        df = ak.stock_margin_account_info()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_margin_detail_sse(date: str = "20230922") -> str:
    """Get margin trading detailed data from the Shanghai Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    date: Date in the format "YYYYMMDD", default is "20230922"
    
    Returns:
    JSON formatted data containing margin trading details with the following fields:
    - 信用交易日期: Credit trading date
    - 标的证券代码: Target security code
    - 标的证券简称: Target security name
    - 融资余额: Margin financing balance (unit: CNY)
    - 融资买入额: Margin financing purchase amount (unit: CNY)
    - 融资偿还额: Margin financing repayment amount (unit: CNY)
    - 融券余量: Securities lending balance (unit: shares)
    - 融券卖出量: Securities lending sales volume (unit: shares)
    - 融券偿还量: Securities lending repayment volume (unit: shares)
    
    
    中文: 上海证券交易所-融资融券数据-融资融券明细数据
    
    返回 JSON 格式的数据。
    
    参数:
    date: 日期，格式为 "YYYYMMDD"，默认值为 "20230922"
    
    返回:
    JSON格式数据，包含融资融券明细信息，具有以下字段：
    - 信用交易日期: 信用交易日期
    - 标的证券代码: 标的证券代码
    - 标的证券简称: 标的证券简称
    - 融资余额: 融资余额（单位：元）
    - 融资买入额: 融资买入额（单位：元）
    - 融资偿还额: 融资偿还额（单位：元）
    - 融券余量: 融券余量
    - 融券卖出量: 融券卖出量
    - 融券偿还量: 融券偿还量
    """
    try:
        df = ak.stock_margin_detail_sse(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_margin_detail_szse(date: str = "20230925") -> str:
    """Get margin trading detailed data from the Shenzhen Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    date: Date in the format "YYYYMMDD", default is "20230925"
    
    Returns:
    JSON formatted data containing margin trading details with the following fields:
    - 证券代码: Security code
    - 证券简称: Security name
    - 融资买入额: Margin financing purchase amount (unit: CNY)
    - 融资余额: Margin financing balance (unit: CNY)
    - 融券卖出量: Securities lending sales volume (unit: shares/units)
    - 融券余量: Securities lending balance (unit: shares/units)
    - 融券余额: Securities lending balance (unit: CNY)
    - 融资融券余额: Margin trading balance (unit: CNY)
    
    
    中文: 深证证券交易所-融资融券数据-融资融券交易明细数据
    
    返回 JSON 格式的数据。
    
    参数:
    date: 日期，格式为 "YYYYMMDD"，默认值为 "20230925"
    
    返回:
    JSON格式数据，包含融资融券交易明细信息，具有以下字段：
    - 证券代码: 证券代码
    - 证券简称: 证券简称
    - 融资买入额: 融资买入额（单位：元）
    - 融资余额: 融资余额（单位：元）
    - 融券卖出量: 融券卖出量（单位：股/份）
    - 融券余量: 融券余量（单位：股/份）
    - 融券余额: 融券余额（单位：元）
    - 融资融券余额: 融资融券余额（单位：元）
    """
    try:
        df = ak.stock_margin_detail_szse(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_margin_ratio_pa(date: str = "20231013") -> str:
    """Get margin trading target securities list and margin ratio query.
    
    Returns data in JSON format.
    
    Parameters:
    date: Date in the format "YYYYMMDD", default is "20231013"
    
    Returns:
    JSON formatted data containing margin trading target securities and their margin ratios with the following fields:
    - 证券代码: Security code
    - 证券简称: Security name
    - 融资比例: Financing ratio
    - 融券比例: Securities lending ratio
    
    
    中文: 融资融券-标的证券名单及保证金比例查询
    
    返回 JSON 格式的数据。
    
    参数:
    date: 日期，格式为 "YYYYMMDD"，默认值为 "20231013"
    
    返回:
    JSON格式数据，包含融资融券标的证券及其保证金比例，具有以下字段：
    - 证券代码: 证券代码
    - 证券简称: 证券简称
    - 融资比例: 融资比例
    - 融券比例: 融券比例
    """
    try:
        df = ak.stock_margin_ratio_pa(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_margin_szse(date: str = "20240411") -> str:
    """Get margin trading summary data from the Shenzhen Stock Exchange.
    
    Returns data in JSON format.
    
    Parameters:
    date: Date in the format "YYYYMMDD", default is "20240411"
    
    Returns:
    JSON formatted data containing margin trading summary with the following fields:
    - 融资买入额: Margin financing purchase amount (unit: 100 million CNY)
    - 融资余额: Margin financing balance (unit: 100 million CNY)
    - 融券卖出量: Securities lending sales volume (unit: 100 million shares/units)
    - 融券余量: Securities lending balance (unit: 100 million shares/units)
    - 融券余额: Securities lending balance (unit: 100 million CNY)
    - 融资融券余额: Margin trading balance (unit: 100 million CNY)
    
    
    中文: 深圳证券交易所-融资融券数据-融资融券汇总数据
    
    返回 JSON 格式的数据。
    
    参数:
    date: 日期，格式为 "YYYYMMDD"，默认值为 "20240411"
    
    返回:
    JSON格式数据，包含融资融券汇总信息，具有以下字段：
    - 融资买入额: 融资买入额（单位：亿元）
    - 融资余额: 融资余额（单位：亿元）
    - 融券卖出量: 融券卖出量（单位：亿股/亿份）
    - 融券余量: 融券余量（单位：亿股/亿份）
    - 融券余额: 融券余额（单位：亿元）
    - 融资融券余额: 融资融券余额（单位：亿元）
    """
    try:
        df = ak.stock_margin_szse(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_market_pb_lg(symbol: str = "上证") -> str:
    """Get price-to-book ratio data for main stock markets from LeGuLeGu.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Market symbol, default is "上证" (Shanghai). Options include "上证" (Shanghai), "深证" (Shenzhen), "创业板" (ChiNext), "科创版" (STAR Market)
    
    Returns:
    JSON formatted data containing price-to-book ratio information with the following fields:
    - 日期: Date
    - 指数: Index value
    - 市净率: Price-to-book ratio
    - 等权市净率: Equal-weighted price-to-book ratio
    - 市净率中位数: Median price-to-book ratio
    
    
    中文: 乐咕乐股-主板市净率
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 市场符号，默认值为 "上证"。选项包括 "上证"，"深证"，"创业板"，"科创版"
    
    返回:
    JSON格式数据，包含市净率信息，具有以下字段：
    - 日期: 日期
    - 指数: 指数值
    - 市净率: 市净率
    - 等权市净率: 等权市净率
    - 市净率中位数: 市净率中位数
    """
    try:
        df = ak.stock_market_pb_lg(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_market_pe_lg(symbol: str = "上证") -> str:
    """Get price-to-earnings ratio data for main stock markets from LeGuLeGu.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Market symbol, default is "上证" (Shanghai). Options include "上证" (Shanghai), "深证" (Shenzhen), "创业板" (ChiNext), "科创版" (STAR Market)
    
    Returns:
    JSON formatted data containing price-to-earnings ratio information with the following fields:
    - 日期: Date
    - 指数: Index value
    - 平均市盈率: Average price-to-earnings ratio
    
    
    中文: 乐咕乐股-主板市盈率
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 市场符号，默认值为 "上证"。选项包括 "上证"（上海），"深证"（深圳），"创业板"（创业板），"科创版"（科创板）
    
    返回:
    JSON格式数据，包含市盈率信息，具有以下字段：
    - 日期: 日期
    - 指数: 指数值
    - 平均市盈率: 平均市盈率
    """
    try:
        df = ak.stock_market_pe_lg(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_mda_ym(symbol: str = "000001") -> str:
    """Get management discussion and analysis (MDA) data from EMoney F10.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code, default is "000001"
    
    Returns:
    JSON formatted data containing management discussion and analysis with the following fields:
    - 报告期: Reporting period
    - 内容: Content of the management discussion and analysis
    
    
    中文: 益盟-F10-管理层讨论与分析
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 股票代码，默认值为 "000001"
    
    返回:
    JSON格式数据，包含管理层讨论与分析信息，具有以下字段：
    - 报告期: 报告期
    - 内容: 管理层讨论与分析内容
    """
    try:
        df = ak.stock_mda_ym(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_new_a_spot_em() -> str:
    """Get real-time market data for newly listed A-shares from East Money.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data containing real-time market information for newly listed stocks with the following fields:
    - 序号: Sequence number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Price change percentage (%)
    - 涨跌额: Price change amount
    - 成交量: Trading volume (hands)
    - 成交额: Trading value (CNY)
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Opening price today
    - 昨收: Closing price yesterday
    - 量比: Volume ratio
    - 换手率: Turnover rate (%)
    - 市盈率-动态: Dynamic price-to-earnings ratio
    - 市净率: Price-to-book ratio
    - 上市时间: Listing time
    - 总市值: Total market value (CNY)
    - 流通市值: Circulating market value (CNY)
    - 涨速: Price change speed
    - 5分钟涨跌: 5-minute price change (%)
    - 60日涨跌幅: 60-day price change (%)
    - 年初至今涨跌幅: Year-to-date price change (%)
    
    
    中文: 东方财富网-新股-实时行情数据
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含新上市股票的实时行情信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格
    - 涨跌幅: 价格变化百分比 (%)
    - 涨跌额: 价格变化金额
    - 成交量: 交易量 (手)
    - 成交额: 交易金额 (元)
    - 振幅: 振幅 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 今日开盘价
    - 昨收: 昨日收盘价
    - 量比: 量比
    - 换手率: 换手率 (%)
    - 市盈率-动态: 动态市盈率
    - 市净率: 市净率
    - 上市时间: 上市时间
    - 总市值: 总市值 (元)
    - 流通市值: 流通市值 (元)
    - 涨速: 涨速
    - 5分钟涨跌: 5分钟涨跌幅 (%)
    - 60日涨跌幅: 60日涨跌幅 (%)
    - 年初至今涨跌幅: 年初至今涨跌幅 (%)
    """
    try:
        df = ak.stock_new_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_new_gh_cninfo() -> str:
    """Get data on newly approved IPO stocks from CNINFO (China Securities Regulatory Commission).
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data containing information about newly approved IPO stocks with the following fields:
    - 公司名称: Company name
    - 上会日期: Meeting date
    - 审核类型: Review type
    - 审议内容: Review content
    - 审核结果: Review result
    - 审核公告日: Review announcement date
    
    
    中文: 巨潮资讯-数据中心-新股数据-新股过会
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含新股过会信息，具有以下字段：
    - 公司名称: 公司名称
    - 上会日期: 上会日期
    - 审核类型: 审核类型
    - 审议内容: 审议内容
    - 审核结果: 审核结果
    - 审核公告日: 审核公告日
    """
    try:
        df = ak.stock_new_gh_cninfo()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_new_ipo_cninfo() -> str:
    """Get data on new IPO issuances from CNINFO (China Securities Regulatory Commission).
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data containing information about new IPO issuances with the following fields:
    - 证劳代码: Security code
    - 证券简称: Security abbreviation
    - 上市日期: Listing date
    - 申购日期: Subscription date
    - 发行价: Issue price (CNY)
    - 总发行数量: Total issuance volume (10,000 shares)
    - 发行市盈率: Issue price-to-earnings ratio
    - 上网发行中签率: Online issuance winning rate (%)
    - 摇号结果公告日: Lottery result announcement date
    - 中签公告日: Winning announcement date
    - 中签缴款日: Payment date for winning subscriptions
    - 网上申购上限: Online subscription limit
    - 上网发行数量: Online issuance volume
    
    
    中文: 巨潮资讯-数据中心-新股数据-新股发行
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含新股发行信息，具有以下字段：
    - 证劳代码: 证券代码
    - 证券简称: 证券简称
    - 上市日期: 上市日期
    - 申购日期: 申购日期
    - 发行价: 发行价格 (元)
    - 总发行数量: 总发行数量 (万股)
    - 发行市盈率: 发行市盈率
    - 上网发行中签率: 上网发行中签率 (%)
    - 摇号结果公告日: 摇号结果公告日
    - 中签公告日: 中签公告日
    - 中签缴款日: 中签缴款日
    - 网上申购上限: 网上申购上限
    - 上网发行数量: 上网发行数量
    """
    try:
        df = ak.stock_new_ipo_cninfo()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_news_main_cx() -> str:
    """Get featured content from Caixin Data - a financial news and data platform.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data containing featured news content with the following fields:
    - tag: News category or tag
    - summary: Summary of the news content
    - interval_time: Time interval information
    - pub_time: Publication time
    - url: URL to the full news article
    
    
    中文: 财新网-财新数据通-内容精选
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含精选新闻内容，具有以下字段：
    - tag: 新闻分类或标签
    - summary: 新闻内容摘要
    - interval_time: 时间间隔信息
    - pub_time: 发布时间
    - url: 新闻文章完整链接
    """
    try:
        df = ak.stock_news_main_cx()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_pg_em() -> str:
    """Get rights issue data from East Money Data Center.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data containing rights issue information with the following fields:
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 配售代码: Rights issue code
    - 配股数量: Number of rights shares (shares)
    - 配股比例: Rights issue ratio
    - 配股价: Rights issue price
    - 最新价: Latest price
    - 配股前总股本: Total share capital before rights issue (shares)
    - 配股后总股本: Total share capital after rights issue (shares)
    - 股权登记日: Record date
    - 缴款起始日期: Payment start date
    - 缴款截止日期: Payment end date
    - 上市日: Listing date
    
    
    中文: 东方财富网-数据中心-新股数据-配股
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含配股信息，具有以下字段：
    - 股票代码: 股票代码
    - 股票简称: 股票简称
    - 配售代码: 配售代码
    - 配股数量: 配股数量 (股)
    - 配股比例: 配股比例
    - 配股价: 配股价格
    - 最新价: 最新价格
    - 配股前总股本: 配股前总股本 (股)
    - 配股后总股本: 配股后总股本 (股)
    - 股权登记日: 股权登记日
    - 缴款起始日期: 缴款起始日期
    - 缴款截止日期: 缴款截止日期
    - 上市日: 上市日期
    """
    try:
        df = ak.stock_pg_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_price_js(symbol: str = "us") -> str:
    """Get target price data for US and Hong Kong stocks from USHK News.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Market symbol, default is "us". Options include "us" (United States) and "hk" (Hong Kong)
    
    Returns:
    JSON formatted data containing target price information with the following fields:
    - 日期: Date
    - 个股名称: Stock name
    - 评级: Rating
    - 先前目标价: Previous target price
    - 最新目标价: Latest target price
    - 机构名称: Institution name
    
    Note: This API may not be currently available. Data available from 2019 to present.
    
    
    中文: 美港电讯-美港目标价数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 市场符号，默认值为 "us"。选项包括 "us" (美国) 和 "hk" (香港)
    
    返回:
    JSON格式数据，包含目标价格信息，具有以下字段：
    - 日期: 日期
    - 个股名称: 股票名称
    - 评级: 评级
    - 先前目标价: 先前目标价
    - 最新目标价: 最新目标价
    - 机构名称: 机构名称
    
    注意: 此API可能目前不可用。数据可用从2019年至今。
    """
    try:
        df = ak.stock_price_js(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_profile_cninfo(symbol: str = "600030") -> str:
    """Get company profile information from CNINFO for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code, default is "600030" (China Merchants Securities)
    
    Returns:
    JSON formatted data containing company profile information with the following fields:
    - 公司名称: Company name
    - 英文名称: English name
    - 曾用简称: Former abbreviation
    - A股代码: A-share code
    - A股简称: A-share abbreviation
    - B股代码: B-share code
    - B股简称: B-share abbreviation
    - H股代码: H-share code
    - H股简称: H-share abbreviation
    - 入选指数: Selected indices
    - 所属市场: Market
    - 所属行业: Industry
    - 法人代表: Legal representative
    - 注册资金: Registered capital
    - 成立日期: Establishment date
    - 上市日期: Listing date
    - 官方网站: Official website
    - 电子邮箱: Email
    - 联系电话: Contact phone
    - 传真: Fax
    - 注册地址: Registered address
    - 办公地址: Office address
    - 邮政编码: Postal code
    - 主营业务: Main business
    - 经营范围: Business scope
    - 机构简介: Institution introduction
    
    
    中文: 巨潮资讯-个股-公司概况
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 股票代码，默认值为 "600030" (中信证券)
    
    返回:
    JSON格式数据，包含公司概况信息，具有以下字段：
    - 公司名称: 公司名称
    - 英文名称: 英文名称
    - 曾用简称: 曾用简称
    - A股代码: A股代码
    - A股简称: A股简称
    - B股代码: B股代码
    - B股简称: B股简称
    - H股代码: H股代码
    - H股简称: H股简称
    - 入选指数: 入选指数
    - 所属市场: 所属市场
    - 所属行业: 所属行业
    - 法人代表: 法人代表
    - 注册资金: 注册资金
    - 成立日期: 成立日期
    - 上市日期: 上市日期
    - 官方网站: 官方网站
    - 电子邮箱: 电子邮箱
    - 联系电话: 联系电话
    - 传真: 传真
    - 注册地址: 注册地址
    - 办公地址: 办公地址
    - 邮政编码: 邮政编码
    - 主营业务: 主营业务
    - 经营范围: 经营范围
    - 机构简介: 机构简介
    """
    try:
        df = ak.stock_profile_cninfo(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_profit_forecast_em() -> str:
    """Get profit forecast data from East Money Data Center's Research Reports.
    
    Returns data in JSON format. Note: This API fixes anomalies in the original web data source.
    
    Returns:
    JSON formatted data containing profit forecast information with the following fields:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 研报数: Number of research reports
    - 机构投资评级(近六个月)-买入: Investment rating (last 6 months) - Buy
    - 机构投资评级(近六个月)-增持: Investment rating (last 6 months) - Increase holdings
    - 机构投资评级(近六个月)-中性: Investment rating (last 6 months) - Neutral
    - 机构投资评级(近六个月)-减持: Investment rating (last 6 months) - Reduce holdings
    - 机构投资评级(近六个月)-卖出: Investment rating (last 6 months) - Sell
    - xxxx预测每股收益: Forecasted earnings per share for various years
    
    
    中文: 东方财富网-数据中心-研究报告-盈利预测
    
    返回 JSON 格式的数据。注意：此API修复了原始网页数据源中的异常。
    
    返回:
    JSON格式数据，包含盈利预测信息，具有以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 研报数: 研究报告数量
    - 机构投资评级(近六个月)-买入: 投资评级(近六个月) - 买入
    - 机构投资评级(近六个月)-增持: 投资评级(近六个月) - 增持
    - 机构投资评级(近六个月)-中性: 投资评级(近六个月) - 中性
    - 机构投资评级(近六个月)-减持: 投资评级(近六个月) - 减持
    - 机构投资评级(近六个月)-卖出: 投资评级(近六个月) - 卖出
    - xxxx预测每股收益: 不同年份的预测每股收益
    """
    try:
        df = ak.stock_profit_forecast_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_profit_forecast_ths(symbol: str = "600519", indicator: str = "预测年报每股收益") -> str:
    """Get profit forecast data from TongHuaShun (10jqka) for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code, default is "600519" (Kweichow Moutai)
    indicator: Forecast indicator type, default is "预测年报每股收益" (Forecasted annual EPS)
              Options include: "预测年报每股收益" (Forecasted annual EPS),
              "预测年报净利润" (Forecasted annual net profit),
              "业绩预测详表-机构" (Performance forecast details - Institutions),
              "业绩预测详表-详细指标预测" (Performance forecast details - Detailed indicators)
    
    Returns:
    JSON formatted data containing profit forecast information. For "预测年报每股收益" indicator, the fields include:
    - 年度: Year
    - 预测机构数: Number of forecasting institutions
    - 最小值: Minimum value
    - 均值: Average value
    - 最大值: Maximum value
    - 行业平均数: Industry average
    
    Note: The output fields may vary depending on the selected indicator.
    
    
    中文: 同花顺-盈利预测
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 股票代码，默认值为 "600519" (贵州茅台)
    indicator: 预测指标类型，默认值为 "预测年报每股收益"
              选项包括："预测年报每股收益" (预测年报每股收益),
              "预测年报净利润" (预测年报净利润),
              "业绩预测详表-机构" (业绩预测详表-机构),
              "业绩预测详表-详细指标预测" (业绩预测详表-详细指标预测)
    
    返回:
    JSON格式数据，包含盈利预测信息。对于 "预测年报每股收益" 指标，字段包括：
    - 年度: 年度
    - 预测机构数: 预测机构数量
    - 最小值: 最小值
    - 均值: 平均值
    - 最大值: 最大值
    - 行业平均数: 行业平均数
    
    注意：输出字段可能因所选指标而异。
    """
    try:
        df = ak.stock_profit_forecast_ths(symbol=symbol, indicator=indicator)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_profit_sheet_by_quarterly_em(symbol: str = "SH600519") -> str:
    """Get quarterly profit sheet data from East Money for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code with exchange prefix, default is "SH600519" (Kweichow Moutai)
           Format should be: SH for Shanghai stocks, SZ for Shenzhen stocks
    
    Returns:
    JSON formatted data containing the quarterly profit sheet with approximately 204 financial indicators
    including revenue, operating costs, gross profit, net profit, and many other financial metrics.
    
    Note: The output contains a comprehensive set of financial indicators (204 items) that are not listed
    individually in this documentation due to their extensive nature.
    
    
    中文: 东方财富-股票-财务分析-利润表-按单季度
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 带有交易所前缀的股票代码，默认值为 "SH600519" (贵州茅台)
           格式应为：SH 代表上海股票，SZ 代表深圳股票
    
    返回:
    JSON格式数据，包含单季度利润表，大约有204个财务指标，
    包括营业收入、营业成本、毛利润、净利润等多种财务指标。
    
    注意：输出包含大量财务指标（204项），由于数量庞大，本文档中不逐一列出。
    """
    try:
        df = ak.stock_profit_sheet_by_quarterly_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_profit_sheet_by_report_delisted_em(symbol: str = "SZ000013") -> str:
    """Get profit sheet data by reporting period for delisted stocks from East Money.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code with exchange prefix for a delisted stock, default is "SZ000013" (Shenzhen Petrochemical)
           Format should be: SH for Shanghai stocks, SZ for Shenzhen stocks
    
    Returns:
    JSON formatted data containing the profit sheet with approximately 203 financial indicators
    including revenue, operating costs, gross profit, net profit, and many other financial metrics.
    
    Note: The output contains a comprehensive set of financial indicators (203 items) that are not listed
    individually in this documentation due to their extensive nature.
    
    
    中文: 东方财富-股票-财务分析-利润表-已退市股票-按报告期
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 带有交易所前缀的已退市股票代码，默认值为 "SZ000013" (深圳石化)
           格式应为：SH 代表上海股票，SZ 代表深圳股票
    
    返回:
    JSON格式数据，包含利润表，大约有203个财务指标，
    包括营业收入、营业成本、毛利润、净利润等多种财务指标。
    
    注意：输出包含大量财务指标（203项），由于数量庞大，本文档中不逐一列出。
    """
    try:
        df = ak.stock_profit_sheet_by_report_delisted_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_profit_sheet_by_report_em(symbol: str = "SH600519") -> str:
    """Get profit sheet data by reporting period from East Money for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code with exchange prefix, default is "SH600519" (Kweichow Moutai)
           Format should be: SH for Shanghai stocks, SZ for Shenzhen stocks
    
    Returns:
    JSON formatted data containing the profit sheet with approximately 203 financial indicators
    including revenue, operating costs, gross profit, net profit, and many other financial metrics.
    
    Note: The output contains a comprehensive set of financial indicators (203 items) that are not listed
    individually in this documentation due to their extensive nature.
    
    
    中文: 东方财富-股票-财务分析-利润表-报告期
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 带有交易所前缀的股票代码，默认值为 "SH600519" (贵州茅台)
           格式应为：SH 代表上海股票，SZ 代表深圳股票
    
    返回:
    JSON格式数据，包含利润表，大约有203个财务指标，
    包括营业收入、营业成本、毛利润、净利润等多种财务指标。
    
    注意：输出包含大量财务指标（203项），由于数量庞大，本文档中不逐一列出。
    """
    try:
        df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_profit_sheet_by_yearly_em(symbol: str = "SH600519") -> str:
    """Get yearly profit sheet data from East Money for a specific stock.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Stock code with exchange prefix, default is "SH600519" (Kweichow Moutai)
           Format should be: SH for Shanghai stocks, SZ for Shenzhen stocks
    
    Returns:
    JSON formatted data containing the yearly profit sheet with approximately 203 financial indicators
    including revenue, operating costs, gross profit, net profit, and many other financial metrics.
    
    Note: The output contains a comprehensive set of financial indicators (203 items) that are not listed
    individually in this documentation due to their extensive nature.
    
    
    中文: 东方财富-股票-财务分析-利润表-按年度
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 带有交易所前缀的股票代码，默认值为 "SH600519" (贵州茅台)
           格式应为：SH 代表上海股票，SZ 代表深圳股票
    
    返回:
    JSON格式数据，包含年度利润表，大约有203个财务指标，
    包括营业收入、营业成本、毛利润、净利润等多种财务指标。
    
    注意：输出包含大量财务指标（203项），由于数量庞大，本文档中不逐一列出。
    """
    try:
        df = ak.stock_profit_sheet_by_yearly_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_qbzf_em() -> str:
    """Get all additional issuance data from East Money Data Center.
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing information about all additional stock issuances, including:
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 增发代码: Additional issuance code
    - 发行方式: Issuance method
    - 发行总数: Total issuance (in shares)
    - 网上发行: Online issuance (in shares)
    - 发行价格: Issuance price
    - 最新价: Latest price
    - 发行日期: Issuance date
    - 增发上市日期: Additional issuance listing date
    - 锁定期: Lock-up period
    
    
    中文: 东方财富网-数据中心-新股数据-增发-全部增发
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含所有股票增发信息，包括：
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 增发代码: 增发代码
    - 发行方式: 发行方式
    - 发行总数: 发行总数（单位：股）
    - 网上发行: 网上发行（单位：股）
    - 发行价格: 发行价格
    - 最新价: 最新价
    - 发行日期: 发行日期
    - 增发上市日期: 增发上市日期
    - 锁定期: 锁定期
    """
    try:
        df = ak.stock_qbzf_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_qsjy_em(date: str = "20200430") -> str:
    """Get monthly performance reports of securities firms from East Money Data Center.
    
    Returns data in JSON format.
    
    Parameters:
    date: Date string in format "YYYYMMDD", default is "20200430"
          This should be the last day of the month you want to query
          Data available from 201006 to 202007, monthly frequency
    
    Returns:
    JSON formatted data containing monthly performance reports of securities firms, including:
    - 简称: Company abbreviation
    - 代码: Stock code
    - 当月净利润-净利润: Monthly net profit (unit: 10,000 yuan)
    - 当月净利润-同比增长: Year-on-year growth of monthly net profit
    - 当月净利润-环比增长: Month-on-month growth of monthly net profit
    - 当年累计净利润-累计净利润: Cumulative net profit for the current year (unit: 10,000 yuan)
    - 当年累计净利润-同比增长: Year-on-year growth of cumulative net profit
    - 当月营业收入-营业收入: Monthly operating income (unit: 10,000 yuan)
    - 当月营业收入-环比增长: Month-on-month growth of monthly operating income
    - 当月营业收入-同比增长: Year-on-year growth of monthly operating income
    - 当年累计营业收入-累计营业收入: Cumulative operating income for the current year (unit: 10,000 yuan)
    - 当年累计营业收入-同比增长: Year-on-year growth of cumulative operating income
    - 净资产-净资产: Net assets (unit: 10,000 yuan)
    - 净资产-同比增长: Year-on-year growth of net assets
    
    
    中文: 东方财富网-数据中心-特色数据-券商业绩月报
    
    返回 JSON 格式的数据。
    
    参数:
    date: 日期字符串，格式为 "YYYYMMDD"，默认值为 "20200430"
          应为您要查询的月份的最后一天
          数据可用范围从 201006 到 202007，月度频率
    
    返回:
    JSON格式数据，包含券商月度业绩报告，包括：
    - 简称: 公司简称
    - 代码: 股票代码
    - 当月净利润-净利润: 当月净利润（单位：万元）
    - 当月净利润-同比增长: 当月净利润同比增长
    - 当月净利润-环比增长: 当月净利润环比增长
    - 当年累计净利润-累计净利润: 当年累计净利润（单位：万元）
    - 当年累计净利润-同比增长: 当年累计净利润同比增长
    - 当月营业收入-营业收入: 当月营业收入（单位：万元）
    - 当月营业收入-环比增长: 当月营业收入环比增长
    - 当月营业收入-同比增长: 当月营业收入同比增长
    - 当年累计营业收入-累计营业收入: 当年累计营业收入（单位：万元）
    - 当年累计营业收入-同比增长: 当年累计营业收入同比增长
    - 净资产-净资产: 净资产（单位：万元）
    - 净资产-同比增长: 净资产同比增长
    """
    try:
        df = ak.stock_qsjy_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_cxfl_ths() -> str:
    """Get continuous volume increase stock ranking data from TongHuaShun (10jqka).
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing stocks with continuous volume increase, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 涨跌幅: Price change percentage (%)
    - 最新价: Latest price (yuan)
    - 成交量: Trading volume (shares)
    - 基准日成交量: Benchmark day trading volume (shares)
    - 放量天数: Number of days with increased volume
    - 阶段涨跌幅: Stage price change percentage (%)
    - 所属行业: Industry sector
    
    
    中文: 同花顺-数据中心-技术选股-持续放量
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含持续放量的股票排行，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 涨跌幅: 价格变化百分比 (%)
    - 最新价: 最新价格 (元)
    - 成交量: 成交量 (股)
    - 基准日成交量: 基准日成交量 (股)
    - 放量天数: 放量天数
    - 阶段涨跌幅: 阶段价格变化百分比 (%)
    - 所属行业: 所属行业板块
    """
    try:
        df = ak.stock_rank_cxfl_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_cxsl_ths() -> str:
    """Get continuous volume decrease stock ranking data from TongHuaShun (10jqka).
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing stocks with continuous volume decrease, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 涨跌幅: Price change percentage (%)
    - 最新价: Latest price (yuan)
    - 成交量: Trading volume (shares)
    - 基准日成交量: Benchmark day trading volume (shares)
    - 缩量天数: Number of days with decreased volume
    - 阶段涨跌幅: Stage price change percentage (%)
    - 所属行业: Industry sector
    
    
    中文: 同花顺-数据中心-技术选股-持续缩量
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含持续缩量的股票排行，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 涨跌幅: 价格变化百分比 (%)
    - 最新价: 最新价格 (元)
    - 成交量: 成交量 (股)
    - 基准日成交量: 基准日成交量 (股)
    - 缩量天数: 缩量天数
    - 阶段涨跌幅: 阶段价格变化百分比 (%)
    - 所属行业: 所属行业板块
    """
    try:
        df = ak.stock_rank_cxsl_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_forecast_cninfo(date: str = "20230817") -> str:
    """Get investment rating data from CNINFO (China Securities Regulatory Commission).
    
    Returns data in JSON format.
    
    Parameters:
    date: Date string in format "YYYYMMDD", default is "20230817"
          This should be a valid trading day
    
    Returns:
    JSON formatted data containing investment ratings for stocks, including:
    - 证券代码: Security code
    - 证券简称: Security name
    - 发布日期: Publication date
    - 研究机构简称: Research institution abbreviation
    - 研究员名称: Researcher name
    - 投资评级: Investment rating
    - 是否首次评级: Whether it's the first rating
    - 评级变化: Rating change
    - 前一次投资评级: Previous investment rating
    - 目标价格-下限: Target price - lower limit
    - 目标价格-上限: Target price - upper limit
    
    
    中文: 巨潮资讯-数据中心-评级预测-投资评级
    
    返回 JSON 格式的数据。
    
    参数:
    date: 日期字符串，格式为 "YYYYMMDD"，默认值为 "20230817"
          应为有效的交易日
    
    返回:
    JSON格式数据，包含股票投资评级信息，包括：
    - 证券代码: 证券代码
    - 证券简称: 证券名称
    - 发布日期: 发布日期
    - 研究机构简称: 研究机构简称
    - 研究员名称: 研究员名称
    - 投资评级: 投资评级
    - 是否首次评级: 是否为首次评级
    - 评级变化: 评级变化
    - 前一次投资评级: 前一次投资评级
    - 目标价格-下限: 目标价格下限
    - 目标价格-上限: 目标价格上限
    """
    try:
        df = ak.stock_rank_forecast_cninfo(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_ljqd_ths() -> str:
    """Get volume and price simultaneous decline stock ranking data from TongHuaShun (10jqka).
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing stocks with simultaneous decline in volume and price, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 最新价: Latest price (yuan)
    - 量价齐跌天数: Number of days with simultaneous decline in volume and price
    - 阶段涨幅: Stage price increase percentage (%)
    - 累计换手率: Cumulative turnover rate (%)
    - 所属行业: Industry sector
    
    
    中文: 同花顺-数据中心-技术选股-量价齐跌
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含量价齐跌的股票排行，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 最新价: 最新价格 (元)
    - 量价齐跌天数: 量价齐跌天数
    - 阶段涨幅: 阶段价格涨幅百分比 (%)
    - 累计换手率: 累计换手率 (%)
    - 所属行业: 所属行业板块
    """
    try:
        df = ak.stock_rank_ljqd_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_ljqs_ths() -> str:
    """Get volume and price simultaneous rise stock ranking data from TongHuaShun (10jqka).
    
    Returns data in JSON format.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing stocks with simultaneous rise in volume and price, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 最新价: Latest price (yuan)
    - 量价齐升天数: Number of days with simultaneous rise in volume and price
    - 阶段涨幅: Stage price increase percentage (%)
    - 累计换手率: Cumulative turnover rate (%)
    - 所属行业: Industry sector
    
    
    中文: 同花顺-数据中心-技术选股-量价齐升
    
    返回 JSON 格式的数据。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含量价齐升的股票排行，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 最新价: 最新价格 (元)
    - 量价齐升天数: 量价齐升天数
    - 阶段涨幅: 阶段价格涨幅百分比 (%)
    - 累计换手率: 累计换手率 (%)
    - 所属行业: 所属行业板块
    """
    try:
        df = ak.stock_rank_ljqs_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_xstp_ths(symbol: str = "500日均线") -> str:
    """Get upward breakthrough stock ranking data from TongHuaShun (10jqka).
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Moving average line to use as the breakthrough reference, default is "500日均线" (500-day moving average)
           Available options: "5日均线", "10日均线", "20日均线", "30日均线", 
                            "60日均线", "90日均线", "250日均线", "500日均线"
    
    Returns:
    JSON formatted data containing stocks with upward breakthrough of the specified moving average, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 最新价: Latest price (yuan)
    - 成交额: Transaction amount (yuan)
    - 成交量: Trading volume (shares)
    - 涨跌幅: Price change percentage (%)
    - 换手率: Turnover rate (%)
    
    
    中文: 同花顺-数据中心-技术选股-向上突破
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 用作突破参考的移动平均线，默认值为 "500日均线" (500天移动平均线)
           可选值: "5日均线", "10日均线", "20日均线", "30日均线", 
                  "60日均线", "90日均线", "250日均线", "500日均线"
    
    返回:
    JSON格式数据，包含向上突破指定移动平均线的股票，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 最新价: 最新价格 (元)
    - 成交额: 成交金额 (元)
    - 成交量: 成交量 (股)
    - 涨跌幅: 价格变化百分比 (%)
    - 换手率: 换手率 (%)
    """
    try:
        df = ak.stock_rank_xstp_ths(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_xxtp_ths(symbol: str = "500日均线") -> str:
    """Get downward breakthrough stock ranking data from TongHuaShun (10jqka).
    
    Returns data in JSON format.
    
    Parameters:
    symbol: Moving average line to use as the breakthrough reference, default is "500日均线" (500-day moving average)
           Available options: "5日均线", "10日均线", "20日均线", "30日均线", 
                            "60日均线", "90日均线", "250日均线", "500日均线"
    
    Returns:
    JSON formatted data containing stocks with downward breakthrough of the specified moving average, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 最新价: Latest price (yuan)
    - 成交额: Transaction amount (yuan)
    - 成交量: Trading volume (shares)
    - 涨跌幅: Price change percentage (%)
    - 换手率: Turnover rate (%)
    
    
    中文: 同花顺-数据中心-技术选股-向下突破
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: 用作突破参考的移动平均线，默认值为 "500日均线" (500天移动平均线)
           可选值: "5日均线", "10日均线", "20日均线", "30日均线", 
                  "60日均线", "90日均线", "250日均线", "500日均线"
    
    返回:
    JSON格式数据，包含向下突破指定移动平均线的股票，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 最新价: 最新价格 (元)
    - 成交额: 成交金额 (元)
    - 成交量: 成交量 (股)
    - 涨跌幅: 价格变化百分比 (%)
    - 换手率: 换手率 (%)
    """
    try:
        df = ak.stock_rank_xxtp_ths(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_rank_xzjp_ths() -> str:
    """Get insurance capital acquisition data from TongHuaShun (10jqka).
    
    Returns data in JSON format about stocks that have been acquired by insurance capital.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing stocks acquired by insurance capital, including:
    - 序号: Sequence number
    - 举牌公告日: Acquisition announcement date
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 现价: Current price (yuan)
    - 涨跌幅: Price change percentage (%)
    - 举牌方: Acquiring insurance institution
    - 增持数量: Increased holding quantity (shares)
    - 交易均价: Average transaction price (yuan)
    - 增持数量占总股本比例: Percentage of increased holdings to total shares (%)
    - 变动后持股总数: Total number of shares held after change (shares)
    - 变动后持股比例: Shareholding percentage after change (%)
    
    
    中文: 同花顺-数据中心-技术选股-险资举牌
    
    返回 JSON 格式的数据，包含被保险资金举牌的股票信息。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含被保险资金举牌的股票，包括：
    - 序号: 序号
    - 举牌公告日: 举牌公告日期
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 现价: 当前价格 (元)
    - 涨跌幅: 价格变化百分比 (%)
    - 举牌方: 举牌的保险机构
    - 增持数量: 增持股票数量 (股)
    - 交易均价: 平均交易价格 (元)
    - 增持数量占总股本比例: 增持数量占总股本的百分比 (%)
    - 变动后持股总数: 变动后持有的股票总数 (股)
    - 变动后持股比例: 变动后持股比例 (%)
    """
    try:
        df = ak.stock_rank_xzjp_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_register_bj() -> str:
    """Get Beijing Stock Exchange IPO audit information from EastMoney.
    
    Returns data in JSON format about companies in the IPO registration process for the Beijing Stock Exchange.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing IPO audit information for the Beijing Stock Exchange, including:
    - 序号: Sequence number
    - 发行人全称: Full name of the issuer
    - 审核状态: Audit status
    - 注册地: Registration location
    - 证监会行业: CSRC industry classification
    - 保荐机构: Sponsoring institution
    - 律师事务所: Law firm
    - 会计师事务所: Accounting firm
    - 更新日期: Update date
    - 受理日期: Acceptance date
    - 拟上市地点: Proposed listing location
    - 招股说明书: Prospectus
    
    
    中文: 东方财富网-数据中心-新股数据-IPO审核信息-北交所
    
    返回 JSON 格式的数据，包含北交所IPO审核信息。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含北交所IPO审核信息，包括：
    - 序号: 序号
    - 发行人全称: 发行人全称
    - 审核状态: 审核状态
    - 注册地: 注册地点
    - 证监会行业: 证监会行业分类
    - 保荐机构: 保荐机构
    - 律师事务所: 律师事务所
    - 会计师事务所: 会计师事务所
    - 更新日期: 更新日期
    - 受理日期: 受理日期
    - 拟上市地点: 计划上市地点
    - 招股说明书: 招股说明书
    """
    try:
        df = ak.stock_register_bj()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_register_cyb() -> str:
    """Get ChiNext (Growth Enterprise Market) IPO audit information from EastMoney.
    
    Returns data in JSON format about companies in the IPO registration process for the ChiNext board.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing IPO audit information for the ChiNext board, including:
    - 序号: Sequence number
    - 发行人全称: Full name of the issuer
    - 审核状态: Audit status
    - 注册地: Registration location
    - 证监会行业: CSRC industry classification
    - 保荐机构: Sponsoring institution
    - 律师事务所: Law firm
    - 会计师事务所: Accounting firm
    - 更新日期: Update date
    - 受理日期: Acceptance date
    - 拟上市地点: Proposed listing location
    - 招股说明书: Prospectus
    
    
    中文: 东方财富网-数据中心-新股数据-IPO审核信息-创业板
    
    返回 JSON 格式的数据，包含创业板IPO审核信息。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含创业板IPO审核信息，包括：
    - 序号: 序号
    - 发行人全称: 发行人全称
    - 审核状态: 审核状态
    - 注册地: 注册地点
    - 证监会行业: 证监会行业分类
    - 保荐机构: 保荐机构
    - 律师事务所: 律师事务所
    - 会计师事务所: 会计师事务所
    - 更新日期: 更新日期
    - 受理日期: 受理日期
    - 拟上市地点: 计划上市地点
    - 招股说明书: 招股说明书
    """
    try:
        df = ak.stock_register_cyb()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_register_db() -> str:
    """Get qualified enterprises data under the registration-based IPO system from EastMoney.
    
    Returns data in JSON format about companies that meet the standards for the registration-based IPO system.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing qualified enterprises information, including:
    - 序号: Sequence number
    - 企业名称: Enterprise name
    - 经营范围: Business scope
    - 近三年营业收入-2019: Revenue in 2019 (yuan)
    - 近三年净利润-2019: Net profit in 2019 (yuan)
    - 近三年研发费用-2019: R&D expenses in 2019 (yuan)
    - 近三年营业收入-2018: Revenue in 2018 (yuan)
    - 近三年净利润-2018: Net profit in 2018 (yuan)
    - 近三年研发费用-2018: R&D expenses in 2018 (yuan)
    - 近三年营业收入-2017: Revenue in 2017 (yuan)
    - 近三年净利润-2017: Net profit in 2017 (yuan)
    - 近三年研发费用-2017: R&D expenses in 2017 (yuan)
    - 近两年累计净利润: Cumulative net profit for the last two years (yuan)
    
    
    中文: 东方财富网-数据中心-新股数据-注册制审核-达标企业
    
    返回 JSON 格式的数据，包含符合注册制IPO标准的企业信息。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含达标企业信息，包括：
    - 序号: 序号
    - 企业名称: 企业名称
    - 经营范围: 经营范围
    - 近三年营业收入-2019: 2019年营业收入 (元)
    - 近三年净利润-2019: 2019年净利润 (元)
    - 近三年研发费用-2019: 2019年研发费用 (元)
    - 近三年营业收入-2018: 2018年营业收入 (元)
    - 近三年净利润-2018: 2018年净利润 (元)
    - 近三年研发费用-2018: 2018年研发费用 (元)
    - 近三年营业收入-2017: 2017年营业收入 (元)
    - 近三年净利润-2017: 2017年净利润 (元)
    - 近三年研发费用-2017: 2017年研发费用 (元)
    - 近两年累计净利润: 近两年累计净利润 (元)
    """
    try:
        df = ak.stock_register_db()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_register_kcb() -> str:
    """Get STAR Market (Science and Technology Innovation Board) IPO audit information from EastMoney.
    
    Returns data in JSON format about companies in the IPO registration process for the STAR Market.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing IPO audit information for the STAR Market, including:
    - 序号: Sequence number
    - 发行人全称: Full name of the issuer
    - 审核状态: Audit status
    - 注册地: Registration location
    - 证监会行业: CSRC industry classification
    - 保荐机构: Sponsoring institution
    - 律师事务所: Law firm
    - 会计师事务所: Accounting firm
    - 更新日期: Update date
    - 受理日期: Acceptance date
    - 拟上市地点: Proposed listing location
    - 招股说明书: Prospectus
    
    
    中文: 东方财富网-数据中心-新股数据-IPO审核信息-科创板
    
    返回 JSON 格式的数据，包含科创板IPO审核信息。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含科创板IPO审核信息，包括：
    - 序号: 序号
    - 发行人全称: 发行人全称
    - 审核状态: 审核状态
    - 注册地: 注册地点
    - 证监会行业: 证监会行业分类
    - 保荐机构: 保荐机构
    - 律师事务所: 律师事务所
    - 会计师事务所: 会计师事务所
    - 更新日期: 更新日期
    - 受理日期: 受理日期
    - 拟上市地点: 计划上市地点
    - 招股说明书: 招股说明书
    """
    try:
        df = ak.stock_register_kcb()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_register_sh() -> str:
    """Get Shanghai Main Board IPO audit information from EastMoney.
    
    Returns data in JSON format about companies in the IPO registration process for the Shanghai Main Board.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing IPO audit information for the Shanghai Main Board, including:
    - 序号: Sequence number
    - 发行人全称: Full name of the issuer
    - 审核状态: Audit status
    - 注册地: Registration location
    - 证监会行业: CSRC industry classification
    - 保荐机构: Sponsoring institution
    - 律师事务所: Law firm
    - 会计师事务所: Accounting firm
    - 更新日期: Update date
    - 受理日期: Acceptance date
    - 拟上市地点: Proposed listing location
    - 招股说明书: Prospectus
    
    
    中文: 东方财富网-数据中心-新股数据-IPO审核信息-上海主板
    
    返回 JSON 格式的数据，包含上海主板IPO审核信息。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含上海主板IPO审核信息，包括：
    - 序号: 序号
    - 发行人全称: 发行人全称
    - 审核状态: 审核状态
    - 注册地: 注册地点
    - 证监会行业: 证监会行业分类
    - 保荐机构: 保荐机构
    - 律师事务所: 律师事务所
    - 会计师事务所: 会计师事务所
    - 更新日期: 更新日期
    - 受理日期: 受理日期
    - 拟上市地点: 计划上市地点
    - 招股说明书: 招股说明书
    """
    try:
        df = ak.stock_register_sh()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_register_sz() -> str:
    """Get Shenzhen Main Board IPO audit information from EastMoney.
    
    Returns data in JSON format about companies in the IPO registration process for the Shenzhen Main Board.
    
    Parameters:
    None
    
    Returns:
    JSON formatted data containing IPO audit information for the Shenzhen Main Board, including:
    - 序号: Sequence number
    - 发行人全称: Full name of the issuer
    - 审核状态: Audit status
    - 注册地: Registration location
    - 证监会行业: CSRC industry classification
    - 保荐机构: Sponsoring institution
    - 律师事务所: Law firm
    - 会计师事务所: Accounting firm
    - 更新日期: Update date
    - 受理日期: Acceptance date
    - 拟上市地点: Proposed listing location
    - 招股说明书: Prospectus
    
    
    中文: 东方财富网-数据中心-新股数据-IPO审核信息-深圳主板
    
    返回 JSON 格式的数据，包含深圳主板IPO审核信息。
    
    参数:
    无
    
    返回:
    JSON格式数据，包含深圳主板IPO审核信息，包括：
    - 序号: 序号
    - 发行人全称: 发行人全称
    - 审核状态: 审核状态
    - 注册地: 注册地点
    - 证监会行业: 证监会行业分类
    - 保荐机构: 保荐机构
    - 律师事务所: 律师事务所
    - 会计师事务所: 会计师事务所
    - 更新日期: 更新日期
    - 受理日期: 受理日期
    - 拟上市地点: 计划上市地点
    - 招股说明书: 招股说明书
    """
    try:
        df = ak.stock_register_sz()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_report_disclosure(market: str = "沪深京", period: str = "2022年报") -> str:
    """Get scheduled financial report disclosure dates from CNINFO.
    
    Returns data in JSON format about the scheduled and actual disclosure dates of financial reports.
    
    Parameters:
    market: str, default="沪深京" (Shanghai, Shenzhen, and Beijing markets)
        Market to query. Options include: "沪深京" (Shanghai, Shenzhen, and Beijing), "深市" (Shenzhen), "深主板" (Shenzhen Main Board), "创业板" (ChiNext), "沪市" (Shanghai), "沪主板" (Shanghai Main Board), "科创板" (STAR Market), "北交所" (Beijing Stock Exchange)
    period: str, default="2022年报" (2022 Annual Report)
        Financial reporting period. Recent options include: "2021一季" (Q1 2021), "2021半年报" (Half-year 2021), "2021三季" (Q3 2021), "2021年报" (Annual 2021)
    
    Returns:
    JSON formatted data containing scheduled disclosure information, including:
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 首次预约: First scheduled disclosure date
    - 初次变更: First change of disclosure date
    - 二次变更: Second change of disclosure date
    - 三次变更: Third change of disclosure date
    - 实际披露: Actual disclosure date
    
    
    中文: 巨潮资讯-数据-预约披露的数据
    
    返回 JSON 格式的数据，包含证券报告预约披露日期信息。
    
    参数:
    market: str, 默认值="沪深京"
        市场类型。可选值包括: "沪深京", "深市", "深主板", "创业板", "沪市", "沪主板", "科创板", "北交所"
    period: str, 默认值="2022年报"
        财务报告期间。最近的选项包括: "2021一季", "2021半年报", "2021三季", "2021年报"
    
    返回:
    JSON格式数据，包含预约披露信息，包括：
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 首次预约: 首次预约披露日期
    - 初次变更: 第一次变更披露日期
    - 二次变更: 第二次变更披露日期
    - 三次变更: 第三次变更披露日期
    - 实际披露: 实际披露日期
    """
    try:
        df = ak.stock_report_disclosure(market=market, period=period)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_report_fund_hold(symbol: str = "基金持仓", date: str = "20200630") -> str:
    """Get institutional holdings of stocks from EastMoney.
    
    Returns data in JSON format about stocks held by various institutional investors such as funds, QFII, social security, brokers, insurance, and trusts.
    
    Parameters:
    symbol: str, default="基金持仓" (Fund Holdings)
        Type of institutional investor. Options include: "基金持仓" (Fund Holdings), "QFII持仓" (QFII Holdings), "社保持仓" (Social Security Holdings), "券商持仓" (Broker Holdings), "保险持仓" (Insurance Holdings), "信托持仓" (Trust Holdings)
    date: str, default="20200630"
        Financial report date in format YYYYMMDD. Typical dates are quarter-end dates: YYYY-03-31, YYYY-06-30, YYYY-09-30, YYYY-12-31
    
    Returns:
    JSON formatted data containing institutional holdings information, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 持有基金家数: Number of funds holding the stock (units: funds)
    - 持股总数: Total number of shares held (units: shares)
    - 持股市值: Market value of holdings (units: yuan)
    - 持股变化: Change in holdings description
    - 持股变动数值: Numerical change in shares held (units: shares)
    - 持股变动比例: Percentage change in holdings (units: %)
    
    
    中文: 东方财富网-数据中心-主力数据-基金持仓
    
    返回 JSON 格式的数据，包含机构投资者持有的股票信息。
    
    参数:
    symbol: str, 默认值="基金持仓"
        机构投资者类型。可选值包括: "基金持仓", "QFII持仓", "社保持仓", "券商持仓", "保险持仓", "信托持仓"
    date: str, 默认值="20200630"
        财报日期，格式为YYYYMMDD。典型日期为季度末: YYYY-03-31, YYYY-06-30, YYYY-09-30, YYYY-12-31
    
    返回:
    JSON格式数据，包含机构持股信息，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 持有基金家数: 持有该股票的基金数量 (单位: 家)
    - 持股总数: 持有股票的总数量 (单位: 股)
    - 持股市值: 持股的市场价值 (单位: 元)
    - 持股变化: 持股变化描述
    - 持股变动数值: 持股数量的变化 (单位: 股)
    - 持股变动比例: 持股变化的百分比 (单位: %)
    """
    try:
        df = ak.stock_report_fund_hold(symbol=symbol, date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_report_fund_hold_detail(symbol: str = "005827", date: str = "20201231") -> str:
    """Get detailed fund holdings information for a specific fund from EastMoney.
    
    Returns data in JSON format about the stock holdings of a specific fund at a given date.
    
    Parameters:
    symbol: str, default="005827"
        Fund code to query
    date: str, default="20201231"
        Financial report date in format YYYYMMDD. Typical dates are quarter-end dates: YYYY-03-31, YYYY-06-30, YYYY-09-30, YYYY-12-31
    
    Returns:
    JSON formatted data containing detailed fund holdings information, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 持股数: Number of shares held (units: shares)
    - 持股市值: Market value of holdings (units: yuan)
    - 占总股本比例: Percentage of total shares outstanding (units: %)
    - 占流通股本比例: Percentage of tradable shares (units: %)
    
    
    中文: 东方财富网-数据中心-主力数据-基金持仓-基金持仓明细表
    
    返回 JSON 格式的数据，包含特定基金在特定日期的股票持仓明细。
    
    参数:
    symbol: str, 默认值="005827"
        要查询的基金代码
    date: str, 默认值="20201231"
        财报日期，格式为YYYYMMDD。典型日期为季度末: YYYY-03-31, YYYY-06-30, YYYY-09-30, YYYY-12-31
    
    返回:
    JSON格式数据，包含基金持股明细信息，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 持股数: 持有股票的数量 (单位: 股)
    - 持股市值: 持股的市场价值 (单位: 元)
    - 占总股本比例: 占公司总股本的百分比 (单位: %)
    - 占流通股本比例: 占公司流通股本的百分比 (单位: %)
    """
    try:
        df = ak.stock_report_fund_hold_detail(symbol=symbol, date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_research_report_em(symbol: str = "000001") -> str:
    """Get stock research reports from EastMoney.
    
    Returns data in JSON format about research reports for a specific stock.
    
    Parameters:
    symbol: str, default="000001"
        Stock code to query
    
    Returns:
    JSON formatted data containing research report information, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 报告名称: Report name
    - 东财评级: EastMoney rating
    - 机构: Institution
    - 近一月个股研报数: Number of research reports for this stock in the past month
    - 2024-盈利预测-收益: 2024 earnings forecast - earnings
    - 2024-盈利预测-市盈率: 2024 earnings forecast - P/E ratio
    - 2025-盈利预测-收益: 2025 earnings forecast - earnings
    - 2025-盈利预测-市盈率: 2025 earnings forecast - P/E ratio
    - 2026-盈利预测-收益: 2026 earnings forecast - earnings
    - 2026-盈利预测-市盈率: 2026 earnings forecast - P/E ratio
    - 行业: Industry
    - 日期: Date
    - 报告PDF链接: Report PDF link
    
    
    中文: 东方财富网-数据中心-研究报告-个股研报
    
    返回 JSON 格式的数据，包含特定股票的研究报告信息。
    
    参数:
    symbol: str, 默认值="000001"
        要查询的股票代码
    
    返回:
    JSON格式数据，包含研究报告信息，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 报告名称: 报告名称
    - 东财评级: 东方财富评级
    - 机构: 发布报告的机构
    - 近一月个股研报数: 近一个月该股票的研究报告数量
    - 2024-盈利预测-收益: 2024年盈利预测 - 收益
    - 2024-盈利预测-市盈率: 2024年盈利预测 - 市盈率
    - 2025-盈利预测-收益: 2025年盈利预测 - 收益
    - 2025-盈利预测-市盈率: 2025年盈利预测 - 市盈率
    - 2026-盈利预测-收益: 2026年盈利预测 - 收益
    - 2026-盈利预测-市盈率: 2026年盈利预测 - 市盈率
    - 行业: 所属行业
    - 日期: 报告日期
    - 报告PDF链接: 报告PDF文件链接
    """
    try:
        df = ak.stock_research_report_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_restricted_release_detail_em(start_date: str = "20221202", end_date: str = "20221204") -> str:
    """Get detailed information about restricted stock releases from EastMoney.
    
    Returns data in JSON format about restricted stock releases within a specified date range.
    
    Parameters:
    start_date: str, default="20221202"
        Start date of the query period in format YYYYMMDD
    end_date: str, default="20221204"
        End date of the query period in format YYYYMMDD
    
    Returns:
    JSON formatted data containing restricted stock release information, including:
    - 序号: Sequence number
    - 股票代码: Stock code
    - 股票简称: Stock name
    - 解禁时间: Release date
    - 限售股类型: Type of restricted stock
    - 解禁数量: Number of shares released (units: shares)
    - 实际解禁数量: Actual number of shares released (units: shares)
    - 实际解禁市值: Actual market value of released shares (units: yuan)
    - 占解禁前流通市值比例: Proportion of pre-release circulating market value
    - 解禁前一交易日收盘价: Closing price on the trading day before release
    - 解禁前20日涨跌幅: Price change in the 20 days before release (units: %)
    - 解禁后20日涨跌幅: Price change in the 20 days after release (units: %)
    
    
    中文: 东方财富网-数据中心-限售股解禁-解禁详情一览
    
    返回 JSON 格式的数据，包含指定日期范围内的限售股解禁信息。
    
    参数:
    start_date: str, 默认值="20221202"
        查询开始日期，格式为YYYYMMDD
    end_date: str, 默认值="20221204"
        查询结束日期，格式为YYYYMMDD
    
    返回:
    JSON格式数据，包含限售股解禁信息，包括：
    - 序号: 序号
    - 股票代码: 股票代码
    - 股票简称: 股票名称
    - 解禁时间: 解禁日期
    - 限售股类型: 限售股类型
    - 解禁数量: 解禁股票数量 (单位: 股)
    - 实际解禁数量: 实际解禁的股票数量 (单位: 股)
    - 实际解禁市值: 实际解禁股票的市场价值 (单位: 元)
    - 占解禁前流通市值比例: 占解禁前流通市值的比例
    - 解禁前一交易日收盘价: 解禁前一个交易日的收盘价
    - 解禁前20日涨跌幅: 解禁前20天的价格变化幅度 (单位: %)
    - 解禁后20日涨跌幅: 解禁后20天的价格变化幅度 (单位: %)
    """
    try:
        df = ak.stock_restricted_release_detail_em(start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_restricted_release_queue_em(symbol: str = "600000") -> str:
    """Get information about restricted stock release batches for a specific stock from EastMoney.
    
    Returns data in JSON format about the release batches of restricted stocks for a specific stock.
    
    Parameters:
    symbol: str, default="600000"
        Stock code to query
    
    Returns:
    JSON formatted data containing restricted stock release batch information, including:
    - 序号: Sequence number
    - 解禁时间: Release date
    - 解禁股东数: Number of shareholders with restricted stock releases
    - 解禁数量: Number of shares to be released (units: shares)
    - 实际解禁数量: Actual number of shares released (units: shares)
    - 未解禁数量: Number of shares not yet released (units: shares)
    - 实际解禁数量市值: Market value of actually released shares (units: yuan)
    - 占总市值比例: Proportion of total market value
    - 占流通市值比例: Proportion of circulating market value
    - 解禁前一交易日收盘价: Closing price on the trading day before release (units: yuan)
    - 限售股类型: Type of restricted stock
    - 解禁前20日涨跌幅: Price change in the 20 days before release (units: %)
    - 解禁后20日涨跌幅: Price change in the 20 days after release (units: %)
    
    
    中文: 东方财富网-数据中心-个股限售解禁-解禁批次
    
    返回 JSON 格式的数据，包含特定股票的限售股解禁批次信息。
    
    参数:
    symbol: str, 默认值="600000"
        要查询的股票代码
    
    返回:
    JSON格式数据，包含限售股解禁批次信息，包括：
    - 序号: 序号
    - 解禁时间: 解禁日期
    - 解禁股东数: 有限售股解禁的股东数量
    - 解禁数量: 要解禁的股票数量 (单位: 股)
    - 实际解禁数量: 实际解禁的股票数量 (单位: 股)
    - 未解禁数量: 尚未解禁的股票数量 (单位: 股)
    - 实际解禁数量市值: 实际解禁股票的市场价值 (单位: 元)
    - 占总市值比例: 占公司总市值的比例
    - 占流通市值比例: 占公司流通市值的比例
    - 解禁前一交易日收盘价: 解禁前一个交易日的收盘价 (单位: 元)
    - 限售股类型: 限售股类型
    - 解禁前20日涨跌幅: 解禁前20天的价格变化幅度 (单位: %)
    - 解禁后20日涨跌幅: 解禁后20天的价格变化幅度 (单位: %)
    """
    try:
        df = ak.stock_restricted_release_queue_em(symbol="600000")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_restricted_release_queue_sina(symbol: str = "600000") -> str:
    """Get information about restricted stock releases from Sina Finance.
    
    Returns data in JSON format about the restricted stock releases for a specific stock.
    
    Parameters:
    symbol: str, default="600000"
        Stock code to query
    
    Returns:
    JSON formatted data containing restricted stock release information, including:
    - 代码: Stock code
    - 名称: Stock name
    - 解禁日期: Release date
    - 解禁数量: Number of shares released (units: 10,000 shares)
    - 解禁股流通市值: Market value of released shares (units: 100 million yuan)
    - 上市批次: Listing batch
    - 公告日期: Announcement date
    
    
    中文: 新浪财经-发行分配-限售解禁
    
    返回 JSON 格式的数据，包含特定股票的限售股解禁信息。
    
    参数:
    symbol: str, 默认值="600000"
        要查询的股票代码
    
    返回:
    JSON格式数据，包含限售股解禁信息，包括：
    - 代码: 股票代码
    - 名称: 股票名称
    - 解禁日期: 解禁日期
    - 解禁数量: 解禁股票数量 (单位: 万股)
    - 解禁股流通市值: 解禁股票的市场价值 (单位: 亿元)
    - 上市批次: 上市批次
    - 公告日期: 公告日期
    """
    try:
        df = ak.stock_restricted_release_queue_sina(symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_restricted_release_stockholder_em(symbol: str = "600000", date: str = "20200904") -> str:
    """Get information about shareholders with restricted stock releases from EastMoney.

    Returns data in JSON format about shareholders with restricted stock releases for a specific stock on a specific date.

    Parameters:
    symbol: str, default="600000"
        Stock code to query
    date: str, default="20200904"
        Release date to query in format YYYYMMDD. This date can be obtained from stock_restricted_release_queue_em function.

    Returns:
    JSON formatted data containing restricted stock release shareholder information, including:
    - 序号: Sequence number
    - 股东名称: Shareholder name
    - 解禁数量: Number of shares to be released (units: shares)
    - 实际解禁数量: Actual number of shares released (units: shares)
    - 解禁市值: Market value of released shares (units: yuan)
    - 锁定期: Lock-up period (units: months)
    - 剩余未解禁数量: Number of shares not yet released (units: shares)
    - 限售股类型: Type of restricted stock
    - 进度: Progress status


    中文: 东方财富网-数据中心-个股限售解禁-解禁股东

    返回 JSON 格式的数据，包含特定股票在特定日期的限售股解禁股东信息。

    参数:
    symbol: str, 默认值="600000"
        要查询的股票代码
    date: str, 默认值="20200904"
        要查询的解禁日期，格式为YYYYMMDD。该日期可以从 stock_restricted_release_queue_em 函数获取。

    返回:
    JSON格式数据，包含限售股解禁股东信息，包括：
    - 序号: 序号
    - 股东名称: 股东名称
    - 解禁数量: 要解禁的股票数量 (单位: 股)
    - 实际解禁数量: 实际解禁的股票数量 (单位: 股)
    - 解禁市值: 解禁股票的市场价值 (单位: 元)
    - 锁定期: 锁定期 (单位: 月)
    - 剩余未解禁数量: 尚未解禁的股票数量 (单位: 股)
    - 限售股类型: 限售股类型
    - 进度: 进度状态
    """
    try:
        df = ak.stock_restricted_release_stockholder_em(symbol=symbol, date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_restricted_release_summary_em(symbol: str = "全部股票", start_date: str = "20221108", end_date: str = "20221209") -> str:
    """Get 东方财富网-数据中心-特色数据-限售股解禁
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-限售股解禁
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_restricted_release_summary_em(symbol, start_date, end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sector_fund_flow_hist(symbol: str = "汽车服务") -> str:
    """Get 东方财富网-数据中心-资金流向-行业资金流-行业历史资金流
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-资金流向-行业资金流-行业历史资金流
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sector_fund_flow_hist(symbol="汽车服务")
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sector_fund_flow_summary(symbol: str = "电源设备", indicator: str = "今日") -> str:
    """Get 东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sector_fund_flow_summary(symbol, indicator)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sgt_reference_exchange_rate_sse() -> str:
    """Get 沪港通-港股通信息披露-参考汇率
    
    Returns data in JSON format.
    
    
    中文: 沪港通-港股通信息披露-参考汇率
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sgt_reference_exchange_rate_sse()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sgt_reference_exchange_rate_szse() -> str:
    """Get 深港通-港股通业务信息-参考汇率
    
    Returns data in JSON format.
    
    
    中文: 深港通-港股通业务信息-参考汇率
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sgt_reference_exchange_rate_szse()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sgt_settlement_exchange_rate_sse() -> str:
    """Get 沪港通-港股通信息披露-结算汇兑
    
    Returns data in JSON format.
    
    
    中文: 沪港通-港股通信息披露-结算汇兑
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sgt_settlement_exchange_rate_sse()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sgt_settlement_exchange_rate_szse() -> str:
    """Get 深港通-港股通业务信息-结算汇率
    
    Returns data in JSON format.
    
    
    中文: 深港通-港股通业务信息-结算汇率
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sgt_settlement_exchange_rate_szse()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sh_a_spot_em() -> str:
    """Get 东方财富网-沪 A 股-实时行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-沪 A 股-实时行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sh_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_share_change_cninfo(symbol: str = "002594", start_date: str = "20091227", end_date: str = "20241021") -> str:
    """Get 巨潮资讯-数据-公司股本变动
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-数据-公司股本变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_share_change_cninfo(symbol=symbol, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_share_hold_change_bse(symbol: str = "430489") -> str:
    """Get 北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动
    
    Returns data in JSON format.
    
    
    中文: 北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_share_hold_change_bse(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_share_hold_change_sse(symbol: str = "600000") -> str:
    """Get 上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动
    
    Returns data in JSON format.
    
    
    中文: 上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_share_hold_change_sse(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_share_hold_change_szse(symbol: str = "001308") -> str:
    """Get 深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动
    
    Returns data in JSON format.
    
    
    中文: 深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_share_hold_change_szse(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_shareholder_change_ths(symbol: str = "688981") -> str:
    """Get 同花顺-公司大事-股东持股变动
    
    Returns data in JSON format.
    
    
    中文: 同花顺-公司大事-股东持股变动
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_shareholder_change_ths(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sns_sseinfo(symbol: str = "603119") -> str:
    """Get 上证e互动-提问与回答
    
    Returns data in JSON format.
    
    
    中文: 上证e互动-提问与回答
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sns_sseinfo(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_staq_net_stop() -> str:
    """Get 东方财富网-行情中心-沪深个股-两网及退市
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-沪深个股-两网及退市
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_staq_net_stop()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sy_em(date: str = "20240630") -> str:
    """Get 东方财富网-数据中心-特色数据-商誉-个股商誉明细
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-商誉-个股商誉明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sy_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sy_hy_em(date: str = "20240930") -> str:
    """Get 东方财富网-数据中心-特色数据-商誉-行业商誉
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-商誉-行业商誉
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sy_hy_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sy_jz_em(date: str = "20230331") -> str:
    """Get 东方财富网-数据中心-特色数据-商誉-个股商誉减值明细
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-商誉-个股商誉减值明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sy_jz_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sy_profile_em() -> str:
    """Get 东方财富网-数据中心-特色数据-商誉-A股商誉市场概况
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-商誉-A股商誉市场概况
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sy_profile_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sy_yq_em(date: str = "20221231") -> str:
    """Get 东方财富网-数据中心-特色数据-商誉-商誉减值预期明细
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-商誉-商誉减值预期明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sy_yq_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_sz_a_spot_em() -> str:
    """Get 东方财富网-深 A 股-实时行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-深 A 股-实时行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_sz_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_tfp_em(date: str = "20240426") -> str:
    """Get 东方财富网-数据中心-特色数据-停复牌信息
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-停复牌信息
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_tfp_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_us_famous_spot_em(symbol: str = '科技类') -> str:
    """Get 美股-知名美股的实时行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-港股市场-知名港股实时行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_us_famous_spot_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_us_hist_min_em(symbol: str = "105.ATER") -> str:
    """Get 东方财富网-行情首页-美股-每日分时行情
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情首页-美股-每日分时行情
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_us_hist_min_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_us_pink_spot_em() -> str:
    """Get 美股粉单市场的实时行情数据
    
    Returns data in JSON format.
    
    
    中文: 美股粉单市场的实时行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_us_pink_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_us_spot() -> str:
    """Get 东方财富网-美股-实时行情
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-美股; 获取的数据有 15 分钟延迟; 建议使用 ak.stock_us_spot_em() 来获取数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_us_spot()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_value_em(symbol: str = "300766") -> str:
    """Get 东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_value_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_xgsglb_em(symbol: str = "全部股票") -> str:
    """Get 东方财富网-数据中心-新股数据-新股申购-新股申购与中签查询
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-新股数据-新股申购-新股申购与中签查询
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_xgsglb_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_xgsr_ths() -> str:
    """Get 同花顺-数据中心-新股数据-新股上市首日
    
    Returns data in JSON format.
    
    
    中文: 同花顺-数据中心-新股数据-新股上市首日
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_xgsr_ths()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_xjll_em(date: str = "20240331") -> str:
    """Get 东方财富-数据中心-年报季报-业绩快报-现金流量表
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-业绩快报-现金流量表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_xjll_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_yjbb_em(date: str = "20220331") -> str:
    """Get 东方财富-数据中心-年报季报-业绩报表
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-业绩报表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_yjbb_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_yjkb_em(date: str = "20200331") -> str:
    """Get 东方财富-数据中心-年报季报-业绩快报
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-业绩快报
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_yjkb_em(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_yjyg_em(date: str = "20190331") -> str:
    """Get 东方财富-数据中心-年报季报-业绩预告
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-业绩预告
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_yjyg_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_yysj_em(symbol: str = "沪深A股", date: str = "20211231") -> str:
    """Get 东方财富-数据中心-年报季报-预约披露时间
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-预约披露时间
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_yysj_em(symbol, date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_yzxdr_em(date: str = "20210331") -> str:
    """Get 东方财富网-数据中心-特色数据-一致行动人
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-一致行动人
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_yzxdr_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zcfz_bj_em(date: str = "20240331") -> str:
    """Get 东方财富-数据中心-年报季报-业绩快报-资产负债表
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-业绩快报-资产负债表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zcfz_bj_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zcfz_em(date: str = "20240331") -> str:
    """Get 东方财富-数据中心-年报季报-业绩快报-资产负债表
    
    Returns data in JSON format.
    
    
    中文: 东方财富-数据中心-年报季报-业绩快报-资产负债表
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zcfz_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zdhtmx_em(start_date: str = "20220819", end_date: str = "20230819") -> str:
    """Get 东方财富网-数据中心-重大合同-重大合同明细
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-重大合同-重大合同明细
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zdhtmx_em(start_date, end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_cdr_daily(symbol: str = 'sh689009', start_date: str = '20201103', end_date: str = '20201116') -> str:
    """Get 上海证券交易所-科创板-CDR
    
    Returns data in JSON format.
    
    
    中文: 上海证券交易所-科创板-CDR
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_a_cdr_daily(symbol, start_date, end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_disclosure_relation_cninfo(symbol: str = "000001", market: str = "沪深京", start_date: str = "20230619", end_date: str = "20231220") -> str:
    """Get 巨潮资讯-首页-公告查询-信息披露调研-沪深京
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-首页-公告查询-信息披露调研-沪深京
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_a_disclosure_relation_cninfo(symbol, market, start_date, end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_disclosure_report_cninfo(symbol: str = "000001", market: str = "沪深京", start_date: str = "20230619", end_date: str = "20231220") -> str:
    """Get 巨潮资讯-首页-公告查询-信息披露公告-沪深京
    
    Returns data in JSON format.
    
    
    中文: 巨潮资讯-首页-公告查询-信息披露公告-沪深京
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_a_disclosure_report_cninfo(symbol, market, category, start_date, end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_gdhs(symbol: str = "20230930") -> str:
    """Get 东方财富网-数据中心-特色数据-股东户数数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股东户数数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_a_gdhs(symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_gdhs_detail_em(symbol: str = "000001") -> str:
    """Get 东方财富网-数据中心-特色数据-股东户数详情
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-数据中心-特色数据-股东户数详情
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_a_gdhs_detail_em(symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_hist(symbol: str = "000001", period: str = "daily", start_date: str = "20170301", end_date: str = '20240528', adjust: str = "") -> str:
    """Get historical A-share stock data from Eastmoney with daily, weekly, or monthly frequency.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code without market identifier, e.g., '000001'. Can be obtained from stock_zh_a_spot_em(). Default is "000001".
    period: str - Data frequency, options: {'daily', 'weekly', 'monthly'}. Default is "daily".
    start_date: str - Start date in YYYYMMDD format, e.g., '20170301'. Default is "20170301".
    end_date: str - End date in YYYYMMDD format, e.g., '20240528'. Default is "20240528".
    adjust: str - Price adjustment method: '' for no adjustment, 'qfq' for forward adjustment, 'hfq' for backward adjustment. Default is "".
    
    Returns:
    JSON formatted data including the following fields:
    - 日期: Trading date
    - 股票代码: Stock code without market identifier
    - 开盘: Opening price
    - 收盘: Closing price
    - 最高: Highest price
    - 最低: Lowest price
    - 成交量: Trading volume (unit: lots)
    - 成交额: Trading amount (unit: CNY)
    - 振幅: Amplitude (%)
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount (unit: CNY)
    - 换手率: Turnover rate (%)
    
    Note: For the current day's closing price, please retrieve after market close.
    This function returns historical market data for a specific A-share stock with the specified frequency.
    
    
    中文: 东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，不带市场标识，例如 '000001'。可以从 stock_zh_a_spot_em() 中获取。默认值为 "000001"。
    period: str - 数据周期，可选值为 {'daily', 'weekly', 'monthly'}，默认为 'daily'。
    start_date: str - 开始查询的日期，格式为 YYYYMMDD，例如 '20170301'。默认值为 "20170301"。
    end_date: str - 结束查询的日期，格式为 YYYYMMDD，例如 '20240528'。默认值为 "20240528"。
    adjust: str - 复权调整，可选值为 {'', 'qfq', 'hfq'}，'': 不复权, 'qfq': 前复权, 'hfq': 后复权。默认值为 ""。
    
    返回:
    JSON格式数据，包含以下字段：
    - 日期: 交易日
    - 股票代码: 不带市场标识的股票代码
    - 开盘: 开盘价
    - 收盘: 收盘价
    - 最高: 最高价
    - 最低: 最低价
    - 成交量: 成交量（单位：手）
    - 成交额: 成交额（单位：元）
    - 振幅: 振幅（%）
    - 涨跌幅: 涨跌幅（%）
    - 涨跌额: 涨跌额（单位：元）
    - 换手率: 换手率（%）
    
    注意：当日收盘价请在收盘后获取。
    该函数返回指定沪深京 A 股上市公司、指定周期和指定日期间的历史行情数据。
    """
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_hist_pre_min_em(symbol: str = "000001", start_time: str = "09:00:00", end_time: str = "15:40:00") -> str:
    """Get pre-market minute data for A-share stocks from Eastmoney.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code, e.g., "000001". Default is "000001".
    start_time: str - Start time in HH:MM:SS format, e.g., "09:00:00". Default is "09:00:00".
    end_time: str - End time in HH:MM:SS format, e.g., "15:40:00". Default is "15:40:00".
    
    Returns:
    JSON formatted data including the following fields:
    - 时间: Time
    - 开盘: Opening price
    - 收盘: Closing price
    - 最高: Highest price
    - 最低: Lowest price
    - 成交量: Trading volume (unit: lots)
    - 成交额: Trading amount
    - 最新价: Latest price
    
    Note: This function returns minute data for the most recent trading day, including pre-market data.
    
    
    中文: 东方财富-股票行情-盘前数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，例如 "000001"。默认值为 "000001"。
    start_time: str - 开始时间，格式为 HH:MM:SS，例如 "09:00:00"。默认值为 "09:00:00"。
    end_time: str - 结束时间，格式为 HH:MM:SS，例如 "15:40:00"。默认值为 "15:40:00"。
    
    返回:
    JSON格式数据，包含以下字段：
    - 时间: 时间
    - 开盘: 开盘价
    - 收盘: 收盘价
    - 最高: 最高价
    - 最低: 最低价
    - 成交量: 成交量（单位：手）
    - 成交额: 成交额
    - 最新价: 最新价
    
    注意：该函数返回最近一个交易日的股票分钟数据，包含盘前分钟数据。
    """
    try:
        df = ak.stock_zh_a_hist_pre_min_em(symbol=symbol, start_time=start_time, end_time=end_time)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_hist_tx(symbol: str = "sz000001", start_date: str = "20200101", end_date: str = "20231027", adjust: str = "") -> str:
    """Get historical A-share stock data from Tencent Securities with daily frequency.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock code with market identifier, e.g., "sz000001". Default is "sz000001".
    start_date: str - Start date in YYYYMMDD format, e.g., "20200101". Default is "20200101".
    end_date: str - End date in YYYYMMDD format, e.g., "20231027". Default is "20231027".
    adjust: str - Price adjustment method: '' for no adjustment, 'qfq' for forward adjustment, 'hfq' for backward adjustment. Default is "".
    
    Returns:
    JSON formatted data including the following fields:
    - date: Trading date
    - open: Opening price
    - close: Closing price
    - high: Highest price
    - low: Lowest price
    - amount: Trading volume (unit: lots)
    
    Note: For the current day's closing price, please retrieve after market close.
    
    
    中文: 腾讯证券-日频-股票历史数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，带市场标识，例如 "sz000001"。默认值为 "sz000001"。
    start_date: str - 开始查询的日期，格式为 YYYYMMDD，例如 "20200101"。默认值为 "20200101"。
    end_date: str - 结束查询的日期，格式为 YYYYMMDD，例如 "20231027"。默认值为 "20231027"。
    adjust: str - 复权调整，可选值为 {'', 'qfq', 'hfq'}，'': 不复权, 'qfq': 前复权, 'hfq': 后复权。默认值为 ""。
    
    返回:
    JSON格式数据，包含以下字段：
    - date: 交易日
    - open: 开盘价
    - close: 收盘价
    - high: 最高价
    - low: 最低价
    - amount: 成交量（单位：手）
    
    注意：当日收盘价请在收盘后获取。
    """
    try:
        df = ak.stock_zh_a_hist_tx(symbol=symbol, start_date=start_date, end_date=end_date, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_new_em() -> str:
    """Get information about newly listed A-share stocks from Eastmoney.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each newly listed stock:
    - 序号: Serial number
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount
    - 成交量: Trading volume
    - 成交额: Trading amount
    - 振幅: Amplitude (%)
    - 最高: Highest price
    - 最低: Lowest price
    - 今开: Opening price
    - 昨收: Previous closing price
    - 量比: Volume ratio
    - 换手率: Turnover rate (%)
    - 市盈率-动态: P/E ratio (dynamic)
    - 市净率: P/B ratio
    
    Note: Returns data for all newly listed stocks for the current trading day.
    
    
    中文: 东方财富网-行情中心-沪深个股-新股
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每只新股的以下字段：
    - 序号: 序号
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格
    - 涨跌幅: 涨跌幅 (%)
    - 涨跌额: 涨跌额
    - 成交量: 成交量
    - 成交额: 成交额
    - 振幅: 振幅 (%)
    - 最高: 最高价
    - 最低: 最低价
    - 今开: 开盘价
    - 昨收: 昨日收盘价
    - 量比: 量比
    - 换手率: 换手率 (%)
    - 市盈率-动态: 市盈率(动态)
    - 市净率: 市净率
    
    注意：返回当前交易日新股板块的所有股票的行情数据。
    """
    try:
        df = ak.stock_zh_a_new_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_a_tick_tx(symbol: str) -> str:
    """Get tick-by-tick transaction data for a specific A-share stock from Tencent Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Stock symbol with market identifier (e.g., 'sh600000' for Shanghai, 'sz000001' for Shenzhen)
    
    Returns:
    JSON formatted data including the following fields:
    - 成交时间: Transaction time
    - 成交价格: Transaction price (in CNY)
    - 价格变动: Price change (in CNY)
    - 成交量: Transaction volume (in lots)
    - 成交额: Transaction amount (in CNY)
    - 性质: Nature of transaction (buy/sell indicator)
    
    Note: Data is provided at 16:00 each trading day. If data is missing, please use the ak.stock_zh_a_tick_163() interface (note that there may be some differences in the data).
    
    
    中文: 获取腾讯财经的 A 股逆向交易数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 股票代码，需要带市场标识，例如 'sh600000' 表示上海市场，'sz000001' 表示深圳市场
    
    返回:
    JSON格式数据，包含以下字段：
    - 成交时间: 成交时间
    - 成交价格: 成交价格（单位：元）
    - 价格变动: 价格变动（单位：元）
    - 成交量: 成交量（单位：手）
    - 成交额: 成交额（单位：元）
    - 性质: 买卖盘标记
    
    注意：每个交易日 16:00 提供当日数据; 如遇到数据缺失, 请使用 ak.stock_zh_a_tick_163() 接口(注意数据会有一定差异)。
    """
    try:
        df = ak.stock_zh_a_tick_tx_js(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_ah_daily(symbol: str = "02318", start_year: str = "2022", end_year: str = "2024", adjust: str = "") -> str:
    """Get historical A+H stock data from Tencent Finance.
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - Hong Kong stock code, can be obtained through the ak.stock_zh_ah_name() function. Default is "02318".
    start_year: str - Start year for historical data. Default is "2022".
    end_year: str - End year for historical data. Default is "2024".
    adjust: str - Price adjustment method: '' for no adjustment, 'qfq' for forward adjustment, 'hfq' for backward adjustment. Default is ''.
    
    Returns:
    JSON formatted data including the following fields:
    - 日期: Date
    - 开盘: Opening price
    - 收盘: Closing price
    - 最高: Highest price
    - 最低: Lowest price
    - 成交量: Trading volume
    
    
    中文: 腾讯财经-A+H 股数据
    
    返回 JSON 格式的数据。
    
    参数:
    symbol: str - 港股股票代码，可以通过 ak.stock_zh_ah_name() 函数获取。默认值为 "02318"。
    start_year: str - 开始年份。默认值为 "2022"。
    end_year: str - 结束年份。默认值为 "2024"。
    adjust: str - 复权调整，可选值为 {'', 'qfq', 'hfq'}，'': 不复权, 'qfq': 前复权, 'hfq': 后复权。默认值为 ''。
    
    返回:
    JSON格式数据，包含以下字段：
    - 日期: 日期
    - 开盘: 开盘价
    - 收盘: 收盘价
    - 最高: 最高价
    - 最低: 最低价
    - 成交量: 成交量
    """
    try:
        df = ak.stock_zh_ah_daily(symbol=symbol, start_year=start_year, end_year=end_year, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_ah_name() -> str:
    """Get the list of all A+H listed companies from Tencent Finance.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each A+H listed company:
    - 代码: Stock code
    - 名称: Stock name
    
    Note: This function returns the codes and names of all A+H listed companies, which can be used as input for other functions such as stock_zh_ah_daily.
    
    
    中文: A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每个 A+H 上市公司的以下字段：
    - 代码: 股票代码
    - 名称: 股票名称
    
    注意：该函数返回所有 A+H 上市公司的代码和名称，可用于其他函数的输入，例如 stock_zh_ah_daily。
    """
    try:
        df = ak.stock_zh_ah_name()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_ah_spot() -> str:
    """Get real-time A+H stock data from Tencent Finance.
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data including the following fields for each A+H listed company:
    - 代码: Stock code
    - 名称: Stock name
    - 最新价: Latest price
    - 涨跌幅: Change percentage (%)
    - 涨跌额: Change amount
    - 买入: Buy price
    - 卖出: Sell price
    - 成交量: Trading volume
    - 成交额: Trading amount
    - 今开: Opening price
    - 昨收: Previous closing price
    - 最高: Highest price
    - 最低: Lowest price
    
    Note: Data is delayed by 15 minutes.
    
    
    中文: A+H 股数据是从腾讯财经获取的数据, 延迟 15 分钟更新
    
    返回 JSON 格式的数据。
    
    返回:
    JSON格式数据，包含每个 A+H 上市公司的以下字段：
    - 代码: 股票代码
    - 名称: 股票名称
    - 最新价: 最新价格
    - 涨跌幅: 涨跌幅 (%)
    - 涨跌额: 涨跌额
    - 买入: 买入价
    - 卖出: 卖出价
    - 成交量: 成交量
    - 成交额: 成交额
    - 今开: 开盘价
    - 昨收: 昨日收盘价
    - 最高: 最高价
    - 最低: 最低价
    
    注意：数据延迟 15 分钟更新。
    """
    try:
        df = ak.stock_zh_ah_spot()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_b_daily(symbol: str = "sh900901", start_date: str = "19900103", end_date: str = "20240722", adjust: str = "qfq") -> str:
    """Get B 股数据是从新浪财经获取的数据, 历史数据按日频率更新
    
    Returns data in JSON format.
    
    
    中文: B 股数据是从新浪财经获取的数据, 历史数据按日频率更新
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_b_daily(symbol, start_date, end_date, adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_b_minute(symbol: str = 'sh900901', period: str = '1', adjust: str = "qfq") -> str:
    """Get 新浪财经 B 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
    
    Returns data in JSON format.
    
    
    中文: 新浪财经 B 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_b_minute(symbol, period, adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_b_spot() -> str:
    """Get 东方财富网-实时行情数据
    
    Returns data in JSON format.
    
    
    中文: B 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_b_spot()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_b_spot_em() -> str:
    """Get 东方财富网-实时行情数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-实时行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_b_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_kcb_daily(symbol: str = "sh688399", adjust: str = "hfq") -> str:
    """Get 新浪财经-科创板股票历史行情数据
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-科创板股票历史行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_kcb_daily(symbol, adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_kcb_report_em(from_page: int = 1, to_page: int = 100) -> str:
    """Get 东方财富-科创板报告数据
    
    Returns data in JSON format.
    
    
    中文: 东方财富-科创板报告数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_kcb_report_em(from_page, to_page)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_kcb_spot() -> str:
    """Get 新浪财经-科创板股票实时行情数据
    
    Returns data in JSON format.
    
    
    中文: 新浪财经-科创板股票实时行情数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_kcb_spot()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_valuation_baidu(symbol: str = "002044", indicator: str = "总市值", period: str = "近一年") -> str:
    """Get 百度股市通-A 股-财务报表-估值数据
    
    Returns data in JSON format.
    
    
    中文: 百度股市通-A 股-财务报表-估值数据
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_valuation_baidu(symbol, indicator, period)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zh_vote_baidu(symbol: str = "000001", indicator: str = "指数") -> str:
    """Get 百度股市通- A 股或指数-股评-投票
    
    Returns data in JSON format.
    
    
    中文: 百度股市通- A 股或指数-股评-投票
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zh_vote_baidu(symbo, indicator)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zt_pool_dtgc_em(date: str = '20241011') -> str:
    """Get 东方财富网-行情中心-涨停板行情-跌停股池
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-涨停板行情-跌停股池
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zt_pool_dtgc_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zt_pool_em(date: str = '20241008') -> str:
    """Get 东方财富网-行情中心-涨停板行情-涨停股池
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-涨停板行情-涨停股池
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zt_pool_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zt_pool_previous_em(date: str = '20240415') -> str:
    """Get 东方财富网-行情中心-涨停板行情-昨日涨停股池
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-涨停板行情-昨日涨停股池
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zt_pool_previous_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zt_pool_strong_em(date: str = '20241231') -> str:
    """Get 东方财富网-行情中心-涨停板行情-强势股池
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-涨停板行情-强势股池
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zt_pool_strong_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zt_pool_sub_new_em(date: str = '20241231') -> str:
    """Get 东方财富网-行情中心-涨停板行情-次新股池
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-涨停板行情-次新股池
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zt_pool_sub_new_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zt_pool_zbgc_em(date: str = '20241011') -> str:
    """Get 东方财富网-行情中心-涨停板行情-炸板股池
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-行情中心-涨停板行情-炸板股池
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zt_pool_zbgc_em(date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zygc_em(symbol: str = "000001", date: str = "20231231") -> str:
    """Get 东方财富网-个股-主营构成
    
    Returns data in JSON format.
    
    
    中文: 东方财富网-个股-主营构成
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zygc_em(symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zygc_ym(symbol: str = "000001") -> str:
    """Get 益盟-F10-主营构成
    
    Returns data in JSON format.
    
    
    中文: 益盟-F10-主营构成
    
    Returns data in JSON format.
    
    Returns:
    JSON formatted data
    
    返回:
    JSON格式数据
    """
    try:
        df = ak.stock_zygc_ym(symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def stock_zyjs_ths(symbol: str = "000066") -> str:
    """Get 同花顺-主营介绍
    
    Returns data in JSON format.
    
    
    中文: 同花顺-主营介绍
    
    Returns data in JSON format.
    
    Parameters:
    symbol: str - 股票代码，例如 "000066"
    
    Returns:
    JSON formatted data with fields including stock code, main business, product type, product name, and business scope
    
    参数:
    symbol: str - 股票代码，例如 "000066"
    
    返回:
    JSON格式数据，包含股票代码、主营业务、产品类型、产品名称、经营范围等字段
    """
    try:
        df = ak.stock_zyjs_ths(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})
