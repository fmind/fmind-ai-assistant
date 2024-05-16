"""Answer questions about my background using natural language.."""

# %% IMPORTS

import os
import logging
import typing as T

import gradio as gr

import vertexai
from vertexai.generative_models import GenerativeModel


# %% CONFIGS

# %% - Models

MODEL_NAME = os.environ["MODEL_NAME"]
MODEL_SYSTEM= """
You are Fmind AI Assistant, designed to provide concise and professional information about Médéric Hurier (also known as Fmind). Your primary focus is to answer questions regarding his background, experience, and expertise.

Please use the information below (in Markdown format) as your knowledge base. If a question falls outside of this scope or is unrelated to Médéric Hurier, politely decline to answer and suggest that the user rephrase or provide a different question.
"""
MODEL_CONTEXT = open("files/linkedin.md").read()
MODEL_CONFIG = {
    "max_output_tokens": 1000,
    "temperature": 1,
    "top_p": 0.95,
}

# %% - Logging

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")

# %% - Projects

PROJECT_ID = os.environ["PROJECT_ID"]
PROJECT_LOCATION = os.environ["PROJECT_LOCATION"]

# %% - Interfaces

INTERFACE_THEME = "soft"
INTERFACE_TITLE = "Fmind AI Assistant"
INTERFACE_EXAMPLES = [
    "Who is Médéric Hurier (Fmind)?",
    "Is Fmind open to new opportunities?",
    "Can you share details about Médéric PhD?",
    "Elaborate on Médéric's current work position",
    "Describe his proficiency with Python programming",
    "What is the answer to life, the universe, and everything?",
]
INTERFACE_DESCRIPTION = (
    "<center>"
    "Visit my website: <a href='https://fmind.dev'>https://fmind.dev</a>"
    " - Médéric HURIER (Fmind)"
    " - Freelancer: AI/FM/MLOps Engineer | Data Scientist | MLOps Community Organizer | MLflow Ambassador | Hacker | PhD"
    "</center>"
)
INTERFACE_CACHE_EXAMPLES = "lazy"
INTERFACE_CONCURRENCY_LIMIT = None

# %% CLIENTS

# %% - Logging

logging.basicConfig(
    level=getattr(logging, LOGGING_LEVEL),
    format="[%(asctime)s][%(levelname)s] %(message)s",
)

# %% - Vertex AI

vertexai.init(project=PROJECT_ID, location=PROJECT_LOCATION)

model = GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=MODEL_CONFIG,
    system_instruction=[MODEL_SYSTEM, MODEL_CONTEXT],
)

# %% FUNCTIONS


def answer(message: str, history: list[tuple[str, str]]) -> T.Iterable[str]:
    """Answer questions about my background using natural language.."""
    # messages
    messages = []
    for user, assistant in history:
        messages.append({"role": "user", "parts": [{"text": user}]})
        messages.append({"role": "model", "parts": [{"text": assistant}]})
    messages.append({"role": "user", "parts": [{"text": message}]})
    # response
    response = model.generate_content(message, stream=True)
    # content
    content = ""
    for chunk in response:
        content += chunk.text
        yield content
    # usage
    usage = str(chunk.usage_metadata).replace("\n", "; ")
    logging.info("Usage: %s", usage)


# %% INTERFACES

demo = gr.ChatInterface(
    fn=answer,
    theme=INTERFACE_THEME,
    title=INTERFACE_TITLE,
    examples=INTERFACE_EXAMPLES,
    description=INTERFACE_DESCRIPTION,
    cache_examples=INTERFACE_CACHE_EXAMPLES,
    concurrency_limit=INTERFACE_CONCURRENCY_LIMIT,
    clear_btn=None,
    retry_btn=None,
    undo_btn=None,
)


if __name__ == "__main__":
    demo.launch()

# %%
