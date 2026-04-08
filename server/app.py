import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Import your local logic
try:
    from .smarthome_support_v1_environment import SmartHomeSupportEnv
    from ..models import SmartHomeAction, SmartHomeObservation
except (ImportError, ValueError):
    from server.smarthome_support_v1_environment import SmartHomeSupportEnv
    from models import SmartHomeAction, SmartHomeObservation

app = FastAPI(title="SmartHome Support OpenEnv", version="0.1.0")

# Global environment instance for the session
env_instance = SmartHomeSupportEnv()

@app.get("/")
async def root():
    """Redirect root to API docs."""
    return RedirectResponse(url="/docs")

@app.post("/reset")
async def reset(task_id: Optional[str] = "password-reset"):
    global env_instance
    env_instance = SmartHomeSupportEnv(task_id=task_id)
    return env_instance.reset()

@app.post("/step")
async def step(action: SmartHomeAction):
    obs, reward, done, info = env_instance.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
async def state():
    return env_instance.state()

def main():
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    main()
