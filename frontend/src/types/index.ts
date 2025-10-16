// Core data types for the VUTAX platform

export interface Stock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap?: number;
  sector?: string;
  industry?: string;
  lastUpdated: string;
}

export interface StockRecommendation {
  symbol: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  riskTier: 'conservative' | 'regular' | 'high-risk';
  confidence: number; // 0-100
  targetPrice?: number;
  stopLoss?: number;
  reasoning: string;
  timestamp: string;
  validUntil: string;
}

export interface TechnicalIndicator {
  name: string;
  value: number;
  signal: 'bullish' | 'bearish' | 'neutral';
  description: string;
}

export interface StockAnalysis {
  symbol: string;
  technicalIndicators: TechnicalIndicator[];
  sentimentScore: number; // -1 to 1
  prediction: {
    price1d: number;
    price1w: number;
    price1m: number;
    confidence: number;
  };
  riskMetrics: {
    volatility: number;
    beta: number;
    sharpeRatio?: number;
  };
}

export interface PortfolioPosition {
  symbol: string;
  quantity: number;
  avgCostBasis: number;
  currentPrice: number;
  totalValue: number;
  unrealizedGainLoss: number;
  unrealizedGainLossPercent: number;
  dateAdded: string;
}

export interface Portfolio {
  id: string;
  name: string;
  totalValue: number;
  totalGainLoss: number;
  totalGainLossPercent: number;
  positions: PortfolioPosition[];
  cashBalance: number;
  lastUpdated: string;
}

export interface Watchlist {
  id: string;
  name: string;
  symbols: string[];
  createdAt: string;
  lastUpdated: string;
}

export interface PriceHistory {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface ChartData {
  symbol: string;
  timeframe: '1d' | '1w' | '1m' | '1y' | '5y';
  data: PriceHistory[];
  predictive?: {
    data: PriceHistory[];
    confidence: number;
  };
}

export interface Alert {
  id: string;
  symbol: string;
  type: 'price' | 'recommendation' | 'news';
  message: string;
  priority: 'low' | 'medium' | 'high';
  timestamp: string;
  read: boolean;
}

export interface UserSettings {
  emailNotifications: boolean;
  riskTolerance: 'conservative' | 'moderate' | 'aggressive';
  preferredTimeframe: '1d' | '1w' | '1m' | '1y' | '5y';
  watchlistLimit: number;
  portfolioLimit: number;
}

export interface MarketStatus {
  isOpen: boolean;
  nextOpen?: string;
  nextClose?: string;
  timezone: string;
}

export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  url: string;
  source: string;
  publishedAt: string;
  symbols: string[];
  sentiment: 'positive' | 'negative' | 'neutral';
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

// WebSocket message types
export interface WSMessage {
  type: 'stock_update' | 'recommendation' | 'alert' | 'market_status';
  data: any;
  timestamp: string;
}

// Chart configuration types
export interface ChartConfig {
  type: 'line' | 'candlestick' | 'area';
  timeframe: '1d' | '1w' | '1m' | '1y' | '5y';
  indicators: string[];
  showPrediction: boolean;
}

// Risk assessment types
export interface RiskAssessment {
  overall: 'low' | 'medium' | 'high';
  factors: {
    volatility: number;
    marketCap: 'small' | 'mid' | 'large';
    sector: string;
    technicalRisk: number;
    sentimentRisk: number;
  };
  recommendation: string;
}

export type TimeFrame = '1d' | '1w' | '1m' | '3m' | '6m' | '1y' | '2y' | '5y';
export type RiskTier = 'conservative' | 'regular' | 'high-risk';
export type ActionType = 'BUY' | 'SELL' | 'HOLD';
export type SignalType = 'bullish' | 'bearish' | 'neutral';
