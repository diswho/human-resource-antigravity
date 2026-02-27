import { useState, useEffect } from 'react';
import api from '../services/api';
import { Calendar, Clock, ChevronLeft, ChevronRight } from 'lucide-react';

interface AttendanceLog {
    id: number;
    timestamp: string;
    punch_type: string;
    terminal_id?: number;
    employee_id: number;
    employee_name?: string; // Optional if we join
}

const Attendance = () => {
    const [logs, setLogs] = useState<AttendanceLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [skip, setSkip] = useState(0);
    const limit = 20;

    const fetchLogs = async () => {
        setLoading(true);
        try {
            // For now, we fetch logs for a sample ID or the first employee we find
            // In a real app, this would be the logged-in employee's view or an HR view
            const response = await api.get('/attendance/1', { // Hardcoded 1 for demo
                params: { skip, limit }
            });
            setLogs(response.data);
        } catch (err) {
            console.error('Failed to fetch attendance logs');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLogs();
    }, [skip]);

    const formatDate = (dateStr: string) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
    };

    const formatTime = (dateStr: string) => {
        const date = new Date(dateStr);
        return date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Attendance History</h1>
                <p className="text-slate-500 dark:text-slate-400">View check-in and check-out logs tracking work hours.</p>
            </div>

            <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-premium border border-slate-200 dark:border-slate-800 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 dark:bg-slate-800/50 border-bottom border-slate-200 dark:border-slate-800">
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Time</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Type</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Terminal</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {loading ? (
                                <tr>
                                    <td colSpan={4} className="px-6 py-12 text-center text-slate-500 italic">Loading logs...</td>
                                </tr>
                            ) : logs.length === 0 ? (
                                <tr>
                                    <td colSpan={4} className="px-6 py-12 text-center text-slate-500 italic">No attendance records found.</td>
                                </tr>
                            ) : (
                                logs.map((log) => (
                                    <tr key={log.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                                        <td className="px-6 py-4 text-slate-900 dark:text-white flex items-center gap-3">
                                            <Calendar size={16} className="text-slate-400" />
                                            {formatDate(log.timestamp)}
                                        </td>
                                        <td className="px-6 py-4 font-mono text-sm text-slate-600 dark:text-slate-400">
                                            <div className="flex items-center gap-2">
                                                <Clock size={16} className="text-slate-400" />
                                                {formatTime(log.timestamp)}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${log.punch_type === '0'
                                                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                                                : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                                                }`}>
                                                {log.punch_type === '0' ? 'Check-In' : 'Check-Out'}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-slate-500 dark:text-slate-400 text-sm">
                                            Terminal {log.terminal_id || '#1'}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>

                <div className="p-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                    <p className="text-sm text-slate-500">Showing {logs.length} most recent records</p>
                    <div className="flex gap-2">
                        <button
                            disabled={skip === 0}
                            onClick={() => setSkip(Math.max(0, skip - limit))}
                            className="p-2 border border-slate-200 dark:border-slate-700 rounded-lg hover:bg-white dark:hover:bg-slate-800 disabled:opacity-50 transition-all"
                        >
                            <ChevronLeft size={20} />
                        </button>
                        <button
                            onClick={() => setSkip(skip + limit)}
                            className="p-2 border border-slate-200 dark:border-slate-700 rounded-lg hover:bg-white dark:hover:bg-slate-800 transition-all"
                        >
                            <ChevronRight size={20} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Attendance;
