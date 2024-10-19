FROM node:latest

WORKDIR /var/run/

EXPOSE 8801

COPY package.json .

RUN npm install

CMD ["npm", "start"]