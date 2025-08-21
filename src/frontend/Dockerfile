FROM node:24-slim

WORKDIR /app

RUN npm install -g http-server

COPY . .

EXPOSE 3000

CMD ["http-server", ".", "-p", "3000", "-a", "0.0.0.0"]
