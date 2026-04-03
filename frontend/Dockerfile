FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
# 具体的启动命令由 docker-compose 的 command 覆盖