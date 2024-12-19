FROM python:3.11-slim
WORKDIR /app

COPY . /app

ENV PYTHONIOENCODING=UTF-8

RUN python3 -m venv /venv && \
    /venv/bin/pip install -r requirements.txt && \
    chmod +x /app/rung /app/runp

CMD ["/app/rung"]
