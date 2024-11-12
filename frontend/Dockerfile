# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

COPY . .

# Start app
RUN npm run build
CMD npm run start
