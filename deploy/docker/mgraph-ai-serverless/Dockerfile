FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install mangum uvicorn httpx fastapi python-multipart
RUN pip install osbot-aws osbot-fast-api

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

RUN python --version
ENV PORT=8080

WORKDIR /app
COPY ../../../mgraph_ai_serverless /app/mgraph_ai_serverless

ENV PYTHONPATH="/app"

COPY ./deploy/docker/mgraph-ai-serverless/start.sh /app/start.sh

CMD ["./start.sh"]

