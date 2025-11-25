import health from './health.js';
import info from './info.js';

export default async function routes(fastify, opts) {
  await fastify.register(health);
  await fastify.register(info);
}
