import { useState, useEffect } from 'react';
import api from '../services/api';
import { Banknote, Calculator, ChevronLeft, ChevronRight, Edit2, Search } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

interface Payroll {
    id: number;
    employee_id: number;
    employee_name?: string;
    month: number;
    year: number;
    actual_work_days: number;
    required_work_days: number;
    late_early_minutes: number;
    ot_hours: number;
    base_salary_earned: number;
    gasoline_allowance: number;
    bonus_other: number;
    social_insurance: number;
    discipline_late: number;
    discipline_rules: number;
    discipline_cashier: number;
    utility_electric: number;
    utility_water: number;
    advance_payment: number;
    security_deposit: number;
    total_earnings: number;
    total_deductions: number;
    net_salary: number;
    status: string;
}

const PayrollPage = () => {
    const { user: currentUser } = useAuth();
    const [payrolls, setPayrolls] = useState<Payroll[]>([]);
    const [loading, setLoading] = useState(true);
    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());
    const [calculating, setCalculating] = useState(false);

    const fetchPayrolls = async () => {
        setLoading(true);
        try {
            const response = await api.get('/payroll', {
                params: { month, year }
            });
            setPayrolls(response.data.data);
        } catch (err) {
            console.error('Failed to fetch payrolls');
        } finally {
            setLoading(false);
        }
    };

    const handleCalculate = async () => {
        setCalculating(true);
        try {
            await api.post('/payroll/calculate', null, {
                params: { month, year }
            });
            fetchPayrolls();
        } catch (err) {
            console.error('Calculation failed');
        } finally {
            setCalculating(false);
        }
    };

    useEffect(() => {
        if (currentUser?.role === 'hr' || currentUser?.role === 'admin') {
            fetchPayrolls();
        }
    }, [month, year, currentUser]);

    if (currentUser?.role !== 'hr' && currentUser?.role !== 'admin') {
        return <div className="p-8 text-center text-slate-500">Access denied.</div>;
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
                        <Banknote className="text-green-600" size={32} />
                        Payroll Management
                    </h1>
                    <p className="text-slate-500 dark:text-slate-400">Calculate and manage monthly salaries.</p>
                </div>

                <div className="flex items-center gap-3">
                    <select
                        value={month}
                        onChange={(e) => setMonth(Number(e.target.value))}
                        className="px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl outline-none"
                    >
                        {Array.from({ length: 12 }, (_, i) => (
                            <option key={i + 1} value={i + 1}>Month {i + 1}</option>
                        ))}
                    </select>
                    <select
                        value={year}
                        onChange={(e) => setYear(Number(e.target.value))}
                        className="px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl outline-none"
                    >
                        {[2024, 2025, 2026].map(y => (
                            <option key={y} value={y}>{y}</option>
                        ))}
                    </select>
                    <button
                        onClick={handleCalculate}
                        disabled={calculating}
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-xl font-semibold shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50"
                    >
                        <Calculator size={18} />
                        {calculating ? 'Calculating...' : 'Calculate All'}
                    </button>
                </div>
            </div>

            <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-premium border border-slate-200 dark:border-slate-800 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800">
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Employee</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase text-center">Days</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase text-right">Income</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase text-right">Deductions</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase text-right">Net Salary</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase text-center">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {loading ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-500">Loading payroll data...</td></tr>
                            ) : payrolls.length === 0 ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-500">No payrolls calculated for this period.</td></tr>
                            ) : (
                                payrolls.map((p) => (
                                    <tr key={p.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30">
                                        <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">{p.employee_name}</td>
                                        <td className="px-6 py-4 text-center">{p.actual_work_days}/{p.required_work_days}</td>
                                        <td className="px-6 py-4 text-right text-green-600 font-semibold">{p.total_earnings.toLocaleString()} LAK</td>
                                        <td className="px-6 py-4 text-right text-red-500 font-semibold">{p.total_deductions.toLocaleString()} LAK</td>
                                        <td className="px-6 py-4 text-right">
                                            <span className="bg-blue-50 dark:bg-blue-900/20 px-3 py-1 rounded-full text-blue-600 dark:text-blue-400 font-bold">
                                                {p.net_salary.toLocaleString()} LAK
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <button className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
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
        </div>
    );
};

export default PayrollPage;
