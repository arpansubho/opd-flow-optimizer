import React, { useState } from 'react';
import PatientForm from './components/PatientForm';
import TokenDisplay from './components/TokenDisplay';
import MLOpsPanel from './components/MLOpsPanel';
import DoctorDashboard from './components/DoctorDashboard';
import { Activity } from 'lucide-react';

function App() {
  const [prediction, setPrediction] = useState(null);

  return (
    <div className="min-h-screen bg-slate-50 pb-12">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 p-2 rounded-lg">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-800 tracking-tight">OPD Flow Optimizer</h1>
              <p className="text-xs text-slate-500 font-medium tracking-wide uppercase">Smart Token Routing System</p>
            </div>
          </div>
          <div className="text-sm text-slate-500">
            Powered by ML
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Form & Token */}
          <div className="lg:col-span-1 space-y-6">
            <section>
              <h3 className="text-lg font-medium text-slate-800 mb-3">Patient Registration</h3>
              <PatientForm onPrediction={setPrediction} />
            </section>

            {prediction && (
              <section>
                <TokenDisplay prediction={prediction} />
              </section>
            )}
          </div>

          {/* Right Column: Dashboards */}
          <div className="lg:col-span-2 space-y-8">
            <section>
              <DoctorDashboard />
            </section>

            <section>
              <MLOpsPanel />
            </section>
          </div>
        </div>

      </main>
    </div>
  );
}

export default App;
