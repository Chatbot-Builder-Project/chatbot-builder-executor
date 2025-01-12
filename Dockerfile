FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install required system dependencies (git, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . /app

# Add the Python path for the app
ENV PYTHONPATH=/app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Clone or pull the latest .proto files
RUN git clone https://github.com/Chatbot-Builder-Project/chatbot-builder-protos.git

# Create the directory structure for generated gRPC files
RUN mkdir -p app/generated/v1

# Generate gRPC code
RUN python -m grpc_tools.protoc \
    --proto_path=chatbot-builder-protos/protos \
    --python_out=app/generated \
    --grpc_python_out=app/generated \
    chatbot-builder-protos/protos/v1/executor/*.proto

# Fix imports in the generated gRPC files
RUN find app/generated/v1/executor/ -name "*_pb2*.py" \
    -exec sed -i 's/from v1\.executor/from app.generated.v1.executor/g' {} +

# Expose the gRPC server port
EXPOSE 50051

# Command to run the gRPC server
CMD ["python", "app/main.py"]
