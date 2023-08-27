1. Deploy

```sh
docker compose up -d  
```
OR
```sh
docker build -t mfcer . 
```
```sh
docker run -d --name mfcerbot -p 8000:8000 mfcer  
```

2. Swagger
> http://localhost:8000/docs