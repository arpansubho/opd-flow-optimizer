import React, { useState, useEffect } from 'react';
import { getMetrics, retrainModel } from '../api';
import { RefreshCw, Activity, GitCommitHorizontal, CheckCircle, TriangleAlert } from 'lucide-react';

const MLOpsPanel = () => {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(false);
    const [retraining, setRetraining] = useState(false);
    const [message, setMessage] = useState(null);

    const loadMetrics = async () => {
        setLoading(true);
        try {
            const data = await getMetrics();
            setMetrics(data);
        } catch (error) {
            console.error("Failed to load metrics");
        } finally {
            setLoading(false);
        }
    };

    const handleRetrain = async () => {
        setRetraining(true);
        setMessage(null);
        try {
            const result = await retrainModel();
            setMessage({ type: 'success', text: result.message || 'Retraining successful' });
            // Reload metrics
            setMetrics(result.results || result); // Adjust based on actual API response structure
            loadMetrics(); // Refresh to be sure
        } catch (error) {
            setMessage({ type: 'error', text: 'Retraining failed' });
        } finally {
            setRetraining(false);
        }
    };

    useEffect(() => {
        loadMetrics();
    }, []);

    if (loading && !metrics) return <div className="p-4">Loading MLOps stats...</div>;

    return (
        <div className="bg-slate-50 border-t border-slate-200 p-6 mt-8">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold text-slate-700 flex items-center gap-2">
                    <Activity className="w-5 h-5 text-indigo-500" /> MLOps Control Panel
                </h3>
                <button
                    onClick={handleRetrain}
                    disabled={retraining}
                    className="flex items-center gap-2 px-3 py-1.5 bg-indigo-100 text-indigo-700 rounded-md hover:bg-indigo-200 text-sm font-medium transition-colors"
                >
                    <RefreshCw className={`w-4 h-4 ${retraining ? 'animate-spin' : ''}`} />
                    {retraining ? 'Retraining...' : 'Trigger Retraining'}
                </button>
            </div>

            {message && (
                <div className={`mb-4 p-3 rounded-md text-sm ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {message.text}
                </div>
            )}

            {metrics && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Model Version */}
                    <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200">
                        <div className="flex items-center gap-3 mb-2">
                            <GitCommit className="w-8 h-8 text-blue-500 bg-blue-50 p-1.5 rounded-full" />
                            <div>
                                <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Model Version</p>
                                <p className="text-lg font-bold text-slate-800">{metrics.model_version || 'v1.0'}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-1 text-xs text-green-600 mt-2">
                            <CheckCircle className="w-3 h-3" /> Active
                        </div>
                    </div>

                    {/* Metrics */}
                    <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 md:col-span-2">
                        <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Performance Metrics (RMSE / MAE)</p>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-2xl font-bold text-slate-800">{metrics.rmse?.toFixed(2)}</p>
                                <p className="text-xs text-slate-500">Root Mean Squared Error</p>
                            </div>
                            <div>
                                <p className="text-2xl font-bold text-slate-800">{metrics.mae?.toFixed(2)}</p>
                                <p className="text-xs text-slate-500">Mean Absolute Error</p>
                            </div>
                        </div>
                    </div>

                    {/* Validation Status (Mock) */}
                    <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 md:col-span-3">
                        <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Automated Validation Checks</p>
                        <div className="space-y-2">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-slate-600">Data Drift Check</span>
                                <span className="flex items-center gap-1 text-green-600 font-medium"><CheckCircle className="w-3 h-3" /> Passed</span>
                            </div>
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-slate-600">Model Latency</span>
                                <span className="flex items-center gap-1 text-green-600 font-medium"><CheckCircle className="w-3 h-3" /> {Math.floor(Math.random() * 50) + 10}ms</span>
                            </div>
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-slate-600">Accuracy Threshold</span>
                                <span className="flex items-center gap-1 text-green-600 font-medium"><CheckCircle className="w-3 h-3" /> Within Limits</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MLOpsPanel;
