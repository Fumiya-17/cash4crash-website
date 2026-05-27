FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# We install libpq-dev and gcc to compile psycopg2 if needed, 
# but it's better to use psycopg2-binary in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary uvicorn

COPY . .

# Wait for DB script if needed, or just run uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
