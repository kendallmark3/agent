# 🧠 Python LLM Agent Microservice in CI/CD Pipeline

This document explains how to create a Python-based AI agent (using LangChain and LLMs like LLaMA or Hugging Face models), expose it as a microservice, and invoke it from a DevOps pipeline such as Jenkins or GitHub Actions.

---

## ⚙️ Architecture Overview

1. **Agent**: Python agent using LangChain, LLaMA, Hugging Face, etc.
2. **Microservice**: REST API (e.g., FastAPI) to expose the agent
3. **CI/CD Trigger**: Jenkins or GitHub Actions pipeline to invoke the service
4. **Optional**: Dockerize the microservice for portability

---

## 🧠 Step-by-Step Implementation

### 1. Python Agent Microservice with FastAPI + LangChain

#### `agent_service/main.py`
```python
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import HuggingFaceHub

app = FastAPI()

llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature": 0.7})

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
def ask_agent(request: PromptRequest):
    result = llm(request.prompt)
    return {"response": result}
```

---

### 2. Dockerfile

#### `Dockerfile`
```Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn langchain huggingface_hub

ENV HUGGINGFACEHUB_API_TOKEN=your_token_here

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

### 3. GitHub Actions Workflow

#### `.github/workflows/agent-call.yml`
```yaml
name: Call Agent Microservice

on:
  workflow_dispatch:

jobs:
  call-agent:
    runs-on: ubuntu-latest

    steps:
    - name: Hit the microservice endpoint
      run: |
        RESPONSE=$(curl -s -X POST http://your-agent-host:8080/ask \
          -H "Content-Type: application/json" \
          -d '{"prompt":"Explain microservices in 1 sentence."}')
        echo "Agent said: $RESPONSE"
```

> Replace `http://your-agent-host` with the IP or DNS name of your deployed microservice.

---

### 4. Jenkins Pipeline Example

```groovy
pipeline {
  agent any
  stages {
    stage('Query AI Agent') {
      steps {
        script {
          def response = sh(script: '''
            curl -s -X POST http://your-agent-host:8080/ask \
              -H "Content-Type: application/json" \
              -d '{"prompt": "What are Kubernetes controllers?"}'
          ''', returnStdout: true).trim()

          echo "Agent replied: ${response}"
        }
      }
    }
  }
}
```

---

## 🧪 Running a Local LLaMA Model Instead

If you want to run a local model instead of using Hugging Face:

```python
from langchain.llms import LlamaCpp

llm = LlamaCpp(
    model_path="/models/llama-2-7b.gguf",
    n_gpu_layers=40,
    temperature=0.5,
    max_tokens=256
)
```

---

## 🔧 Tools Used

- [LangChain](https://www.langchain.com/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jenkins](https://www.jenkins.io/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Docker](https://www.docker.com/)
- [llama.cpp](https://github.com/ggerganov/llama.cpp) (for local inference)

---

## ✅ Use Cases in a DevOps Shared Services Model

You can build microservice-based agents that:
- Summarize or analyze JIRA issues
- Review code PRs
- Generate release notes
- Detect security issues from scan logs
- Respond to pipeline events

---

## 🚀 Want More?

You can expand this setup by:
- Adding LangChain tools and memory
- Creating multi-agent collaboration with AutoGen or CrewAI
- Running agents asynchronously with background queues

