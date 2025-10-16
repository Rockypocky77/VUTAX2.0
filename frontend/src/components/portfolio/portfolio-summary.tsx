'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Portfolio } from '@/types';
import { formatCurrency, formatPercent, getChangeColor } from '@/lib/utils';
import { TrendingUp, TrendingDown, DollarSign, PieChart } from 'lucide-react';

interface PortfolioSummaryProps {
  portfolio?: Portfolio;
  loading?: boolean;
}

export function PortfolioSummary({ portfolio, loading }: PortfolioSummaryProps) {
  if (loading) {
    return (
      <Card className="matte-card">
        <CardHeader>
          <CardTitle>Portfolio Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-slate-200 rounded w-3/4"></div>
            <div className="h-4 bg-slate-200 rounded w-1/2"></div>
            <div className="h-4 bg-slate-200 rounded w-2/3"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!portfolio) {
    return (
      <Card className="matte-card">
        <CardHeader>
          <CardTitle>Portfolio Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-slate-600">No portfolio data available</p>
        </CardContent>
      </Card>
    );
  }

  const isPositive = portfolio.totalGainLoss >= 0;

  return (
    <Card className="matte-card">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <PieChart className="w-5 h-5" />
          <span>Portfolio Summary</span>
          <Badge variant="outline" className="ml-auto">
            Paper Trading
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Total Value */}
        <div className="text-center">
          <div className="text-3xl font-bold text-slate-900">
            {formatCurrency(portfolio.totalValue)}
          </div>
          <div className={`text-lg ${getChangeColor(portfolio.totalGainLoss)} flex items-center justify-center mt-1`}>
            {isPositive ? (
              <TrendingUp className="w-4 h-4 mr-1" />
            ) : (
              <TrendingDown className="w-4 h-4 mr-1" />
            )}
            {formatCurrency(Math.abs(portfolio.totalGainLoss))} ({formatPercent(portfolio.totalGainLossPercent)})
          </div>
        </div>

        {/* Portfolio Breakdown */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-slate-50 rounded-lg">
            <div className="text-sm text-slate-600">Invested</div>
            <div className="font-semibold text-slate-900">
              {formatCurrency(portfolio.totalValue - portfolio.cashBalance)}
            </div>
          </div>
          <div className="text-center p-3 bg-slate-50 rounded-lg">
            <div className="text-sm text-slate-600">Cash</div>
            <div className="font-semibold text-slate-900">
              {formatCurrency(portfolio.cashBalance)}
            </div>
          </div>
        </div>

        {/* Top Positions */}
        <div>
          <h4 className="font-medium text-slate-900 mb-3">Top Positions</h4>
          <div className="space-y-2">
            {portfolio.positions.slice(0, 3).map((position) => (
              <div key={position.symbol} className="flex items-center justify-between p-2 bg-slate-50 rounded">
                <div className="flex items-center space-x-3">
                  <div className="font-medium text-slate-900">{position.symbol}</div>
                  <div className="text-sm text-slate-600">{position.quantity} shares</div>
                </div>
                <div className="text-right">
                  <div className="font-medium">{formatCurrency(position.totalValue)}</div>
                  <div className={`text-sm ${getChangeColor(position.unrealizedGainLoss)}`}>
                    {formatPercent(position.unrealizedGainLossPercent)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-3 gap-3 text-center text-sm">
          <div>
            <div className="text-slate-600">Positions</div>
            <div className="font-semibold">{portfolio.positions.length}</div>
          </div>
          <div>
            <div className="text-slate-600">Best Performer</div>
            <div className="font-semibold text-success-600">
              {portfolio.positions.reduce((best, pos) => 
                pos.unrealizedGainLossPercent > best.unrealizedGainLossPercent ? pos : best
              ).symbol}
            </div>
          </div>
          <div>
            <div className="text-slate-600">Last Updated</div>
            <div className="font-semibold">
              {new Date(portfolio.lastUpdated).toLocaleTimeString()}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
