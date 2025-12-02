export const predictBodySchema = {
  type: 'object',
  required: ['text'],
  properties: {
    text: { type: 'string', minLength: 1 }
  },
  additionalProperties: false
};

export const predictResponseSchema = {
  200: {
    type: 'object',
    required: ['prediction', 'confidence'],
    properties: {
      prediction: { type: 'string' },
      confidence: { type: 'number', minimum: 0, maximum: 1 }
    },
    additionalProperties: false
  }
};