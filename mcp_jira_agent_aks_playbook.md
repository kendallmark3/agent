# 🚀 MCP JIRA Agent Deployment on Azure AKS — Final Playbook

## ✅ Step 1: Build and Push Docker Image

```bash
git clone https://your-repo/mcp-jira-agent.git
cd mcp-jira-agent

docker build -t yourdockeruser/mcp-jira-agent:latest .
docker push yourdockeruser/mcp-jira-agent:latest
```

## ☁️ Step 2: Create AKS Cluster

```bash
RESOURCE_GROUP=mcp-jira-rg
CLUSTER_NAME=mcp-jira-aks
LOCATION=eastus

az group create --name $RESOURCE_GROUP --location $LOCATION
az aks create --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --node-count 1 --generate-ssh-keys
az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME
```

## 🔐 Step 3: Create Kubernetes Secrets

```bash
kubectl create secret generic jira-secrets \
  --from-literal=JIRA_API_TOKEN='your-jira-api-token'
```

## 📄 Step 4: Create and Apply Kubernetes Job

`jira-agent-job.yaml`:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: mcp-jira-agent
spec:
  template:
    spec:
      containers:
      - name: jira-agent
        image: yourdockeruser/mcp-jira-agent:latest
        env:
        - name: JIRA_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: jira-secrets
              key: JIRA_API_TOKEN
        volumeMounts:
        - name: output
          mountPath: /app/output
      restartPolicy: Never
      volumes:
      - name: output
        emptyDir: {}
  backoffLimit: 3
```

Apply it:

```bash
kubectl apply -f jira-agent-job.yaml
kubectl logs job/mcp-jira-agent
```

## 🗃️ Step 5: Extract or View Report Output

```bash
kubectl get pods
kubectl cp <pod-name>:/app/output/summary_report.png ./summary_report.png
```

## 📥 Step 6: Import Mock JIRA Stories via CSV

### 🔁 Option: Use Atlassian JIRA Cloud Free
- Go to https://www.atlassian.com/software/jira/free
- Create a free cloud instance

### 📋 Prepare Your CSV

Example format:

```csv
Summary,Issue Type,Priority,Status,Story Points,Assignee,Reporter,Description,Created,Updated
Add login page,Story,Medium,Done,5,mark.kendall,mark.kendall,Login UI with validation,2023-02-01,2023-02-07
Fix checkout bug,Bug,High,In Progress,3,mark.kendall,qa.user,Fix payment redirect error,2023-04-12,2023-04-14
Data pipeline refactor,Task,Low,To Do,8,backend.dev,pm.user,Refactor ETL logic for orders,2023-06-01,2023-06-10
```

### 📤 Import in JIRA:

1. Navigate to **Jira Settings → System → External System Import → CSV**
2. Upload CSV file
3. Map fields (e.g., Summary → Summary, Issue Type → Issue Type)
4. Add "Story Points" custom field if needed

You're ready to run real analysis now.

---
