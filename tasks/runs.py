"""Run tasks of the project."""

# %% IMPORTS

from invoke import task
from invoke.context import Context

# %% TASKS


@task
def app(ctx: Context) -> None:
    """Run the main application."""
    ctx.run("UV_ENV_FILE=.env uv run gradio app.py")


@task(pre=[app], default=True)
def all(_: Context) -> None:
    """Run all run tasks."""
