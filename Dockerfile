# https://docs.docker.com/engine/reference/builder/

FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=8080
ENV LOGGING_LEVEL=INFO
ENV MODEL_NAME=NOT_SET
ENV GOOGLE_CLOUD_PROJECT=NOT_SET
ENV GOOGLE_CLOUD_LOCATION=NOT_SET
ENV GOOGLE_GENAI_USE_VERTEXAI=NOT_SET
ENV PYTHONUNBUFFERED=1

RUN useradd -ms /bin/bash gradio

USER gradio
EXPOSE 8080
WORKDIR /home/gradio

COPY app.py .
COPY files ./files
COPY assets ./assets
COPY requirements.txt .

RUN uv venv
RUN uv pip install -r requirements.txt

CMD uv run app.py
