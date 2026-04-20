import React from 'react';

const CooccurrenceHeatmap = ({ data, isLoading }) => {
  if (isLoading) {
    return <div className="glass-card h-[400px] animate-pulse" />;
  }

  // Extract top 15 skills for axes
  const skillsSet = new Set();
  data.forEach(item => {
    skillsSet.add(item.skill_a);
    skillsSet.add(item.skill_b);
  });
  const skills = Array.from(skillsSet).slice(0, 15);

  const getIntensity = (s1, s2) => {
    const match = data.find(
      d => (d.skill_a === s1 && d.skill_b === s2) || (d.skill_a === s2 && d.skill_b === s1)
    );
    return match ? match.count : 0;
  };

  const maxCount = Math.max(...data.map(d => d.count), 1);

  return (
    <div className="glass-card">
      <h3 className="text-xl font-bold mb-6 text-white">Skill Co-occurrence Heatmap</h3>
      <div className="overflow-x-auto">
        <div className="min-w-[600px]">
          <div className="flex">
            <div className="w-24 h-10"></div>
            {skills.map(s => (
              <div key={s} className="w-10 h-10 flex items-center justify-center -rotate-45 text-[10px] text-slate-400">
                {s}
              </div>
            ))}
          </div>
          {skills.map(s1 => (
            <div key={s1} className="flex">
              <div className="w-24 h-10 flex items-center pr-2 text-xs text-slate-400 justify-end">
                {s1}
              </div>
              {skills.map(s2 => {
                const count = getIntensity(s1, s2);
                const opacity = s1 === s2 ? 0.05 : count / maxCount;
                return (
                  <div
                    key={`${s1}-${s2}`}
                    className="w-10 h-10 border border-slate-900 flex items-center justify-center group relative"
                    style={{ backgroundColor: `rgba(59, 130, 246, ${Math.max(0.05, opacity)})` }}
                  >
                    {count > 0 && s1 !== s2 && (
                      <span className="hidden group-hover:block absolute z-10 bottom-full bg-slate-800 text-white text-[10px] rounded px-1 py-0.5">
                        {count}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CooccurrenceHeatmap;
