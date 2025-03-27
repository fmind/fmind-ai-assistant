# run clean tasks
[group('clean')]
clean: clean-gradio clean-mypy clean-python clean-ruff

# clean gradio folders
[group('clean')]
clean-gradio:
    rm -rf gradio_cached_examples/

# clean mypy folders
[group('clean')]
clean-mypy:
    rm -rf .mypy_cache/

# clean python caches
[group('clean')]
clean-python:
    find . -type f -name '*.py[co]' -delete
    find . -type d -name __pycache__ -exec rm -r {} \+

# clean requirements file
[group('clean')]
clean-requirements:
    rm -f requirements.txt

# clean ruff cache
[group('clean')]
clean-ruff:
    rm -rf .ruff_cache/

# clean venv folder
[confirm]
[group('clean')]
clean-venv:
    rm -rf .venv/
