"""Answer questions about my background in natural language.."""

# %% IMPORTS

import logging
import os

import gradio as gr
import vertexai
import vertexai.generative_models as genai

# %% CONFIGS

# %% - Models

MODEL_NAME = os.environ["MODEL_NAME"]
MODEL_SYSTEM = """
You are Fmind AI Assistant, designed to provide concise and professional information about Médéric Hurier (also known as Fmind). Your primary focus is to answer questions regarding his background, experience, and expertise.

Please use the information below (in Markdown format) as your knowledge base. If a question falls outside of this scope or is unrelated to Médéric Hurier, politely decline to answer and suggest that the user rephrase or provide a different question.
"""
MODEL_CONTEXT = open("files/linkedin.md").read()
MODEL_CONFIG = {
    "max_output_tokens": 1000,
    "temperature": 0.0,
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

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=MODEL_CONFIG,
    system_instruction=[MODEL_SYSTEM, MODEL_CONTEXT],
    safety_settings={
        genai.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        genai.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        genai.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        genai.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
)

# %% FUNCTIONS


def answer(message: str, history: list[tuple[str, str]]) -> str:
    """Answer questions about my background using natural language."""
    # contents
    contents = []
    for user_text, model_text in history:
        contents.append(genai.Content(role="user", parts=[genai.Part.from_text(user_text)]))
        contents.append(genai.Content(role="model", parts=[genai.Part.from_text(model_text)]))
    contents.append(genai.Content(role="user", parts=[genai.Part.from_text(message)]))
    # response
    response = model.generate_content(contents=contents)
    if response.prompt_feedback:
        logging.warning("Prompt feedback: %s", response.prompt_feedback)
    if response.usage_metadata:
        logging.info(
            "Usage metadata: total tokens=%s, inputs tokens=%s, output tokens=%s",
            response.usage_metadata.total_token_count,
            response.usage_metadata.prompt_token_count,
            response.usage_metadata.candidates_token_count,
        )
    return response.text


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
