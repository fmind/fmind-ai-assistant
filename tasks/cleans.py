"""Clean tasks for the project."""

# %% IMPORTS

from invoke import task
from invoke.context import Context

# %% TASKS


@task
def install(ctx: Context) -> None:
    """Clean the install."""
    ctx.run("rm -rf .venv/")


@task
def mypy(ctx: Context) -> None:
    """Clean the mypy cache."""
    ctx.run("rm -rf .mypy_cache/")


@task
def ruff(ctx: Context) -> None:
    """Clean the ruff cache."""
    ctx.run("rm -rf .ruff_cache/")


@task
def gradio(ctx: Context) -> None:
    """Clean the gradio cache."""
    ctx.run("rm -rf gradio_cached_examples/")


@task
def python(ctx: Context) -> None:
    """Clean python files and folders."""
    ctx.run("find . -type f -name '*.py[co]' -delete")
    ctx.run("find . -type d -name __pycache__ -delete")


@task(pre=[mypy, ruff, gradio, python], default=True)
def all(_: Context) -> None:
    """Run all clean tasks."""


@task(pre=[all, install])
def reset(_: Context) -> None:
    """Reset the project state."""
