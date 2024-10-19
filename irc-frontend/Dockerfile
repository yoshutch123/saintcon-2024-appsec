FROM node:18-alpine AS builder

WORKDIR /var/run/irc-frontend

COPY package.json package-lock.json ./
RUN npm install --dev
COPY . .
EXPOSE 5173

CMD ["npm", "run", "dev", "--expose"]