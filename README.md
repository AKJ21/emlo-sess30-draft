# Create an EC2 Instance, with 64 Cores



sudo apt install zip python3-pip
curl -fsSL <https://get.docker.com> -o get-docker.sh
sudo usermod -aG docker $USER
pip install jupyterlab
echo "export PATH=\\$PATH:/home/ubuntu/.local/bin" >> ~/.bashrc

## Setup LocalAI
Download Mixtral 8x7B ggml model
```
wget https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q3_K_M.gguf
```

Create following files:
- .env
- embeddings.yaml
- mixtral.yaml
- mixtral-chat.tmpl
- mixtral-completion.tmpl

Create docker-compose.yml

Start the Server!
```
docker compose up -d
```
We can test the model working:
```
curl <http://localhost:8080/embeddings> -X POST -H "Content-Type: application/json" -d '{
  "input": "Your text string goes here",
  "model": "text-embedding-ada-002"
}'

curl <http://localhost:8080/v1/chat/completions> -H "Content-Type: application/json" -d '{ "model": "mistral", "messages": [{"role": "user", "content": "How are you?"}], "temperature": 0.9 }'
```

## Setup FastAPI
Create following files:
- server.py
- requirements.txt
- Dockerfile

## Deployment
```
docker compose build
```

```
docker compose up-d
```

You may check status of both LocalAI and FastAPI service run using below command:
```
docker compose logs -f
```


