# Use Node.js for building the React app
FROM node:22-alpine AS build
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install --frozen-lockfile

# Copy application files and build the React app
COPY . .
RUN npm run build

# Use Nginx for serving the built React app
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for serving the React app
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]



