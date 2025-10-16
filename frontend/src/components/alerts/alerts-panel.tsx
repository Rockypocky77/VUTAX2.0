'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Bell, AlertTriangle, Info, CheckCircle, X } from 'lucide-react';

export function AlertsPanel() {
  const alerts = [
    {
      id: '1',
      type: 'recommendation',
      symbol: 'AAPL',
      message: 'New BUY signal detected',
      priority: 'high',
      timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
      read: false
    },
    {
      id: '2',
      type: 'price',
      symbol: 'TSLA',
      message: 'Price target reached: $250',
      priority: 'medium',
      timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
      read: false
    },
    {
      id: '3',
      type: 'news',
      symbol: 'MSFT',
      message: 'Earnings report released',
      priority: 'low',
      timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
      read: true
    }
  ];

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'recommendation':
        return <AlertTriangle className="w-4 h-4" />;
      case 'price':
        return <CheckCircle className="w-4 h-4" />;
      default:
        return <Info className="w-4 h-4" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-danger-600 bg-danger-50';
      case 'medium':
        return 'text-warning-600 bg-warning-50';
      default:
        return 'text-slate-600 bg-slate-50';
    }
  };

  const formatTimeAgo = (timestamp: string) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInMinutes = Math.floor((now.getTime() - time.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    const hours = Math.floor(diffInMinutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  };

  return (
    <Card className="matte-card">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Bell className="w-5 h-5" />
          <span>Alerts</span>
          <Badge variant="destructive" className="ml-auto">
            {alerts.filter(a => !a.read).length}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {alerts.map((alert) => (
          <div 
            key={alert.id} 
            className={`p-3 rounded-lg border transition-colors ${
              alert.read ? 'bg-slate-50 border-slate-200' : 'bg-white border-primary/20 shadow-sm'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3 flex-1">
                <div className={`p-1 rounded ${getPriorityColor(alert.priority)}`}>
                  {getAlertIcon(alert.type)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-medium text-slate-900">{alert.symbol}</span>
                    <Badge variant="outline" className="text-xs">
                      {alert.type}
                    </Badge>
                  </div>
                  <p className="text-sm text-slate-700 leading-relaxed">
                    {alert.message}
                  </p>
                  <p className="text-xs text-slate-500 mt-1">
                    {formatTimeAgo(alert.timestamp)}
                  </p>
                </div>
              </div>
              
              <Button variant="ghost" size="sm" className="p-1 ml-2">
                <X className="w-3 h-3" />
              </Button>
            </div>
          </div>
        ))}
        
        {alerts.length === 0 && (
          <div className="text-center py-6 text-slate-500">
            <Bell className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No alerts at the moment</p>
          </div>
        )}
        
        <Button variant="outline" className="w-full mt-4" size="sm">
          View All Alerts
        </Button>
      </CardContent>
    </Card>
  );
}
