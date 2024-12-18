"""Docker tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% CONFIGS

DOCKER_TAG = "fmind-ai-assistant:latest"

# %% TASKS


@task
def requirements(ctx: Context) -> None:
    """Export the project requirements file."""
    ctx.run(
        "uv export --format=requirements-txt --no-dev "
        "--no-hashes --no-editable --no-emit-project "
        f"--output-file=requirements.txt"
    )


@task(pre=[requirements])
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
