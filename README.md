# Chatbot Builder Executor

## Description

This is the execution service for the Chatbot Builder, responsible for executing the chatbot flow logic such as
LLM generation calls, and other processing tasks.

## Setup

- Add `.env` file in the `app` directory with the following content:

```env
LOG_LEVEL= (optional)
SENTRY_DSN=
SENTRY_LOG_LEVEL= (optional)
SENTRY_ENVIRONMENT= (optional)
```

## Commands

### Build & Run

```bash
docker-compose up --build
```
