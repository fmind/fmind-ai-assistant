# run install tasks
[group('install')]
install: install-project

# install the project
[group('install')]
install-project:
    uv sync --all-groups
