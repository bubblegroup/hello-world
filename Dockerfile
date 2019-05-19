# Use an official Python runtime as a parent image
FROM node:10.13.0

# Install any needed packages specified in requirements.txt
RUN npm ci

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["node", "hello_world.js"]