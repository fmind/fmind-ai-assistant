"""Check tasks of the project."""

# %% IMPORTS

from invoke import task
from invoke.context import Context

# %% TASKS


@task
def type(ctx: Context) -> None:
    """Check the types with mypy."""
    ctx.run("uv run mypy *.py")


@task
def code(ctx: Context) -> None:
    """Check the codes with ruff check."""
    ctx.run("uv run ruff check *.py")


@task
def format(ctx: Context) -> None:
    """Check the formats with ruff format."""
    ctx.run("uv run ruff format --check *.py")


@task(pre=[type, code, format], default=True)
def all(_: Context) -> None:
    """Run all check tasks."""
