from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class TransactionCreate(BaseModel):
    stock_symbol: str
    transaction_type: TransactionType
    price: float
    quantity: int
    
class TransactionResponse(BaseModel):
    id: int
    stock_symbol: str
    transaction_type: TransactionType
    price: float
    quantity: int
    timestamp: datetime
    
class PortfolioSummary(BaseModel):
    stock_symbol: str
    total_quantity: int
    avg_buy_price: float
    current_price: float
    profit_loss: float
    profit_loss_percentage: float

class QueryRequest(BaseModel):
    query: str
    
class QueryResponse(BaseModel):
    query: str
    response: str
    sources: Optional[List[str]] = None
