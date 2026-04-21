import React from 'react';
import { Briefcase, Building2, Calendar, TrendingUp } from 'lucide-react';

const STAT_CONFIG = {
  totalJobs: {
    title: 'Total Jobs',
    icon: Briefcase,
    bg: 'bg-blue-500/10',
    text: 'text-blue-400'
  },
  companies: {
    title: 'Unique Companies',
    icon: Building2,
    bg: 'bg-purple-500/10',
    text: 'text-purple-400'
  },
  dateRange: {
    title: 'Date Range',
    icon: Calendar,
    bg: 'bg-emerald-500/10',
    text: 'text-emerald-400'
  },
  topRole: {
    title: 'Top Role',
    icon: TrendingUp,
    bg: 'bg-amber-500/10',
    text: 'text-amber-400'
  }
};

const StatCard = ({ value, type }) => {
  const config = STAT_CONFIG[type];
  if (!config) return null;
  
  const Icon = config.icon;

  return (
    <div className="glass-card flex items-center space-x-4">
      <div className={`p-3 rounded-xl ${config.bg} ${config.text}`}>
        <Icon size={24} />
      </div>
      <div>
        <p className="text-slate-400 text-sm font-medium">{config.title}</p>
        <p className="text-2xl font-bold text-white">{value}</p>
      </div>
    </div>
  );
};

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
        type="totalJobs"
        value={stats?.total_jobs?.toLocaleString()}
      />
      <StatCard
        type="companies"
        value={stats?.total_companies?.toLocaleString()}
      />
      <StatCard
        type="dateRange"
        value={stats?.date_range}
      />
      <StatCard
        type="topRole"
        value={stats?.top_role}
      />
    </div>
  );
};

export default StatsCards;
