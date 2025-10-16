'use client';

import { useEffect, useRef } from 'react';

interface StockChartProps {
  symbol: string;
  showPrediction?: boolean;
}

export function StockChart({ symbol, showPrediction = false }: StockChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // In a real implementation, you would integrate with Chart.js or similar
    // For now, we'll show a placeholder
    if (chartRef.current) {
      chartRef.current.innerHTML = `
        <div class="flex items-center justify-center h-full bg-slate-100 rounded-lg">
          <div class="text-center">
            <div class="text-slate-600 mb-2">📈</div>
            <div class="text-sm text-slate-600">Chart for ${symbol}</div>
            ${showPrediction ? '<div class="text-xs text-primary mt-1">AI Prediction: Enabled</div>' : ''}
          </div>
        </div>
      `;
    }
  }, [symbol, showPrediction]);

  return (
    <div className="h-48 w-full">
      <div ref={chartRef} className="h-full w-full"></div>
    </div>
  );
}
