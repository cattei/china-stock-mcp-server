from typing import Any, Dict, List, Optional, Union
import json
from mcp.server.fastmcp import FastMCP
import akshare as ak

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
    
    Returns a summary of the Shanghai Stock Exchange market data including:
    - Total market value
    - Average P/E ratio
    - Number of listed companies
    - Number of listed stocks
    - Circulation market value
    - Report time
    - Total share capital
    """
    try:
        df = ak.stock_sse_summary()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Shenzhen Stock Exchange Summary
@mcp.tool()
def stock_szse_summary(date: str) -> str:
    """Get Shenzhen Stock Exchange market overview data.
    
    Args:
        date: Date in format YYYYMMDD (e.g., 20240305)
        
    Returns a summary of the Shenzhen Stock Exchange market data including:
    - Security type
    - Quantity
    - Transaction amount
    - Total market value
    - Circulation market value
    """
    try:
        df = ak.stock_szse_summary(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-share Real-time Quotes
@mcp.tool()
def stock_zh_a_spot_em() -> str:
    """Get A-share market real-time quotes for all stocks.
    
    Returns real-time market data for all A-share stocks including:
    - Stock code
    - Stock name
    - Latest price
    - Change amount
    - Change percentage
    - Volume
    - Amount
    - Amplitude
    - Turnover rate
    - PE ratio
    - And many other metrics
    """
    try:
        df = ak.stock_zh_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# MCP Tools Implementation

# Shanghai Stock Exchange Summary
@mcp.tool()
def stock_szse_area_summary(date: str) -> str:
    """Get Shenzhen Stock Exchange regional trading ranking data.
    
    Args:
        date: Date in format YYYYMM (e.g., 202403)
        
    Returns regional trading data including:
    - Rank
    - Region
    - Total transaction amount
    - Market share percentage
    - Stock transaction amount
    - Fund transaction amount
    - Bond transaction amount
    """
    try:
        df = ak.stock_szse_area_summary(date=date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-Share Individual Stock Data
@mcp.tool()
def stock_zh_a_daily(symbol: str, start_date: str, end_date: str, adjust: str = "") -> str:
    """Get A-share individual stock historical daily data.
    
    Args:
        symbol: Stock symbol (e.g., 000001 for Ping An Bank)
        start_date: Start date in format YYYYMMDD (e.g., 20240101)
        end_date: End date in format YYYYMMDD (e.g., 20240305)
        adjust: Price adjustment method: "" for no adjustment, "qfq" for forward adjustment, "hfq" for backward adjustment
        
    Returns daily stock data including:
    - Date
    - Open price
    - High price
    - Low price
    - Close price
    - Volume
    - Amount
    - Amplitude
    - Change percentage
    - Change amount
    - Turnover rate
    """
    try:
        df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, end_date=end_date, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-Share Index Data
@mcp.tool()
def stock_zh_a_spot(symbol: str) -> str:
    """Get real-time quote for a specific A-share stock.
    
    Args:
        symbol: Stock symbol (e.g., sh000001 for SSE, sz399001 for SZSE)
        
    Returns real-time data for the specified stock.
    """
    try:
        df = ak.stock_zh_a_spot(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-Share Top Gainers
@mcp.tool()
def stock_bj_a_spot_em() -> str:
    """Get Beijing Stock Exchange real-time quotes for all stocks.
    
    Returns real-time market data for all Beijing Stock Exchange stocks.
    """
    try:
        df = ak.stock_bj_a_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Individual Stock Information
@mcp.tool()
def stock_individual_info_em(symbol: str) -> str:
    """Get detailed information for a specific stock.
    
    Args:
        symbol: Stock symbol (e.g., 000001 for Ping An Bank)
        
    Returns detailed information about the stock including:
    - Stock name
    - Industry
    - Main business
    - Company profile
    - And other fundamental information
    """
    try:
        df = ak.stock_individual_info_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Bid-Ask Data
@mcp.tool()
def stock_bid_ask_em(symbol: str) -> str:
    """Get real-time bid-ask data for a specific stock.
    
    Args:
        symbol: Stock symbol (e.g., 000001 for Ping An Bank)
        
    Returns real-time bid-ask data including:
    - Bid prices and volumes
    - Ask prices and volumes
    - Spread information
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
    
    Args:
        symbol: Sector symbol (e.g., U, M, S, P, Q)
        date: Date in format YYYYMM (e.g., 202403)
        
    Returns sector transaction data including:
    - Sector name
    - Number of stocks
    - Transaction amount
    - Market share
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
    
    Args:
        date: Date in format YYYYMMDD (e.g., 20240305), default is None for the latest data
        
    Returns daily trading data including:
    - Trading volume
    - Trading value
    - Number of transactions
    - And other trading statistics
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
    
    Args:
        symbol: Stock symbol (e.g., sh600000)
        period: Time period (1, 5, 15, 30, 60 minutes)
        adjust: Price adjustment method: "" for no adjustment, "qfq" for forward adjustment, "hfq" for backward adjustment
        
    Returns minute-level data including:
    - Time
    - Open
    - High
    - Low
    - Close
    - Volume
    """
    try:
        df = ak.stock_zh_a_minute(symbol=symbol, period=period, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Minute-level Data (Eastmoney)
@mcp.tool()
def stock_zh_a_hist_min_em(symbol: str, start_date: str, end_date: str, period: str = "1") -> str:
    """Get minute-level historical data for a specific A-share stock from Eastmoney.
    
    Args:
        symbol: Stock symbol (e.g., 000001)
        start_date: Start date in format YYYY-MM-DD HH:MM:SS (e.g., 2024-03-01 09:30:00)
        end_date: End date in format YYYY-MM-DD HH:MM:SS (e.g., 2024-03-05 15:00:00)
        period: Time period (1, 5, 15, 30, 60 minutes), default is "1"
        
    Returns minute-level data including:
    - Time
    - Open
    - High
    - Low
    - Close
    - Volume
    - Amount
    """
    try:
        df = ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Intraday Data
@mcp.tool()
def stock_intraday_em(symbol: str) -> str:
    """Get intraday data for a specific A-share stock from Eastmoney.
    
    Args:
        symbol: Stock symbol (e.g., 000001)
        
    Returns intraday data including:
    - Time
    - Price
    - Volume
    - Turnover
    """
    try:
        df = ak.stock_intraday_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock New Listings
@mcp.tool()
def stock_zh_a_new() -> str:
    """Get information about newly listed A-share stocks.
    
    Returns data about newly listed stocks including:
    - Stock code
    - Stock name
    - Listing date
    - Issue price
    - P/E ratio
    - And other IPO-related information
    """
    try:
        df = ak.stock_zh_a_new()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock ST Status
@mcp.tool()
def stock_zh_a_st_em() -> str:
    """Get information about A-share stocks with ST status.
    
    Returns data about ST stocks including:
    - Stock code
    - Stock name
    - Latest price
    - Change percentage
    - ST reason
    - ST date
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
    """
    try:
        df = ak.stock_zh_a_stop_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# A-H Share Comparison
@mcp.tool()
def stock_zh_ah_spot_em() -> str:
    """Get comparison data for stocks listed on both A-share and H-share markets.
    
    Returns comparison data including:
    - Stock code (A and H)
    - Stock name
    - A-share price
    - H-share price
    - Price difference
    - Premium ratio
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
    """
    try:
        df = ak.stock_us_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# US Stock Historical Data
@mcp.tool()
def stock_us_hist(symbol: str, start_date: str, end_date: str, adjust: str = "") -> str:
    """Get historical data for a specific US stock.
    
    Args:
        symbol: Stock symbol (e.g., AAPL for Apple)
        start_date: Start date in format YYYYMMDD (e.g., 20240101)
        end_date: End date in format YYYYMMDD (e.g., 20240305)
        adjust: Price adjustment method: "" for no adjustment, "qfq" for forward adjustment, "hfq" for backward adjustment
        
    Returns historical data including:
    - Date
    - Open
    - High
    - Low
    - Close
    - Volume
    """
    try:
        df = ak.stock_us_hist(symbol=symbol, start_date=start_date, end_date=end_date, adjust=adjust)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Index List
@mcp.tool()
def stock_sector_spot(indicator: str = "板块涨幅") -> str:
    """Get real-time data for stock industry sectors.
    
    Args:
        indicator: Indicator type (e.g., "板块涨幅" for sector gains), default is "板块涨幅"
        
    Returns real-time sector data including:
    - Sector name
    - Latest price
    - Change percentage
    - Number of stocks
    - Leading stocks
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
    
    Args:
        sector: Sector name (e.g., "半导体" for semiconductor)
        
    Returns detailed sector data including:
    - Stock code
    - Stock name
    - Latest price
    - Change percentage
    - And other market metrics
    """
    try:
        df = ak.stock_sector_detail(sector=sector)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Fund Flow
@mcp.tool()
def stock_individual_fund_flow(stock: str) -> str:
    """Get fund flow data for a specific stock.
    
    Args:
        stock: Stock symbol (e.g., 600000 for SPDB)
        
    Returns fund flow data including:
    - Date
    - Net inflow amount
    - Net inflow percentage
    - Main inflow
    - Retail inflow
    """
    try:
        df = ak.stock_individual_fund_flow(stock=stock)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market Fund Flow
@mcp.tool()
def stock_market_fund_flow() -> str:
    """Get overall market fund flow data.
    
    Returns market fund flow data including:
    - Date
    - Net inflow amount
    - Net inflow percentage
    - Main inflow
    - Retail inflow
    """
    try:
        df = ak.stock_market_fund_flow()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Sector Fund Flow
@mcp.tool()
def stock_sector_fund_flow_rank() -> str:
    """Get fund flow ranking data for industry sectors.
    
    Returns sector fund flow data including:
    - Sector name
    - Net inflow amount
    - Net inflow percentage
    - Sector index change percentage
    """
    try:
        df = ak.stock_sector_fund_flow_rank()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Concept Data
@mcp.tool()
def stock_board_concept_name_em() -> str:
    """Get a list of all stock concept boards from Eastmoney.
    
    Returns a list of concept boards including:
    - Concept code
    - Concept name
    - Number of stocks
    - Average price
    - Change percentage
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
    
    Args:
        symbol: Concept board code (e.g., BK0501 for 5G)
        
    Returns stocks in the concept board including:
    - Stock code
    - Stock name
    - Latest price
    - Change percentage
    - And other market metrics
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
    
    Returns a list of industry boards including:
    - Industry code
    - Industry name
    - Number of stocks
    - Average price
    - Change percentage
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
    
    Args:
        symbol: Industry board code (e.g., BK0475 for banks)
        
    Returns stocks in the industry board including:
    - Stock code
    - Stock name
    - Latest price
    - Change percentage
    - And other market metrics
    """
    try:
        df = ak.stock_board_industry_cons_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Financial Report
@mcp.tool()
def stock_financial_analysis_indicator(symbol: str) -> str:
    """Get financial analysis indicators for a specific stock.
    
    Args:
        symbol: Stock symbol (e.g., 600000)
        
    Returns financial analysis data including:
    - Revenue growth
    - Profit growth
    - Gross margin
    - Net margin
    - And other financial indicators
    """
    try:
        df = ak.stock_financial_analysis_indicator(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Dividend
@mcp.tool()
def stock_dividend_cninfo(symbol: str) -> str:
    """Get dividend history for a specific stock from CNINFO.
    
    Args:
        symbol: Stock symbol (e.g., 600000)
        
    Returns dividend history including:
    - Announcement date
    - Ex-dividend date
    - Record date
    - Dividend amount
    - Dividend yield
    """
    try:
        df = ak.stock_dividend_cninfo(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Margin Trading
@mcp.tool()
def stock_margin_sse() -> str:
    """Get margin trading summary for Shanghai Stock Exchange.
    
    Returns margin trading summary including:
    - Date
    - Margin buying amount
    - Margin buying balance
    - Short selling amount
    - Short selling balance
    """
    try:
        df = ak.stock_margin_sse()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Short Interest
@mcp.tool()
def stock_institute_hold(quarter: str = "") -> str:
    """Get institutional investors' holdings data.
    
    Args:
        quarter: Quarter in format YYYYQ (e.g., 20234 for 2023Q4), default is empty for the latest data
        
    Returns institutional holdings data including:
    - Stock code
    - Stock name
    - Institution name
    - Holding amount
    - Holding value
    - Holding percentage
    """
    try:
        df = ak.stock_institute_hold(quarter=quarter)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Forecast
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
    """
    try:
        df = ak.stock_analyst_detail_em(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock News
@mcp.tool()
def stock_news_em() -> str:
    """Get latest stock market news from Eastmoney.
    
    Returns news data including:
    - News title
    - News content
    - News time
    - News source
    """
    try:
        df = ak.stock_news_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Company News
@mcp.tool()
def stock_notice_report() -> str:
    """Get latest stock announcements.
    
    Returns announcement data including:
    - Stock code
    - Stock name
    - Announcement title
    - Announcement time
    - Announcement link
    """
    try:
        df = ak.stock_notice_report()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Company Announcements
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
    """
    try:
        df = ak.stock_individual_fund_flow_rank()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Sector Fund Flow
@mcp.tool()
def stock_market_activity_legu() -> str:
    """Get market sentiment and activity data.
    
    Returns market sentiment data including:
    - Date
    - Market activity
    - Bullish sentiment
    - Bearish sentiment
    - Turnover rate
    """
    try:
        df = ak.stock_market_activity_legu()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Market PE
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
    """
    try:
        df = ak.stock_hk_spot_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - HK Stock Daily
@mcp.tool()
def stock_hk_daily(symbol: str) -> str:
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
    """
    try:
        df = ak.stock_hk_daily(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - US Stocks List
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
    """
    try:
        df = ak.stock_us_daily(symbol=symbol)
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - US Stock Financials
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
    """
    try:
        df = ak.stock_repurchase_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Restricted Shares
@mcp.tool()
def stock_margin_underlying_info_szse() -> str:
    """Get list of securities eligible for margin trading in Shenzhen Stock Exchange.
    
    Returns margin trading securities list including:
    - Stock code
    - Stock name
    - Inclusion date
    - Status
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
    """
    try:
        df = ak.stock_account_statistics_em()
        return format_dataframe_to_json(df)
    except Exception as e:
        return json.dumps({"error": str(e)})

# Stock Market - Stock Account Opening

