"""Task collections."""
# mypy: ignore-errors

# %% IMPORTS

from invoke import Collection

from . import check, clean, docker, format, install, run

# %% NAMESPACES

ns = Collection()

# %% COLLECTIONS


ns.add_collection(check)
ns.add_collection(clean)
ns.add_collection(docker)
ns.add_collection(format)
ns.add_collection(install)
ns.add_collection(run, default=True)
