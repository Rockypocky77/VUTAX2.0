'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Eye, Plus, Star, TrendingUp, TrendingDown } from 'lucide-react';
import { formatCurrency, formatPercent, getChangeColor } from '@/lib/utils';

export function WatchlistPanel() {
  const [watchlist] = useState([
    { symbol: 'NVDA', name: 'NVIDIA Corp', price: 456.78, change: 12.34, changePercent: 2.78 },
    { symbol: 'AMD', name: 'Advanced Micro Devices', price: 102.45, change: -1.23, changePercent: -1.19 },
    { symbol: 'INTC', name: 'Intel Corporation', price: 43.21, change: 0.87, changePercent: 2.05 },
    { symbol: 'CRM', name: 'Salesforce Inc', price: 234.56, change: -3.45, changePercent: -1.45 },
  ]);

  return (
    <Card className="matte-card">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Eye className="w-5 h-5" />
          <span>Watchlist</span>
          <Badge variant="outline" className="ml-auto">
            {watchlist.length}/50
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {watchlist.map((stock) => (
          <div key={stock.symbol} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
            <div className="flex items-center space-x-3">
              <Button variant="ghost" size="sm" className="p-1">
                <Star className="w-4 h-4 text-yellow-500 fill-current" />
              </Button>
              <div>
                <div className="font-medium text-slate-900">{stock.symbol}</div>
                <div className="text-xs text-slate-600 truncate max-w-[120px]">{stock.name}</div>
              </div>
            </div>
            
            <div className="text-right">
              <div className="font-medium text-slate-900">
                {formatCurrency(stock.price)}
              </div>
              <div className={`text-xs flex items-center ${getChangeColor(stock.change)}`}>
                {stock.change >= 0 ? (
                  <TrendingUp className="w-3 h-3 mr-1" />
                ) : (
                  <TrendingDown className="w-3 h-3 mr-1" />
                )}
                {formatPercent(stock.changePercent)}
              </div>
            </div>
          </div>
        ))}
        
        <Button variant="outline" className="w-full mt-4">
          <Plus className="w-4 h-4 mr-2" />
          Add Stock
        </Button>
      </CardContent>
    </Card>
  );
}
