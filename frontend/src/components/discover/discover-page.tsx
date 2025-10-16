'use client';

import { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  Search, 
  TrendingUp, 
  Star, 
  Filter,
  ArrowRight,
  Sparkles,
  BarChart3
} from 'lucide-react';
import { StockCard } from '@/components/stocks/stock-card';
import { cn } from '@/lib/utils';

// Import stock symbols data
import stockSymbols from '@/data/stock-symbols.json';

interface StockSymbol {
  symbol: string;
  name: string;
  sector: string;
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
      duration: 0.8,
      ease: [0.25, 0.46, 0.45, 0.94]
    }
  }
};

const searchVariants = {
  hidden: { scale: 0.95, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: [0.25, 0.46, 0.45, 0.94]
    }
  }
};

export function DiscoverPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSector, setSelectedSector] = useState('all');
  const [selectedStock, setSelectedStock] = useState<StockSymbol | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isSearchFocused, setIsSearchFocused] = useState(false);

  // Filter and search logic
  const filteredStocks = useMemo(() => {
    let filtered = stockSymbols;

    // Filter by sector
    if (selectedSector !== 'all') {
      filtered = filtered.filter(stock => 
        stock.sector.toLowerCase() === selectedSector.toLowerCase()
      );
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(stock =>
        stock.symbol.toLowerCase().includes(query) ||
        stock.name.toLowerCase().includes(query)
      );
    }

    return filtered.slice(0, 50); // Limit results for performance
  }, [searchQuery, selectedSector]);

  // Get unique sectors
  const sectors = useMemo(() => {
    const sectorSet = new Set(stockSymbols.map(stock => stock.sector));
    return ['all', ...Array.from(sectorSet)];
  }, []);

  // Popular stocks for initial display
  const popularStocks = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B'
  ];

  const handleStockSelect = (stock: StockSymbol) => {
    setSelectedStock(stock);
    setSearchQuery('');
    setShowSuggestions(false);
  };

  const handleSearchFocus = () => {
    setIsSearchFocused(true);
    setShowSuggestions(true);
  };

  const handleSearchBlur = () => {
    setIsSearchFocused(false);
    // Delay hiding suggestions to allow for clicks
    setTimeout(() => setShowSuggestions(false), 200);
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
        <motion.div variants={itemVariants} className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <motion.div
              className="w-12 h-12 bg-gradient-to-br from-primary to-purple-600 rounded-2xl flex items-center justify-center mr-4"
              whileHover={{ scale: 1.1, rotate: 5 }}
              transition={{ duration: 0.3 }}
            >
              <Sparkles className="w-6 h-6 text-white" />
            </motion.div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent">
              Discover Stocks
            </h1>
          </div>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Explore thousands of stocks with AI-powered insights and real-time analysis
          </p>
        </motion.div>

        {/* Search Section */}
        <motion.div variants={searchVariants} className="max-w-4xl mx-auto mb-12">
          <Card className="matte-card border-2 border-transparent hover:border-primary/20 transition-all duration-500">
            <CardContent className="p-6">
              <div className="relative">
                <div className="relative">
                  <Search className={cn(
                    "absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 transition-colors duration-300",
                    isSearchFocused ? "text-primary" : "text-slate-400"
                  )} />
                  <Input
                    placeholder="Search stocks by symbol or company name..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onFocus={handleSearchFocus}
                    onBlur={handleSearchBlur}
                    className="pl-12 pr-4 py-6 text-lg border-none bg-slate-50 focus:bg-white transition-all duration-300 rounded-xl"
                  />
                </div>

                {/* Search Suggestions */}
                <AnimatePresence>
                  {showSuggestions && (searchQuery.length > 0 || isSearchFocused) && (
                    <motion.div
                      initial={{ opacity: 0, y: -10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: -10, scale: 0.95 }}
                      transition={{ duration: 0.3, ease: [0.25, 0.46, 0.45, 0.94] }}
                      className="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-2xl border border-slate-200 z-50 max-h-80 overflow-y-auto"
                    >
                      {filteredStocks.length > 0 ? (
                        <div className="p-2">
                          {filteredStocks.map((stock, index) => (
                            <motion.div
                              key={stock.symbol}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.05, duration: 0.3 }}
                              onClick={() => handleStockSelect(stock)}
                              className="flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 cursor-pointer transition-all duration-200 group"
                            >
                              <div className="flex items-center space-x-3">
                                <div className="w-10 h-10 bg-gradient-to-br from-primary/10 to-purple-600/10 rounded-lg flex items-center justify-center group-hover:from-primary/20 group-hover:to-purple-600/20 transition-all duration-200">
                                  <span className="font-bold text-primary text-sm">{stock.symbol}</span>
                                </div>
                                <div>
                                  <div className="font-medium text-slate-900">{stock.symbol}</div>
                                  <div className="text-sm text-slate-600 truncate max-w-xs">{stock.name}</div>
                                </div>
                              </div>
                              <div className="flex items-center space-x-2">
                                <Badge variant="outline" className="text-xs">
                                  {stock.sector}
                                </Badge>
                                <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-primary transition-colors duration-200" />
                              </div>
                            </motion.div>
                          ))}
                        </div>
                      ) : (
                        <div className="p-6 text-center text-slate-500">
                          <Search className="w-8 h-8 mx-auto mb-2 opacity-50" />
                          <p>No stocks found matching "{searchQuery}"</p>
                        </div>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Sector Filter */}
              <div className="flex flex-wrap gap-2 mt-6">
                {sectors.map((sector) => (
                  <motion.button
                    key={sector}
                    onClick={() => setSelectedSector(sector)}
                    className={cn(
                      "px-4 py-2 rounded-full text-sm font-medium transition-all duration-300",
                      selectedSector === sector
                        ? "bg-primary text-white shadow-lg"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    )}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {sector === 'all' ? 'All Sectors' : sector}
                  </motion.button>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Selected Stock Display */}
        <AnimatePresence>
          {selectedStock && (
            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -50, scale: 0.9 }}
              transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}
              className="max-w-4xl mx-auto mb-12"
            >
              <StockCard 
                stock={{
                  symbol: selectedStock.symbol,
                  name: selectedStock.name,
                  price: Math.random() * 200 + 50, // Mock price
                  change: (Math.random() - 0.5) * 10,
                  changePercent: (Math.random() - 0.5) * 5,
                  volume: Math.floor(Math.random() * 10000000),
                  sector: selectedStock.sector,
                  lastUpdated: new Date().toISOString()
                }}
                showChart={true}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Popular Stocks */}
        {!selectedStock && (
          <motion.div variants={itemVariants}>
            <Card className="matte-card mb-8">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <TrendingUp className="w-5 h-5" />
                  <span>Popular Stocks</span>
                  <Badge variant="outline" className="ml-auto">
                    Trending
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {popularStocks.map((symbol, index) => {
                    const stock = stockSymbols.find(s => s.symbol === symbol);
                    if (!stock) return null;

                    return (
                      <motion.div
                        key={symbol}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1, duration: 0.5 }}
                        onClick={() => handleStockSelect(stock)}
                        className="p-4 bg-slate-50 rounded-xl hover:bg-white hover:shadow-lg cursor-pointer transition-all duration-300 group"
                        whileHover={{ y: -5 }}
                      >
                        <div className="flex items-center space-x-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-primary/10 to-purple-600/10 rounded-xl flex items-center justify-center group-hover:from-primary/20 group-hover:to-purple-600/20 transition-all duration-300">
                            <span className="font-bold text-primary">{symbol}</span>
                          </div>
                          <div>
                            <div className="font-medium text-slate-900">{symbol}</div>
                            <div className="text-xs text-slate-600">{stock.sector}</div>
                          </div>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Browse by Sector */}
        {!selectedStock && (
          <motion.div variants={itemVariants}>
            <Card className="matte-card">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="w-5 h-5" />
                  <span>Browse by Sector</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {sectors.slice(1).map((sector, index) => {
                    const sectorCount = stockSymbols.filter(s => s.sector === sector).length;
                    
                    return (
                      <motion.div
                        key={sector}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.1, duration: 0.5 }}
                        onClick={() => setSelectedSector(sector)}
                        className="p-6 bg-gradient-to-br from-slate-50 to-white rounded-xl hover:shadow-lg cursor-pointer transition-all duration-300 group border border-slate-100 hover:border-primary/20"
                        whileHover={{ y: -3, scale: 1.02 }}
                      >
                        <div className="flex items-center justify-between mb-3">
                          <h3 className="font-semibold text-slate-900 group-hover:text-primary transition-colors duration-300">
                            {sector}
                          </h3>
                          <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-primary transition-colors duration-300" />
                        </div>
                        <p className="text-sm text-slate-600">
                          {sectorCount} stocks available
                        </p>
                        <div className="mt-3 w-full bg-slate-200 rounded-full h-1">
                          <motion.div
                            className="bg-gradient-to-r from-primary to-purple-600 h-1 rounded-full"
                            initial={{ width: 0 }}
                            animate={{ width: `${Math.min((sectorCount / 500) * 100, 100)}%` }}
                            transition={{ delay: index * 0.1 + 0.5, duration: 0.8 }}
                          />
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
