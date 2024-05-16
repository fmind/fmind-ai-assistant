"""Install tasks for the project."""

# %% IMPORTS

from invoke import task
from invoke.context import Context

# %% TASKS


@task
def venv(ctx: Context) -> None:
    """Create a virtual environment."""
    ctx.run("python3 -m venv .venv/")
    ctx.run(".venv/bin/pip install uv")


@task
def lock(ctx: Context) -> None:
    """Lock the main project dependencies."""
    ctx.run("uv pip compile requirements.txt -o requirements.lock")
    ctx.run("uv pip compile requirements-dev.txt -o requirements-dev.lock")


@task
def main(ctx: Context) -> None:
    """Install the main dependencies."""
    ctx.run("uv pip install -r requirements.lock")


@task
def dev(ctx: Context) -> None:
    """Install the development dependencies."""
    ctx.run("uv pip install -r requirements-dev.lock")


@task(pre=[venv, lock, main, dev], default=True)
def all(_: Context) -> None:
    """Run all install tasks."""
