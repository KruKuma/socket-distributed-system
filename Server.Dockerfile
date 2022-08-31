FROM python:3-stretch

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 64001

CMD ["python", "server.py"]
