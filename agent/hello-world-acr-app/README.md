# Hello World FastAPI on Azure with ACR
http://helloacrcontainer30562.eastus.azurecontainer.io:8000


This project contains a minimal FastAPI app that:
- Is containerized with Docker
- Is deployed to Azure App Service
- Uses Azure Container Registry (ACR) instead of Docker Hub

## 🧱 Files

- `main.py` - FastAPI app
- `Dockerfile` - Container spec
- `deploy_hello_acr.py` - Full build, push, and deploy flow using Azure CLI

## 🚀 Quick Start

```bash
# Login to Azure
az login

# Install dependencies
pip install fastapi uvicorn requests

# Deploy to Azure (builds Docker, pushes to ACR, deploys to App Service)
python deploy_hello_acr.py
```

## 🔗 Endpoint

After deployment, your API will be available at:

```
https://<app_name>.azurewebsites.net/
```
