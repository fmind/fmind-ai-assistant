"""Answer questions about my background in natural language.."""

# %% IMPORTS

import functools
import io
import logging
import os
import typing as T

import gradio as gr
from google import genai
from google.genai import types

# %% CONFIGS

# %% - Models

MODEL_NAME = os.environ["MODEL_NAME"]
MODEL_CONTEXT = open("files/linkedin.md").read()
MODEL_SYSTEM_INSTRUCTIONS = """
You are Fmind AI Assistant, designed to provide concise and professional information about Médéric Hurier (also known as Fmind). Your primary focus is to answer questions regarding his background, experience, and expertise.

Please use the information below (in Markdown format) as your knowledge base. If a question falls outside of this scope or is unrelated to Médéric Hurier, politely decline to answer and suggest that the user rephrase or provide a different question.
"""

# %% - Logging

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")

# %% - Interfaces

INTERFACE_THEME = "soft"
INTERFACE_TITLE = "Fmind AI Assistant"
INTERFACE_FAVICON = "assets/favicon.ico"
INTERFACE_EXAMPLES = [
    "Who is Médéric Hurier (Fmind)?",
    "Summarize the education of Médéric",
    "What are the main skills of Médéric?",
    "What do other people say about Médéric?",
    "What is Médéric's current work position?",
    "Is Médéric open to new work opportunities?",
    "Can you share details about Médéric's thesis?",
    "Describe his proficiency with Python programming",
]
INTERFACE_DESCRIPTION = (
    "<center>"
    "Visit my <a href='https://fmind.dev'>Website</a>, "
    "<a href='https://www.linkedin.com/in/fmind-dev/'>LinkedIn</a>, "
    "<a href='https://github.com/fmind/'>GitHub</a>, "
    "<a href='https://medium.com/@fmind'>Medium</a>, "
    "<a href='https://twitter.com/fmind_dev'>Twitter</a> "
    "to connect and learn more."
    "</center>"
)

# %% CLIENTS

# %% - Logging

logging.basicConfig(
    level=getattr(logging, LOGGING_LEVEL), format="[%(asctime)s][%(levelname)s] %(message)s"
)

# %% - Generative AI

model_client = genai.Client()
model_config = types.GenerateContentConfig(
    temperature=0,
    max_output_tokens=1000,
    system_instruction=[MODEL_SYSTEM_INSTRUCTIONS, MODEL_CONTEXT],
    safety_settings=[
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_LOW_AND_ABOVE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"
        ),
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"),
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
    ],
)
stream = functools.partial(
    model_client.models.generate_content_stream, model=MODEL_NAME, config=model_config
)

# %% FUNCTIONS


def chat(message: str, history: list[dict[str, str]]) -> T.Iterator[str]:
    """Answer the user message with generate AI and contents."""
    contents = []
    for previous in history:
        text = previous["content"]
        role = "user" if previous["role"] == "user" else "model"
        content = types.Content(role=role, parts=[types.Part.from_text(text)])
        contents.append(content)
    contents.append(types.Content(role="user", parts=[types.Part.from_text(message)]))
    response = stream(contents=contents)
    answer = io.StringIO()
    for i, chunk in enumerate(response):
        if usage := chunk.usage_metadata:
            logging.info(
                "[%s] Usage metadata: total tokens=%s (inputs tokens=%s, output tokens=%s)",
                i,
                usage.total_token_count,
                usage.prompt_token_count,
                usage.candidates_token_count,
            )
        if feedback := chunk.prompt_feedback:
            logging.warning("[%s] Prompt feedback: %s", i, feedback)
        answer.write(chunk.text)
        yield answer.getvalue()


# %% INTERFACES

demo = gr.ChatInterface(
    fn=chat,
    type="messages",
    theme=INTERFACE_THEME,
    title=INTERFACE_TITLE,
    examples=INTERFACE_EXAMPLES,
    description=INTERFACE_DESCRIPTION,
    show_progress="hidden",
    concurrency_limit=None,
)
demo.launch(show_api=False, favicon_path=INTERFACE_FAVICON)
