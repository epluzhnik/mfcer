1. Deploy

```sh
docker compose up -d  
```
> ! Придется немного подождать загрузки модели

OR
```sh
docker build -t mfcer . 
```
```sh
docker run -d --name mfcerbot -p 8000:8000 mfcer  
```

2. Swagger
> http://localhost:8000/docs

3. Run UI Demo
```sh
pip install -r front_requirements.txt
streamlit run front.py
``` 
