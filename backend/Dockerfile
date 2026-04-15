FROM python:3.11-slim

WORKDIR /app

# ✅ Install SSH client
RUN apt-get update && apt-get install -y openssh-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x k8s-cluster.sh

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
