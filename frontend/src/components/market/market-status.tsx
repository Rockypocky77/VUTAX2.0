'use client';

import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { MarketStatus as MarketStatusType } from '@/types';
import { Clock, TrendingUp } from 'lucide-react';

interface MarketStatusProps {
  status?: MarketStatusType;
}

export function MarketStatus({ status }: MarketStatusProps) {
  // Mock market status for testing
  const mockStatus: MarketStatusType = {
    isOpen: true, // You can change this to test different states
    nextOpen: new Date('2024-01-16T09:30:00').toISOString(),
    nextClose: new Date('2024-01-16T16:00:00').toISOString(),
    timezone: 'US/Eastern'
  };

  const marketStatus = status || mockStatus;
  const currentTime = new Date().toLocaleTimeString();

  return (
    <Card className="matte-card">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                marketStatus.isOpen ? 'bg-success-500 animate-pulse' : 'bg-slate-400'
              }`}></div>
              <span className="font-medium text-slate-900">
                US Markets
              </span>
            </div>
            
            <Badge variant={marketStatus.isOpen ? 'default' : 'secondary'}>
              {marketStatus.isOpen ? 'OPEN' : 'CLOSED'}
            </Badge>
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-slate-600">
            <div className="flex items-center space-x-1">
              <Clock className="w-4 h-4" />
              <span>{currentTime} ET</span>
            </div>
            
            {marketStatus.isOpen ? (
              <div className="flex items-center space-x-1 text-success-600">
                <TrendingUp className="w-4 h-4" />
                <span>Live Data</span>
              </div>
            ) : (
              <span className="text-slate-500">
                Opens {marketStatus.nextOpen ? 
                  new Date(marketStatus.nextOpen).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) 
                  : '9:30 AM'} ET
              </span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
