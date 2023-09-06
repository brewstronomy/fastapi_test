# Local Notes for Running a Local FAST API Instance

1. Build app locally
   1. assuming directory is at `~/Desktop/<app>/`
   2. assuming app is built in `main.py`
2. start the local web server with `Uvicorn`
   1. run `uvicorn main:app --reload`
      1. `main` is the name of the script
      2. `app` is the name of the app
      3. `--reload` restarts the server after code updates
3. Navigate to the app URL
   1. `Uvicorn` typically spits out an endpoint like `INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`