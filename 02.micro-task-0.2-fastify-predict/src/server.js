import Fastify from 'fastify';
import routes from './routes/index.js';

const app = Fastify({
  logger: true,
});

app.register(routes);
app.listen({ port: 3000, host: '0.0.0.0' }, (err, address) => {
  if (err) {
    app.log.error(err);
    process.exit(1);
  }
  app.log.info(`Server listening at ${address}`);
});