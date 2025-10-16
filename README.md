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

[Setup instructions will be added as components are built]

## 📈 Roadmap

- [x] Project architecture and planning
- [ ] Core infrastructure setup
- [ ] Real-time data pipeline
- [ ] ML model development
- [ ] Frontend dashboard
- [ ] Paper trading system
- [ ] Email notifications
- [ ] Legal compliance integration

---

**Disclaimer**: This platform provides information only and does not constitute financial advice. All trading involves risk.
