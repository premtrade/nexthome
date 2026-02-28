const { Client } = require('pg');

async function run() {
    const url = process.env.DATABASE_URL || process.env.DATABASE_PUBLIC_URL;
    const client = new Client({
        connectionString: url,
        ssl: { rejectUnauthorized: false }
    });
    await client.connect();

    try {
        const id = 'lW5mGPOkiPI7jHXs'; // V2 Workflow ID
        const res = await client.query('SELECT nodes, settings FROM workflow_entity WHERE id = $1', [id]);

        if (res.rows.length === 0) {
            console.error('Workflow not found in Railway DB');
            return;
        }

        let nodes = typeof res.rows[0].nodes === 'string' ? JSON.parse(res.rows[0].nodes) : res.rows[0].nodes;
        let settings = typeof res.rows[0].settings === 'string' ? JSON.parse(res.rows[0].settings) : res.rows[0].settings;

        // 1. Update SEO Generation Node (Mixtral Fix)
        const seoNode = nodes.find(n => n.name === 'SEO Generation');
        if (seoNode) {
            console.log('Updating Railway SEO Generation node...');
            seoNode.parameters.jsonBody = "={\n  \"question\": \"generate seo\",\n  \"title\": \"{{ ($json.title || '').substring(0, 50) }}\",\n  \"location\": \"{{ ($json.parish || '').substring(0, 50) }}\",\n  \"price\": \"{{ $json.price }}\",\n  \"amenities\": \"{{ ($json.amenities_text || '').substring(0, 100) }}\",\n  \"overrideConfig\": {\n    \"modelName\": \"mixtral-8x7b-32768\"\n  }\n}";
            seoNode.waitBetweenRetries = 20000;
            seoNode.maxRetries = 5;
        }

        // 2. Update Persona Classification Node (Mixtral Fix)
        const personaNode = nodes.find(n => n.name === 'Persona Classification');
        if (personaNode) {
            console.log('Updating Railway Persona Classification node...');
            personaNode.parameters.jsonBody = "={\n  \"question\": \"classify persona\",\n  \"title\": \"{{ ($node[\\\"Normalization\\\"].json.title || '').substring(0, 50) }}\",\n  \"description\": \"{{ ($node[\\\"Normalization\\\"].json.description || '').substring(0, 200) }}\",\n  \"overrideConfig\": {\n    \"modelName\": \"mixtral-8x7b-32768\"\n  }\n}";
            personaNode.retryOnFail = true;
            personaNode.maxRetries = 3;
            personaNode.waitBetweenRetries = 15000;
        }

        // 3. Enable Execution Logging (Railway)
        settings = {
            ...settings,
            saveExecutionProgress: true,
            saveManualExecutions: true,
            saveDataErrorExecution: 'all',
            saveDataSuccessExecution: 'all'
        };

        // 4. Update DB
        await client.query('UPDATE workflow_entity SET nodes = $1, settings = $2, name = \'Next Home - Property AI Processor V2\', "updatedAt" = NOW(), "versionCounter" = "versionCounter" + 1 WHERE id = $3', [JSON.stringify(nodes), JSON.stringify(settings), id]);
        console.log('Railway Workflow updated and logging enabled.');

    } catch (e) {
        console.error('Railway update failed:', e);
    } finally {
        await client.end();
    }
}

run();
