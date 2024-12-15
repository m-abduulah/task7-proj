FROM python:3.8

WORKDIR /app

COPY Application /app/Application
COPY models /app/models
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "Application/app.py" ]