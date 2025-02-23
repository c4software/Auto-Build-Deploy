FROM alpine:latest

RUN apk add --no-cache \
    git \
    docker \
    python3 \
    curl \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY webhook.py /app/webhook.py

EXPOSE 8080

CMD ["python3", "/app/webhook.py"]
