```markdown
# 🚀 Stock Market AI Agent



![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A powerful, AI-driven stock market portfolio management system with conversational insights**

[Demo](#demo) • [Features](#features) • [Installation](#installation) • [API Docs](#api-documentation) • [Contributing](#contributing)



---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [AI Capabilities](#ai-capabilities)
- [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **Stock Market AI Agent** is a comprehensive portfolio management platform that combines real-time market data with AI-powered insights. It features a conversational AI assistant that remembers your portfolio context and provides personalized investment recommendations.

### Key Highlights

- 🤖 **Conversational AI** with memory and portfolio awareness
- 📊 **Real-time Stock Data** from NSE, BSE, NASDAQ, and more
- 💼 **Portfolio Management** with P&L tracking
- 📈 **Market Analysis** with top gainers/losers
- 🎨 **Modern Web Interface** with responsive design
- 🐳 **Docker Ready** for easy deployment

---

## ✨ Features

### 💼 Portfolio Management
- **Transaction Tracking** - Record buy/sell transactions
- **Real-time P&L** - Live profit/loss calculations
- **Portfolio Analytics** - Comprehensive performance metrics
- **Multi-exchange Support** - NSE, BSE, NASDAQ, S&P 500

### 🤖 AI Assistant
- **Conversational Interface** - Natural language interactions
- **Portfolio Awareness** - AI knows your current holdings
- **Personalized Recommendations** - Stock suggestions based on your portfolio
- **Memory Persistence** - Remembers previous conversations
- **Market Analysis** - Real-time market insights and trends

### 📊 Market Data
- **Live Stock Prices** - Real-time price updates
- **Index Tracking** - NIFTY, SENSEX, NASDAQ, S&P 500
- **Market Movers** - Top gainers and losers
- **Technical Indicators** - P/E ratios, volume, market cap

### 🎨 User Interface
- **Responsive Design** - Works on desktop and mobile
- **Real-time Chat** - WhatsApp-style conversation interface
- **Visual Analytics** - Color-coded profit/loss indicators
- **Intuitive Navigation** - Easy-to-use tabbed interface

---

## 🛠 Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **yfinance** - Real-time market data

### AI & ML
- **Google Gemini** - Advanced language model for conversations
- **LangChain** - Framework for building AI applications
- **Ollama** - Local LLM support (optional)

### Frontend
- **HTML5/CSS3** - Modern web technologies
- **JavaScript** - Interactive user interface
- **Responsive Design** - Mobile-first approach

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL Container** - Database in Docker

---

## 🚀 Installation

### Prerequisites

- Docker and Docker Compose
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Quick Start

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/stock-market-ai-agent.git
   cd stock-market-ai-agent
   ```

2. **Set up environment variables**
   ```
   # Create .env file
   echo "GEMINI_API_KEY=your_actual_gemini_api_key_here" > .env
   ```

3. **Start the application**
   ```
   docker-compose up -d
   ```

4. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5433

### Manual Installation

If you prefer to run without Docker:

1. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL**
   ```
   # Install PostgreSQL and create database
   createdb stockdb
   ```

3. **Configure environment**
   ```
   export GEMINI_API_KEY="your_api_key"
   export DATABASE_URL="postgresql://user:password@localhost/stockdb"
   ```

4. **Run the application**
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Required Files Structure

```
stock-market-ai-agent/
├── app/
│   ├── models/
│   │   ├── database.py
│   │   └── schemas.py
│   └── services/
│       ├── ai_agent.py
│       ├── market_data.py
│       └── portfolio.py
├── main.py
├── index.html
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
```

---

## 📖 Usage

### Getting Started

1. **Open the web interface** at http://localhost:8000
2. **Add some transactions** to build your portfolio
3. **Chat with the AI** for personalized insights
4. **Monitor your portfolio** performance in real-time

### Example Conversations

```
👤 User: "Hello"
🤖 AI: "Hello! I can see you currently hold 3 different stocks 
      with a total portfolio value of ₹45,000. How can I help you today?"

👤 User: "What should I buy on Monday?"
🤖 AI: "Based on your current holdings (RELIANCE, TCS, HDFC), 
      here are my recommendations for Monday:
      
      1. **INFY** - IT sector diversification, strong Q3 results
      2. **BAJFINANCE** - NBFC exposure, different from banking
      3. **ITC** - Defensive FMCG play for portfolio stability"

👤 User: "How is my portfolio doing?"
🤖 AI: "Your portfolio is up ₹3,200 (7.8% gain). RELIANCE is your 
      best performer at +12%, but HDFC is down 3%. Overall good 
      diversification across sectors!"
```

---

## 📚 API Documentation

### Core Endpoints

#### Portfolio Management
```
POST /transactions/          # Add buy/sell transaction
GET  /portfolio/            # Get portfolio summary
POST /sell/                 # Process sell transaction
GET  /profit-loss/{symbol}  # Calculate P&L for specific stock
```

#### Market Data
```
GET /stock/{symbol}         # Get stock price data
GET /index/{index_name}     # Get index data (NIFTY, SENSEX, etc.)
GET /market/gainers-losers  # Get top gainers and losers
```

#### AI Assistant
```
POST /chat/                 # Conversational AI with memory
POST /query/               # Legacy query endpoint
```

### Example API Calls

**Add Transaction:**
```
curl -X POST "http://localhost:8000/transactions/" \
     -H "Content-Type: application/json" \
     -d '{
       "stock_symbol": "RELIANCE",
       "transaction_type": "buy",
       "price": 2450.50,
       "quantity": 10
     }'
```

**Chat with AI:**
```
curl -X POST "http://localhost:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What should I buy tomorrow?"
     }'
```

**Get Stock Price:**
```
curl "http://localhost:8000/stock/RELIANCE?exchange=NSE"
```

---

## 🧠 AI Capabilities

### Conversational Features
- **Memory Persistence** - Remembers previous conversations
- **Portfolio Context** - Knows your current holdings and performance
- **Natural Language** - Understands casual conversation
- **Personalized Advice** - Recommendations based on your portfolio

### Market Analysis
- **Technical Analysis** - Chart patterns, indicators, and signals
- **Fundamental Analysis** - P/E ratios, earnings, financial metrics
- **Risk Assessment** - Portfolio diversification and risk factors
- **Market Sentiment** - Current trends and market direction

### Educational Content
- **Concept Explanations** - Learn about financial terms and concepts
- **Trading Strategies** - Educational insights on trading approaches
- **Market Insights** - Understanding market movements and patterns

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | - | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgre@db:5432/stockdb` | ✅ |

### Docker Configuration

The application runs on Docker with the following services:

- **App Container**: FastAPI application (Port 8000)
- **Database Container**: PostgreSQL 13 (Port 5433)
- **Volume**: Persistent database storage

### Dockerfile Example

```
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==1.4.41
psycopg2-binary==2.9.5
yfinance==0.2.28
google-generativeai==0.3.2
langchain==0.0.350
langchain-community==0.0.13
pydantic==2.5.0
pandas==2.0.3
requests==2.31.0
python-multipart==0.0.6
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```
   python -m pytest tests/
   ```
5. **Commit and push**
   ```
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```
6. **Create a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Use semantic commit messages

### Areas for Contribution

- 🔧 **New Features**: Additional market indicators, portfolio analytics
- 🎨 **UI/UX**: Frontend improvements, mobile responsiveness
- 🤖 **AI Enhancement**: Better prompts, additional AI models
- 📊 **Data Sources**: New market data providers, additional exchanges
- 🧪 **Testing**: Unit tests, integration tests, performance tests

---

## 🚨 Troubleshooting

### Common Issues

**1. Database Connection Error**
```
# Check if PostgreSQL container is running
docker-compose ps

# Restart the database
docker-compose restart db
```

**2. Gemini API Key Issues**
```
# Verify API key is set
echo $GEMINI_API_KEY

# Check .env file
cat .env
```

**3. Port Already in Use**
```
# Kill processes using port 8000
sudo lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
```

**4. Market Data Not Loading**
- Check internet connection
- Verify yfinance is working: `python -c "import yfinance; print(yfinance.__version__)"`
- Try different stock symbols

---

## 📄 License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2025 Stock Market AI Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **Google Gemini** for powerful AI capabilities
- **yfinance** for reliable market data
- **FastAPI** for excellent API framework
- **Docker** for seamless deployment
- **PostgreSQL** for robust data storage
- **LangChain** for AI application framework

---

## 📞 Support

### Getting Help

- 📖 **Documentation**: Check the [API docs](http://localhost:8000/docs)
- 🐛 **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/stock-market-ai-agent/issues)
- 💬 **Discussions**: Join conversations in [GitHub Discussions](https://github.com/yourusername/stock-market-ai-agent/discussions)

### FAQ

**Q: How do I get a Gemini API key?**
A: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get your free API key.

**Q: Can I use different AI models?**
A: Yes! The application supports Ollama for local LLMs. Uncomment the Ollama sections in `ai_agent.py`.

**Q: How accurate is the market data?**
A: We use yfinance which provides reliable data from Yahoo Finance. Data may have a slight delay.

**Q: Is my portfolio data secure?**
A: Yes, all data is stored locally in your PostgreSQL database. Nothing is sent to external services except AI queries.

**Q: Can I add more stock exchanges?**
A: Yes! Modify the `market_data.py` file to include additional exchanges and their ticker formats.

**Q: How do I backup my data?**
A: Use Docker volumes or PostgreSQL dump commands:
```
docker-compose exec db pg_dump -U postgres stockdb > backup.sql
```

---

## 🔮 Roadmap

### Upcoming Features

- [ ] **Mobile App** - React Native mobile application
- [ ] **Advanced Charts** - TradingView integration
- [ ] **News Integration** - Real-time financial news
- [ ] **Portfolio Analytics** - Advanced risk metrics
- [ ] **Options Trading** - Options chain and analysis
- [ ] **Paper Trading** - Virtual trading environment
- [ ] **Alerts System** - Price and portfolio alerts
- [ ] **Multiple Portfolios** - Track different portfolios
- [ ] **Social Features** - Share insights with community
- [ ] **API Rate Limiting** - Enhanced API management

---



**⭐ Star this repository if you found it helpful!**

Made with ❤️ and ☕ by developers who love the stock market

[🔝 Back to Top](#-stock-market-ai-agent)



---

> **Disclaimer**: This application is for educational purposes only. The AI provides educational insights and should not be considered as financial advice. Always consult with qualified financial professionals before making investment decisions. Past performance does not guarantee future results.

> **Risk Warning**: Trading and investing in stocks involves substantial risk of loss and is not suitable for all investors. Please ensure you fully understand the risks involved.
```

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/5156f6d3-a76e-4e25-a602-a0a68e5f019c/docker-compose.yml
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/796139ce-45a4-4c44-8d31-68809fee24a6/database.py
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/3c5ad851-3b2b-455c-ad4b-a965f77e8d1a/schemas.py
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/1d0a1be5-4ed6-484b-949a-fe2109113a38/market_data.py
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/b86e731e-934a-4f8d-a444-a1ad6d236769/portfolio.py
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/54e6d981-a90f-4baf-bcea-dc4e86ea149d/index.html
[7] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/674973ca-3af5-4229-b828-1228baa0f11b/ai_agent.py
[8] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/90290259/a90c1af3-ed63-405b-93ff-ead1d748b159/main.py