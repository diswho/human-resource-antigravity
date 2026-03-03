import { useState, useEffect } from 'react';
import api from '../services/api';
import { FileText, Clock, PlusCircle, MinusCircle, Wallet, Download } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

interface Payroll {
    id: number;
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
}

const PayrollSlip = () => {
    const { user: currentUser } = useAuth();
    const [slips, setSlips] = useState<Payroll[]>([]);
    const [selectedSlip, setSelectedSlip] = useState<Payroll | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchSlips = async () => {
        setLoading(true);
        try {
            const response = await api.get('/payroll/me');
            setSlips(response.data.data);
            if (response.data.data.length > 0) {
                setSelectedSlip(response.data.data[0]);
            }
        } catch (err) {
            console.error('Failed to fetch slips');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSlips();
    }, []);

    if (loading) return <div className="p-8 text-center">Loading your payroll slips...</div>;

    if (slips.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center h-[50vh] text-slate-500">
                <FileText size={48} className="mb-4 opacity-20" />
                <p>No payroll slips available yet.</p>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
                        <Wallet className="text-blue-600" size={32} />
                        My Payroll Slips
                    </h1>
                    <p className="text-slate-500 dark:text-slate-400">View and download your monthly compensation details.</p>
                </div>

                <select
                    className="px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl outline-none font-semibold"
                    onChange={(e) => setSelectedSlip(slips.find(s => s.id === Number(e.target.value)) || null)}
                    value={selectedSlip?.id}
                >
                    {slips.map(s => (
                        <option key={s.id} value={s.id}>Month {s.month}/{s.year}</option>
                    ))}
                </select>
            </div>

            {selectedSlip && (
                <div className="bg-white dark:bg-slate-900 rounded-3xl shadow-premium border border-slate-200 dark:border-slate-800 overflow-hidden">
                    {/* Header */}
                    <div className="p-8 bg-slate-50 dark:bg-slate-800/50 border-b border-slate-100 dark:border-slate-800 flex justify-between items-start">
                        <div>
                            <p className="text-blue-600 font-bold uppercase tracking-widest text-xs mb-2">Payroll Slip</p>
                            <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Month {selectedSlip.month}, {selectedSlip.year}</h2>
                            <p className="text-slate-500">{currentUser?.full_name}</p>
                        </div>
                        <button className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm font-semibold hover:bg-slate-50 transition-all">
                            <Download size={16} />
                            PDF
                        </button>
                    </div>

                    <div className="p-8 grid grid-cols-1 md:grid-cols-3 gap-8">
                        {/* Part A: Work Info */}
                        <div className="space-y-6">
                            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                                <Clock size={16} /> Part A: Work Info
                            </h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-800/30 rounded-xl">
                                    <span className="text-slate-600 dark:text-slate-400 text-sm">Working Days</span>
                                    <span className="font-bold">{selectedSlip.actual_work_days} / {selectedSlip.required_work_days}</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-800/30 rounded-xl">
                                    <span className="text-slate-600 dark:text-slate-400 text-sm">Late/Early (Mins)</span>
                                    <span className="font-bold text-orange-500">{selectedSlip.late_early_minutes}</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-800/30 rounded-xl">
                                    <span className="text-slate-600 dark:text-slate-400 text-sm">Overtime (Hours)</span>
                                    <span className="font-bold text-blue-500">{selectedSlip.ot_hours}</span>
                                </div>
                            </div>
                        </div>

                        {/* Part B: Earnings (+) */}
                        <div className="space-y-6">
                            <h3 className="text-sm font-bold text-green-600 uppercase tracking-wider flex items-center gap-2">
                                <PlusCircle size={16} /> Part B: Earnings
                            </h3>
                            <div className="space-y-3">
                                <div className="flex justify-between text-sm">
                                    <span className="text-slate-500">Base Salary Earned</span>
                                    <span className="font-semibold">{selectedSlip.base_salary_earned.toLocaleString()}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-slate-500">Gasoline Allowance</span>
                                    <span className="font-semibold">{selectedSlip.gasoline_allowance.toLocaleString()}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-slate-500">Bonuses / Other</span>
                                    <span className="font-semibold">{selectedSlip.bonus_other.toLocaleString()}</span>
                                </div>
                                <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-between">
                                    <span className="font-bold text-slate-900 dark:text-white">Total Income</span>
                                    <span className="font-bold text-green-600">{selectedSlip.total_earnings.toLocaleString()}</span>
                                </div>
                            </div>
                        </div>

                        {/* Part C: Deductions (-) */}
                        <div className="space-y-6">
                            <h3 className="text-sm font-bold text-red-500 uppercase tracking-wider flex items-center gap-2">
                                <MinusCircle size={16} /> Part C: Deductions
                            </h3>
                            <div className="space-y-3">
                                <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                                    <span>Social Insurance</span>
                                    <span>({selectedSlip.social_insurance.toLocaleString()})</span>
                                </div>
                                <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                                    <span>Discipline / Rules</span>
                                    <span>({(selectedSlip.discipline_late + selectedSlip.discipline_rules + selectedSlip.discipline_cashier).toLocaleString()})</span>
                                </div>
                                <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                                    <span>Utilities (E/W)</span>
                                    <span>({(selectedSlip.utility_electric + selectedSlip.utility_water).toLocaleString()})</span>
                                </div>
                                <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                                    <span>Advance Payment</span>
                                    <span>({selectedSlip.advance_payment.toLocaleString()})</span>
                                </div>
                                <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                                    <span>Security Deposit</span>
                                    <span>({selectedSlip.security_deposit.toLocaleString()})</span>
                                </div>
                                <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-between">
                                    <span className="font-bold text-slate-900 dark:text-white">Total Deductions</span>
                                    <span className="font-bold text-red-500">{selectedSlip.total_deductions.toLocaleString()}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Footer */}
                    <div className="p-8 bg-blue-600 flex flex-col md:flex-row items-center justify-between text-white rounded-b-3xl">
                        <div className="mb-4 md:mb-0">
                            <p className="text-blue-100 text-sm font-semibold uppercase tracking-wider mb-1">Thực Lĩnh (Net Salary)</p>
                            <h4 className="text-4xl font-black">{selectedSlip.net_salary.toLocaleString()} <span className="text-xl font-normal">LAK</span></h4>
                        </div>
                        <div className="text-right">
                            <p className="text-blue-100 text-xs italic">Transferring to: {currentUser?.bank_account || 'Not specified'}</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PayrollSlip;
