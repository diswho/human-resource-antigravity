import { useAuth } from '../hooks/useAuth';
import { Users, Clock, AlertCircle, CheckCircle } from 'lucide-react';

const Dashboard = () => {
    const { user } = useAuth();

    const stats = [
        { label: 'Total Employees', value: '841', icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
        { label: 'Today Attendance', value: '782', icon: Clock, icon_color: 'text-green-600', bg: 'bg-green-100' },
        { label: 'Late Entries', value: '12', icon: AlertCircle, icon_color: 'text-amber-600', bg: 'bg-amber-100' },
        { label: 'On Leave', value: '5', icon: CheckCircle, icon_color: 'text-purple-600', bg: 'bg-purple-100' },
    ];

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Dashboard Overview</h1>
                <p className="text-slate-500 dark:text-slate-400">Welcome back, {user?.full_name || user?.email}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, i) => (
                    <div key={i} className="bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-premium border border-slate-200 dark:border-slate-800">
                        <div className="flex items-center justify-between mb-4">
                            <div className={`p-3 rounded-xl ${stat.bg} ${stat.icon_color || stat.color}`}>
                                <stat.icon size={24} />
                            </div>
                        </div>
                        <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{stat.label}</p>
                        <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{stat.value}</p>
                    </div>
                ))}
            </div>

            <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-premium border border-slate-200 dark:border-slate-800 p-8">
                <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">Recent Activity</h2>
                <div className="space-y-4">
                    <p className="text-slate-500 dark:text-slate-400 italic">No recent activities to show.</p>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
