## 🚀 Step 3: Python Deployment Script (`deploy_hello_acr.py`)

```python
import subprocess
import requests
import time

# CONFIGURE THESE
resource_group = "myResourceGroup"
registry_name = "myacrname"
image_name = "hello-world-api"
app_name = "helloacrwebapp"
region = "eastus"

# Step 1: Create Resource Group
subprocess.run(["az", "group", "create", "--name", resource_group, "--location", region], check=True)

# Step 2: Create Azure Container Registry
subprocess.run(["az", "acr", "create", "--resource-group", resource_group, "--name", registry_name, "--sku", "Basic"], check=True)

# Step 3: Login to ACR
subprocess.run(["az", "acr", "login", "--name", registry_name], check=True)

# Step 4: Get ACR login server
acr_login_server = subprocess.check_output([
    "az", "acr", "show",
    "--name", registry_name,
    "--query", "loginServer",
    "-o", "tsv"
], text=True).strip()

full_image_name = f"{acr_login_server}/{image_name}:v1"

# Step 5: Build and push Docker image
subprocess.run(["docker", "build", "-t", full_image_name, "."], check=True)
subprocess.run(["docker", "push", full_image_name], check=True)

# Step 6: Create App Service Plan
subprocess.run([
    "az", "appservice", "plan", "create",
    "--name", f"{app_name}-plan",
    "--resource-group", resource_group,
    "--is-linux",
    "--sku", "B1"
], check=True)

# Step 7: Deploy to Azure App Service
subprocess.run([
    "az", "webapp", "create",
    "--resource-group", resource_group,
    "--plan", f"{app_name}-plan",
    "--name", app_name,
    "--deployment-container-image-name", full_image_name,
    "--registry-login-server", acr_login_server,
    "--role", "acrpull"
], check=True)

# Step 8: Configure port
subprocess.run([
    "az", "webapp", "config", "appsettings", "set",
    "--resource-group", resource_group,
    "--name", app_name,
    "--settings", "WEBSITES_PORT=8000"
], check=True)

# Step 9: Test API
hostname = subprocess.check_output([
    "az", "webapp", "show",
    "--resource-group", resource_group,
    "--name", app_name,
    "--query", "defaultHostName",
    "-o", "tsv"
], text=True).strip()

url = f"https://{hostname}/"
print(f"Waiting for {url} to be ready...")
time.sleep(30)

try:
    response = requests.get(url)
    print("✅ API Response:", response.status_code, response.json())
except Exception as e:
    print("❌ Failed to call API:", e)
```

---

## 🧪 Step 4: Run Everything

### 1. Install dependencies
```bash
pip install fastapi uvicorn requests
```

### 2. Install Azure CLI
- macOS: `brew install azure-cli`
- Windows/Linux: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

### 3. Login to Azure
```bash
az login
```

### 4. Deploy to Azure
```bash
python deploy_hello_acr.py
```

---

## 🌐 Step 5: Verify

Your API will be deployed at:

```
https://<app_name>.azurewebsites.net/
```

And should return:

```json
{"message": "Hello, world from Azure ACR!"}
```

---

## 💡 Tips

- Make sure `app_name` and `registry_name` are globally unique.
- Use the Azure Portal to monitor and configure the App Service.
- You can connect a GitHub repo and automate deployment via Actions (optional).

---
