# Chatbot Builder Executor

## Description

This is the execution service for the Chatbot Builder, responsible for executing the chatbot flow logic such as
LLM generation calls, and other processing tasks.

## Setup

1. Add `.env` file in the `app` directory (no variables are required for now).

2. Before running the service, you’ll need to generate the gRPC code from the `.proto` files to ensure the service can
   communicate with other services.

### Generate gRPC Code Locally

To generate the necessary gRPC code for Python, follow these steps:

1. **Clone or Pull the Latest `.proto` Files**
   ```bash
   git clone https://github.com/Chatbot-Builder-Project/chatbot-builder-protos.git
   ```
   Or if you already have the repository:
   ```bash
   cd chatbot-builder-protos
   git pull
   cd ..
   ```

2. **Create Directory Structure**
   ```bash
   mkdir -p app/generated/v1
   ```

3. **Generate Python gRPC Code**
   ```bash
   python -m grpc_tools.protoc --proto_path=chatbot-builder-protos/protos --python_out=app/generated --grpc_python_out=app/generated chatbot-builder-protos/protos/v1/executor/*.proto
   ```

4. **Fix Imports**
   ```shell
   Get-ChildItem -Path "app/generated/v1/executor/" -Filter "*_pb2*.py" | ForEach-Object {
    (Get-Content $_.FullName) -replace "from v1\.executor", "from app.generated.v1.executor" | Set-Content $_.FullName
   }
   ```

## Commands

### Build & Run

```bash
docker-compose up --build
```
