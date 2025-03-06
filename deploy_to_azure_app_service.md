# Deploying a Containerized Application to Azure Web App

This guide walks you through the process of creating Docker images from your backend and frontend directories, pushing them to Azure Container Registry (ACR), and deploying them to an Azure Web App.

### Creating Docker Images Locally

Ensure you have Docker Desktop or a Docker terminal installed. Run the following commands to build images and run containers locally for both backend and frontend applications.

```console
# Navigate to the backend directory and build the Docker image
cd backend
docker build -t chinook-backend .

docker images

docker run -d -p 80:80 chinook-backend:latest

docker ps

docker stop <container-name>

# Navigate to the frontend directory and build the Docker image
cd frontend
docker build -t chinook-frontend .

docker images

docker run -d -p 8080:80 chinook-frontend:latest

docker ps

docker stop <container-name>
```

This will create Docker images and run the containers. If your app is a web service, you can access it via http://localhost in your browser (or the mapped port).

### Tagging and Pushing to Azure Container Registry (ACR)

Before pushing your images, ensure you have an active Azure account and ACR setup.

```console
# Login to Azure
az login
az account set --subscription "<YOUR-SUBSCRIPTION-ID>"

# List your Azure Container Registries
az acr list --query "[].{acrLoginServer:loginServer}" --output table

# Login to ACR  
az acr login --name <YOUR-ACR-NAME>

# Tag Docker images for ACR
docker tag chinook-backend:latest <YOUR-ACR-NAME>.azurecr.io/chinook-backend:latest
docker tag chinook-frontend:latest <YOUR-ACR-NAME>.azurecr.io/chinook-frontend:latest

# Push images to ACR
docker push <YOUR-ACR-NAME>.azurecr.io/chinook-backend:latest
docker push <YOUR-ACR-NAME>.azurecr.io/chinook-frontend:latest

# Verify repository list in ACR
az acr repository list --name <YOUR-ACR-NAME> --output table
```

### Deploying to Azure App Service

After pushing the images, deploy them to an Azure Web App with the following steps:

```console
# Create a resource group
az group create --name <YOUR-RESOURCE-GROUP-NAME> --location <YOUR-LOCATION>

# Create an App Service plan
az appservice plan create --name <YOUR-APP-SERVICE-PLAN-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME> --sku B1 --is-linux

# Create a web app for the backend
az webapp create --resource-group <YOUR-RESOURCE-GROUP-NAME> --plan <YOUR-APP-SERVICE-PLAN-NAME> --name <YOUR-BACKEND-WEBAPP-NAME> --deployment-container-image-name <YOUR-ACR-NAME>.azurecr.io/chinook-backend:latest

# Configure the backend web app to use the ACR
az webapp config container set --name <YOUR-BACKEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME> --docker-custom-image-name <YOUR-ACR-NAME>.azurecr.io/chinook-backend:latest --docker-registry-server-url https://<YOUR-ACR-NAME>.azurecr.io --docker-registry-server-user <YOUR-ACR-USERNAME> --docker-registry-server-password <YOUR-ACR-PASSWORD>

# Create a web app for the frontend
az webapp create --resource-group <YOUR-RESOURCE-GROUP-NAME> --plan <YOUR-APP-SERVICE-PLAN-NAME> --name <YOUR-FRONTEND-WEBAPP-NAME> --deployment-container-image-name <YOUR-ACR-NAME>.azurecr.io/chinook-frontend:latest

# Configure the frontend web app to use the ACR
az webapp config container set --name <YOUR-FRONTEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME> --docker-custom-image-name <YOUR-ACR-NAME>.azurecr.io/chinook-frontend:latest --docker-registry-server-url https://<YOUR-ACR-NAME>.azurecr.io --docker-registry-server-user <YOUR-ACR-USERNAME> --docker-registry-server-password <YOUR-ACR-PASSWORD>

# Restart the backend web app to apply changes
az webapp restart --name <YOUR-BACKEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME>

# Restart the frontend web app to apply changes
az webapp restart --name <YOUR-FRONTEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME>
```

### Conclusion

Your backend and frontend applications are now deployed to Azure Web App as containerized services. If you need to update your application, rebuild and push the new images to ACR, then restart the web app for changes to take effect.