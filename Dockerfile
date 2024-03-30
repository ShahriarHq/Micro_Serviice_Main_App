FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /main_app.py
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD python main.py
