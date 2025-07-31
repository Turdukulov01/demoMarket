FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# ───────── Системные зависимости (если нужны C-расширения) ─────────
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential libpq5 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ───────── Копируем проект ─────────
COPY pyproject.toml ./
 # манифест
COPY . .
  # исходники

# ───────── Ставим uv и сам проект с зависимостями ─────────
RUN pip install --no-cache-dir uv \
 && uv pip install --system -e .

# ───────── Запуск приложения ─────────
ENV PYTHONPATH=/app/src
#EXPOSE 8000
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 5000
CMD ["python", "run.py"]
