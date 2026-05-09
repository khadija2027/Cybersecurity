FROM node:18-alpine

WORKDIR /app

# Install http-server to serve static files
RUN npm install -g http-server

# Copy frontend files
COPY . .

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/index.html || exit 1

# Start http-server
CMD ["http-server", ".", "-p", "3000", "-c-1"]
