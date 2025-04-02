FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# Create data directory and set permissions
RUN mkdir -p /app/data && chmod 777 /app/data

# Run tests
RUN pytest src/test_main.py -v --cov=src --cov-report=term-missing

CMD ["python", "src/main.py"] 