'use client';

import { useData } from './lib/useData';
import { formatPrice, timeAgo, getCompBadgeClass, getPersonaIcon } from './lib/types';
import {
  Building2, Cpu, TrendingUp, AlertTriangle,
  CheckCircle2, XCircle, Clock, RefreshCw, ArrowUpRight
} from 'lucide-react';
import Link from 'next/link';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area
} from 'recharts';

export default function Dashboard() {
  const { data, loading, refresh } = useData(8000);

  if (loading || !data) {
    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 32 }}>
          <div>
            <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 4 }}>Dashboard</h1>
            <p style={{ color: 'var(--color-text-muted)', fontSize: 14 }}>Loading intelligence data...</p>
          </div>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20 }}>
          {[1, 2, 3, 4].map(i => <div key={`skeleton-${i}`} className="skeleton" style={{ height: 140, borderRadius: 16 }} />)}
        </div>
      </div>
    );
  }

  const { properties, execStats, recentExecs } = data;
  const totalProps = properties.length;
  const aiProcessed = properties.filter(p => p.ai_processed === true || p.ai_processed === 't' || p.ai_processed === 'true').length;
  const pending = totalProps - aiProcessed;
  const successExecs = execStats.find(e => e.status === 'success');
  const errorExecs = execStats.find(e => e.status === 'error');
  const successCount = parseInt(successExecs?.count || '0');
  const errorCount = parseInt(errorExecs?.count || '0');
  const totalExecs = successCount + errorCount;
  const successRate = totalExecs > 0 ? ((successCount / totalExecs) * 100).toFixed(1) : '0';

  // Parish distribution for bar chart
  const parishMap: Record<string, number> = {};
  properties.forEach(p => {
    const parish = p.parish || 'Unknown';
    parishMap[parish] = (parishMap[parish] || 0) + 1;
  });
  const parishData = Object.entries(parishMap).map(([name, count]) => ({ name: name.replace('St. ', 'St.'), count }));

  // Persona distribution for pie chart
  const personaMap: Record<string, number> = {};
  properties.forEach(p => {
    if (p.buyer_persona) {
      personaMap[p.buyer_persona] = (personaMap[p.buyer_persona] || 0) + 1;
    }
  });
  const personaData = Object.entries(personaMap).map(([name, value]) => ({ name, value }));
  const pieColors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e'];

  // Competitiveness distribution
  const compMap: Record<string, number> = {};
  properties.forEach(p => {
    if (p.competitiveness) {
      compMap[p.competitiveness] = (compMap[p.competitiveness] || 0) + 1;
    }
  });
  const compData = Object.entries(compMap).map(([name, value]) => ({ name, value }));

  // Price range chart
  const priceRanges = [
    { range: '<$500K', count: 0 },
    { range: '$500K-1M', count: 0 },
    { range: '$1M-2M', count: 0 },
    { range: '$2M-5M', count: 0 },
    { range: '$5M+', count: 0 },
  ];
  properties.forEach(p => {
    const price = parseFloat(p.price);
    if (price < 500000) priceRanges[0].count++;
    else if (price < 1000000) priceRanges[1].count++;
    else if (price < 2000000) priceRanges[2].count++;
    else if (price < 5000000) priceRanges[3].count++;
    else priceRanges[4].count++;
  });

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 32 }}>
        <div>
          <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 4 }}>Dashboard</h1>
          <p style={{ color: 'var(--color-text-muted)', fontSize: 14 }}>
            Real-time property intelligence overview
          </p>
        </div>
        <button className="btn-secondary" onClick={refresh} style={{ gap: 6 }}>
          <RefreshCw size={14} /> Refresh
        </button>
      </div>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20, marginBottom: 28 }}>
        <div className="kpi-card accent">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>
                Total Properties
              </div>
              <div style={{ fontSize: 36, fontWeight: 800, lineHeight: 1 }}>{totalProps}</div>
            </div>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--color-accent-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Building2 size={20} color="var(--color-accent-light)" />
            </div>
          </div>
          <div style={{ marginTop: 12, fontSize: 12, color: 'var(--color-text-muted)' }}>
            <span style={{ color: 'var(--color-emerald)' }}>+{pending}</span> awaiting AI processing
          </div>
        </div>

        <div className="kpi-card emerald">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>
                AI Processed
              </div>
              <div style={{ fontSize: 36, fontWeight: 800, lineHeight: 1 }}>{aiProcessed}</div>
            </div>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--color-emerald-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CheckCircle2 size={20} color="var(--color-emerald)" />
            </div>
          </div>
          <div style={{ marginTop: 12, fontSize: 12, color: 'var(--color-text-muted)' }}>
            <span style={{ color: 'var(--color-emerald)' }}>{totalProps > 0 ? ((aiProcessed / totalProps) * 100).toFixed(0) : 0}%</span> completion rate
          </div>
        </div>

        <div className="kpi-card cyan">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>
                Success Rate
              </div>
              <div style={{ fontSize: 36, fontWeight: 800, lineHeight: 1 }}>{successRate}%</div>
            </div>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--color-cyan-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Cpu size={20} color="var(--color-cyan)" />
            </div>
          </div>
          <div style={{ marginTop: 12, fontSize: 12, color: 'var(--color-text-muted)' }}>
            {successCount} successful / {totalExecs} total runs
          </div>
        </div>

        <div className="kpi-card amber">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>
                Avg. Price
              </div>
              <div style={{ fontSize: 36, fontWeight: 800, lineHeight: 1 }}>
                {formatPrice(properties.reduce((s, p) => s + parseFloat(p.price || '0'), 0) / (totalProps || 1))}
              </div>
            </div>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--color-amber-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <TrendingUp size={20} color="var(--color-amber)" />
            </div>
          </div>
          <div style={{ marginTop: 12, fontSize: 12, color: 'var(--color-text-muted)' }}>
            Across all active listings
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20, marginBottom: 28 }}>
        {/* Price Distribution */}
        <div className="glass-card" style={{ padding: 24 }}>
          <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 20 }}>Price Distribution</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={priceRanges}>
              <XAxis dataKey="range" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: '#1a1f2e', border: '1px solid #2a3149', borderRadius: 8, fontSize: 12 }}
                labelStyle={{ color: '#f1f5f9' }}
              />
              <Bar dataKey="count" fill="url(#barGradient)" radius={[6, 6, 0, 0]} />
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#4f46e5" />
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Buyer Persona Pie */}
        <div className="glass-card" style={{ padding: 24 }}>
          <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 20 }}>Buyer Personas</h3>
          {personaData.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie data={personaData} cx="50%" cy="50%" innerRadius={45} outerRadius={70} dataKey="value" paddingAngle={4}>
                    {personaData.map((p, i) => <Cell key={`cell-${p.name}-${i}`} fill={pieColors[i % pieColors.length]} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid #2a3149', borderRadius: 8, fontSize: 12 }} />
                </PieChart>
              </ResponsiveContainer>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, justifyContent: 'center' }}>
                {personaData.map((p, i) => (
                  <div key={`legend-${p.name}-${i}`} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12 }}>
                    <div style={{ width: 8, height: 8, borderRadius: '50%', background: pieColors[i % pieColors.length] }} />
                    <span style={{ color: 'var(--color-text-secondary)' }}>{getPersonaIcon(p.name)} {p.name}</span>
                    <span style={{ color: 'var(--color-text-muted)' }}>({p.value})</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div style={{ color: 'var(--color-text-muted)', fontSize: 13, textAlign: 'center', paddingTop: 60 }}>
              No persona data yet
            </div>
          )}
        </div>
      </div>

      {/* Bottom Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Recent Properties */}
        <div className="glass-card" style={{ padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h3 style={{ fontSize: 15, fontWeight: 600 }}>Recent Properties</h3>
            <Link href="/properties" style={{ fontSize: 12, color: 'var(--color-accent-light)', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 4 }}>
              View All <ArrowUpRight size={12} />
            </Link>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {properties.slice(0, 5).map((p, i) => (
              <div key={p.id} className="animate-slide-in" style={{ animationDelay: `${i * 60}ms`, display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 16px', background: 'var(--color-bg-primary)', borderRadius: 10, border: '1px solid var(--color-border)' }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 2 }}>{p.title}</div>
                  <div style={{ fontSize: 12, color: 'var(--color-text-muted)' }}>
                    {p.parish} · {p.bedrooms}bd/{p.bathrooms}ba · {formatPrice(p.price)}
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  {p.ai_processed === true || p.ai_processed === 't' || p.ai_processed === 'true' ? (
                    <span className="badge badge-success">✓ Processed</span>
                  ) : (
                    <span className="badge badge-warning">⏳ Pending</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Pipeline Activity */}
        <div className="glass-card" style={{ padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h3 style={{ fontSize: 15, fontWeight: 600 }}>Pipeline Activity</h3>
            <Link href="/pipeline" style={{ fontSize: 12, color: 'var(--color-accent-light)', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 4 }}>
              View All <ArrowUpRight size={12} />
            </Link>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {recentExecs.slice(0, 8).map((ex, i) => (
              <div key={ex.id} className="animate-slide-in" style={{ animationDelay: `${i * 40}ms`, display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: 'var(--color-bg-primary)', borderRadius: 8, border: '1px solid var(--color-border)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{ fontSize: 12, color: 'var(--color-text-muted)', fontFamily: 'monospace' }}>#{ex.id}</span>
                  {ex.status === 'success' ? (
                    <CheckCircle2 size={14} color="var(--color-emerald)" />
                  ) : ex.status === 'running' ? (
                    <Clock size={14} color="var(--color-amber)" />
                  ) : (
                    <XCircle size={14} color="var(--color-rose)" />
                  )}
                  <span style={{ fontSize: 13, color: 'var(--color-text-secondary)' }}>{ex.status}</span>
                </div>
                <span style={{ fontSize: 11, color: 'var(--color-text-muted)' }}>{timeAgo(ex.startedAt)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
