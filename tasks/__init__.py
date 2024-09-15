"""Task collections."""
# mypy: ignore-errors

# %% IMPORTS

from invoke import Collection

from . import checks, cleans, containers, formats, installs, runs

# %% NAMESPACES

ns = Collection()

# %% COLLECTIONS


ns.add_collection(checks)
ns.add_collection(cleans)
ns.add_collection(containers)
ns.add_collection(formats)
ns.add_collection(installs)
ns.add_collection(runs, default=True)
