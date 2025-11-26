export default async function healthRoute(fastify, opts) { 
    fastify.get('/health', async (request, reply) => {
        return { status: 'ok' };
    });
}