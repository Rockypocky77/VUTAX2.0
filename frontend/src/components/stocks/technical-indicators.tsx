'use client';

import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface TechnicalIndicatorsProps {
  symbol: string;
}

export function TechnicalIndicators({ symbol }: TechnicalIndicatorsProps) {
  // Mock technical indicators for demonstration
  const indicators = [
    { name: 'RSI (14)', value: 67.3, signal: 'neutral', description: 'Slightly overbought' },
    { name: 'MACD', value: 2.45, signal: 'bullish', description: 'Bullish crossover' },
    { name: 'Moving Avg', value: 5.2, signal: 'bullish', description: 'Above 20-day MA' },
    { name: 'Bollinger', value: 0.8, signal: 'neutral', description: 'Mid-range position' },
  ];

  const getSignalIcon = (signal: string) => {
    switch (signal) {
      case 'bullish':
        return <TrendingUp className="w-3 h-3" />;
      case 'bearish':
        return <TrendingDown className="w-3 h-3" />;
      default:
        return <Minus className="w-3 h-3" />;
    }
  };

  const getSignalColor = (signal: string) => {
    switch (signal) {
      case 'bullish':
        return 'text-success-600 bg-success-50 border-success-200';
      case 'bearish':
        return 'text-danger-600 bg-danger-50 border-danger-200';
      default:
        return 'text-slate-600 bg-slate-50 border-slate-200';
    }
  };

  return (
    <div className="grid grid-cols-2 gap-3">
      {indicators.map((indicator) => (
        <div key={indicator.name} className="p-3 bg-slate-50 rounded-lg">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-medium text-slate-600">{indicator.name}</span>
            <Badge variant="outline" className={`text-xs border ${getSignalColor(indicator.signal)}`}>
              {getSignalIcon(indicator.signal)}
              <span className="ml-1 capitalize">{indicator.signal}</span>
            </Badge>
          </div>
          <div className="text-sm font-semibold text-slate-900">{indicator.value}</div>
          <div className="text-xs text-slate-500 mt-1">{indicator.description}</div>
        </div>
      ))}
    </div>
  );
}
