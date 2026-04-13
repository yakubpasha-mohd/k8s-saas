FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies (including dev)
RUN npm install

# Copy source
COPY . .

# Ensure vite is available
RUN npm install -g vite

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
