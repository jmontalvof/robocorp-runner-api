import os
import subprocess
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

API_KEY = os.getenv("RUNNER_API_KEY", "runner123")
ACTIONS_DIR = Path(os.getenv("ACTIONS_DIR", "/var/actions")).resolve()
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "300"))

app = FastAPI(title="Robocorp Runner API", version="1.0.0")


class RunRequest(BaseModel):
    file: str = Field(..., examples=["validar_qa.py"])
    params: dict = Field(default_factory=dict)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "actions_dir": str(ACTIONS_DIR)
    }


@app.post("/run")
def run_action(req: RunRequest, authorization: str | None = Header(default=None)):
    expected = f"Bearer {API_KEY}"

    if authorization != expected:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if req.file.startswith("/") or ".." in Path(req.file).parts:
        raise HTTPException(status_code=400, detail="Invalid script path")

    script_path = ACTIONS_DIR / req.file

    if not script_path.exists():
        raise HTTPException(status_code=404, detail=f"Script not found: {req.file}")

    if script_path.suffix != ".py":
        raise HTTPException(status_code=400, detail="Only .py files are allowed")

    env = os.environ.copy()

    for key, value in req.params.items():
        env[f"PARAM_{key.upper()}"] = str(value)

    try:
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            env=env
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "script": str(script_path)
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Execution timeout")