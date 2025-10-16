import { Suspense } from 'react';
import { Dashboard } from '@/components/dashboard/dashboard';
import { Header } from '@/components/layout/header';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { LegalDisclaimer } from '@/components/legal/legal-disclaimer';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            Welcome to VUTAX 2.0
          </h1>
          <p className="text-lg text-slate-600">
            AI-powered stock analysis and paper trading platform for smart investors
          </p>
        </div>

        <Suspense fallback={<LoadingSpinner />}>
          <Dashboard />
        </Suspense>
      </div>

      <LegalDisclaimer />
    </main>
  );
}
