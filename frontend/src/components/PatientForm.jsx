import React, { useState } from 'react';
import { predictWaitTime } from '../api';
import { Loader2 } from 'lucide-react';

const PatientForm = ({ onPrediction }) => {
    const [formData, setFormData] = useState({
        Department: 'Cardiology',
        PriorityFlag: 0,
        ScheduledTime: '',
        DoctorID: '' // Optional
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const departments = ['Cardiology', 'Orthopedics', 'Dermatology', 'Pediatrics', 'Neurology'];

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            // Format scheduled time to ISO string if needed, but backend expects datetime
            // Let's assume user inputs local time and we send it.
            // Need valid ISO format for Pydantic: YYYY-MM-DDTHH:MM:SS
            const scheduledTime = formData.ScheduledTime ? new Date(formData.ScheduledTime).toISOString() : new Date().toISOString();

            const payload = {
                ...formData,
                ScheduledTime: scheduledTime,
                PriorityFlag: parseInt(formData.PriorityFlag)
            };

            const result = await predictWaitTime(payload);
            onPrediction(result);
        } catch (err) {
            setError('Failed to get prediction. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">New Patient Token</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Department</label>
                    <select
                        name="Department"
                        value={formData.Department}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    >
                        {departments.map(dept => (
                            <option key={dept} value={dept}>{dept}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Priority (0=Normal, 1=High)</label>
                    <select
                        name="PriorityFlag"
                        value={formData.PriorityFlag}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    >
                        <option value={0}>Normal</option>
                        <option value={1}>High Priority</option>
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Scheduled Time (Optional)</label>
                    <input
                        type="datetime-local"
                        name="ScheduledTime"
                        value={formData.ScheduledTime}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    />
                    <p className="text-xs text-gray-500 mt-1">Leave blank for current time</p>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Doctor Preference (Optional)</label>
                    <input
                        type="text"
                        name="DoctorID"
                        value={formData.DoctorID}
                        onChange={handleChange}
                        placeholder="e.g. DOC_001"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    />
                </div>

                {error && <p className="text-red-500 text-sm">{error}</p>}

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    {loading ? <Loader2 className="animate-spin h-5 w-5" /> : 'Generate Token'}
                </button>
            </form>
        </div>
    );
};

export default PatientForm;
