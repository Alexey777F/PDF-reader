FROM python:3.9.18-bullseye
WORKDIR /app
COPY server.py /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "server.py"]
