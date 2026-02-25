import { NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function GET() {
    try {
        const propertiesResult = await query(
            `SELECT id, tenant_id, title, description, price, parish, bedrooms, bathrooms, lot_size, status, ai_processed, seo_description, meta_title, meta_description, buyer_persona, competitiveness, created_at, updated_at FROM properties ORDER BY updated_at DESC`
        );

        // Get execution stats  
        const execStatsResult = await query(
            `SELECT status, COUNT(*) as count FROM execution_entity GROUP BY status`
        );

        // Get recent executions
        const recentExecsResult = await query(
            `SELECT id, status, "startedAt", "stoppedAt" FROM execution_entity ORDER BY "startedAt" DESC LIMIT 20`
        );

        // Get AI errors
        const errorsResult = await query(
            `SELECT * FROM ai_errors ORDER BY created_at DESC LIMIT 20`
        );

        return NextResponse.json({
            properties: propertiesResult.rows,
            execStats: execStatsResult.rows,
            recentExecs: recentExecsResult.rows,
            errors: errorsResult.rows,
        });
    } catch (error) {
        console.error('DB Error:', error);
        return NextResponse.json({ error: 'Database connection failed' }, { status: 500 });
    }
}

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { action, data } = body;

        if (action === 'add_property') {
            const { title, description, price, parish, bedrooms, bathrooms } = data;

            // Sanitize inputs for SQL safety
            const cleanTitle = (title || 'New Property').trim();
            const cleanDesc = (description || '').trim();
            const cleanParish = (parish || 'St. James').trim();
            const numPrice = parseFloat(price as string) || 0;
            const numBeds = parseInt(bedrooms as string) || 0;
            const numBaths = parseInt(bathrooms as string) || 0;

            const sql = `INSERT INTO properties (tenant_id, title, description, price, parish, bedrooms, bathrooms, status, ai_processed) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`;
            const params = ['00000000-0000-0000-0000-000000000001', cleanTitle, cleanDesc, numPrice, cleanParish, numBeds, numBaths, 'active', false];

            await query(sql, params);
            return NextResponse.json({ success: true });
        }

        if (action === 'reprocess') {
            await query(
                `UPDATE properties SET ai_processed = false, seo_description = NULL, meta_title = NULL, meta_description = NULL, buyer_persona = NULL, competitiveness = NULL WHERE id = $1`,
                [data.id]
            );
            return NextResponse.json({ success: true });
        }

        if (action === 'delete_property') {
            await query(`DELETE FROM properties WHERE id = $1`, [data.id]);
            return NextResponse.json({ success: true });
        }

        return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    } catch (error) {
        console.error('POST Error:', error);
        return NextResponse.json({ error: 'Action failed' }, { status: 500 });
    }
}
