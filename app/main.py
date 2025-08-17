from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import *
from app.services.market_data import MarketDataService
from app.services.ai_agent import AIAgent
from app.services.portfolio import PortfolioService
from typing import List, Optional
import uuid

app = FastAPI(title="Stock Market AI Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
market_service = MarketDataService()
ai_agent = AIAgent()
portfolio_service = PortfolioService()

@app.get("/")
async def root():
    return {"message": "Stock Market AI Agent API is running!"}

# AI Chat endpoint with memory and context
@app.post("/chat/", response_model=QueryResponse)
async def chat_with_ai(query_request: QueryRequest, session_id: Optional[str] = None):
    """Conversational AI chat with memory and portfolio awareness"""
    try:
        # Get user's current portfolio for context
        portfolio_data = portfolio_service.get_portfolio_summary()
        
        # Process query with full conversational context
        response = ai_agent.process_conversational_query(
            query_request.query, 
            portfolio_data
        )
        
        return QueryResponse(
            query=query_request.query,
            response=response['response'],
            sources=response['sources']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced query endpoint (legacy support)
@app.post("/query/", response_model=QueryResponse)
async def process_query(query_request: QueryRequest):
    """Process queries with portfolio awareness"""
    try:
        # Get portfolio context
        portfolio_data = portfolio_service.get_portfolio_summary()
        
        # Update AI agent with current portfolio
        if portfolio_data:
            ai_agent.update_portfolio_context(portfolio_data)
        
        query = query_request.query.lower()
        
        if "top gainers" in query or "top losers" in query:
            market_data = market_service.get_top_gainers_losers()
            response = ai_agent.process_conversational_query(query_request.query, portfolio_data)
        elif "recommend" in query or "should buy" in query or "what to buy" in query:
            response = ai_agent.process_conversational_query(query_request.query, portfolio_data)
        else:
            response = ai_agent.process_conversational_query(query_request.query, portfolio_data)
        
        return QueryResponse(
            query=query_request.query,
            response=response['response'],
            sources=response['sources']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Transaction endpoints
@app.post("/transactions/", response_model=TransactionResponse)
async def add_transaction(transaction: TransactionCreate):
    """Add a buy/sell transaction"""
    try:
        db_transaction = portfolio_service.add_transaction(transaction)
        
        # Update AI agent's portfolio context after transaction
        portfolio_data = portfolio_service.get_portfolio_summary()
        ai_agent.update_portfolio_context(portfolio_data)
        
        return TransactionResponse(
            id=db_transaction.id,
            stock_symbol=db_transaction.stock_symbol,
            transaction_type=db_transaction.transaction_type.value,
            price=db_transaction.price,
            quantity=db_transaction.quantity,
            timestamp=db_transaction.timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio/")
async def get_portfolio():
    """Get portfolio summary"""
    try:
        portfolio_data = portfolio_service.get_portfolio_summary()
        # Update AI context whenever portfolio is accessed
        ai_agent.update_portfolio_context(portfolio_data)
        return portfolio_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sell/")
async def sell_stock(symbol: str, quantity: int, price: float):
    """Sell stocks and update portfolio"""
    try:
        result = portfolio_service.process_sell_transaction(symbol, quantity, price)
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['message'])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Market data endpoints
@app.get("/stock/{symbol}")
async def get_stock_data(symbol: str, exchange: str = "NSE"):
    """Get current stock price and data"""
    try:
        return market_service.get_stock_price(symbol, exchange)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/gainers-losers")
async def get_gainers_losers(market: str = "NSE", period: str = "1d"):
    """Get top gainers and losers"""
    try:
        return market_service.get_top_gainers_losers(market, period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/index/{index_name}")
async def get_index_data(index_name: str):
    """Get index data (NIFTY, SENSEX, etc.)"""
    try:
        return market_service.get_index_data(index_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Query endpoints
@app.post("/query/", response_model=QueryResponse)
async def process_query(query_request: QueryRequest):
    """Process natural language queries about stocks and market"""
    try:
        # Handle specific query patterns
        query = query_request.query.lower()
        
        if "top gainers" in query or "top losers" in query:
            market_data = market_service.get_top_gainers_losers()
            response = ai_agent.process_query(query_request.query, market_data)
        elif "recommend" in query or "should buy" in query or "profit in long run" in query:
            response = ai_agent.analyze_stock_recommendation(query_request.query)
            return QueryResponse(
                query=query_request.query,
                response=response['recommendation'],
                sources=[response['disclaimer']]
            )
        else:
            response = ai_agent.process_query(query_request.query)
        
        return QueryResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Specific query handlers for your examples
@app.get("/profit-loss/{symbol}")
async def calculate_profit_loss(symbol: str, sell_quantity: int):
    """Calculate profit/loss for selling specific quantity"""
    try:
        portfolio = portfolio_service.get_portfolio_summary()
        stock_position = next((p for p in portfolio if p['stock_symbol'].upper() == symbol.upper()), None)
        
        if not stock_position:
            raise HTTPException(status_code=404, detail=f"No position found for {symbol}")
        
        if stock_position['total_quantity'] < sell_quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient quantity. Available: {stock_position['total_quantity']}")
        
        current_price = stock_position['current_price']
        avg_buy_price = stock_position['avg_buy_price']
        
        profit_loss_per_share = current_price - avg_buy_price
        total_profit_loss = profit_loss_per_share * sell_quantity
        
        return {
            "symbol": symbol,
            "sell_quantity": sell_quantity,
            "current_price": current_price,
            "avg_buy_price": avg_buy_price,
            "profit_loss_per_share": round(profit_loss_per_share, 2),
            "total_profit_loss": round(total_profit_loss, 2),
            "remaining_quantity": stock_position['total_quantity'] - sell_quantity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
