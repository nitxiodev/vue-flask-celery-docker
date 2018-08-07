FROM python:2

RUN mkdir -p app/countdown_backend
COPY ./countdown_backend /app/countdown_backend
WORKDIR /app
RUN pip install -r ./countdown_backend/requirements.txt
