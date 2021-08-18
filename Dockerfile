FROM python:3.7

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN export FLASK_APP=app.py

CMD ["flask", "run", "-h", "0.0.0.0"]