FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY streaming_json_parser.py .
COPY test_streaming_json_parser.py .
COPY pytest.ini .

# Run tests by default
CMD ["pytest", "-v"]