# run format tasks
[group('format')]
format: format-import format-source

# format code import
[group('format')]
format-import:
    uv run ruff check --select=I --fix {{SOURCES}}

# format code source
[group('format')]
format-source:
    uv run ruff format {{SOURCES}}
