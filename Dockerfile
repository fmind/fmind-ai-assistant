# https://docs.docker.com/engine/reference/builder/

FROM python:3.11-slim

ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=8080
ENV LOGGING_LEVEL=INFO
ENV MODEL_NAME=NOT_SET
ENV PROJECT_ID=NOT_SET
ENV PROJECT_LOCATION=NOT_SET
ENV PYTHONUNBUFFERED=1

RUN useradd -ms /bin/bash gradio

USER gradio
EXPOSE 8080
WORKDIR /home/gradio
ENV PATH="/home/gradio/.local/bin:${PATH}"

COPY app.py .
COPY files ./files
COPY requirements.lock .

RUN pip install --no-cache-dir -r requirements.lock

CMD python app.py
