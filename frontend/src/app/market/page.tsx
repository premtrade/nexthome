'use client';

import { useMemo } from 'react';
import { useData } from '@/app/lib/useData';
import { formatPrice, PARISHES } from '@/app/lib/types';
import {
    TrendingUp, MapPin, DollarSign, BarChart3, Building2, RefreshCw
} from 'lucide-react';
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
    PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, Radar
} from 'recharts';

export default function MarketPage() {
    const { data, loading, refresh } = useData(15000);

    const analytics = useMemo(() => {
        if (!data?.properties) return null;
        const props = data.properties;

        // Parish breakdown
        const parishStats: Record<string, { count: number; totalPrice: number; underpriced: number; overpriced: number }> = {};
        props.forEach(p => {
            const parish = p.parish || 'Unknown';
            if (!parishStats[parish]) parishStats[parish] = { count: 0, totalPrice: 0, underpriced: 0, overpriced: 0 };
            parishStats[parish].count++;
            parishStats[parish].totalPrice += parseFloat(p.price || '0');
            if (p.competitiveness?.toLowerCase() === 'underpriced') parishStats[parish].underpriced++;
            if (p.competitiveness?.toLowerCase() === 'overpriced') parishStats[parish].overpriced++;
        });

        const parishData = Object.entries(parishStats).map(([name, stats]) => ({
            name: name.replace('St. ', 'St.'),
            fullName: name,
            listings: stats.count,
            avgPrice: stats.count > 0 ? stats.totalPrice / stats.count : 0,
            underpriced: stats.underpriced,
            overpriced: stats.overpriced,
        })).sort((a, b) => b.listings - a.listings);

        // Competitiveness breakdown
        const compStats: Record<string, number> = { Underpriced: 0, Fair: 0, Overpriced: 0 };
        props.forEach(p => {
            const c = p.competitiveness || '';
            if (c in compStats) compStats[c]++;
        });
        const compData = Object.entries(compStats).map(([name, value]) => ({ name, value }));

        // Price stats
        const prices = props.map(p => parseFloat(p.price || '0')).filter(p => p > 0);
        const avgPrice = prices.length > 0 ? prices.reduce((a, b) => a + b, 0) / prices.length : 0;
        const medianPrice = prices.length > 0 ? prices.sort((a, b) => a - b)[Math.floor(prices.length / 2)] : 0;
        const maxPrice = prices.length > 0 ? Math.max(...prices) : 0;
        const minPrice = prices.length > 0 ? Math.min(...prices) : 0;

        // Bedroom distribution
        const bedroomData: Record<string, number> = {};
        props.forEach(p => {
            const beds = p.bedrooms || '0';
            bedroomData[`${beds} Bed`] = (bedroomData[`${beds} Bed`] || 0) + 1;
        });
        const bedroomChart = Object.entries(bedroomData).map(([name, count]) => ({ name, count })).sort((a, b) => a.name.localeCompare(b.name));

        return { parishData, compData, avgPrice, medianPrice, maxPrice, minPrice, bedroomChart, total: props.length };
    }, [data]);

    if (loading || !analytics) {
        return (
            <div>
                <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 32 }}>Market Intelligence</h1>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
                    {[1, 2, 3, 4].map(i => <div key={i} className="skeleton" style={{ height: 120, borderRadius: 16 }} />)}
                </div>
            </div>
        );
    }

    const compColors = { Underpriced: '#10b981', Fair: '#f59e0b', Overpriced: '#f43f5e' };

    return (
        <div className="animate-fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 28 }}>
                <div>
                    <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 4 }}>Market Intelligence</h1>
                    <p style={{ color: 'var(--color-text-muted)', fontSize: 14 }}>AI-driven market analysis across {analytics.parishData.length} parishes</p>
                </div>
                <button className="btn-secondary" onClick={refresh}><RefreshCw size={14} /></button>
            </div>

            {/* Price KPIs */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 28 }}>
                <div className="kpi-card accent">
                    <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>Average Price</div>
                    <div style={{ fontSize: 28, fontWeight: 800 }}>{formatPrice(analytics.avgPrice)}</div>
                </div>
                <div className="kpi-card cyan">
                    <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>Median Price</div>
                    <div style={{ fontSize: 28, fontWeight: 800 }}>{formatPrice(analytics.medianPrice)}</div>
                </div>
                <div className="kpi-card emerald">
                    <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>Lowest</div>
                    <div style={{ fontSize: 28, fontWeight: 800 }}>{formatPrice(analytics.minPrice)}</div>
                </div>
                <div className="kpi-card amber">
                    <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>Highest</div>
                    <div style={{ fontSize: 28, fontWeight: 800 }}>{formatPrice(analytics.maxPrice)}</div>
                </div>
            </div>

            {/* Charts Row */}
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20, marginBottom: 28 }}>
                {/* Average Price by Parish */}
                <div className="glass-card" style={{ padding: 24 }}>
                    <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 20 }}>Average Price by Parish</h3>
                    <ResponsiveContainer width="100%" height={260}>
                        <BarChart data={analytics.parishData} layout="vertical">
                            <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => formatPrice(v)} />
                            <YAxis type="category" dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} width={80} />
                            <Tooltip
                                contentStyle={{ background: '#1a1f2e', border: '1px solid #2a3149', borderRadius: 8, fontSize: 12 }}
                                formatter={(value: any) => [formatPrice(Number(value) || 0), 'Avg Price']}
                            />
                            <Bar dataKey="avgPrice" fill="url(#marketBarGradient)" radius={[0, 6, 6, 0]} />
                            <defs>
                                <linearGradient id="marketBarGradient" x1="0" y1="0" x2="1" y2="0">
                                    <stop offset="0%" stopColor="#4f46e5" />
                                    <stop offset="100%" stopColor="#06b6d4" />
                                </linearGradient>
                            </defs>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Competitiveness Pie */}
                <div className="glass-card" style={{ padding: 24 }}>
                    <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 20 }}>Market Competitiveness</h3>
                    <ResponsiveContainer width="100%" height={200}>
                        <PieChart>
                            <Pie data={analytics.compData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" paddingAngle={4}>
                                {analytics.compData.map((entry) => (
                                    <Cell key={entry.name} fill={compColors[entry.name as keyof typeof compColors] || '#64748b'} />
                                ))}
                            </Pie>
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid #2a3149', borderRadius: 8 }} />
                        </PieChart>
                    </ResponsiveContainer>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: 16, marginTop: 8 }}>
                        {analytics.compData.map(c => (
                            <div key={c.name} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12 }}>
                                <div style={{ width: 8, height: 8, borderRadius: '50%', background: compColors[c.name as keyof typeof compColors] || '#64748b' }} />
                                <span style={{ color: 'var(--color-text-secondary)' }}>{c.name} ({c.value})</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Bottom Row */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
                {/* Bedroom Distribution */}
                <div className="glass-card" style={{ padding: 24 }}>
                    <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 20 }}>Bedroom Distribution</h3>
                    <ResponsiveContainer width="100%" height={220}>
                        <BarChart data={analytics.bedroomChart}>
                            <XAxis dataKey="name" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid #2a3149', borderRadius: 8 }} />
                            <Bar dataKey="count" fill="#06b6d4" radius={[6, 6, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Parish Comparison Table */}
                <div className="glass-card" style={{ padding: 24 }}>
                    <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 16 }}>Parish Comparison</h3>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Parish</th>
                                <th>Listings</th>
                                <th>Avg Price</th>
                                <th>Underpriced</th>
                            </tr>
                        </thead>
                        <tbody>
                            {analytics.parishData.map(p => (
                                <tr key={p.fullName}>
                                    <td style={{ fontWeight: 600, color: 'var(--color-text-primary)' }}>{p.fullName}</td>
                                    <td>{p.listings}</td>
                                    <td>{formatPrice(p.avgPrice)}</td>
                                    <td>
                                        {p.underpriced > 0 ? (
                                            <span className="badge badge-success">{p.underpriced}</span>
                                        ) : (
                                            <span style={{ color: 'var(--color-text-muted)' }}>—</span>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
