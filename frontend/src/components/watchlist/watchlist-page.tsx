'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  Star, 
  Search, 
  Filter,
  TrendingUp,
  TrendingDown,
  BarChart3,
  Plus,
  Minus,
  Eye,
  Trash2,
  Settings
} from 'lucide-react';
import { StockCard } from '@/components/stocks/stock-card';
import { cn, formatCurrency, formatPercent, getChangeColor } from '@/lib/utils';

interface WatchlistStock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  sector: string;
  addedDate: string;
  isExpanded?: boolean;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

const itemVariants = {
  hidden: { y: 30, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: [0.25, 0.46, 0.45, 0.94]
    }
  }
};

const cardVariants = {
  hidden: { scale: 0.95, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: {
      duration: 0.4,
      ease: [0.25, 0.46, 0.45, 0.94]
    }
  },
  hover: {
    y: -8,
    scale: 1.02,
    transition: {
      duration: 0.3,
      ease: [0.25, 0.46, 0.45, 0.94]
    }
  }
};

export function WatchlistPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'symbol' | 'change' | 'volume' | 'added'>('symbol');
  const [filterSector, setFilterSector] = useState('all');
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());

  // Mock watchlist data
  const [watchlistStocks] = useState<WatchlistStock[]>([
    {
      symbol: 'AAPL',
      name: 'Apple Inc.',
      price: 175.43,
      change: 2.34,
      changePercent: 1.35,
      volume: 45678900,
      sector: 'Technology',
      addedDate: '2024-01-15'
    },
    {
      symbol: 'MSFT',
      name: 'Microsoft Corporation',
      price: 378.85,
      change: -1.23,
      changePercent: -0.32,
      volume: 23456789,
      sector: 'Technology',
      addedDate: '2024-01-20'
    },
    {
      symbol: 'GOOGL',
      name: 'Alphabet Inc.',
      price: 142.56,
      change: 3.45,
      changePercent: 2.48,
      volume: 34567890,
      sector: 'Technology',
      addedDate: '2024-01-18'
    },
    {
      symbol: 'TSLA',
      name: 'Tesla Inc.',
      price: 248.50,
      change: -5.67,
      changePercent: -2.23,
      volume: 67890123,
      sector: 'Automotive',
      addedDate: '2024-01-22'
    },
    {
      symbol: 'NVDA',
      name: 'NVIDIA Corporation',
      price: 456.78,
      change: 12.34,
      changePercent: 2.78,
      volume: 56789012,
      sector: 'Technology',
      addedDate: '2024-01-25'
    }
  ]);

  // Filter and sort stocks
  const filteredStocks = watchlistStocks
    .filter(stock => {
      const matchesSearch = stock.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           stock.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesSector = filterSector === 'all' || stock.sector === filterSector;
      return matchesSearch && matchesSector;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'change':
          return b.changePercent - a.changePercent;
        case 'volume':
          return b.volume - a.volume;
        case 'added':
          return new Date(b.addedDate).getTime() - new Date(a.addedDate).getTime();
        default:
          return a.symbol.localeCompare(b.symbol);
      }
    });

  const sectors = ['all', ...Array.from(new Set(watchlistStocks.map(s => s.sector)))];

  const toggleExpanded = (symbol: string) => {
    const newExpanded = new Set(expandedCards);
    if (newExpanded.has(symbol)) {
      newExpanded.delete(symbol);
    } else {
      newExpanded.add(symbol);
    }
    setExpandedCards(newExpanded);
  };

  const removeFromWatchlist = (symbol: string) => {
    // In a real app, this would update the watchlist
    console.log('Remove from watchlist:', symbol);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
      <motion.div
        className="container mx-auto px-4 py-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-primary to-purple-600 rounded-2xl flex items-center justify-center">
                <Star className="w-6 h-6 text-white fill-current" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900">My Watchlist</h1>
                <p className="text-slate-600">Track your favorite stocks in one place</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <Badge variant="outline" className="px-3 py-1">
                {watchlistStocks.length} / 50 stocks
              </Badge>
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </Button>
            </div>
          </div>

          {/* Controls */}
          <Card className="matte-card">
            <CardContent className="p-6">
              <div className="flex flex-col md:flex-row gap-4">
                {/* Search */}
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input
                    placeholder="Search stocks..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>

                {/* Sort */}
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="px-4 py-2 border border-slate-200 rounded-lg bg-white"
                >
                  <option value="symbol">Sort by Symbol</option>
                  <option value="change">Sort by Change</option>
                  <option value="volume">Sort by Volume</option>
                  <option value="added">Sort by Date Added</option>
                </select>

                {/* Filter */}
                <select
                  value={filterSector}
                  onChange={(e) => setFilterSector(e.target.value)}
                  className="px-4 py-2 border border-slate-200 rounded-lg bg-white"
                >
                  {sectors.map(sector => (
                    <option key={sector} value={sector}>
                      {sector === 'all' ? 'All Sectors' : sector}
                    </option>
                  ))}
                </select>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Watchlist Grid */}
        <motion.div variants={itemVariants}>
          {filteredStocks.length === 0 ? (
            <Card className="matte-card">
              <CardContent className="p-12 text-center">
                <Eye className="w-16 h-16 mx-auto mb-4 text-slate-300" />
                <h3 className="text-xl font-semibold text-slate-900 mb-2">No stocks found</h3>
                <p className="text-slate-600 mb-6">
                  {searchQuery ? 'Try adjusting your search or filters' : 'Start building your watchlist by adding some stocks'}
                </p>
                <Button>
                  <Plus className="w-4 h-4 mr-2" />
                  Add Stocks
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {filteredStocks.map((stock, index) => (
                <motion.div
                  key={stock.symbol}
                  variants={cardVariants}
                  initial="hidden"
                  animate="visible"
                  whileHover="hover"
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="matte-card overflow-hidden cursor-pointer">
                    <CardHeader 
                      className="pb-3"
                      onClick={() => toggleExpanded(stock.symbol)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-primary/10 to-purple-600/10 rounded-xl flex items-center justify-center">
                            <span className="font-bold text-primary">{stock.symbol}</span>
                          </div>
                          <div>
                            <CardTitle className="text-lg">{stock.symbol}</CardTitle>
                            <p className="text-sm text-slate-600 truncate max-w-[200px]">{stock.name}</p>
                          </div>
                        </div>

                        <div className="flex items-center space-x-2">
                          <motion.button
                            onClick={(e) => {
                              e.stopPropagation();
                              removeFromWatchlist(stock.symbol);
                            }}
                            className="p-2 text-slate-400 hover:text-danger-500 hover:bg-danger-50 rounded-lg transition-colors"
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                          >
                            <Trash2 className="w-4 h-4" />
                          </motion.button>
                          
                          <motion.div
                            animate={{ rotate: expandedCards.has(stock.symbol) ? 180 : 0 }}
                            transition={{ duration: 0.3 }}
                          >
                            <BarChart3 className="w-5 h-5 text-slate-400" />
                          </motion.div>
                        </div>
                      </div>
                    </CardHeader>

                    <CardContent className="pt-0">
                      {/* Price Info */}
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <div className="text-2xl font-bold text-slate-900">
                            {formatCurrency(stock.price)}
                          </div>
                          <div className={cn("flex items-center text-sm", getChangeColor(stock.change))}>
                            {stock.change >= 0 ? (
                              <TrendingUp className="w-4 h-4 mr-1" />
                            ) : (
                              <TrendingDown className="w-4 h-4 mr-1" />
                            )}
                            {formatCurrency(Math.abs(stock.change))} ({formatPercent(stock.changePercent)})
                          </div>
                        </div>

                        <div className="text-right">
                          <Badge variant="outline">{stock.sector}</Badge>
                          <div className="text-xs text-slate-500 mt-1">
                            Vol: {stock.volume.toLocaleString()}
                          </div>
                        </div>
                      </div>

                      {/* Expanded Content */}
                      <AnimatePresence>
                        {expandedCards.has(stock.symbol) && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.4, ease: [0.25, 0.46, 0.45, 0.94] }}
                            className="overflow-hidden"
                          >
                            <div className="border-t pt-4 mt-4">
                              <StockCard
                                stock={{
                                  symbol: stock.symbol,
                                  name: stock.name,
                                  price: stock.price,
                                  change: stock.change,
                                  changePercent: stock.changePercent,
                                  volume: stock.volume,
                                  sector: stock.sector,
                                  lastUpdated: new Date().toISOString()
                                }}
                                showChart={true}
                                compact={false}
                                isInWatchlist={true}
                                onRemoveFromWatchlist={removeFromWatchlist}
                              />
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>

                      {/* Quick Stats */}
                      <div className="grid grid-cols-2 gap-4 text-sm mt-4">
                        <div>
                          <span className="text-slate-600">Added:</span>
                          <span className="ml-2 font-medium">
                            {new Date(stock.addedDate).toLocaleDateString()}
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-600">Days:</span>
                          <span className="ml-2 font-medium">
                            {Math.floor((Date.now() - new Date(stock.addedDate).getTime()) / (1000 * 60 * 60 * 24))}d
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Summary Stats */}
        <motion.div variants={itemVariants} className="mt-8">
          <Card className="matte-card">
            <CardHeader>
              <CardTitle>Watchlist Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-900">{watchlistStocks.length}</div>
                  <div className="text-sm text-slate-600">Total Stocks</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-success-600">
                    {watchlistStocks.filter(s => s.change > 0).length}
                  </div>
                  <div className="text-sm text-slate-600">Gainers</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-danger-600">
                    {watchlistStocks.filter(s => s.change < 0).length}
                  </div>
                  <div className="text-sm text-slate-600">Losers</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-900">
                    {Array.from(new Set(watchlistStocks.map(s => s.sector))).length}
                  </div>
                  <div className="text-sm text-slate-600">Sectors</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>
    </div>
  );
}
