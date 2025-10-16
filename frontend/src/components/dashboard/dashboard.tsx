'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { StockCard } from '@/components/stocks/stock-card';
import { PortfolioSummary } from '@/components/portfolio/portfolio-summary';
import { WatchlistPanel } from '@/components/watchlist/watchlist-panel';
import { RecommendationsPanel } from '@/components/recommendations/recommendations-panel';
import { MarketStatus } from '@/components/market/market-status';
import { AlertsPanel } from '@/components/alerts/alerts-panel';
import { TrendingUp, TrendingDown, Activity, DollarSign } from 'lucide-react';
import { useStockData } from '@/hooks/useStockData';
import { usePortfolio } from '@/hooks/usePortfolio';
import { useRecommendations } from '@/hooks/useRecommendations';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.5,
      ease: 'easeOut',
    },
  },
};

export function Dashboard() {
  const [selectedTimeframe, setSelectedTimeframe] = useState<'1d' | '1w' | '1m' | '1y'>('1d');
  const { portfolio, loading: portfolioLoading } = usePortfolio();
  const { recommendations, loading: recommendationsLoading } = useRecommendations();
  const { marketStatus } = useStockData();

  // Mock data for demonstration
  const mockStats = {
    totalValue: 125430.50,
    dayChange: 2340.20,
    dayChangePercent: 1.89,
    totalGainLoss: 15430.50,
    totalGainLossPercent: 13.95,
  };

  const mockTopStocks = [
    { symbol: 'AAPL', name: 'Apple Inc.', price: 175.43, change: 2.34, changePercent: 1.35 },
    { symbol: 'MSFT', name: 'Microsoft Corp.', price: 378.85, change: -1.23, changePercent: -0.32 },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 142.56, change: 3.45, changePercent: 2.48 },
    { symbol: 'TSLA', name: 'Tesla Inc.', price: 248.50, change: -5.67, changePercent: -2.23 },
  ];

  return (
    <motion.div
      className="space-y-8"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Market Status */}
      <motion.div variants={itemVariants}>
        <MarketStatus status={marketStatus} />
      </motion.div>

      {/* Key Metrics */}
      <motion.div variants={itemVariants}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="matte-card">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">
                Portfolio Value
              </CardTitle>
              <DollarSign className="h-4 w-4 text-slate-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-slate-900">
                ${mockStats.totalValue.toLocaleString()}
              </div>
              <p className={`text-xs ${mockStats.dayChange >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                {mockStats.dayChange >= 0 ? '+' : ''}${mockStats.dayChange.toFixed(2)} 
                ({mockStats.dayChangePercent >= 0 ? '+' : ''}{mockStats.dayChangePercent}%) today
              </p>
            </CardContent>
          </Card>

          <Card className="matte-card">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">
                Total Gain/Loss
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-slate-500" />
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${mockStats.totalGainLoss >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                {mockStats.totalGainLoss >= 0 ? '+' : ''}${mockStats.totalGainLoss.toLocaleString()}
              </div>
              <p className={`text-xs ${mockStats.totalGainLossPercent >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                {mockStats.totalGainLossPercent >= 0 ? '+' : ''}{mockStats.totalGainLossPercent}% all time
              </p>
            </CardContent>
          </Card>

          <Card className="matte-card">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">
                Active Positions
              </CardTitle>
              <Activity className="h-4 w-4 text-slate-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-slate-900">
                {portfolio?.positions?.length || 0}
              </div>
              <p className="text-xs text-slate-600">
                Across {mockTopStocks.length} watchlist items
              </p>
            </CardContent>
          </Card>

          <Card className="matte-card">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">
                AI Confidence
              </CardTitle>
              <TrendingDown className="h-4 w-4 text-slate-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-success-600">
                87%
              </div>
              <p className="text-xs text-slate-600">
                Average prediction accuracy
              </p>
            </CardContent>
          </Card>
        </div>
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Recommendations & Portfolio */}
        <motion.div className="lg:col-span-2 space-y-8" variants={itemVariants}>
          {/* Recommendations */}
          <RecommendationsPanel 
            recommendations={recommendations}
            loading={recommendationsLoading}
          />

          {/* Portfolio Summary */}
          <PortfolioSummary 
            portfolio={portfolio}
            loading={portfolioLoading}
          />

          {/* Top Stocks */}
          <Card className="matte-card">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-slate-900">
                Market Movers
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {mockTopStocks.map((stock, index) => (
                  <motion.div
                    key={stock.symbol}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <StockCard stock={stock} compact />
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Right Column - Watchlist & Alerts */}
        <motion.div className="space-y-8" variants={itemVariants}>
          <WatchlistPanel />
          <AlertsPanel />
        </motion.div>
      </div>

      {/* Timeframe Selector */}
      <motion.div 
        className="flex justify-center space-x-2"
        variants={itemVariants}
      >
        {(['1d', '1w', '1m', '1y'] as const).map((timeframe) => (
          <Button
            key={timeframe}
            variant={selectedTimeframe === timeframe ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedTimeframe(timeframe)}
            className="transition-all duration-200"
          >
            {timeframe}
          </Button>
        ))}
      </motion.div>
    </motion.div>
  );
}
