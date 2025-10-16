'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Bell, 
  Settings, 
  User, 
  TrendingUp, 
  Activity,
  Menu,
  X
} from 'lucide-react';
import { motion } from 'framer-motion';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-purple-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-slate-900">VUTAX 2.0</h1>
            </div>
            
            <Badge variant="outline" className="hidden sm:inline-flex">
              <Activity className="w-3 h-3 mr-1" />
              Live Market Data
            </Badge>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#dashboard" className="text-slate-600 hover:text-slate-900 transition-colors">
              Dashboard
            </a>
            <a href="#portfolio" className="text-slate-600 hover:text-slate-900 transition-colors">
              Portfolio
            </a>
            <a href="#watchlist" className="text-slate-600 hover:text-slate-900 transition-colors">
              Watchlist
            </a>
            <a href="#analytics" className="text-slate-600 hover:text-slate-900 transition-colors">
              Analytics
            </a>
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-3">
            {/* Notifications */}
            <Button variant="ghost" size="sm" className="relative">
              <Bell className="w-4 h-4" />
              <span className="absolute -top-1 -right-1 w-2 h-2 bg-danger-500 rounded-full"></span>
            </Button>

            {/* Settings */}
            <Button variant="ghost" size="sm">
              <Settings className="w-4 h-4" />
            </Button>

            {/* User Profile (Not integrated yet) */}
            <Button variant="ghost" size="sm" className="hidden sm:flex">
              <User className="w-4 h-4" />
              <span className="ml-2 text-sm">Guest User</span>
            </Button>

            {/* Mobile Menu Toggle */}
            <Button 
              variant="ghost" 
              size="sm" 
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-slate-200 py-4"
          >
            <nav className="flex flex-col space-y-3">
              <a href="#dashboard" className="text-slate-600 hover:text-slate-900 transition-colors py-2">
                Dashboard
              </a>
              <a href="#portfolio" className="text-slate-600 hover:text-slate-900 transition-colors py-2">
                Portfolio
              </a>
              <a href="#watchlist" className="text-slate-600 hover:text-slate-900 transition-colors py-2">
                Watchlist
              </a>
              <a href="#analytics" className="text-slate-600 hover:text-slate-900 transition-colors py-2">
                Analytics
              </a>
              <div className="pt-2 border-t border-slate-200">
                <div className="flex items-center space-x-2 py-2">
                  <User className="w-4 h-4 text-slate-500" />
                  <span className="text-sm text-slate-600">Guest User</span>
                </div>
              </div>
            </nav>
          </motion.div>
        )}
      </div>
    </header>
  );
}
