'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { StockRecommendation } from '@/types';
import { formatCurrency, getRiskColor, getConfidenceColor } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus, Target, Shield, Clock } from 'lucide-react';

interface RecommendationsPanelProps {
  recommendations?: StockRecommendation[];
  loading?: boolean;
}

export function RecommendationsPanel({ recommendations, loading }: RecommendationsPanelProps) {
  if (loading) {
    return (
      <Card className="matte-card">
        <CardHeader>
          <CardTitle>AI Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="p-4 bg-slate-50 rounded-lg">
                <div className="h-4 bg-slate-200 rounded w-1/4 mb-2"></div>
                <div className="h-3 bg-slate-200 rounded w-3/4"></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <Card className="matte-card">
        <CardHeader>
          <CardTitle>AI Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-slate-600">No recommendations available at the moment.</p>
        </CardContent>
      </Card>
    );
  }

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'BUY':
        return <TrendingUp className="w-4 h-4" />;
      case 'SELL':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Minus className="w-4 h-4" />;
    }
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'BUY':
        return 'text-success-600 bg-success-50 border-success-200';
      case 'SELL':
        return 'text-danger-600 bg-danger-50 border-danger-200';
      default:
        return 'text-slate-600 bg-slate-50 border-slate-200';
    }
  };

  return (
    <Card className="matte-card">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Target className="w-5 h-5" />
          <span>AI Recommendations</span>
          <Badge variant="outline" className="ml-auto">
            Live Analysis
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {recommendations.map((rec) => (
          <div key={rec.symbol} className="p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <h4 className="font-semibold text-lg text-slate-900">{rec.symbol}</h4>
                <Badge className={`${getActionColor(rec.action)} border`}>
                  {getActionIcon(rec.action)}
                  <span className="ml-1">{rec.action}</span>
                </Badge>
              </div>
              
              <div className="text-right">
                <div className={`text-sm font-medium ${getConfidenceColor(rec.confidence)}`}>
                  {rec.confidence}% Confidence
                </div>
                <Badge variant="outline" className={getRiskColor(rec.riskTier)}>
                  <Shield className="w-3 h-3 mr-1" />
                  {rec.riskTier}
                </Badge>
              </div>
            </div>

            {/* Price Targets */}
            {(rec.targetPrice || rec.stopLoss) && (
              <div className="flex items-center space-x-4 mb-3 text-sm">
                {rec.targetPrice && (
                  <div className="flex items-center space-x-1">
                    <span className="text-slate-600">Target:</span>
                    <span className="font-medium text-success-600">
                      {formatCurrency(rec.targetPrice)}
                    </span>
                  </div>
                )}
                {rec.stopLoss && (
                  <div className="flex items-center space-x-1">
                    <span className="text-slate-600">Stop:</span>
                    <span className="font-medium text-danger-600">
                      {formatCurrency(rec.stopLoss)}
                    </span>
                  </div>
                )}
              </div>
            )}

            {/* Reasoning */}
            <p className="text-sm text-slate-700 mb-3 leading-relaxed">
              {rec.reasoning}
            </p>

            {/* Footer */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-1 text-xs text-slate-500">
                <Clock className="w-3 h-3" />
                <span>Valid until {new Date(rec.validUntil).toLocaleDateString()}</span>
              </div>
              
              <div className="flex space-x-2">
                <Button size="sm" variant="outline">
                  View Analysis
                </Button>
                {rec.action === 'BUY' && (
                  <Button size="sm" variant="default">
                    Add to Portfolio
                  </Button>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Disclaimer */}
        <div className="mt-6 p-3 bg-warning-50 border border-warning-200 rounded-lg">
          <p className="text-xs text-warning-800">
            <strong>⚠️ Disclaimer:</strong> These recommendations are for informational purposes only and do not constitute financial advice. 
            Always conduct your own research and consider your risk tolerance before making investment decisions.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
