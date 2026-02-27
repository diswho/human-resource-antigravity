import { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, Edit2, X } from 'lucide-react';

interface Employee {
    id: number;
    emp_pin: string;
    firstname: string;
    lastname: string;
    lao_name?: string;
    bank_account?: string;
    gasoline_allowance: number;
    department_id?: number;
    position_id?: number;
}

const Employees = () => {
    const [employees, setEmployees] = useState<Employee[]>([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);
    const [editingEmp, setEditingEmp] = useState<Employee | null>(null);
    const [editData, setEditData] = useState({ lao_name: '', bank_account: '', gasoline_allowance: 0 });

    const fetchEmployees = async () => {
        setLoading(true);
        try {
            const response = await api.get('/employees', {
                params: { query: search, limit: 100 }
            });
            setEmployees(response.data);
        } catch (err) {
            console.error('Failed to fetch employees');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchEmployees();
        }, 500);
        return () => clearTimeout(timer);
    }, [search]);

    const handleEdit = (emp: Employee) => {
        setEditingEmp(emp);
        setEditData({
            lao_name: emp.lao_name || '',
            bank_account: emp.bank_account || '',
            gasoline_allowance: emp.gasoline_allowance || 0,
        });
    };

    const handleUpdate = async () => {
        if (!editingEmp) return;
        try {
            const response = await api.patch(`/employees/${editingEmp.id}`, editData);
            setEmployees(employees.map(e => e.id === editingEmp.id ? response.data : e));
            setEditingEmp(null);
        } catch (err) {
            alert('Failed to update employee');
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Employee Management</h1>
                    <p className="text-slate-500 dark:text-slate-400">View and manage extended employee records.</p>
                </div>

                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                    <input
                        type="text"
                        placeholder="Search by name, ID, or Lao name..."
                        className="pl-12 pr-4 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none w-full md:w-96 transition-all shadow-sm"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
            </div>

            <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-premium border border-slate-200 dark:border-slate-800 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 dark:bg-slate-800/50 border-bottom border-slate-200 dark:border-slate-800">
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">ID</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Full Name (EN)</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Lao Name</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Bank Account</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Gasoline</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {loading ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-12 text-center text-slate-500 italic">Loading employees...</td>
                                </tr>
                            ) : employees.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-12 text-center text-slate-500 italic">No employees found.</td>
                                </tr>
                            ) : (
                                employees.map((emp) => (
                                    <tr key={emp.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                                        <td className="px-6 py-4 font-mono text-sm text-slate-600 dark:text-slate-400">{emp.emp_pin}</td>
                                        <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">{emp.firstname} {emp.lastname}</td>
                                        <td className="px-6 py-4 text-slate-700 dark:text-slate-300">{emp.lao_name || '-'}</td>
                                        <td className="px-6 py-4 font-mono text-sm text-slate-600 dark:text-slate-400">{emp.bank_account || '-'}</td>
                                        <td className="px-6 py-4 text-slate-700 dark:text-slate-300">
                                            {emp.gasoline_allowance.toLocaleString()} LAK
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <button
                                                onClick={() => handleEdit(emp)}
                                                className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-all"
                                            >
                                                <Edit2 size={18} />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Edit Modal */}
            {editingEmp && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 backdrop-blur-sm p-4">
                    <div className="bg-white dark:bg-slate-900 w-full max-w-lg rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden animate-in fade-in zoom-in duration-200">
                        <div className="flex items-center justify-between p-6 border-b border-slate-100 dark:border-slate-800">
                            <h3 className="text-xl font-bold text-slate-900 dark:text-white">Edit Employee Info</h3>
                            <button onClick={() => setEditingEmp(null)} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
                                <X size={24} />
                            </button>
                        </div>

                        <div className="p-6 space-y-6">
                            <div className="bg-slate-50 dark:bg-slate-800/50 p-4 rounded-xl border border-slate-100 dark:border-slate-800">
                                <p className="text-sm font-semibold text-slate-900 dark:text-white">{editingEmp.firstname} {editingEmp.lastname}</p>
                                <p className="text-xs text-slate-500">ID: {editingEmp.emp_pin}</p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Lao Name</label>
                                <input
                                    type="text"
                                    value={editData.lao_name}
                                    onChange={(e) => setEditData({ ...editData, lao_name: e.target.value })}
                                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all dark:text-white"
                                    placeholder="ຊື່ ແລະ ນາມສະກຸນ"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Bank Account (BCEL)</label>
                                <input
                                    type="text"
                                    value={editData.bank_account}
                                    onChange={(e) => setEditData({ ...editData, bank_account: e.target.value })}
                                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all dark:text-white"
                                    placeholder="0572XXXXXXXXXXXX"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Gasoline Allowance (LAK)</label>
                                <input
                                    type="number"
                                    value={editData.gasoline_allowance}
                                    onChange={(e) => setEditData({ ...editData, gasoline_allowance: Number(e.target.value) })}
                                    className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all dark:text-white"
                                />
                            </div>
                        </div>

                        <div className="p-6 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-800 flex gap-4">
                            <button
                                onClick={() => setEditingEmp(null)}
                                className="flex-1 py-3 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-semibold rounded-xl hover:bg-white dark:hover:bg-slate-800 transition-all"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleUpdate}
                                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow-lg shadow-blue-500/20 transition-all"
                            >
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Employees;
