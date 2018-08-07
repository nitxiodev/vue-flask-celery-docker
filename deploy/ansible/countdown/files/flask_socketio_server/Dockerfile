FROM python:2

RUN mkdir -p app/countdown_backend
COPY ./countdown_backend /app/countdown_backend
RUN pip install -r /app/countdown_backend/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD ["python", "/app/countdown_backend/src/server/flask_socketio_server.py"]
EXPOSE 8000
