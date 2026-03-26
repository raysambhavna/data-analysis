# Deploy This Project (Streamlit App)

## Fastest Option: Streamlit Community Cloud

1. Create a new GitHub repository from this folder.
2. Push this project to GitHub.
3. Open Streamlit Community Cloud.
4. Click **New app**.
5. Select your GitHub repo and set:
   - Main file path: `app.py`
6. Click **Deploy**.

## Option 2: Render (already configured)

This repo includes `render.yaml` for one-click deployment.

1. Push this project to GitHub.
2. In Render dashboard, click **New +** -> **Blueprint**.
3. Connect your GitHub repo.
4. Render detects `render.yaml` and deploys automatically.

## What is already prepared in this repo

- `requirements.txt` with required packages.
- `render.yaml` with correct Streamlit start command using `$PORT` and `0.0.0.0`.
- `.gitignore`.
- Git repo initialized with first commit.

## Local test command

```powershell
streamlit run app.py
```
