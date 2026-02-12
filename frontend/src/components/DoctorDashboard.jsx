import React from 'react';
import { Users, Clock } from 'lucide-react';

// Mock data for dashboard since we don't have a real backend for queue state yet
const mockDoctors = [
    { id: 'DOC_001', name: 'Dr. Smith', dept: 'Cardiology', queue: 5, avgWait: 15 },
    { id: 'DOC_002', name: 'Dr. Jones', dept: 'Orthopedics', queue: 3, avgWait: 10 },
    { id: 'DOC_003', name: 'Dr. Emily', dept: 'Pediatrics', queue: 8, avgWait: 25 },
    { id: 'DOC_004', name: 'Dr. Brow', dept: 'Dermatology', queue: 2, avgWait: 5 },
];

const DoctorDashboard = () => {
    return (
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 mt-8">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 flex items-center gap-2">
                <Users className="w-6 h-6 text-indigo-600" /> Doctor Load Dashboard
            </h2>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Doctor</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Queue Length</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Wait</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {mockDoctors.map((doc) => (
                            <tr key={doc.id}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{doc.name} <span className="text-gray-400 text-xs">({doc.id})</span></td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{doc.dept}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.queue}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 flex items-center gap-1">
                                    <Clock className="w-3 h-3" /> {doc.avgWait} min
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${doc.queue > 5 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                                        {doc.queue > 5 ? 'Busy' : 'Available'}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DoctorDashboard;
