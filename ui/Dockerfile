# UI Dockerfile

# Use a Node.js image as the base image
FROM node:18 as build

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the application
RUN npm run build

# Use an Nginx image to serve the built application
FROM nginx:alpine

ENV VITE_REACT_APP_API_BASE_URL="http://localhost:5002/api"

# Copy the built application to Nginx's web directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
