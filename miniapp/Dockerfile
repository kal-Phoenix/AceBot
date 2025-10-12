# Build stage for frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app

# Copy frontend package files
COPY package*.json ./
RUN npm ci

# Copy frontend source
COPY . .

# Set API URL for production build
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

# Build frontend
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Copy server package files
COPY server/package*.json ./
RUN npm ci --production

# Copy server source
COPY server/ ./

# Copy built frontend
COPY --from=frontend-builder /app/dist ./public

# Expose port
EXPOSE 8080

# Start server
CMD ["node", "server.js"]
