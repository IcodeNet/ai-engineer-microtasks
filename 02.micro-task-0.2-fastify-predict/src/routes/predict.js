import { predictBodySchema, predictResponseSchema } from '../schemas/index.js';

async function handlePredict(text) {
    // e.g. if text contains 'bad' → 'negative', else 'positive'
    // return { prediction, confidence }
    if (text.toLowerCase().includes('bad')) {
        return { prediction: 'negative', confidence: 0.9 };
    } else {
        return { prediction: 'positive', confidence: 0.9 };
    }
}
export default async function predictRoute(fastify, opts) {
    fastify.post('/predict',
        {
            schema: {
                body: predictBodySchema,
                response: predictResponseSchema
            }
        },
        async (request, reply) => {
            const { text } = request.body;
            const result = await handlePredict(text);
            return result;
        });
}