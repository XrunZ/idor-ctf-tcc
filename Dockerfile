FROM python:3.11-slim

LABEL maintainer="WSE DIVISION </XrunZ>"
LABEL description="SawitNet — IDOR CTF Challenge"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
