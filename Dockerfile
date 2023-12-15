FROM python:3.9.18-bullseye
WORKDIR /app
COPY server.py /app
COPY requirements1.txt /app
RUN pip install --no-cache-dir -r requirements1.txt
CMD ["python3", "server.py"]
