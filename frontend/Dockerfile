# Stage 1: Build the Next.js application
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package metadata first
COPY package.json ./

# Install dependencies
RUN npm install

# Copy source code and config
COPY . .

# Build standard application
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 2: Serve the application in a lightweight production container
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy build artifacts and dependencies
COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Expose Next.js port
EXPOSE 3000

CMD ["npm", "run", "start"]
