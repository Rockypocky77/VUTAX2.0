'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  BarChart3,
  Star,
  Plus,
  Minus
} from 'lucide-react';
import { cn, formatCurrency, formatPercent, getChangeColor } from '@/lib/utils';
import { Stock } from '@/types';
import { StockChart } from './stock-chart';
import { TechnicalIndicators } from './technical-indicators';

interface StockCardProps {
  stock: Stock;
  compact?: boolean;
  showChart?: boolean;
  onAddToWatchlist?: (symbol: string) => void;
  onRemoveFromWatchlist?: (symbol: string) => void;
  isInWatchlist?: boolean;
}

export function StockCard({
  stock,
  compact = false,
  showChart = false,
  onAddToWatchlist,
  onRemoveFromWatchlist,
  isInWatchlist = false
}: StockCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showPrediction, setShowPrediction] = useState(false);

  const changeColor = getChangeColor(stock.change);
  const isPositive = stock.change >= 0;

  const handleWatchlistToggle = () => {
    if (isInWatchlist && onRemoveFromWatchlist) {
      onRemoveFromWatchlist(stock.symbol);
    } else if (!isInWatchlist && onAddToWatchlist) {
      onAddToWatchlist(stock.symbol);
    }
  };

  if (compact) {
    return (
      <motion.div
        whileHover={{ scale: 1.02 }}
        transition={{ duration: 0.2 }}
      >
        <Card className="stock-card cursor-pointer" onClick={() => setIsExpanded(!isExpanded)}>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  <h3 className="font-semibold text-slate-900">{stock.symbol}</h3>
                  <Badge variant="outline" className="text-xs">
                    {stock.sector || 'Technology'}
                  </Badge>
                </div>
                <p className="text-sm text-slate-600 truncate">{stock.name}</p>
              </div>
              
              <div className="text-right">
                <div className="font-semibold text-slate-900">
                  {formatCurrency(stock.price)}
                </div>
                <div className={cn("text-sm flex items-center", changeColor)}>
                  {isPositive ? (
                    <TrendingUp className="w-3 h-3 mr-1" />
                  ) : (
                    <TrendingDown className="w-3 h-3 mr-1" />
                  )}
                  {formatPercent(stock.changePercent)}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="stock-card overflow-hidden">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="flex items-center space-x-2">
                <span className="text-xl font-bold text-slate-900">{stock.symbol}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleWatchlistToggle}
                  className="p-1 h-auto"
                >
                  <Star 
                    className={cn(
                      "w-4 h-4",
                      isInWatchlist 
                        ? "fill-yellow-400 text-yellow-400" 
                        : "text-slate-400 hover:text-yellow-400"
                    )} 
                  />
                </Button>
              </div>
              
              <div className="flex items-center space-x-4 mt-2">
                <div>
                  <div className="text-2xl font-bold text-slate-900">
                    {formatCurrency(stock.price)}
                  </div>
                  <div className={cn("flex items-center text-sm", changeColor)}>
                    {isPositive ? (
                      <TrendingUp className="w-4 h-4 mr-1" />
                    ) : (
                      <TrendingDown className="w-4 h-4 mr-1" />
                    )}
                    <span className="font-medium">
                      {formatCurrency(stock.change, 'USD', 2)} ({formatPercent(stock.changePercent)})
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-right space-y-2">
              <Badge 
                variant={isPositive ? "default" : "destructive"}
                className="font-medium"
              >
                {isPositive ? "↗" : "↘"} {Math.abs(stock.changePercent).toFixed(2)}%
              </Badge>
              
              <div className="text-xs text-slate-500">
                Vol: {stock.volume?.toLocaleString() || 'N/A'}
              </div>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Company Info */}
          <div>
            <h4 className="font-medium text-slate-900 mb-1">{stock.name}</h4>
            <div className="flex items-center space-x-4 text-sm text-slate-600">
              <span>{stock.sector || 'Technology'}</span>
              <span>•</span>
              <span>{stock.industry || 'Software'}</span>
              {stock.marketCap && (
                <>
                  <span>•</span>
                  <span>Cap: {formatCurrency(stock.marketCap, 'USD', 0)}</span>
                </>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowChart(!showChart)}
              className="flex-1"
            >
              <BarChart3 className="w-4 h-4 mr-2" />
              {showChart ? 'Hide Chart' : 'Show Chart'}
            </Button>
            
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsExpanded(!isExpanded)}
              className="flex-1"
            >
              <Activity className="w-4 h-4 mr-2" />
              {isExpanded ? 'Less Info' : 'More Info'}
            </Button>
          </div>

          {/* Chart Section */}
          {showChart && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="border-t pt-4">
                <div className="flex items-center justify-between mb-3">
                  <h5 className="font-medium text-slate-900">Price Chart</h5>
                  <Button
                    variant={showPrediction ? "default" : "outline"}
                    size="sm"
                    onClick={() => setShowPrediction(!showPrediction)}
                  >
                    AI Prediction
                  </Button>
                </div>
                <StockChart 
                  symbol={stock.symbol} 
                  showPrediction={showPrediction}
                />
              </div>
            </motion.div>
          )}

          {/* Expanded Information */}
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="border-t pt-4 space-y-4">
                {/* Technical Indicators */}
                <div>
                  <h5 className="font-medium text-slate-900 mb-3">Technical Indicators</h5>
                  <TechnicalIndicators symbol={stock.symbol} />
                </div>

                {/* Key Metrics */}
                <div>
                  <h5 className="font-medium text-slate-900 mb-3">Key Metrics</h5>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-slate-600">52W High:</span>
                      <span className="ml-2 font-medium">$185.42</span>
                    </div>
                    <div>
                      <span className="text-slate-600">52W Low:</span>
                      <span className="ml-2 font-medium">$124.17</span>
                    </div>
                    <div>
                      <span className="text-slate-600">P/E Ratio:</span>
                      <span className="ml-2 font-medium">28.5</span>
                    </div>
                    <div>
                      <span className="text-slate-600">Beta:</span>
                      <span className="ml-2 font-medium">1.23</span>
                    </div>
                  </div>
                </div>

                {/* AI Insights */}
                <div>
                  <h5 className="font-medium text-slate-900 mb-3">AI Insights</h5>
                  <div className="bg-slate-50 rounded-lg p-3">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge variant="outline" className="text-success-600 border-success-200">
                        BUY Signal
                      </Badge>
                      <span className="text-sm text-slate-600">Confidence: 87%</span>
                    </div>
                    <p className="text-sm text-slate-700">
                      Strong bullish momentum with RSI showing oversold conditions. 
                      MACD crossover suggests potential upward movement. 
                      Consider position sizing based on risk tolerance.
                    </p>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-2 pt-2">
                  <Button variant="success" className="flex-1">
                    <Plus className="w-4 h-4 mr-2" />
                    Add to Portfolio
                  </Button>
                  <Button variant="outline" className="flex-1">
                    View Details
                  </Button>
                </div>
              </div>
            </motion.div>
          )}

          {/* Last Updated */}
          <div className="text-xs text-slate-500 text-center pt-2 border-t">
            Last updated: {new Date(stock.lastUpdated).toLocaleTimeString()}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
