# 🚀 Getting Started with VUTAX 2.0

Welcome to VUTAX 2.0, your AI-powered fintech platform for short-term stock market investing and analysis.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 18.0 or higher)
- **Python** (version 3.9 or higher)
- **Docker & Docker Compose** (recommended for easy setup)
- **Git** for version control

### Required API Keys

To fully utilize VUTAX 2.0, you'll need these API keys:

1. **Alpha Vantage API Key** (free tier available)
   - Sign up at: https://www.alphavantage.co/support/#api-key
   - Provides stock market data

2. **Resend API Key** (for email alerts)
   - Sign up at: https://resend.com
   - Handles email notifications

3. **Optional: Polygon.io API Key**
   - Sign up at: https://polygon.io
   - Enhanced real-time data (premium)

## 🏗️ Installation Methods

### Method 1: Docker Compose (Recommended)

This is the fastest way to get VUTAX 2.0 running with all services.

1. **Clone the repository**:
```bash
git clone <your-repository-url>
cd VUTAX-2.0
```

2. **Set up environment variables**:
```bash
cp .env.example .env
```

3. **Edit the `.env` file** with your API keys:
```bash
# Required API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
RESEND_API_KEY=your_resend_api_key_here

# Optional
POLYGON_API_KEY=your_polygon_key_here
```

4. **Start all services**:
```bash
docker-compose up -d
```

5. **Access the application**:
   - **Frontend**: http://localhost:3000
   - **API Gateway**: http://localhost:3001
   - **ML Service**: http://localhost:8001

### Method 2: Manual Installation

If you prefer to run services individually:

#### Step 1: Database Setup

```bash
# Install PostgreSQL and Redis (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib redis-server

# Create database
sudo -u postgres createdb vutax

# Start Redis
sudo systemctl start redis-server
```

#### Step 2: Backend Services

**API Gateway**:
```bash
cd backend/api-gateway
npm install
cp .env.example .env
# Edit .env with your configuration
npm run dev
```

**ML Service** (in a new terminal):
```bash
cd backend/ml-service
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python main.py
```

#### Step 3: Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your configuration
npm run dev
```

## 🎯 First Steps

### 1. Verify Installation

Once everything is running, verify your installation:

1. **Check Frontend**: Visit http://localhost:3000
   - You should see the VUTAX dashboard
   - Legal disclaimer should appear at the bottom

2. **Check API Health**:
   - API Gateway: http://localhost:3001/health
   - ML Service: http://localhost:8001/health

3. **Test Stock Data**: 
   - Search for a stock symbol (e.g., "AAPL")
   - Verify real-time price updates

### 2. Explore Key Features

#### Dashboard Overview
- **Portfolio Summary**: View your paper trading performance
- **Market Status**: Check if markets are open
- **Stock Recommendations**: AI-generated buy/sell signals
- **Watchlist**: Track your favorite stocks

#### Interactive Stock Cards
- Click on any stock to see detailed analysis
- View technical indicators and AI insights
- Toggle between chart views and predictions

#### Paper Trading
- Add stocks to your virtual portfolio
- Track gains/losses in real-time
- Perfect for learning without financial risk

### 3. Understanding the AI Models

VUTAX 2.0 uses two separate AI models:

#### Analytical Model
- **Purpose**: Stock analysis and recommendations
- **Features**: Technical indicators, risk scoring, price predictions
- **Target Accuracy**: 80%+
- **Updates**: Every 30 minutes during market hours

#### Chatbot Model
- **Purpose**: User interaction and explanations
- **Features**: Portfolio interpretation, recommendation explanations
- **Use Cases**: Ask questions about stocks, get investment education

### 4. Risk Management

VUTAX categorizes recommendations into three risk tiers:

- **Conservative**: Lower volatility, stable stocks
- **Regular**: Balanced risk-reward ratio
- **High-Risk**: Higher volatility, potential for larger gains/losses

## 🔧 Configuration

### Environment Variables

Key configuration options in your `.env` file:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_ML_API_URL=http://localhost:8001

# Feature Flags
ENABLE_PAPER_TRADING=true
ENABLE_EMAIL_ALERTS=true
ENABLE_REAL_TIME_DATA=true
ENABLE_ML_PREDICTIONS=true

# Model Configuration
MODEL_UPDATE_INTERVAL=1800000  # 30 minutes
MODEL_ACCURACY_THRESHOLD=0.75
PREDICTION_CONFIDENCE_MIN=0.6
```

### Customization Options

1. **Risk Tolerance**: Adjust your risk preference in settings
2. **Email Notifications**: Toggle email alerts on/off
3. **Watchlist Limits**: Customize how many stocks to track
4. **Update Frequency**: Configure data refresh intervals

## 📊 Using the Platform

### Adding Stocks to Watchlist

1. Use the search bar to find stocks
2. Click the star icon on stock cards
3. View your watchlist in the right sidebar

### Paper Trading

1. Click "Add to Portfolio" on any stock card
2. Enter the quantity you want to "buy"
3. Track performance in the portfolio section
4. "Sell" positions to realize gains/losses

### Getting AI Recommendations

1. Check the recommendations panel on the dashboard
2. Filter by risk tier (conservative/regular/high-risk)
3. Click on recommendations for detailed explanations
4. Use the chatbot to ask follow-up questions

### Setting Up Email Alerts

1. Go to Settings (gear icon)
2. Enable email notifications
3. Configure alert preferences
4. Receive notifications when recommendations update

## 🚨 Important Legal Information

**Please Read Carefully**:

- VUTAX 2.0 is for **educational purposes only**
- All information provided is **not financial advice**
- **Paper trading only** for users under 18
- Always **do your own research** before making investment decisions
- **Past performance does not guarantee future results**

The legal disclaimer at the bottom of the page contains complete terms and conditions.

## 🛠️ Troubleshooting

### Common Issues

**1. "Cannot connect to API"**
- Check if backend services are running
- Verify API URLs in environment variables
- Check firewall settings

**2. "No stock data available"**
- Verify your Alpha Vantage API key
- Check API key quotas and limits
- Ensure internet connectivity

**3. "ML models not loading"**
- Check Python dependencies are installed
- Verify sufficient system resources (RAM/CPU)
- Check ML service logs for errors

**4. "WebSocket connection failed"**
- Check WebSocket URL configuration
- Verify no proxy blocking WebSocket connections
- Try refreshing the page

### Getting Help

1. **Check Logs**:
   ```bash
   # Docker Compose
   docker-compose logs -f
   
   # Individual services
   docker-compose logs api-gateway
   docker-compose logs ml-service
   ```

2. **Health Checks**:
   - Visit health endpoints to verify service status
   - Check browser console for frontend errors

3. **Resource Usage**:
   ```bash
   # Check Docker resource usage
   docker stats
   
   # Check system resources
   htop  # or top
   ```

## 🎓 Learning Resources

### Understanding Technical Indicators

- **RSI**: Measures overbought/oversold conditions
- **MACD**: Shows trend changes and momentum
- **Bollinger Bands**: Indicates volatility and potential price levels
- **Moving Averages**: Smooths price data to identify trends

### Investment Basics

- **Diversification**: Don't put all eggs in one basket
- **Risk vs. Return**: Higher potential returns usually mean higher risk
- **Time Horizon**: Short-term vs. long-term investing strategies
- **Dollar-Cost Averaging**: Regular investing regardless of market conditions

### Using AI Predictions

- **Confidence Scores**: Higher confidence doesn't guarantee accuracy
- **Multiple Factors**: Consider AI alongside other analysis
- **Risk Management**: Never invest more than you can afford to lose
- **Continuous Learning**: Markets change, so should your strategy

## 🔄 Next Steps

1. **Explore the Dashboard**: Familiarize yourself with all features
2. **Build a Watchlist**: Add 5-10 stocks you're interested in
3. **Try Paper Trading**: Start with small virtual positions
4. **Ask the Chatbot**: Get explanations for recommendations
5. **Read Educational Content**: Use the platform to learn about investing

## 📞 Support

If you encounter issues or have questions:

1. Check this guide and the troubleshooting section
2. Review the logs for error messages
3. Consult the API documentation
4. Check the project's issue tracker

---

**Remember**: VUTAX 2.0 is a powerful educational tool. Use it to learn about investing, understand market dynamics, and develop your analytical skills. Always consult with qualified financial professionals before making real investment decisions.

Happy investing! 📈
