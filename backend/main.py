from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

class UserResponse(BaseModel):
    text: str

@app.post("/purpose/")
async def create_item(user_response: UserResponse):
    return {"message": "Purpose Processed"}

#Gaze Evaluation
import Gaze.Gaze as Gaze
GazeEval=Gaze.GazeEvaluator()
@app.get("/gaze")
async def root():
    return {"currently_running":GazeEval._running,"FPS": GazeEval._FPS,"horizontal range":GazeEval._hor_Range,"vertical range":GazeEval._ver_Range}

@app.get("/gaze/start")
async def root():
    GazeEval.reset()
    GazeEval.run()
    return {"message": f"Gaze Evaluation started"}

@app.get("/gaze/stop")
async def root():
    GazeEval.stop()
    return {"message":"Finished correctly."}

@app.get("/gaze/reset")
async def root():
    GazeEval.reset()
    return {"message": f"Attention got reset successfully"}

@app.get("/gaze/getAttention")
async def root():
    temp=GazeEval.getAttention()
    return {"message": f"Attention rating is {temp}","attention": temp}
