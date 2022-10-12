FROM python:3.10-alpine3.16

COPY ./ /home/fastapi-chat-app/
WORKDIR /home/fastapi-chat-app/

RUN apk update && \
    apk add --update --no-cache alpine-sdk gcc libffi-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]