import React from 'react';
import { Ticket, Clock, User } from 'lucide-react';

const TokenDisplay = ({ prediction }) => {
    if (!prediction) return null;

    return (
        <div className="bg-white p-6 rounded-lg shadow-md border border-green-100 mt-6 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4 text-green-700 flex items-center gap-2">
                <Ticket className="w-6 h-6" /> Token Generated
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-green-50 p-4 rounded-md">
                    <p className="text-sm text-green-600 font-medium">Token Number</p>
                    <p className="text-4xl font-bold text-green-800">{prediction.TokenNumber}</p>
                </div>

                <div className="bg-blue-50 p-4 rounded-md">
                    <p className="text-sm text-blue-600 font-medium flex items-center gap-1"><Clock className="w-3 h-3" /> Est. Wait Time</p>
                    <p className="text-2xl font-bold text-blue-800">{prediction.WaitTime_Minutes.toFixed(1)} mins</p>
                    <p className="text-xs text-blue-500 mt-1">Consult Time: {new Date(prediction.PredictedConsultTime).toLocaleTimeString()}</p>
                </div>

                <div className="bg-purple-50 p-4 rounded-md col-span-1 md:col-span-2">
                    <p className="text-sm text-purple-600 font-medium flex items-center gap-1"><User className="w-3 h-3" /> Assigned Doctor</p>
                    <p className="text-lg font-bold text-purple-800">{prediction.DoctorID}</p>
                </div>
            </div>
        </div>
    );
};

export default TokenDisplay;
