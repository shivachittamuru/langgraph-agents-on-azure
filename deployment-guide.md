# Deploying a Containerized Application to Azure Web App

This guide walks you through the process of creating Docker images from your backend and frontend directories, pushing them to Azure Container Registry (ACR), and deploying them to an Azure Web App.

### Creating Docker Images Locally

Ensure you have Docker Desktop or a Docker terminal installed. Run the following commands to build images and run containers locally for both backend and frontend applications.

> **Note:** Before running the following commands, update the `main.py` file to ensure the Uvicorn server is configured to run on port 80 for the Docker setup.

```console
# Navigate to the backend directory and build the Docker image
cd backend
docker build -t chinook-backend .

docker images

# This command works if you also include the .env file in the Docker image
<!-- docker run -d -p 80:80 chinook-backend:latest -->

# However, ensure that you do not include the .env file in the Docker image for security reasons.
# Instead, use the -e flag to provide environment variables when running the container.

```console
docker run -d -p 80:80 ^
    -e AZURE_OPENAI_DEPLOYMENT_NAME=<YOUR-DEPLOYMENT-NAME> ^
    -e AZURE_OPENAI_API_KEY=<YOUR-API-KEY> ^
    -e AZURE_OPENAI_ENDPOINT=<YOUR-ENDPOINT> ^
    -e AZURE_OPENAI_API_VERSION=<YOUR-API-VERSION> ^
    -e APPLICATIONINSIGHTS_CONNECTION_STRING="<YOUR-CONNECTION-STRING>" ^
    -e AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=<YOUR-RECORDING-ENABLED> ^
    -e AZURE_SDK_TRACING_IMPLEMENTATION=<YOUR-TRACING-IMPLEMENTATION> ^
    -e PG_VECTOR_HOST=<YOUR-PG-HOST> ^
    -e PG_VECTOR_USER=<YOUR-PG-USER> ^
    -e PGPORT=<YOUR-PG-PORT> ^
    -e PGDATABASE=<YOUR-PG-DATABASE> ^
    -e PG_VECTOR_PASSWORD="<YOUR-PG-PASSWORD>" ^
    chinook-backend:latest
```

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

az webapp config appsettings set --name <YOUR-BACKEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME> --settings ^
    AZURE_OPENAI_DEPLOYMENT_NAME=<YOUR-DEPLOYMENT-NAME> ^
    AZURE_OPENAI_API_KEY=<YOUR-API-KEY> ^
    AZURE_OPENAI_ENDPOINT=<YOUR-ENDPOINT> ^
    AZURE_OPENAI_API_VERSION=<YOUR-API-VERSION> ^
    APPLICATIONINSIGHTS_CONNECTION_STRING="<YOUR-CONNECTION-STRING>" ^
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=<YOUR-RECORDING-ENABLED> ^
    AZURE_SDK_TRACING_IMPLEMENTATION=<YOUR-TRACING-IMPLEMENTATION> ^
    PG_VECTOR_HOST=<YOUR-PG-HOST> ^
    PG_VECTOR_USER=<YOUR-PG-USER> ^
    PGPORT=<YOUR-PG-PORT> ^
    PGDATABASE=<YOUR-PG-DATABASE> ^
    PG_VECTOR_PASSWORD="<YOUR-PG-PASSWORD>"

# Create a web app for the frontend
az webapp create --resource-group <YOUR-RESOURCE-GROUP-NAME> --plan <YOUR-APP-SERVICE-PLAN-NAME> --name <YOUR-FRONTEND-WEBAPP-NAME> --deployment-container-image-name <YOUR-ACR-NAME>.azurecr.io/chinook-frontend:latest

# Configure the frontend web app to use the ACR
az webapp config container set --name <YOUR-FRONTEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME> --docker-custom-image-name <YOUR-ACR-NAME>.azurecr.io/chinook-frontend:latest --docker-registry-server-url https://<YOUR-ACR-NAME>.azurecr.io --docker-registry-server-user <YOUR-ACR-USERNAME> --docker-registry-server-password <YOUR-ACR-PASSWORD>

az webapp config appsettings set --name <YOUR-FRONTEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME> --settings REACT_APP_API_URL=<YOUR-BACKEND-WEBAPP-DOMAIN>

# Restart the backend web app to apply changes
az webapp restart --name <YOUR-BACKEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME>

# Restart the frontend web app to apply changes
az webapp restart --name <YOUR-FRONTEND-WEBAPP-NAME> --resource-group <YOUR-RESOURCE-GROUP-NAME>
```

### Deploy to AKS

Follow these steps to deploy your application to Azure Kubernetes Service (AKS).

```console
# Create a resource group
az group create --name <YOUR-RESOURCE-GROUP-NAME> --location <YOUR-LOCATION>
```

```console
# Create an AKS cluster
az aks create --resource-group <YOUR-RESOURCE-GROUP-NAME> --name <YOUR-AKS-CLUSTER-NAME> --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

```console
# Get AKS credentials
az aks get-credentials --resource-group <YOUR-RESOURCE-GROUP-NAME> --name <YOUR-AKS-CLUSTER-NAME>
```

```console
# Create a namespace for your application
kubectl create namespace chinook
```

```console
# Create a secret for ACR credentials
kubectl create secret docker-registry acr-secret --namespace chinook --docker-server=<YOUR-ACR-NAME>.azurecr.io --docker-username=<YOUR-ACR-USERNAME> --docker-password=<YOUR-ACR-PASSWORD> --docker-email=<YOUR-EMAIL>
```

```console
# Deploy backend to AKS
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
    name: chinook-backend
    namespace: chinook
spec:
    replicas: 1
    selector:
        matchLabels:
            app: chinook-backend
    template:
        metadata:
            labels:
                app: chinook-backend
        spec:
            containers:
            - name: chinook-backend
                image: <YOUR-ACR-NAME>.azurecr.io/chinook-backend:latest
                ports:
                - containerPort: 80
                env:
                - name: AZURE_OPENAI_DEPLOYMENT_NAME
                    value: "<YOUR-DEPLOYMENT-NAME>"
                - name: AZURE_OPENAI_API_KEY
                    value: "<YOUR-API-KEY>"
                - name: AZURE_OPENAI_ENDPOINT
                    value: "<YOUR-ENDPOINT>"
                - name: AZURE_OPENAI_API_VERSION
                    value: "<YOUR-API-VERSION>"
                - name: APPLICATIONINSIGHTS_CONNECTION_STRING
                    value: "<YOUR-CONNECTION-STRING>"
                - name: AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED
                    value: "<YOUR-RECORDING-ENABLED>"
                - name: AZURE_SDK_TRACING_IMPLEMENTATION
                    value: "<YOUR-TRACING-IMPLEMENTATION>"
                - name: PG_VECTOR_HOST
                    value: "<YOUR-PG-HOST>"
                - name: PG_VECTOR_USER
                    value: "<YOUR-PG-USER>"
                - name: PGPORT
                    value: "<YOUR-PG-PORT>"
                - name: PGDATABASE
                    value: "<YOUR-PG-DATABASE>"
                - name: PG_VECTOR_PASSWORD
                    value: "<YOUR-PG-PASSWORD>"
            imagePullSecrets:
            - name: acr-secret
EOF
```

```console
# Deploy frontend to AKS
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
    name: chinook-frontend
    namespace: chinook
spec:
    replicas: 1
    selector:
        matchLabels:
            app: chinook-frontend
    template:
        metadata:
            labels:
                app: chinook-frontend
        spec:
            containers:
            - name: chinook-frontend
                image: <YOUR-ACR-NAME>.azurecr.io/chinook-frontend:latest
                ports:
                - containerPort: 80
            imagePullSecrets:
            - name: acr-secret
EOF
```

```console
# Expose backend service
kubectl expose deployment chinook-backend --type=LoadBalancer --name=chinook-backend-service --namespace=chinook --port=80 --target-port=80
```

```console
# Expose frontend service
kubectl expose deployment chinook-frontend --type=LoadBalancer --name=chinook-frontend-service --namespace=chinook --port=80 --target-port=80
```

```console
# Get the external IP addresses for the services
kubectl get services --namespace chinook
```
