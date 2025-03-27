# run check tasks
[group('check')]
check: check-code check-type check-format

# check code quality
[group('check')]
check-code:
    uv run ruff check {{SOURCES}}

# check code format
[group('check')]
check-format:
    uv run ruff format --check {{SOURCES}}

# check code typing
[group('check')]
check-type:
    uv run mypy {{SOURCES}}
