'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  AlertTriangle, 
  Shield, 
  BookOpen, 
  Users, 
  ChevronDown,
  ChevronUp,
  Info
} from 'lucide-react';

export function LegalDisclaimer() {
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  const sections = [
    {
      id: 'investment-risk',
      title: 'Investment Risk Warning',
      icon: AlertTriangle,
      color: 'text-danger-600',
      content: `All investments carry risk of loss. Past performance does not guarantee future results. 
      The value of investments can go down as well as up, and you may not get back the amount you invested. 
      Stock prices can be volatile and unpredictable.`
    },
    {
      id: 'not-advice',
      title: 'Not Financial Advice',
      icon: Info,
      color: 'text-warning-600',
      content: `VUTAX provides information and analysis for educational purposes only. Nothing on this platform 
      constitutes personalized financial, investment, or trading advice. Always consult with qualified 
      financial professionals before making investment decisions.`
    },
    {
      id: 'ai-limitations',
      title: 'AI Model Limitations',
      icon: Shield,
      color: 'text-slate-600',
      content: `Our AI models are based on historical data and technical analysis. They cannot predict 
      market events, economic changes, or company-specific developments. Model accuracy may vary and 
      should not be the sole basis for investment decisions.`
    },
    {
      id: 'age-restrictions',
      title: 'Age & Paper Trading',
      icon: Users,
      color: 'text-success-600',
      content: `Users under 18 can only access paper trading features. Real money trading requires 
      appropriate age verification and compliance with local regulations. Paper trading results 
      may not reflect real market conditions including slippage and fees.`
    },
    {
      id: 'educational-purpose',
      title: 'Educational Platform',
      icon: BookOpen,
      color: 'text-primary',
      content: `VUTAX is designed as an educational platform to help users learn about investing and 
      market analysis. Use this platform to develop your understanding of financial markets, 
      not as a substitute for professional financial advice.`
    }
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50">
      <motion.div
        initial={{ y: '100%' }}
        animate={{ y: isExpanded ? 0 : 'calc(100% - 60px)' }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="bg-white border-t border-slate-200 shadow-lg"
      >
        {/* Collapsed Header */}
        <div 
          className="flex items-center justify-between p-4 cursor-pointer hover:bg-slate-50 transition-colors"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-5 h-5 text-warning-600" />
            <span className="font-medium text-slate-900">
              Important Legal Information
            </span>
            <Badge variant="outline" className="text-xs">
              Required Reading
            </Badge>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className="text-sm text-slate-600 hidden sm:block">
              Click to {isExpanded ? 'minimize' : 'expand'}
            </span>
            {isExpanded ? (
              <ChevronDown className="w-5 h-5 text-slate-600" />
            ) : (
              <ChevronUp className="w-5 h-5 text-slate-600" />
            )}
          </div>
        </div>

        {/* Expanded Content */}
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className="border-t border-slate-200 bg-slate-50"
            >
              <div className="max-w-6xl mx-auto p-6">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-slate-900 mb-2">
                    Legal Disclaimers & Important Information
                  </h2>
                  <p className="text-slate-600">
                    Please read these important disclaimers before using VUTAX. 
                    By continuing to use this platform, you acknowledge and agree to these terms.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                  {sections.map((section) => {
                    const IconComponent = section.icon;
                    const isActive = activeSection === section.id;
                    
                    return (
                      <Card 
                        key={section.id}
                        className={`cursor-pointer transition-all duration-200 hover:shadow-md ${
                          isActive ? 'ring-2 ring-primary' : ''
                        }`}
                        onClick={() => setActiveSection(isActive ? null : section.id)}
                      >
                        <CardHeader className="pb-3">
                          <CardTitle className="flex items-center space-x-2 text-sm">
                            <IconComponent className={`w-4 h-4 ${section.color}`} />
                            <span>{section.title}</span>
                          </CardTitle>
                        </CardHeader>
                        
                        <AnimatePresence>
                          {isActive && (
                            <motion.div
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: 'auto' }}
                              exit={{ opacity: 0, height: 0 }}
                              transition={{ duration: 0.2 }}
                            >
                              <CardContent className="pt-0">
                                <p className="text-sm text-slate-700 leading-relaxed">
                                  {section.content}
                                </p>
                              </CardContent>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </Card>
                    );
                  })}
                </div>

                {/* Key Points Summary */}
                <div className="bg-white rounded-lg p-6 border border-slate-200">
                  <h3 className="font-semibold text-slate-900 mb-4 flex items-center">
                    <Shield className="w-5 h-5 mr-2 text-primary" />
                    Key Points to Remember
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="space-y-2">
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-danger-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-slate-700">
                          <strong>High Risk:</strong> All stock investments carry significant risk of loss
                        </span>
                      </div>
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-warning-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-slate-700">
                          <strong>No Guarantees:</strong> AI predictions are not guaranteed to be accurate
                        </span>
                      </div>
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-slate-700">
                          <strong>Educational Only:</strong> This platform is for learning purposes
                        </span>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-success-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-slate-700">
                          <strong>Paper Trading:</strong> Safe environment for minors to learn
                        </span>
                      </div>
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-slate-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-slate-700">
                          <strong>Professional Advice:</strong> Consult qualified advisors for real decisions
                        </span>
                      </div>
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-indigo-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-slate-700">
                          <strong>Your Responsibility:</strong> Always do your own research
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Footer Actions */}
                <div className="flex items-center justify-between mt-6 pt-4 border-t border-slate-200">
                  <div className="text-sm text-slate-600">
                    Last updated: {new Date().toLocaleDateString()}
                  </div>
                  
                  <div className="flex space-x-3">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => window.open('/terms-of-service', '_blank')}
                    >
                      Full Terms of Service
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => window.open('/privacy-policy', '_blank')}
                    >
                      Privacy Policy
                    </Button>
                    <Button 
                      size="sm"
                      onClick={() => setIsExpanded(false)}
                    >
                      I Understand
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
