FROM python:3.9.18-bullseye
WORKDIR /app
COPY server.py /app
CMD ["python3", "server.py"]
