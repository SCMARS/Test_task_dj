import type { Cat } from '@/types/cat';
import { PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

interface CatCardProps {
    cat: Cat;
    onEdit: (cat: Cat) => void;
    onDelete: (id: number) => void;
}

export function CatCard({ cat, onEdit, onDelete }: CatCardProps) {
    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9 }}
            whileHover={{ y: -5 }}
            className="group relative overflow-hidden rounded-2xl bg-white/5 p-6 backdrop-blur-lg border border-white/10 shadow-xl transition-all hover:shadow-2xl hover:bg-white/10"
        >
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 via-purple-500/5 to-pink-500/10 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

            <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                    <div>
                        <h3 className="text-xl font-bold text-white mb-1 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-indigo-400 group-hover:to-pink-400 transition-all">
                            {cat.name}
                        </h3>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                            {cat.breed}
                        </span>
                    </div>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        <button
                            onClick={() => onEdit(cat)}
                            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white transition-colors"
                            title="Update Salary"
                        >
                            <PencilIcon className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => onDelete(cat.id)}
                            className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300 transition-colors"
                            title="Remove Spy Cat"
                        >
                            <TrashIcon className="w-4 h-4" />
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mt-6">
                    <div className="bg-black/20 rounded-xl p-3">
                        <p className="text-xs text-gray-400 mb-1 uppercase tracking-wider">Experience</p>
                        <p className="text-lg font-semibold text-white">{cat.years_of_experience} Years</p>
                    </div>
                    <div className="bg-black/20 rounded-xl p-3">
                        <p className="text-xs text-gray-400 mb-1 uppercase tracking-wider">Salary</p>
                        <p className="text-lg font-semibold text-green-400">
                            ${cat.salary.toLocaleString()}
                        </p>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
