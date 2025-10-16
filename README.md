# VUTAX 2.0 - Fintech Platform for Short-Term Investors

A comprehensive web-based fintech platform designed for short-term investors (≤6 months, ages 14+) in the US stock market.

## 🚀 Features

### Core Functionality
- **Stock Finder System**: Real-time scanning of US equities with 30-minute updates
- **AI-Powered Recommendations**: Dual ML models for analysis and user interaction
- **Paper Trading**: Fully integrated portfolio simulation and tracking
- **Interactive Stock Cards**: Clean, responsive cards with predictive graphs
- **Risk Management**: Three-tier risk system (conservative, regular, high-risk)
- **Email Alerts**: Customizable notifications via Resend API

### Technical Highlights
- Real-time data updates (minute-level precision)
- Two separate ML models: Analytical + Chatbot
- Mobile-first responsive design
- Matte UI with smooth animations
- Historical data: 1d to 5y charts
- Predictive forecasting with confidence scores

## 🏗️ Architecture

```
VUTAX-2.0/
├── frontend/          # Next.js 14 + TypeScript
├── backend/
│   ├── api-gateway/   # Node.js/Express API gateway
│   ├── ml-service/    # Python FastAPI for ML models
│   └── data-service/  # Real-time data pipeline
├── models/            # ML model training and inference
├── database/          # PostgreSQL schemas and migrations
└── docs/             # Documentation and compliance
```

## 🛠️ Tech Stack

- **Frontend**: Next.js 14, TypeScript, TailwindCSS, shadcn/ui, Framer Motion
- **Backend**: Python FastAPI, Node.js/Express, PostgreSQL, Redis
- **ML**: scikit-learn, TensorFlow, pandas, numpy
- **Data**: Alpha Vantage, Polygon.io, Yahoo Finance APIs
- **Email**: Resend API
- **Charts**: Chart.js, Recharts

## 📊 ML Models

### 1. Analytical Model (~80% accuracy target)
- Stock ranking and buy/sell recommendations
- Risk scoring and technical indicators
- Minor sentiment analysis integration
- Real-time inference optimized

### 2. Chatbot Model
- Portfolio interpretation and explanations
- User question answering
- Recommendation explanations
- Natural language interface

## 🎯 Target Users

- Short-term investors (≤6 months holding period)
- Ages 14+ (with appropriate disclaimers)
- US stock market focus
- Paper trading for minors

## ⚖️ Compliance

- Information-only platform (not financial advice)
- Comprehensive disclaimers and TOS
- Age-appropriate restrictions
- Educational focus for minors

## 🚦 Getting Started

### 1. **Prerequisites**
- **Docker Desktop** (must be running)
- **Internet connection** (for market data)
- **10GB free space** (for AI models)

### 2. **Clone Repository**
```bash
git clone https://github.com/Rockypocky77/VUTAX2.0.git
cd "VUTAX 2.0"
```

### 3. **Launch Platform**
```bash
# Just double-click this file:
start_website.bat
```

### 4. **Access Platform**
- **🌐 Main Platform**: http://localhost:3000
- **🤖 Training Dashboard**: http://localhost:5000  
- **🔍 API Docs**: http://localhost:8001/docs

## 🤖 AI Training System

### **Automatic Training** (Recommended)
- Models retrain **every 6 hours** automatically
- No manual intervention needed
- Fresh market data collected continuously
- Performance improves over time

### **Manual Training**
```bash
# Start training with progress tracking:
start_training.bat
```

**Training Dashboard**: http://localhost:5000
- Real-time progress bars
- Accurate time remaining estimates  
- Live training logs
- Model performance metrics

### **Training Stages**
1. **📊 Data Collection** (0-30%) - Fetching market data
2. **🔧 Feature Engineering** (30-50%) - Calculating indicators
3. **🤖 Model Training** (50-80%) - Machine learning
4. **✅ Validation** (80-90%) - Testing accuracy
5. **🚀 Deployment** (90-100%) - Going live

**Expected Time**: 15-30 minutes

## 🎨 Platform Highlights

### **🔍 Discover Page**
- Type to search 3000+ stocks instantly
- Beautiful autocomplete with animations
- Sector filtering and sorting
- Click any stock for AI analysis

### **📊 Interactive Charts** 
- Charts draw themselves with smooth animations
- **Moving arrow** follows the line as it's created
- Hover anywhere to see **exact price and date**
- AI prediction lines show future targets
- Technical indicators with explanations

### **📈 Smart Watchlist**
- **Plus button** on stock cards (top-right) to add
- Click cards to **expand** and see full analysis
- Search and filter your saved stocks
- Remove with smooth delete animations

### **🤖 AI Recommendations**
- Real-time buy/sell signals
- Risk levels: Conservative, Regular, High-Risk
- Confidence scores and explanations
- Historical accuracy tracking

## ⚙️ Configuration (Optional)

### **API Keys** (For Real Data)
Create `.env` file:
```env
# Optional - platform works without these
ALPHA_VANTAGE_API_KEY=your_key_here
RESEND_API_KEY=your_key_here
```

**Get Free API Keys:**
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
- **Resend**: https://resend.com

**Note**: Platform works perfectly with mock data for testing!

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, TypeScript, TailwindCSS, Framer Motion
- **Backend**: Node.js, Python FastAPI, PostgreSQL, Redis
- **AI/ML**: Scikit-learn, TensorFlow, 70+ technical indicators
- **Real-time**: Socket.IO for live updates
- **Deployment**: Docker Compose

## 📊 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **🌐 Main Platform** | http://localhost:3000 | Trading interface |
| **🤖 Training Dashboard** | http://localhost:5000 | AI training progress |
| **🔍 API Gateway** | http://localhost:4000 | Backend API |
| **🧠 ML Service** | http://localhost:8001 | AI/ML endpoints |

## 🚀 What You'll Experience

1. **🎨 Beautiful Interface**: Smooth animations and modern design
2. **🔍 Smart Search**: Find any stock instantly with autocomplete  
3. **📊 Interactive Charts**: Hover for details, watch them draw
4. **🤖 AI Insights**: Real-time recommendations and analysis
5. **📈 Portfolio Tracking**: Monitor investments with AI guidance
6. **⚡ Real-time Updates**: Live market data and notifications

## 🎉 Ready to Start?

### **For Trading:**
```bash
start_website.bat
# Opens: http://localhost:3000
```

### **For AI Training:**
```bash  
start_training.bat
# Opens: http://localhost:5000
```

### **Need Help?**
- **📁 Documentation**: Check `docs/` folder
- **🐛 Issues**: https://github.com/Rockypocky77/VUTAX2.0/issues
- **💬 Support**: Create a GitHub issue

---

**🚀 Built with ❤️ for traders who love beautiful, intelligent platforms**

**Ready to experience the future of trading? Just run `start_website.bat`!** ✨
