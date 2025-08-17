# # from langchain.embeddings import OllamaEmbeddings
# # from langchain.vectorstores import FAISS
# # from langchain.llms import Ollama
# # from langchain.chains import RetrievalQA
# # from langchain.text_splitter import RecursiveCharacterTextSplitter
# # from langchain.document_loaders import WebBaseLoader
# # import google.generativeai as genai
# # from typing import List, Dict
# # # import google.generativeai as genai    # already used in ai_agent.py

# # import os

# # class AIAgent:
# #     def __init__(self):
# #         # Initialize Gemini
# #         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# #         # self.gemini_model = genai.GenerativeModel('gemini-pro')
# #         self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

        
# #         # Initialize Ollama embeddings
# #         self.embeddings = OllamaEmbeddings(model="llama2")
        
# #         # Initialize vector store (will be populated with financial data)
# #         self.vector_store = None
# #         self.qa_chain = None
        
# #         # Initialize knowledge base
# #         self._initialize_knowledge_base()
    
# #     def _initialize_knowledge_base(self):
# #         """Initialize the knowledge base with financial data"""
# #         # You can add financial websites, reports, etc. here
# #         financial_urls = [
# #             "https://www.moneycontrol.com",
# #             "https://economictimes.indiatimes.com/markets",
# #             # Add more relevant financial data sources
# #         ]
        
# #         documents = []
# #         text_splitter = RecursiveCharacterTextSplitter(
# #             chunk_size=1000,
# #             chunk_overlap=200
# #         )
        
# #         # Load and process documents (implement based on your needs)
# #         # For now, we'll create a simple vector store with basic financial concepts
# #         sample_docs = [
# #             "Stock market analysis involves evaluating company fundamentals and technical indicators.",
# #             "BSE and NSE are the major stock exchanges in India.",
# #             "NIFTY 50 represents the top 50 companies by market cap on NSE.",
# #             "PE ratio is price-to-earnings ratio, indicating stock valuation.",
# #             "Portfolio diversification helps reduce investment risk."
# #         ]
        
# #         try:
# #             self.vector_store = FAISS.from_texts(sample_docs, self.embeddings)
            
# #             # Create QA chain
# #             llm = Ollama(model="llama2")
# #             self.qa_chain = RetrievalQA.from_chain_type(
# #                 llm=llm,
# #                 chain_type="stuff",
# #                 retriever=self.vector_store.as_retriever()
# #             )
# #         except Exception as e:
# #             print(f"Warning: Could not initialize vector store: {e}")
    
# #     def process_query(self, query: str, market_context: Dict = None) -> Dict:
# #         """Process user query and generate AI response"""
# #         try:
# #             # Enhance query with market context if available
# #             enhanced_query = self._enhance_query_with_context(query, market_context)
            
# #             # Try using the QA chain first
# #             if self.qa_chain:
# #                 try:
# #                     response = self.qa_chain.run(enhanced_query)
# #                 except:
# #                     # Fallback to Gemini
# #                     response = self._query_gemini(enhanced_query)
# #             else:
# #                 # Use Gemini directly
# #                 response = self._query_gemini(enhanced_query)
            
# #             return {
# #                 "query": query,
# #                 "response": response,
# #                 "sources": ["AI Analysis", "Market Data"]
# #             }
# #         except Exception as e:
# #             return {
# #                 "query": query,
# #                 "response": f"I apologize, but I encountered an error processing your query: {str(e)}",
# #                 "sources": []
# #             }
    
# #     def _enhance_query_with_context(self, query: str, context: Dict = None) -> str:
# #         """Enhance query with market context"""
# #         if not context:
# #             return query
            
# #         context_str = f"""
# #         Current Market Context:
# #         - Query: {query}
# #         - Additional Context: {context}
        
# #         Please provide a detailed analysis based on the query and context.
# #         """
# #         return context_str
    
# #     def _query_gemini(self, query: str) -> str:
# #         """Query Gemini for responses"""
# #         try:
# #             response = self.gemini_model.generate_content(query)
# #             return response.text
# #         except Exception as e:
# #             return f"Unable to generate AI response: {str(e)}"
    
# #     def analyze_stock_recommendation(self, query: str) -> Dict:
# #         """Provide stock recommendations based on query"""
# #         recommendation_prompt = f"""
# #         As a financial advisor, analyze this query: {query}
        
# #         Provide recommendations considering:
# #         1. Market fundamentals
# #         2. Technical analysis
# #         3. Risk factors
# #         4. Time horizon
# #         5. Diversification
        
# #         Format your response with clear reasoning and risk warnings.
# #         """
        
# #         response = self._query_gemini(recommendation_prompt)
        
# #         return {
# #             "query": query,
# #             "recommendation": response,
# #             "disclaimer": "This is AI-generated advice. Please consult with a financial advisor before making investment decisions."
# #         }


# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.llms import Ollama
# from langchain.chains import RetrievalQA
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import WebBaseLoader
# import google.generativeai as genai
# from typing import List, Dict, Optional
# import os
# import re

# class AIAgent:
#     def __init__(self):
#         """Initialize the AI Agent with Gemini and optional Ollama support"""
#         # Initialize Gemini with updated model name
#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#         self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
        
#         # Initialize Ollama components (optional)
#         self.embeddings = None
#         self.vector_store = None
#         self.qa_chain = None
        
#         # Try to initialize Ollama (gracefully handle failure)
#         try:
#             self._initialize_knowledge_base()
#         except Exception as e:
#             print(f"Ollama not available, using Gemini only: {e}")

#     def _initialize_knowledge_base(self):
#         """Initialize the knowledge base with financial data"""
#         try:
#             # Initialize Ollama embeddings
#             self.embeddings = OllamaEmbeddings(model="llama2")
            
#             # Enhanced financial knowledge base
#             sample_docs = [
#                 "Stock market analysis involves evaluating company fundamentals like P/E ratio, revenue growth, and debt levels.",
#                 "Technical analysis uses chart patterns, moving averages, RSI, and volume indicators to predict price movements.",
#                 "BSE and NSE are India's major stock exchanges. NSE is larger by trading volume.",
#                 "NIFTY 50 represents the top 50 companies by market cap on NSE, serving as a market benchmark.",
#                 "PE ratio compares stock price to earnings per share. Lower PE may indicate undervaluation.",
#                 "Portfolio diversification across sectors, market caps, and asset classes reduces risk.",
#                 "Market sentiment indicators include VIX (volatility index), FII/DII flows, and sector rotation.",
#                 "Support and resistance levels are key price points where stocks tend to reverse direction.",
#                 "Volume analysis confirms price movements. High volume with price increase suggests strong trend.",
#                 "Economic indicators like GDP, inflation, interest rates significantly impact stock markets."
#             ]
            
#             # Create vector store
#             self.vector_store = FAISS.from_texts(sample_docs, self.embeddings)
            
#             # Create QA chain
#             llm = Ollama(model="llama2")
#             self.qa_chain = RetrievalQA.from_chain_type(
#                 llm=llm,
#                 chain_type="stuff",
#                 retriever=self.vector_store.as_retriever()
#             )
            
#             print("Successfully initialized Ollama knowledge base")
            
#         except Exception as e:
#             print(f"Warning: Could not initialize Ollama vector store: {e}")
#             self.embeddings = None
#             self.vector_store = None
#             self.qa_chain = None

#     def process_query(self, query: str, market_context: Dict = None) -> Dict:
#         """Process user query and generate enhanced AI response"""
#         try:
#             # Extract stock symbols from query for context
#             stock_symbols = self._extract_stock_symbols(query)
            
#             # Enhance query with market context
#             enhanced_query = self._enhance_query_with_context(query, market_context, stock_symbols)
            
#             # Try QA chain first (if available), then fallback to Gemini
#             if self.qa_chain:
#                 try:
#                     response = self.qa_chain.run(enhanced_query)
#                     # If response is too generic, enhance with Gemini
#                     if len(response) < 100 or "I don't know" in response:
#                         response = self._query_gemini_enhanced(enhanced_query)
#                 except Exception:
#                     response = self._query_gemini_enhanced(enhanced_query)
#             else:
#                 response = self._query_gemini_enhanced(enhanced_query)

#             return {
#                 "query": query,
#                 "response": response,
#                 "sources": ["Market Analysis", "Technical Indicators", "Financial Data"]
#             }
#         except Exception as e:
#             return {
#                 "query": query,
#                 "response": f"I encountered an error analyzing your query: {str(e)}. Please try rephrasing your question.",
#                 "sources": []
#             }

#     def _enhance_query_with_context(self, query: str, market_context: Dict = None, stock_symbols: List[str] = None) -> str:
#         """Enhance query with comprehensive market context"""
#         context_parts = [f"User Query: {query}"]
        
#         if market_context:
#             context_parts.append(f"Current Market Data: {market_context}")
        
#         if stock_symbols:
#             context_parts.append(f"Mentioned Stocks: {', '.join(stock_symbols)}")
        
#         enhanced_query = "\n".join(context_parts)
#         return enhanced_query

#     def _query_gemini_enhanced(self, query: str) -> str:
#         """Enhanced Gemini query with better prompting"""
#         try:
#             prompt = f"""
# As a knowledgeable market analyst, provide detailed educational analysis for this query:

# {query}

# Please include specific insights about:
# 1. **Market Trends & Data**: Current patterns, historical context, and relevant statistics
# 2. **Technical Analysis**: Chart patterns, indicators, and technical signals if applicable
# 3. **Fundamental Factors**: Company/sector fundamentals, earnings, financial metrics
# 4. **Risk Assessment**: Potential risks, volatility factors, and market conditions
# 5. **Educational Context**: Explain concepts and terminology for better understanding

# Provide actionable insights while being educational. Use specific examples and data where possible.

# Format your response with clear sections and practical insights.

# Important: This is educational market analysis. Always emphasize the importance of personal research and professional consultation for investment decisions.
# """
            
#             response = self.gemini_model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             return f"Unable to generate market analysis: {str(e)}"

#     def analyze_stock_recommendation(self, query: str) -> Dict:
#         """Provide comprehensive stock analysis and recommendations"""
#         recommendation_prompt = f"""
# As a professional market analyst, provide comprehensive educational analysis for: {query}

# Structure your analysis as follows:

# **MARKET ANALYSIS:**
# - Current market trends and sentiment
# - Sector performance and outlook
# - Technical indicators and patterns

# **FUNDAMENTAL ANALYSIS:**
# - Company/sector fundamentals if specific stocks mentioned
# - Financial metrics and valuations
# - Growth prospects and competitive position

# **TECHNICAL INSIGHTS:**
# - Chart patterns and technical signals
# - Support/resistance levels
# - Volume analysis and momentum indicators

# **RISK FACTORS:**
# - Market risks and volatility concerns
# - Sector-specific risks
# - Economic and regulatory factors

# **EDUCATIONAL SCENARIOS:**
# Present 3 scenarios:
# 1. **Bullish Case**: Positive factors and potential upside
# 2. **Bearish Case**: Negative factors and potential downside  
# 3. **Neutral Case**: Balanced view and key factors to monitor

# **KEY TAKEAWAYS:**
# - Specific observations and insights
# - Important metrics to track
# - Timeline considerations

# Provide specific, actionable educational insights while maintaining analytical objectivity.

# End with: "This analysis is for educational purposes. Conduct thorough research and consult qualified financial advisors before making investment decisions."
# """
        
#         response = self._query_gemini_enhanced(recommendation_prompt)
        
#         return {
#             "query": query,
#             "recommendation": response,
#             "disclaimer": "Educational market analysis only. Always conduct independent research and consult licensed financial professionals for investment advice."
#         }

#     def analyze_market_sentiment(self, market_data: Dict) -> str:
#         """Analyze current market sentiment from data"""
#         try:
#             sentiment_prompt = f"""
# Analyze the current market sentiment based on this data:

# {market_data}

# Provide insights on:
# 1. **Market Direction**: Overall trend analysis
# 2. **Sector Rotation**: Which sectors are gaining/losing favor
# 3. **Volatility Assessment**: Current market stability
# 4. **Key Drivers**: Main factors influencing market movement
# 5. **Short-term Outlook**: What to expect in the near term

# Focus on educational analysis of market patterns and investor behavior.
# """
            
#             response = self.gemini_model.generate_content(sentiment_prompt)
#             return response.text
#         except Exception as e:
#             return f"Unable to analyze market sentiment: {str(e)}"

#     def explain_concept(self, concept: str) -> str:
#         """Explain financial concepts in detail"""
#         try:
#             concept_prompt = f"""
# Provide a comprehensive educational explanation of: {concept}

# Include:
# 1. **Definition**: Clear, simple explanation
# 2. **How it Works**: Practical mechanics and calculations
# 3. **Why it Matters**: Importance for investors
# 4. **Real Examples**: Practical examples and scenarios
# 5. **Common Mistakes**: What to avoid
# 6. **Pro Tips**: Advanced insights and best practices

# Make it educational and actionable for both beginners and intermediate investors.
# """
            
#             response = self.gemini_model.generate_content(concept_prompt)
#             return response.text
#         except Exception as e:
#             return f"Unable to explain concept: {str(e)}"

#     def _extract_stock_symbols(self, query: str) -> List[str]:
#         """Extract potential stock symbols from query"""
#         # Common Indian stock symbols pattern
#         symbols = re.findall(r'\b[A-Z]{2,10}\b', query.upper())
        
#         # Filter out common words that might match the pattern
#         exclude_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'HAD', 'BY'}
#         symbols = [s for s in symbols if s not in exclude_words and len(s) <= 10]
        
#         return symbols

#     def get_trading_strategy(self, query: str, timeframe: str = "medium") -> Dict:
#         """Provide educational trading strategy insights"""
#         try:
#             strategy_prompt = f"""
# Based on this query: {query}
# Timeframe: {timeframe}

# Provide educational insights on trading strategies:

# **STRATEGY FRAMEWORK:**
# 1. **Entry Strategy**: When and how to enter positions
# 2. **Risk Management**: Position sizing, stop-losses, risk-reward ratios
# 3. **Exit Strategy**: Profit-taking and loss-cutting approaches
# 4. **Time Management**: Optimal holding periods and timing

# **TECHNICAL APPROACH:**
# - Key indicators to monitor
# - Chart patterns to watch
# - Volume and momentum signals

# **FUNDAMENTAL CONSIDERATIONS:**
# - Important metrics and catalysts
# - Sector and market factors
# - Economic indicators impact

# **RISK CONTROLS:**
# - Maximum position sizes
# - Diversification requirements
# - Market condition adjustments

# Emphasize this is educational content for learning purposes only.
# """
            
#             response = self._query_gemini_enhanced(strategy_prompt)
            
#             return {
#                 "strategy": response,
#                 "timeframe": timeframe,
#                 "disclaimer": "Educational trading concepts only. Practice with virtual trading and consult professionals before implementing real strategies."
#             }
#         except Exception as e:
#             return {
#                 "strategy": f"Unable to generate strategy insights: {str(e)}",
#                 "timeframe": timeframe,
#                 "disclaimer": "Please consult qualified financial advisors for trading strategies."
#             }

#     def analyze_portfolio_query(self, query: str, portfolio_data: Optional[Dict] = None) -> str:
#         """Analyze portfolio-related queries"""
#         try:
#             portfolio_prompt = f"""
# Analyze this portfolio query: {query}

# ${f"Current Portfolio: {portfolio_data}" if portfolio_data else ""}

# Provide insights on:
# 1. **Portfolio Health**: Balance, diversification, risk assessment
# 2. **Optimization Ideas**: Potential improvements and adjustments
# 3. **Risk Analysis**: Concentration risks and volatility factors
# 4. **Performance Metrics**: Key ratios and benchmarks to track
# 5. **Rebalancing Strategy**: When and how to adjust positions

# Focus on educational portfolio management principles.
# """
            
#             response = self.gemini_model.generate_content(portfolio_prompt)
#             return response.text
#         except Exception as e:
#             return f"Unable to analyze portfolio query: {str(e)}"

# # Additional utility functions for enhanced functionality
# def format_financial_number(number: float) -> str:
#     """Format financial numbers for better readability"""
#     if number >= 1e7:  # 1 crore
#         return f"₹{number/1e7:.2f} Cr"
#     elif number >= 1e5:  # 1 lakh
#         return f"₹{number/1e5:.2f} L"
#     elif number >= 1000:
#         return f"₹{number/1000:.2f} K"
#     else:
#         return f"₹{number:.2f}"



from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import google.generativeai as genai
from typing import List, Dict, Optional
import os
import re
import json
from datetime import datetime

class AIAgent:
    def __init__(self):
        """Initialize the AI Agent with memory and context awareness"""
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Memory storage for conversation context
        self.conversation_memory = []
        self.user_portfolio = None
        self.user_preferences = {}
        
        # Initialize Ollama components (optional)
        self.embeddings = None
        self.vector_store = None
        self.qa_chain = None
        
        try:
            self._initialize_knowledge_base()
        except Exception as e:
            print(f"Ollama not available, using Gemini only: {e}")

    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with financial data"""
        try:
            self.embeddings = OllamaEmbeddings(model="llama2")
            
            sample_docs = [
                "Stock market analysis involves evaluating company fundamentals like P/E ratio, revenue growth, and debt levels.",
                "Technical analysis uses chart patterns, moving averages, RSI, and volume indicators to predict price movements.",
                "BSE and NSE are India's major stock exchanges. NSE is larger by trading volume.",
                "NIFTY 50 represents the top 50 companies by market cap on NSE, serving as a market benchmark.",
                "PE ratio compares stock price to earnings per share. Lower PE may indicate undervaluation.",
                "Portfolio diversification across sectors, market caps, and asset classes reduces risk.",
                "Market sentiment indicators include VIX (volatility index), FII/DII flows, and sector rotation.",
                "Support and resistance levels are key price points where stocks tend to reverse direction.",
                "Volume analysis confirms price movements. High volume with price increase suggests strong trend.",
                "Economic indicators like GDP, inflation, interest rates significantly impact stock markets."
            ]
            
            self.vector_store = FAISS.from_texts(sample_docs, self.embeddings)
            llm = Ollama(model="llama2")
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever()
            )
            
            print("Successfully initialized Ollama knowledge base")
            
        except Exception as e:
            print(f"Warning: Could not initialize Ollama vector store: {e}")
            self.embeddings = None
            self.vector_store = None
            self.qa_chain = None

    def update_portfolio_context(self, portfolio_data: List[Dict]):
        """Update the bot's knowledge of user's current portfolio"""
        self.user_portfolio = portfolio_data
        
        # Create portfolio summary for context
        if portfolio_data:
            total_value = sum([p['total_quantity'] * p['current_price'] for p in portfolio_data])
            stocks_owned = [p['stock_symbol'] for p in portfolio_data]
            
            portfolio_summary = {
                "total_stocks": len(portfolio_data),
                "stocks_owned": stocks_owned,
                "total_portfolio_value": total_value,
                "last_updated": datetime.now().isoformat()
            }
            
            self.user_preferences['portfolio_summary'] = portfolio_summary

    def add_to_conversation_memory(self, user_input: str, bot_response: str):
        """Add conversation to memory for context"""
        self.conversation_memory.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "bot": bot_response
        })
        
        # Keep only last 10 conversations to avoid token limits
        if len(self.conversation_memory) > 10:
            self.conversation_memory = self.conversation_memory[-10:]

    def process_conversational_query(self, query: str, portfolio_data: Optional[List[Dict]] = None) -> Dict:
        """Process query with full conversational context and memory"""
        
        # Update portfolio context if provided
        if portfolio_data:
            self.update_portfolio_context(portfolio_data)
        
        # Detect query type and respond appropriately
        query_lower = query.lower().strip()
        
        # Handle simple greetings
        if self._is_greeting(query_lower):
            response = self._handle_greeting(query)
        # Handle portfolio-specific questions
        elif self._is_portfolio_question(query_lower):
            response = self._handle_portfolio_question(query)
        # Handle buying recommendations
        elif self._is_buying_question(query_lower):
            response = self._handle_buying_recommendation(query)
        # Handle general market questions
        else:
            response = self._handle_general_query(query)
        
        # Add to conversation memory
        self.add_to_conversation_memory(query, response)
        
        return {
            "query": query,
            "response": response,
            "sources": ["Personal Portfolio", "Market Data", "AI Analysis"],
            "conversation_id": len(self.conversation_memory)
        }

    def _is_greeting(self, query: str) -> bool:
        """Check if query is a simple greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you']
        return any(greeting in query for greeting in greetings)

    def _is_portfolio_question(self, query: str) -> bool:
        """Check if query is about user's portfolio"""
        portfolio_keywords = ['my portfolio', 'my stocks', 'my holdings', 'what do i own', 'my investments']
        return any(keyword in query for keyword in portfolio_keywords)

    def _is_buying_question(self, query: str) -> bool:
        """Check if query is about buying recommendations"""
        buying_keywords = ['what to buy', 'should i buy', 'recommend', 'monday', 'tomorrow', 'next week']
        return any(keyword in query for keyword in buying_keywords)

    def _handle_greeting(self, query: str) -> str:
        """Handle simple greetings conversationally"""
        greetings_responses = [
            "Hello! I'm your personal stock market assistant. I have access to your portfolio and can help you make informed investment decisions.",
            "Hi there! Ready to discuss your investments? I can see your current holdings and suggest new opportunities.",
            "Hey! Good to chat with you again. How can I help you with your portfolio today?",
            "Hello! I'm here to help you navigate the markets. What would you like to know about your investments?"
        ]
        
        # Add portfolio context if available
        if self.user_portfolio:
            portfolio_value = sum([p['total_quantity'] * p['current_price'] for p in self.user_portfolio])
            stocks_count = len(self.user_portfolio)
            
            return f"Hello! Great to see you again. I can see you currently hold {stocks_count} different stocks with a total portfolio value of ₹{portfolio_value:,.2f}. How can I help you today?"
        
        import random
        return random.choice(greetings_responses)

    def _handle_portfolio_question(self, query: str) -> str:
        """Handle questions about user's portfolio"""
        if not self.user_portfolio:
            return "I don't have access to your portfolio data right now. Please make sure you're logged in and try again."
        
        # Analyze portfolio and provide insights
        total_value = sum([p['total_quantity'] * p['current_price'] for p in self.user_portfolio])
        total_invested = sum([p['total_quantity'] * p['avg_buy_price'] for p in self.user_portfolio])
        total_pnl = total_value - total_invested
        pnl_percentage = (total_pnl / total_invested * 100) if total_invested > 0 else 0
        
        winners = [p for p in self.user_portfolio if p['profit_loss'] > 0]
        losers = [p for p in self.user_portfolio if p['profit_loss'] < 0]
        
        response = f"""📊 **Your Portfolio Overview:**

**Portfolio Summary:**
- Total Stocks: {len(self.user_portfolio)}
- Current Value: ₹{total_value:,.2f}
- Total Invested: ₹{total_invested:,.2f}
- Overall P&L: ₹{total_pnl:,.2f} ({pnl_percentage:.2f}%)

**Your Holdings:**
"""
        
        for stock in self.user_portfolio:
            status = "🟢" if stock['profit_loss'] > 0 else "🔴" if stock['profit_loss'] < 0 else "⚪"
            response += f"• {status} **{stock['stock_symbol']}**: {stock['total_quantity']} shares, ₹{stock['current_price']} (P&L: ₹{stock['profit_loss']})\n"
        
        if winners:
            best_performer = max(winners, key=lambda x: x['profit_loss_percentage'])
            response += f"\n🏆 **Best Performer**: {best_performer['stock_symbol']} (+{best_performer['profit_loss_percentage']:.2f}%)"
        
        if losers:
            worst_performer = min(losers, key=lambda x: x['profit_loss_percentage'])
            response += f"\n⚠️ **Needs Attention**: {worst_performer['stock_symbol']} ({worst_performer['profit_loss_percentage']:.2f}%)"
        
        return response

    def _handle_buying_recommendation(self, query: str) -> str:
        """Handle buying recommendations based on portfolio"""
        try:
            # Create context for recommendation
            portfolio_context = ""
            if self.user_portfolio:
                owned_stocks = [p['stock_symbol'] for p in self.user_portfolio]
                portfolio_value = sum([p['total_quantity'] * p['current_price'] for p in self.user_portfolio])
                
                portfolio_context = f"""
User's Current Portfolio:
- Stocks owned: {', '.join(owned_stocks)}
- Portfolio value: ₹{portfolio_value:,.2f}
- Number of holdings: {len(self.user_portfolio)}
"""
            
            prompt = f"""
You are a personal investment advisor. Based on the user's query: "{query}" and their portfolio context:

{portfolio_context}

Provide specific stock recommendations for Monday/this week with:

1. **3-5 Specific Stock Picks** with exact stock symbols (NSE/BSE)
2. **Why each stock** - brief reason for recommendation
3. **Diversification advice** - avoid over-concentration in sectors they already own
4. **Risk level** for each pick (Low/Medium/High)
5. **Suggested allocation** - how much to invest in each

Format as a clean list with actionable advice. Keep it conversational and personalized.

Remember: This is educational advice. Always do your own research.
"""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"I'm having trouble generating recommendations right now. Error: {str(e)}. Please try asking again!"

    def _handle_general_query(self, query: str) -> str:
        """Handle general market/stock questions"""
        try:
            # Add conversation context
            recent_context = ""
            if self.conversation_memory:
                recent_context = f"Recent conversation context: {self.conversation_memory[-3:]}"
            
            prompt = f"""
As a knowledgeable market advisor, answer this query conversationally: "{query}"

{recent_context}

Keep your response:
- Conversational and friendly
- Specific and actionable
- Under 200 words
- Educational but not overly technical

If asking about specific stocks, provide current market insights.
"""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"I'm having trouble processing that question. Could you try rephrasing it? Error: {str(e)}"

    # Keep your existing methods for compatibility
    def process_query(self, query: str, market_context: Dict = None) -> Dict:
        """Legacy method - redirects to conversational processing"""
        return self.process_conversational_query(query)
    
    def analyze_stock_recommendation(self, query: str) -> Dict:
        """Legacy method for stock recommendations"""
        response = self._handle_buying_recommendation(query)
        return {
            "query": query,
            "recommendation": response,
            "disclaimer": "This is educational advice. Please do your own research and consult professionals."
        }
