import { predictBodySchema, predictResponseSchema } from '../schemas/index.js';
import { predictText } from '../ml/predictor.js';


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
            const result = await predictText(text);
            return result;
        });
}