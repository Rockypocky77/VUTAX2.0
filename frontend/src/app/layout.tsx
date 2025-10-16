import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Toaster } from '@/components/ui/toaster';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'VUTAX 2.0 - Smart Stock Trading Platform',
  description: 'AI-powered fintech platform for short-term investors with real-time stock analysis, paper trading, and predictive insights.',
  keywords: 'stock trading, fintech, AI predictions, paper trading, stock analysis, investment platform',
  authors: [{ name: 'VUTAX Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    title: 'VUTAX 2.0 - Smart Stock Trading Platform',
    description: 'AI-powered fintech platform for short-term investors',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'VUTAX 2.0 - Smart Stock Trading Platform',
    description: 'AI-powered fintech platform for short-term investors',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen bg-background">
            {children}
          </div>
          <Toaster />
        </Providers>
      </body>
    </html>
  );
}
