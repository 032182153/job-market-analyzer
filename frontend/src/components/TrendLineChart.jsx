import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const TrendLineChart = ({ data, isLoading, skills }) => {
  if (isLoading) {
    return <div className="glass-card h-[400px] animate-pulse" />;
  }

  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

  return (
    <div className="glass-card h-[450px]">
      <h3 className="text-xl font-bold mb-6 text-white">Skill Trends (Last 12 Months)</h3>
      <div className="h-[350px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="month" tick={{ fill: '#94a3b8' }} />
            <YAxis tick={{ fill: '#94a3b8' }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
              itemStyle={{ fontWeight: 'bold' }}
            />
            <Legend verticalAlign="top" height={36} />
            {skills.map((skill, index) => (
              <Line
                key={skill}
                type="monotone"
                dataKey={skill}
                stroke={colors[index % colors.length]}
                strokeWidth={3}
                dot={{ r: 4, fill: colors[index % colors.length] }}
                activeDot={{ r: 6 }}
                animationDuration={1500}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default TrendLineChart;
