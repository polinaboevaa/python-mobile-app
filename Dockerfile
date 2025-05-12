FROM python:3.12 AS builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -e .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

CMD ["python", "-m", "app"]

