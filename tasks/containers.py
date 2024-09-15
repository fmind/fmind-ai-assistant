"""Docker tasks for pyinvoke."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% CONFIGS

DOCKER_TAG = "fmind-ai-assistant:latest"

# %% TASKS


@task
def build(ctx: Context) -> None:
    """Build the docker image."""
    ctx.run(f"docker build -t {DOCKER_TAG} .")


@task
def run(ctx: Context) -> None:
    """Run the docker image."""
    ctx.run(f"docker run --rm --env-file .env -p 8080:8080 {DOCKER_TAG}")


@task(pre=[build, run], default=True)
def all(_: Context) -> None:
    """Run all container tasks."""
