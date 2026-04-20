import React from 'react';
import { ExternalLink, MapPin, Building, Banknote } from 'lucide-react';

const JobsTable = ({ jobs, isLoading, page, onPageChange }) => {
  if (isLoading) {
    return <div className="glass-card h-[600px] animate-pulse" />;
  }

  return (
    <div className="glass-card">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-white">Latest Job Listings</h3>
        <div className="flex space-x-2">
          <button 
            disabled={page === 1}
            onClick={() => onPageChange(page - 1)}
            className="px-3 py-1 bg-slate-800 disabled:opacity-50 rounded hover:bg-slate-700 transition"
          >
            Prev
          </button>
          <span className="px-3 py-1 bg-slate-900 border border-slate-700 rounded text-slate-400">
            Page {page}
          </span>
          <button 
            onClick={() => onPageChange(page + 1)}
            className="px-3 py-1 bg-slate-800 rounded hover:bg-slate-700 transition"
          >
            Next
          </button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 text-sm">
              <th className="pb-4 font-medium uppercase tracking-wider">Job Details</th>
              <th className="pb-4 font-medium uppercase tracking-wider">Location</th>
              <th className="pb-4 font-medium uppercase tracking-wider">Salary</th>
              <th className="pb-4 font-medium uppercase tracking-wider">Skills</th>
              <th className="pb-4 font-medium uppercase tracking-wider text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {jobs?.map((job) => (
              <tr key={job.id} className="group hover:bg-white/[0.02]">
                <td className="py-4">
                  <p className="font-bold text-white group-hover:text-primary transition">{job.title}</p>
                  <div className="flex items-center text-sm text-slate-400 mt-1">
                    <Building size={14} className="mr-1" /> {job.company}
                  </div>
                </td>
                <td className="py-4 text-sm text-slate-400">
                  <div className="flex items-center">
                    <MapPin size={14} className="mr-1" /> {job.location || 'Remote'}
                  </div>
                </td>
                <td className="py-4 text-sm text-slate-300">
                  {job.salary_min ? (
                    <div className="flex items-center">
                      <Banknote size={14} className="mr-1 text-accent" />
                      ${(job.salary_min/1000).toFixed(0)}k - ${(job.salary_max/1000).toFixed(0)}k
                    </div>
                  ) : (
                    <span className="text-slate-600">N/A</span>
                  )}
                </td>
                <td className="py-4">
                  <div className="flex flex-wrap gap-1">
                    {job.skills?.slice(0, 3).map(skill => (
                      <span key={skill.id} className="badge bg-primary/10 text-primary border border-primary/20">
                        {skill.name}
                      </span>
                    ))}
                    {job.skills?.length > 3 && (
                      <span className="text-[10px] text-slate-500">+{job.skills.length - 3}</span>
                    )}
                  </div>
                </td>
                <td className="py-4 text-right">
                  <a 
                    href={job.source_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium transition"
                  >
                    View <ExternalLink size={12} className="ml-1.5" />
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default JobsTable;
