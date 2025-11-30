# Dockerfile for Fastify gateway service

# 1. Use an official Node.js runtime as a parent image
FROM node:20-alpine

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy package.json (and package-lock.json if you add it later)
COPY package.json ./

# 4. Install dependencies
RUN npm install --production

# 5. Copy application source
COPY server.js ./

# 6. Expose port 3000 for the Fastify service
EXPOSE 3000

# 7. Start the Fastify server
CMD ["npm", "start"]