FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt loguru python-dotenv tenacity
COPY . .
CMD ["python", "main.py"]
