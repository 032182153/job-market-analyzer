import React from 'react';
import { Briefcase, Building2, Calendar, TrendingUp } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, color }) => (
  <div className="glass-card flex items-center space-x-4">
    <div className={`p-3 rounded-xl bg-${color}/10 text-${color}`}>
      <Icon size={24} />
    </div>
    <div>
      <p className="text-slate-400 text-sm font-medium">{title}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
    </div>
  </div>
);

const StatsCards = ({ stats, isLoading }) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="glass-card h-24 animate-pulse bg-white/5" />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard 
        title="Total Jobs" 
        value={stats?.total_jobs?.toLocaleString()} 
        icon={Briefcase} 
        color="blue-500" 
      />
      <StatCard 
        title="Unique Companies" 
        value={stats?.total_companies?.toLocaleString()} 
        icon={Building2} 
        color="purple-500" 
      />
      <StatCard 
        title="Date Range" 
        value={stats?.date_range} 
        icon={Calendar} 
        color="emerald-500" 
      />
      <StatCard 
        title="Top Role" 
        value={stats?.top_role} 
        icon={TrendingUp} 
        color="amber-500" 
      />
    </div>
  );
};

export default StatsCards;
