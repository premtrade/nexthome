'use client';

import { useState, useEffect, useCallback } from 'react';
import type { DashboardData } from './types';

export function useData(refreshInterval = 10000) {
    const [data, setData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        try {
            const res = await fetch('/api/data');
            if (!res.ok) throw new Error('Fetch failed');
            const json = await res.json();
            setData(json);
            setError(null);
        } catch (e) {
            setError((e as Error).message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, refreshInterval);
        return () => clearInterval(interval);
    }, [fetchData, refreshInterval]);

    const postAction = async (action: string, actionData: Record<string, unknown>) => {
        try {
            const res = await fetch('/api/data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action, data: actionData }),
            });
            if (!res.ok) throw new Error('Action failed');
            await fetchData();
            return true;
        } catch {
            return false;
        }
    };

    return { data, loading, error, refresh: fetchData, postAction };
}
