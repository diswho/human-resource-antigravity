import { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, Edit2, X, ChevronLeft, ChevronRight, Filter } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

interface Employee {
    id: number;
    emp_pin: string;
    firstname: string;
    lastname: string;
    email?: string;
    lao_name?: string;
    bank_account?: string;
    gasoline_allowance: number;
    department_id?: number;
    position_id?: number;
}

interface Department {
    id: number;
    name: string;
    parent_id?: number;
}

interface DepartmentNode extends Department {
    children: DepartmentNode[];
}

const Employees = () => {
    const { user: currentUser } = useAuth();
    const [employees, setEmployees] = useState<Employee[]>([]);
    const [departments, setDepartments] = useState<Department[]>([]);
    const [search, setSearch] = useState('');
    const [selectedDept, setSelectedDept] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [totalCount, setTotalCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const limit = 10;

    const [editingEmp, setEditingEmp] = useState<Employee | null>(null);
    const [editData, setEditData] = useState({ lao_name: '', bank_account: '', gasoline_allowance: 0 });

    const fetchDepartments = async () => {
        if (currentUser?.role === 'employee') return;
        try {
            const response = await api.get('/employees/departments');
            setDepartments(response.data.data);
        } catch (err) {
            console.error('Failed to fetch departments');
        }
    };

    const buildDeptTree = (items: Department[], parentId: number | null = null): DepartmentNode[] => {
        return items
            .filter(item => (parentId === null ? !item.parent_id : item.parent_id === parentId))
            .map(item => ({
                ...item,
                children: buildDeptTree(items, item.id)
            }));
    };

    const renderDeptOptions = (nodes: DepartmentNode[], level: number = 0): JSX.Element[] => {
        return nodes.flatMap(node => [
            <option key={node.id} value={node.id}>
                {'\u00A0'.repeat(level * 4)}{level > 0 ? '↳ ' : ''}{node.name}
            </option>,
            ...renderDeptOptions(node.children, level + 1)
        ]);
    };

    const deptTree = buildDeptTree(departments);

    const fetchEmployees = async () => {
        setLoading(true);
        try {
            const skip = (currentPage - 1) * limit;
            const params: any = {
                skip: skip,
                limit: limit
            };
            if (currentUser?.role !== 'employee') {
                if (search) params.query = search;
                if (selectedDept) params.dept_id = selectedDept;
            }

            const response = await api.get('/employees', { params });
            setEmployees(response.data.data);
            setTotalCount(response.data.count);
        } catch (err) {
            console.error('Failed to fetch employees');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDepartments();
    }, [currentUser]);

    useEffect(() => {
        const timer = setTimeout(() => {
            setCurrentPage(1); // Reset to first page on search
            fetchEmployees();
        }, 500);
        return () => clearTimeout(timer);
    }, [search, selectedDept]);

    useEffect(() => {
        fetchEmployees();
    }, [currentPage]);

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

    const totalPages = Math.ceil(totalCount / limit);

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                        {currentUser?.role === 'employee' ? 'My Information' : 'Employee Management'}
                    </h1>
                    <p className="text-slate-500 dark:text-slate-400">
                        {currentUser?.role === 'employee' ? 'View and update your personal records.' : 'View and manage extended employee records.'}
                    </p>
                </div>

                {currentUser?.role !== 'employee' && (
                    <div className="flex flex-col sm:flex-row gap-3">
                        <div className="relative">
                            <Filter className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                            <select
                                value={selectedDept}
                                onChange={(e) => setSelectedDept(e.target.value)}
                                className="pl-12 pr-10 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none w-full sm:w-56 appearance-none transition-all shadow-sm text-slate-700 dark:text-slate-300"
                            >
                                <option value="">All Departments</option>
                                {renderDeptOptions(deptTree)}
                            </select>
                        </div>

                        <div className="relative">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                            <input
                                type="text"
                                placeholder="Search employees..."
                                className="pl-12 pr-4 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none w-full sm:w-80 transition-all shadow-sm"
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                            />
                        </div>
                    </div>
                )}
            </div>

            <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-premium border border-slate-200 dark:border-slate-800 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 dark:bg-slate-800/50 border-bottom border-slate-200 dark:border-slate-800">
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">ID</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Full Name (EN)</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Lao Name</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Email</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Bank Account</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Gasoline</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {loading ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-12 text-center text-slate-500 italic">
                                        <div className="flex flex-col items-center gap-2">
                                            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
                                            <span>Loading...</span>
                                        </div>
                                    </td>
                                </tr>
                            ) : employees.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-12 text-center text-slate-500 italic">No records found.</td>
                                </tr>
                            ) : (
                                employees.map((emp) => (
                                    <tr key={emp.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                                        <td className="px-6 py-4 font-mono text-sm text-slate-600 dark:text-slate-400">{emp.emp_pin}</td>
                                        <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">{emp.firstname} {emp.lastname}</td>
                                        <td className="px-6 py-4 text-slate-700 dark:text-slate-300">{emp.lao_name || '-'}</td>
                                        <td className="px-6 py-4 text-slate-600 dark:text-slate-400 text-sm">{emp.email || '-'}</td>
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

                {/* Pagination Controls */}
                {!loading && totalCount > limit && (
                    <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/30 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                        <div className="text-sm text-slate-500 dark:text-slate-400">
                            Showing <span className="font-semibold text-slate-900 dark:text-white">{((currentPage - 1) * limit) + 1}</span> to <span className="font-semibold text-slate-900 dark:text-white">{Math.min(currentPage * limit, totalCount)}</span> of <span className="font-semibold text-slate-900 dark:text-white">{totalCount}</span> results
                        </div>

                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                disabled={currentPage === 1}
                                className="p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-white dark:hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                            >
                                <ChevronLeft size={20} className="text-slate-600 dark:text-slate-400" />
                            </button>

                            <div className="flex items-center gap-1 mx-2">
                                <span className="text-sm text-slate-500">Page</span>
                                <span className="text-sm font-bold text-slate-900 dark:text-white">{currentPage}</span>
                                <span className="text-sm text-slate-500">of {totalPages}</span>
                            </div>

                            <button
                                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                                disabled={currentPage === totalPages}
                                className="p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-white dark:hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                            >
                                <ChevronRight size={20} className="text-slate-600 dark:text-slate-400" />
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* Edit Modal */}
            {editingEmp && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 backdrop-blur-sm p-4">
                    <div className="bg-white dark:bg-slate-900 w-full max-w-lg rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden animate-in fade-in zoom-in duration-200">
                        <div className="flex items-center justify-between p-6 border-b border-slate-100 dark:border-slate-800">
                            <h3 className="text-xl font-bold text-slate-900 dark:text-white">Edit Information</h3>
                            <button onClick={() => setEditingEmp(null)} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
                                <X size={24} />
                            </button>
                        </div>

                        <div className="p-6 space-y-6">
                            <div className="bg-slate-50 dark:bg-slate-800/50 p-4 rounded-xl border border-slate-100 dark:border-slate-800">
                                <p className="text-sm font-semibold text-slate-900 dark:text-white">{editingEmp.firstname} {editingEmp.lastname}</p>
                                <div className="flex justify-between items-center mt-1">
                                    <p className="text-xs text-slate-500">ID: {editingEmp.emp_pin}</p>
                                    <p className="text-xs text-blue-500 font-medium">{editingEmp.email || ''}</p>
                                </div>
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

                            {currentUser?.role !== 'employee' && (
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Gasoline Allowance (LAK)</label>
                                    <input
                                        type="number"
                                        value={editData.gasoline_allowance}
                                        onChange={(e) => setEditData({ ...editData, gasoline_allowance: Number(e.target.value) })}
                                        className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all dark:text-white"
                                    />
                                </div>
                            )}
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
