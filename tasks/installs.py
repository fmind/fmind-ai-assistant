"""Install tasks of the project."""

# %% IMPORTS

from invoke import task
from invoke.context import Context

# %% TASKS


@task
def uv(ctx: Context) -> None:
    """Install uv packages."""
    ctx.run("uv sync --all-groups")


@task(pre=[uv], default=True)
def all(_: Context) -> None:
    """Run all install tasks."""
