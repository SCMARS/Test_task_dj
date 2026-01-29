'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PlusIcon } from '@heroicons/react/24/solid';
import { getCats, deleteCat } from '@/lib/api';
import { CatCard } from '@/components/CatCard';
import { AddCatModal } from '@/components/AddCatModal';
import { EditSalaryModal } from '@/components/EditSalaryModal';
import type { Cat } from '@/types/cat';

export default function Home() {
  const [cats, setCats] = useState<Cat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [editingCat, setEditingCat] = useState<Cat | null>(null);

  async function fetchCats() {
    try {
      const data = await getCats();
      setCats(data);
      setError('');
    } catch (err) {
      setError('Failed to load spy cats. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchCats();
  }, []);

  async function handleDelete(id: number) {
    if (!confirm('Are you sure you want to retire this agent? This action cannot be undone.')) return;

    try {
      await deleteCat(id);
      setCats(cats.filter(cat => cat.id !== id));
    } catch (err) {
      alert('Failed to delete cat');
    }
  }

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-16 max-w-7xl mx-auto pt-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-6">
        <div className="-mt-2">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl font-black mb-2 bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent tracking-tight"
          >
            Spy Cat Agency
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="text-gray-400 text-lg"
          >
            Top Secret Personnel Management
          </motion.p>
        </div>

        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setIsAddModalOpen(true)}
          className="group flex items-center gap-2 bg-white text-black px-6 py-3 rounded-xl font-bold hover:bg-gray-100 transition-all shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:shadow-[0_0_30px_rgba(255,255,255,0.5)]"
        >
          <PlusIcon className="w-5 h-5 transition-transform group-hover:rotate-90" />
          Recruit New Agent
        </motion.button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl mb-8">
          {error}
        </div>
      )}

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 bg-white/5 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : (
        <motion.div
          layout
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          <AnimatePresence>
            {cats.map((cat) => (
              <CatCard
                key={cat.id}
                cat={cat}
                onEdit={setEditingCat}
                onDelete={handleDelete}
              />
            ))}
          </AnimatePresence>
        </motion.div>
      )}

      {!loading && cats.length === 0 && !error && (
        <div className="text-center py-20">
          <p className="text-gray-500 text-xl font-medium">No agents active. Start recruiting!</p>
        </div>
      )}

      <AddCatModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onSuccess={fetchCats}
      />

      <EditSalaryModal
        cat={editingCat}
        onClose={() => setEditingCat(null)}
        onSuccess={fetchCats}
      />
    </main>
  );
}
