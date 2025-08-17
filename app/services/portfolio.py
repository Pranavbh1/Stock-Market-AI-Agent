from sqlalchemy.orm import Session
from app.models.database import Transaction, SessionLocal, TransactionTypeEnum  # Add TransactionTypeEnum import
from app.models.schemas import TransactionCreate, PortfolioSummary
from app.services.market_data import MarketDataService
from typing import List, Dict
from collections import defaultdict

class PortfolioService:
    def __init__(self):
        self.market_service = MarketDataService()

    def add_transaction(self, transaction: TransactionCreate) -> Transaction:
        """Add a new transaction"""
        db = SessionLocal()
        try:
            db_transaction = Transaction(
                stock_symbol=transaction.stock_symbol.upper(),
                transaction_type=TransactionTypeEnum(transaction.transaction_type.value),  # Convert to enum
                price=transaction.price,
                quantity=transaction.quantity
            )
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)
            return db_transaction
        finally:
            db.close()

    def get_portfolio_summary(self) -> List[PortfolioSummary]:
        """Get complete portfolio summary"""
        db = SessionLocal()
        try:
            transactions = db.query(Transaction).all()
            # Group transactions by stock symbol
            stock_positions = defaultdict(list)
            for transaction in transactions:
                stock_positions[transaction.stock_symbol].append(transaction)

            portfolio = []
            for symbol, trans_list in stock_positions.items():
                summary = self._calculate_position_summary(symbol, trans_list)
                if summary['total_quantity'] > 0:  # Only include positions we still hold
                    portfolio.append(summary)
            return portfolio
        finally:
            db.close()

    def _calculate_position_summary(self, symbol: str, transactions: List[Transaction]) -> Dict:
        """Calculate position summary for a stock"""
        total_bought = 0
        total_sold = 0
        total_buy_value = 0
        total_sell_value = 0

        for trans in transactions:
            if trans.transaction_type.value == "buy":
                total_bought += trans.quantity
                total_buy_value += trans.quantity * trans.price
            else:  # sell
                total_sold += trans.quantity
                total_sell_value += trans.quantity * trans.price

        current_quantity = total_bought - total_sold
        avg_buy_price = total_buy_value / total_bought if total_bought > 0 else 0

        # Get current market price
        current_data = self.market_service.get_stock_price(symbol)
        current_price = current_data.get('current_price', 0)

        if current_quantity > 0:
            current_value = current_quantity * current_price
            invested_value = current_quantity * avg_buy_price
            profit_loss = current_value - invested_value
            profit_loss_percentage = (profit_loss / invested_value) * 100 if invested_value > 0 else 0
        else:
            profit_loss = total_sell_value - (total_sold * avg_buy_price)
            profit_loss_percentage = (profit_loss / (total_sold * avg_buy_price)) * 100 if total_sold > 0 else 0

        return {
            "stock_symbol": symbol,
            "total_quantity": current_quantity,
            "avg_buy_price": round(avg_buy_price, 2),
            "current_price": round(current_price, 2),
            "profit_loss": round(profit_loss, 2),
            "profit_loss_percentage": round(profit_loss_percentage, 2)
        }

    def process_sell_transaction(self, symbol: str, quantity: int, price: float) -> Dict:
        """Process sell transaction and update portfolio"""
        # First check if we have enough quantity
        db = SessionLocal()
        try:
            transactions = db.query(Transaction).filter(Transaction.stock_symbol == symbol.upper()).all()
            total_bought = sum(t.quantity for t in transactions if t.transaction_type.value == "buy")
            total_sold = sum(t.quantity for t in transactions if t.transaction_type.value == "sell")
            available_quantity = total_bought - total_sold

            if available_quantity < quantity:
                return {
                    "success": False,
                    "message": f"Insufficient quantity. Available: {available_quantity}, Requested: {quantity}"
                }

            # Add sell transaction
            sell_transaction = TransactionCreate(
                stock_symbol=symbol,
                transaction_type="sell",
                price=price,
                quantity=quantity
            )

            new_transaction = self.add_transaction(sell_transaction)

            return {
                "success": True,
                "message": f"Successfully sold {quantity} shares of {symbol} at {price}",
                "transaction_id": new_transaction.id,
                "remaining_quantity": available_quantity - quantity
            }
        finally:
            db.close()
