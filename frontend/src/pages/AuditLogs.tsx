import { useState, useEffect } from 'react';
import api from '../services/api';
import { ChevronLeft, ChevronRight, Activity, Clock, User as UserIcon } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

interface AuditLog {
    id: number;
    user_id: number;
    user_email?: string;
    action: string;
    target_type: string;
    target_id: number;
    details: any;
    timestamp: string;
}

const AuditLogs = () => {
    const { user: currentUser } = useAuth();
    const [logs, setLogs] = useState<AuditLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [totalCount, setTotalCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const limit = 20;

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const skip = (currentPage - 1) * limit;
            const response = await api.get('/audit', {
                params: { skip, limit }
            });
            setLogs(response.data.data);
            setTotalCount(response.data.count);
        } catch (err) {
            console.error('Failed to fetch audit logs');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (currentUser?.role === 'admin') {
            fetchLogs();
        }
    }, [currentPage, currentUser]);

    const formatDetails = (details: any) => {
        if (!details) return '-';
        return (
            <div className="space-y-1">
                {Object.entries(details).map(([field, vals]: [string, any]) => (
                    <div key={field} className="text-xs">
                        <span className="font-semibold text-slate-700 dark:text-slate-300">{field}:</span>{' '}
                        <span className="text-red-500 line-through">{String(vals.old)}</span>{' '}
                        <span className="text-green-500">→ {String(vals.new)}</span>
                    </div>
                ))}
            </div>
        );
    };

    const totalPages = Math.ceil(totalCount / limit);

    if (currentUser?.role !== 'admin') {
        return (
            <div className="flex items-center justify-center h-[60vh]">
                <p className="text-slate-500">Access denied. Admin privileges required.</p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
                    <Activity className="text-blue-600" size={32} />
                    Audit Logs
                </h1>
                <p className="text-slate-500 dark:text-slate-400">
                    Track all system activities and data changes.
                </p>
            </div>

            <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-premium border border-slate-200 dark:border-slate-800 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 dark:bg-slate-800/50 border-bottom border-slate-200 dark:border-slate-800">
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Timestamp</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">User</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Action</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Target</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Changes</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {loading ? (
                                <tr>
                                    <td colSpan={5} className="px-6 py-12 text-center text-slate-500">
                                        <div className="flex flex-col items-center gap-2">
                                            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
                                            <span>Loading logs...</span>
                                        </div>
                                    </td>
                                </tr>
                            ) : logs.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="px-6 py-12 text-center text-slate-500 italic">No activity logs found.</td>
                                </tr>
                            ) : (
                                logs.map((log) => (
                                    <tr key={log.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                                        <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">
                                            <div className="flex items-center gap-2">
                                                <Clock size={14} className="text-slate-400" />
                                                {new Date(log.timestamp).toLocaleString()}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-slate-900 dark:text-white">
                                            <div className="flex items-center gap-2">
                                                <UserIcon size={14} className="text-slate-400" />
                                                {log.user_email || 'System'}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase ${log.action === 'create' ? 'bg-green-100 text-green-700' :
                                                log.action === 'update' ? 'bg-blue-100 text-blue-700' :
                                                    'bg-red-100 text-red-700'
                                                }`}>
                                                {log.action}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">
                                            {log.target_type} (#{log.target_id})
                                        </td>
                                        <td className="px-6 py-4">
                                            {formatDetails(log.details)}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Pagination */}
                {!loading && totalCount > limit && (
                    <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/30 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                        <div className="text-sm text-slate-500">
                            Showing {((currentPage - 1) * limit) + 1} to {Math.min(currentPage * limit, totalCount)} of {totalCount} logs
                        </div>
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                disabled={currentPage === 1}
                                className="p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-white disabled:opacity-50 transition-all"
                            >
                                <ChevronLeft size={20} />
                            </button>
                            <span className="text-sm font-semibold">{currentPage} / {totalPages}</span>
                            <button
                                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                                disabled={currentPage === totalPages}
                                className="p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-white disabled:opacity-50 transition-all"
                            >
                                <ChevronRight size={20} />
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AuditLogs;
