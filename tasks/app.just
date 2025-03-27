# run app tasks
[group('app')]
app: app-run

# run the application
[group('app')]
app-run:
    UV_ENV_FILE=.env uv run gradio app.py
