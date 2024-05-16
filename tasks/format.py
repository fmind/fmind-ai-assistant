"""Format tasks for the project."""

# %% IMPORTS

from invoke import task
from invoke.context import Context

# %% TASKS


@task
def imports(ctx: Context) -> None:
    """Format code imports with ruff."""
    ctx.run("ruff check --select I --fix *.py")


@task
def sources(ctx: Context) -> None:
    """Format code sources with ruff."""
    ctx.run("ruff format *.py")


@task(pre=[imports, sources], default=True)
def all(_: Context) -> None:
    """Run all format tasks."""
