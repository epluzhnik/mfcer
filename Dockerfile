FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

RUN apt-get update && apt-get install unzip -y

WORKDIR /code

COPY ./resources /code/resources

#RUN unzip /code/resources/embeddings_ru.zip -d /code/resources/ && rm -f /code/resources/embeddings_ru.zip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]