FROM python:3.11-slim

LABEL maintainer="WSE DIVISION </XrunZ>"
LABEL description="SawitNet — IDOR CTF Challenge"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# .dockerignore memastikan file author-only (README/chall/author-notes/solve.py,
# .git, *.db, .env) tidak ikut masuk ke image.
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Worker tunggal: cukup untuk CTF dan menjaga konsistensi sesi/DB.
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
