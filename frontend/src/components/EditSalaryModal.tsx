import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { updateCatSalary } from '@/lib/api';
import type { Cat } from '@/types/cat';

interface EditSalaryModalProps {
    cat: Cat | null;
    onClose: () => void;
    onSuccess: () => void;
}

export function EditSalaryModal({ cat, onClose, onSuccess }: EditSalaryModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    if (!cat) return null;

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setLoading(true);
        setError('');

        const formData = new FormData(e.currentTarget);
        const salary = Number(formData.get('salary'));

        try {
            await updateCatSalary(cat!.id, salary);
            onSuccess();
            onClose();
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={onClose}
                className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
            />
            <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-sm bg-[#1a1b26] border border-white/10 rounded-2xl p-6 shadow-2xl z-50"
            >
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold text-white">
                        Update Salary
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-full hover:bg-white/5 text-gray-400 hover:text-white transition-colors"
                    >
                        <XMarkIcon className="w-5 h-5" />
                    </button>
                </div>

                <p className="text-gray-400 mb-6">
                    Adjusting compensation for <span className="text-indigo-400 font-semibold">{cat.name}</span>
                </p>

                {error && (
                    <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-400 mb-1">New Salary ($)</label>
                        <input
                            name="salary"
                            type="number"
                            min="0"
                            required
                            defaultValue={cat.salary}
                            className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono text-lg"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-emerald-500/25"
                    >
                        {loading ? 'Updating...' : 'Confirm Raise'}
                    </button>
                </form>
            </motion.div>
        </AnimatePresence>
    );
}
