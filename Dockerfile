FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

RUN apt-get update && apt-get install git -y

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY front.py /code/app/front.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]