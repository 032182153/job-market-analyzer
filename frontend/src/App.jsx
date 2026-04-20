import React, { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, MapPin, Calendar, LayoutDashboard } from 'lucide-react';
import * as api from './api';

import StatsCards from './components/StatsCards';
import SkillsBarChart from './components/SkillsBarChart';
import TrendLineChart from './components/TrendLineChart';
import CooccurrenceHeatmap from './components/CooccurrenceHeatmap';
import JobsTable from './components/JobsTable';

function App() {
  const [filters, setFilters] = useState({
    role: '',
    location: '',
    days: 30
  });
  
  const [selectedSkills, setSelectedSkills] = useState(['Python', 'JavaScript']);
  const [jobsPage, setJobsPage] = useState(1);

  // Queries
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: api.fetchStats
  });

  const { data: trending, isLoading: trendingLoading } = useQuery({
    queryKey: ['trending', filters],
    queryFn: () => api.fetchTrendingSkills(filters)
  });

  const { data: cooccurrence, isLoading: cooccurrenceLoading } = useQuery({
    queryKey: ['cooccurrence'],
    queryFn: api.fetchCooccurrence
  });

  const { data: jobs, isLoading: jobsLoading } = useQuery({
    queryKey: ['jobs', filters, jobsPage],
    queryFn: () => api.fetchJobs({ ...filters, page: jobsPage })
  });

  // Fetch trend data for multiple skills
  const trendsQueries = useQuery({
    queryKey: ['trends', selectedSkills, filters.role, filters.location],
    queryFn: async () => {
      const results = await Promise.all(
        selectedSkills.map(skill => 
          api.fetchSkillTrend({ skill, role: filters.role, location: filters.location })
        )
      );
      
      // Merge results into recharts format
      const monthMap = {};
      results.forEach((skillData, idx) => {
        const skillName = selectedSkills[idx];
        skillData.forEach(d => {
          if (!monthMap[d.month]) monthMap[d.month] = { month: d.month };
          monthMap[d.month][skillName] = d.count;
        });
      });
      return Object.values(monthMap).sort((a, b) => a.month.localeCompare(b.month));
    },
    enabled: selectedSkills.length > 0
  });

  const toggleSkill = (skill) => {
    if (selectedSkills.includes(skill)) {
      setSelectedSkills(prev => prev.filter(s => s !== skill));
    } else if (selectedSkills.length < 4) {
      setSelectedSkills(prev => [...prev, skill]);
    }
  };

  return (
    <div className="min-h-screen pb-12">
      {/* Header */}
      <nav className="border-b border-white/10 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-3">
              <div className="bg-primary p-2 rounded-lg">
                <LayoutDashboard className="text-white" size={24} />
              </div>
              <h1 className="text-2xl font-black bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                SKILLTREND
              </h1>
            </div>
            <div className="hidden md:flex items-center text-slate-400 text-sm font-medium">
              Real-time Market Insights
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 space-y-8">
        
        {/* Filter Bar */}
        <div className="glass-card grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase flex items-center">
              <Search size={12} className="mr-1" /> Search Role
            </label>
            <input 
              type="text" 
              placeholder="e.g. Backend Engineer"
              className="w-full filter-input"
              value={filters.role}
              onChange={(e) => setFilters(f => ({ ...f, role: e.target.value }))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase flex items-center">
              <MapPin size={12} className="mr-1" /> Location
            </label>
            <select 
              className="w-full filter-input appearance-none"
              value={filters.location}
              onChange={(e) => setFilters(f => ({ ...f, location: e.target.value }))}
            >
              <option value="">Global</option>
              <option value="Remote">Remote</option>
              <option value="USA">USA</option>
              <option value="UK">UK</option>
              <option value="Europe">Europe</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase flex items-center">
              <Calendar size={12} className="mr-1" /> Date Range
            </label>
            <select 
              className="w-full filter-input appearance-none"
              value={filters.days}
              onChange={(e) => setFilters(f => ({ ...f, days: parseInt(e.target.value) }))}
            >
              <option value={30}>Last 30 Days</option>
              <option value={60}>Last 60 Days</option>
              <option value={90}>Last 90 Days</option>
              <option value={180}>Last 180 Days</option>
            </select>
          </div>
          <button 
            onClick={() => setFilters({ role: '', location: '', days: 30 })}
            className="w-full py-2.5 text-slate-400 hover:text-white text-sm font-medium transition"
          >
            Clear All Filters
          </button>
        </div>

        {/* Stats Cards */}
        <StatsCards stats={stats} isLoading={statsLoading} />

        {/* Top Section Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <SkillsBarChart 
            data={trending || []} 
            isLoading={trendingLoading} 
            onSkillClick={toggleSkill} 
          />
          <TrendLineChart 
            data={trendsQueries.data || []} 
            isLoading={trendsQueries.isLoading} 
            skills={selectedSkills} 
          />
        </div>

        {/* Co-occurrence Heatmap */}
        <CooccurrenceHeatmap data={cooccurrence || []} isLoading={cooccurrenceLoading} />

        {/* Jobs Table */}
        <JobsTable 
          jobs={jobs} 
          isLoading={jobsLoading} 
          page={jobsPage} 
          onPageChange={setJobsPage} 
        />
      </main>

      {/* Footer */}
      <footer className="mt-20 border-t border-white/5 py-12 text-center text-slate-500 text-sm">
        <p>&copy; 2026 SkillTrend Analyzer. Data refreshed from API every 24h.</p>
      </footer>
    </div>
  );
}

export default App;
