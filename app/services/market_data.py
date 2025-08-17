# # import yfinance as yf
# # import requests
# # from typing import Dict, List, Optional
# # import pandas as pd

# # class MarketDataService:
# #     def __init__(self):
# #         self.nse_base_url = "https://www.nseindia.com/api"
# #         self.bse_base_url = "https://api.bseindia.com"
    
# #     def get_stock_price(self, symbol: str, exchange: str = "NSE") -> Dict:
# #         """Get current stock price"""
# #         try:
# #             if exchange.upper() == "NSE":
# #                 # For NSE stocks, append .NS
# #                 ticker = f"{symbol}.NS"
# #             elif exchange.upper() == "BSE":
# #                 # For BSE stocks, append .BO
# #                 ticker = f"{symbol}.BO"
# #             else:
# #                 ticker = symbol
            
# #             stock = yf.Ticker(ticker)
# #             info = stock.info
# #             history = stock.history(period="1d")
            
# #             return {
# #                 "symbol": symbol,
# #                 "current_price": info.get("currentPrice", history['Close'].iloc[-1]),
# #                 "previous_close": info.get("previousClose"),
# #                 "change": info.get("regularMarketChange"),
# #                 "change_percent": info.get("regularMarketChangePercent"),
# #                 "volume": info.get("volume"),
# #                 "market_cap": info.get("marketCap"),
# #                 "pe_ratio": info.get("trailingPE")
# #             }
# #         except Exception as e:
# #             return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}
    
# #     def get_top_gainers_losers(self, market: str = "NSE", period: str = "1d") -> Dict:
# #         """Get top gainers and losers"""
# #         try:
# #             if market.upper() == "NSE":
# #                 # Get NIFTY 50 components
# #                 nifty50_symbols = [
# #                     "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE",
# #                     "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA",
# #                     "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM",
# #                     "HCLTECH", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO",
# #                     "HINDUNILVR", "HDFC", "ICICIBANK", "ITC", "INDUSINDBK",
# #                     "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "M&M",
# #                     "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID",
# #                     "RELIANCE", "SBILIFE", "SHREECEM", "SBIN", "SUNPHARMA",
# #                     "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM",
# #                     "TITAN", "ULTRACEMCO", "UPL", "WIPRO", "ZEEL"
# #                 ]
# #             else:
# #                 nifty50_symbols = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR"]
            
# #             stock_data = []
# #             for symbol in nifty50_symbols[:20]:  # Limit to first 20 for demo
# #                 data = self.get_stock_price(symbol)
# #                 if "error" not in data:
# #                     stock_data.append(data)
            
# #             # Sort by change percentage
# #             gainers = sorted(stock_data, key=lambda x: x.get("change_percent", 0), reverse=True)[:5]
# #             losers = sorted(stock_data, key=lambda x: x.get("change_percent", 0))[:5]
            
# #             return {
# #                 "top_gainers": gainers,
# #                 "top_losers": losers
# #             }
# #         except Exception as e:
# #             return {"error": f"Failed to fetch gainers/losers: {str(e)}"}
    
# #     def get_index_data(self, index_name: str) -> Dict:
# #         """Get index data (NIFTY, SENSEX, etc.)"""
# #         index_mapping = {
# #             "NIFTY": "^NSEI",
# #             "SENSEX": "^BSESN",
# #             "NASDAQ": "^IXIC",
# #             "SP500": "^GSPC"
# #         }
        
# #         try:
# #             ticker = index_mapping.get(index_name.upper(), index_name)
# #             index = yf.Ticker(ticker)
# #             history = index.history(period="1d")
# #             info = index.info
            
# #             return {
# #                 "index": index_name,
# #                 "current_value": history['Close'].iloc[-1],
# #                 "previous_close": history['Close'].iloc[-2] if len(history) > 1 else None,
# #                 "change": history['Close'].iloc[-1] - history['Close'].iloc[-2] if len(history) > 1 else 0,
# #                 "volume": history['Volume'].iloc[-1]
# #             }
# #         except Exception as e:
# #             return {"error": f"Failed to fetch index data for {index_name}: {str(e)}"}



# import yfinance as yf
# import requests
# from typing import Dict, List, Optional
# import pandas as pd
# import time

# class MarketDataService:
#     def __init__(self):
#         self.nse_base_url = "https://www.nseindia.com/api"
#         self.bse_base_url = "https://api.bseindia.com"

#     def get_stock_price(self, symbol: str, exchange: str = "NSE") -> Dict:
#         # ... your existing code ...

#     def get_top_gainers_losers(self, market: str = "NSE", period: str = "1d") -> Dict:
#         # ... your existing code ...

#     def get_index_data(self, index_name: str) -> Dict:
#         """Get index data with retry logic and better error handling"""
#         index_mapping = {
#             "NIFTY": "^NSEI",
#             "SENSEX": "^BSESN", 
#             "NASDAQ": "^IXIC",
#             "SP500": "^GSPC"
#         }

#         ticker = index_mapping.get(index_name.upper(), index_name)
#         max_retries = 3
        
#         for attempt in range(max_retries):
#             try:
#                 # Create ticker object
#                 index = yf.Ticker(ticker)
                
#                 # Get history with timeout
#                 history = index.history(period="2d")  # Get 2 days to ensure we have data
                
#                 # Check if data is empty
#                 if history.empty or len(history) == 0:
#                     raise ValueError(f"No data available for index {index_name}")
                
#                 # Get the most recent data
#                 current_value = float(history['Close'].iloc[-1])
#                 previous_close = float(history['Close'].iloc[-2]) if len(history) > 1 else None
#                 change = current_value - previous_close if previous_close is not None else 0
#                 volume = float(history['Volume'].iloc[-1]) if 'Volume' in history.columns else 0
                
#                 return {
#                     "index": index_name,
#                     "current_value": round(current_value, 2),
#                     "previous_close": round(previous_close, 2) if previous_close else None,
#                     "change": round(change, 2),
#                     "volume": int(volume)
#                 }
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed for {index_name}: {str(e)}")
                
#                 if attempt < max_retries - 1:
#                     # Wait before retrying
#                     time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
#                     continue
#                 else:
#                     # Final attempt failed
#                     return {
#                         "error": f"Failed to fetch index data for {index_name} after {max_retries} attempts: {str(e)}"
#                     }




import yfinance as yf
import requests
from typing import Dict, List, Optional
import pandas as pd
import time

class MarketDataService:
    def __init__(self):
        self.nse_base_url = "https://www.nseindia.com/api"
        self.bse_base_url = "https://api.bseindia.com"

    def get_stock_price(self, symbol: str, exchange: str = "NSE") -> Dict:
        """Get current stock price"""
        try:
            if exchange.upper() == "NSE":
                # For NSE stocks, append .NS
                ticker = f"{symbol}.NS"
            elif exchange.upper() == "BSE":
                # For BSE stocks, append .BO
                ticker = f"{symbol}.BO"
            else:
                ticker = symbol

            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="1d")

            return {
                "symbol": symbol,
                "current_price": info.get("currentPrice", history['Close'].iloc[-1]),
                "previous_close": info.get("previousClose"),
                "change": info.get("regularMarketChange"),
                "change_percent": info.get("regularMarketChangePercent"),
                "volume": info.get("volume"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE")
            }
        except Exception as e:
            return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}

    def get_top_gainers_losers(self, market: str = "NSE", period: str = "1d") -> Dict:
        """Get top gainers and losers"""
        try:
            if market.upper() == "NSE":
                # Get NIFTY 50 components
                nifty50_symbols = [
                    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE",
                    "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA",
                    "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM",
                    "HCLTECH", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO",
                    "HINDUNILVR", "HDFC", "ICICIBANK", "ITC", "INDUSINDBK",
                    "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "M&M",
                    "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID",
                    "RELIANCE", "SBILIFE", "SHREECEM", "SBIN", "SUNPHARMA",
                    "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM",
                    "TITAN", "ULTRACEMCO", "UPL", "WIPRO", "ZEEL"
                ]
            else:
                nifty50_symbols = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR"]

            stock_data = []
            for symbol in nifty50_symbols[:20]:  # Limit to first 20 for demo
                data = self.get_stock_price(symbol)
                if "error" not in data:
                    stock_data.append(data)

            # Sort by change percentage
            gainers = sorted(stock_data, key=lambda x: x.get("change_percent", 0), reverse=True)[:5]
            losers = sorted(stock_data, key=lambda x: x.get("change_percent", 0))[:5]

            return {
                "top_gainers": gainers,
                "top_losers": losers
            }
        except Exception as e:
            return {"error": f"Failed to fetch gainers/losers: {str(e)}"}

    def get_index_data(self, index_name: str) -> Dict:
        """Get index data with retry logic and fallback"""
        index_mapping = {
            "NIFTY": "^NSEI",
            "SENSEX": "^BSESN", 
            "NASDAQ": "^IXIC",
            "SP500": "^GSPC"
        }

        ticker = index_mapping.get(index_name.upper(), index_name)
        max_retries = 3
        
        # Try primary method first
        for attempt in range(max_retries):
            try:
                index = yf.Ticker(ticker)
                history = index.history(period="2d")  # Get 2 days to ensure we have data
                
                if history.empty or len(history) == 0:
                    raise ValueError(f"No data available for index {index_name}")
                
                current_value = float(history['Close'].iloc[-1])
                previous_close = float(history['Close'].iloc[-2]) if len(history) > 1 else None
                change = current_value - previous_close if previous_close is not None else 0
                volume = float(history['Volume'].iloc[-1]) if 'Volume' in history.columns else 0
                
                return {
                    "index": index_name,
                    "current_value": round(current_value, 2),
                    "previous_close": round(previous_close, 2) if previous_close else None,
                    "change": round(change, 2),
                    "volume": int(volume)
                }
                
            except Exception as e:
                print(f"Primary method attempt {attempt + 1} failed for {index_name}: {str(e)}")
                
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    # Primary method failed, try fallback
                    print(f"Trying fallback method for {index_name}")
                    return self.get_index_data_fallback(index_name)

    def get_index_data_fallback(self, index_name: str) -> Dict:
        """Fallback method using different approach"""
        try:
            # Try downloading directly
            if index_name.upper() == "NIFTY":
                ticker = "^NSEI"
            elif index_name.upper() == "SENSEX":
                ticker = "^BSESN"
            elif index_name.upper() == "NASDAQ":
                ticker = "^IXIC"
            elif index_name.upper() == "SP500":
                ticker = "^GSPC"
            else:
                ticker = f"^{index_name}"
                
            # Use download method instead of Ticker
            data = yf.download(ticker, period="2d", interval="1d", progress=False)
            
            if data.empty:
                raise ValueError(f"No data for {index_name}")
                
            current_value = float(data['Close'].iloc[-1])
            previous_close = float(data['Close'].iloc[-2]) if len(data) > 1 else None
            
            return {
                "index": index_name,
                "current_value": round(current_value, 2),
                "previous_close": round(previous_close, 2) if previous_close else None,
                "change": round(current_value - previous_close, 2) if previous_close else 0,
                "volume": int(data['Volume'].iloc[-1]) if 'Volume' in data.columns else 0
            }
        except Exception as e:
            return {"error": f"Fallback method failed for {index_name}: {str(e)}"}
