export default async function infoRoute(fastify, opts) {
    fastify.get('/info', async (request, reply) => {
        return {
          name: "ai-svc", 
          version: "0.1.0",
            description: 'A simple Fastify microservice providing health and info endpoints.'    
        };
    });
}