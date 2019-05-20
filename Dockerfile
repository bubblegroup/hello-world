FROM node:10.13.0

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN npm ci

EXPOSE 8080

CMD ["node", "hello_world.js"]