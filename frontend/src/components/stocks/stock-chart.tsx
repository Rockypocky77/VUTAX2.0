'use client';

import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface StockChartProps {
  symbol: string;
  showPrediction?: boolean;
}

interface ChartPoint {
  x: number;
  y: number;
  price: number;
  date: string;
}

export function StockChart({ symbol, showPrediction = false }: StockChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredPoint, setHoveredPoint] = useState<ChartPoint | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isAnimating, setIsAnimating] = useState(false);

  // Generate mock data for the chart
  const generateChartData = (): ChartPoint[] => {
    const points: ChartPoint[] = [];
    const basePrice = 100 + Math.random() * 100;
    const days = 30;
    
    for (let i = 0; i < days; i++) {
      const date = new Date();
      date.setDate(date.getDate() - (days - i));
      
      const price = basePrice + (Math.sin(i * 0.2) * 20) + (Math.random() - 0.5) * 10;
      points.push({
        x: (i / (days - 1)) * 100, // Percentage across canvas
        y: 20 + (1 - (price - basePrice + 30) / 60) * 60, // Percentage from top
        price: price,
        date: date.toLocaleDateString()
      });
    }
    
    return points;
  };

  const [chartData] = useState<ChartPoint[]>(generateChartData());

  const drawChart = (canvas: HTMLCanvasElement, animationProgress: number = 1) => {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    
    // Set canvas size
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    
    // Clear canvas
    ctx.clearRect(0, 0, rect.width, rect.height);
    
    // Draw grid
    ctx.strokeStyle = '#f1f5f9';
    ctx.lineWidth = 1;
    
    // Horizontal grid lines
    for (let i = 0; i <= 4; i++) {
      const y = (i / 4) * rect.height;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(rect.width, y);
      ctx.stroke();
    }
    
    // Vertical grid lines
    for (let i = 0; i <= 6; i++) {
      const x = (i / 6) * rect.width;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, rect.height);
      ctx.stroke();
    }

    // Calculate actual positions
    const actualPoints = chartData.map(point => ({
      ...point,
      actualX: (point.x / 100) * rect.width,
      actualY: (point.y / 100) * rect.height
    }));

    // Draw animated line
    const animatedPoints = actualPoints.slice(0, Math.floor(actualPoints.length * animationProgress));
    
    if (animatedPoints.length > 1) {
      // Draw gradient fill
      const gradient = ctx.createLinearGradient(0, 0, 0, rect.height);
      gradient.addColorStop(0, 'rgba(59, 130, 246, 0.1)');
      gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.moveTo(animatedPoints[0].actualX, rect.height);
      
      animatedPoints.forEach((point, index) => {
        if (index === 0) {
          ctx.lineTo(point.actualX, point.actualY);
        } else {
          const prevPoint = animatedPoints[index - 1];
          const cpx = (prevPoint.actualX + point.actualX) / 2;
          ctx.quadraticCurveTo(cpx, prevPoint.actualY, point.actualX, point.actualY);
        }
      });
      
      ctx.lineTo(animatedPoints[animatedPoints.length - 1].actualX, rect.height);
      ctx.closePath();
      ctx.fill();

      // Draw main line
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 3;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      ctx.beginPath();
      animatedPoints.forEach((point, index) => {
        if (index === 0) {
          ctx.moveTo(point.actualX, point.actualY);
        } else {
          const prevPoint = animatedPoints[index - 1];
          const cpx = (prevPoint.actualX + point.actualX) / 2;
          ctx.quadraticCurveTo(cpx, prevPoint.actualY, point.actualX, point.actualY);
        }
      });
      ctx.stroke();

      // Draw prediction line if enabled
      if (showPrediction && animationProgress === 1) {
        const lastPoint = animatedPoints[animatedPoints.length - 1];
        const predictionEndX = rect.width;
        const predictionEndY = lastPoint.actualY + (Math.random() - 0.5) * 40;
        
        ctx.strokeStyle = '#8b5cf6';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        
        ctx.beginPath();
        ctx.moveTo(lastPoint.actualX, lastPoint.actualY);
        ctx.lineTo(predictionEndX, predictionEndY);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // Draw animated arrow following the line
      if (isAnimating && animationProgress < 1) {
        const currentIndex = Math.floor((animatedPoints.length - 1) * animationProgress);
        const nextIndex = Math.min(currentIndex + 1, animatedPoints.length - 1);
        
        if (currentIndex < animatedPoints.length) {
          const currentPoint = animatedPoints[currentIndex];
          const nextPoint = animatedPoints[nextIndex];
          
          const t = ((animatedPoints.length - 1) * animationProgress) - currentIndex;
          const arrowX = currentPoint.actualX + (nextPoint.actualX - currentPoint.actualX) * t;
          const arrowY = currentPoint.actualY + (nextPoint.actualY - currentPoint.actualY) * t;
          
          // Draw arrow
          ctx.fillStyle = '#ef4444';
          ctx.beginPath();
          ctx.arc(arrowX, arrowY, 6, 0, Math.PI * 2);
          ctx.fill();
          
          // Arrow tail
          ctx.strokeStyle = '#ef4444';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(arrowX - 10, arrowY);
          ctx.lineTo(arrowX - 4, arrowY);
          ctx.stroke();
        }
      }

      // Draw data points
      animatedPoints.forEach((point, index) => {
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = 2;
        
        ctx.beginPath();
        ctx.arc(point.actualX, point.actualY, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      });
    }
  };

  const handleMouseMove = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    setMousePos({ x: event.clientX, y: event.clientY });

    // Find closest point
    let closestPoint: ChartPoint | null = null;
    let minDistance = Infinity;

    chartData.forEach(point => {
      const actualX = (point.x / 100) * rect.width;
      const actualY = (point.y / 100) * rect.height;
      const distance = Math.sqrt(Math.pow(x - actualX, 2) + Math.pow(y - actualY, 2));
      
      if (distance < minDistance && distance < 30) {
        minDistance = distance;
        closestPoint = point;
      }
    });

    setHoveredPoint(closestPoint);
  };

  const handleMouseLeave = () => {
    setHoveredPoint(null);
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    setIsAnimating(true);
    
    // Animate the chart drawing
    let animationFrame: number;
    let startTime: number;
    const duration = 2000; // 2 seconds

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      
      // Easing function for smooth animation
      const easeOutCubic = 1 - Math.pow(1 - progress, 3);
      
      drawChart(canvas, easeOutCubic);
      
      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      } else {
        setIsAnimating(false);
      }
    };

    animationFrame = requestAnimationFrame(animate);

    return () => {
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
    };
  }, [symbol, showPrediction]);

  return (
    <div className="relative h-48 w-full" ref={containerRef}>
      <motion.canvas
        ref={canvasRef}
        className="w-full h-full cursor-crosshair rounded-lg"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }}
      />
      
      {/* Hover tooltip */}
      <AnimatePresence>
        {hoveredPoint && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 10 }}
            transition={{ duration: 0.2 }}
            className="fixed z-50 bg-white rounded-lg shadow-xl border border-slate-200 p-3 pointer-events-none"
            style={{
              left: mousePos.x + 10,
              top: mousePos.y - 60,
            }}
          >
            <div className="text-sm font-semibold text-slate-900">
              ${hoveredPoint.price.toFixed(2)}
            </div>
            <div className="text-xs text-slate-600">
              {hoveredPoint.date}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chart info overlay */}
      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-sm">
        <div className="text-sm font-semibold text-slate-900">{symbol}</div>
        <div className="text-xs text-slate-600">30-day trend</div>
        {showPrediction && (
          <div className="text-xs text-purple-600 mt-1 flex items-center">
            <div className="w-2 h-2 bg-purple-600 rounded-full mr-1"></div>
            AI Prediction
          </div>
        )}
      </div>
    </div>
  );
}
