#!/bin/bash

uvicorn mgraph_ai_serverless.lambdas.handler:app --host 0.0.0.0 --port 8080