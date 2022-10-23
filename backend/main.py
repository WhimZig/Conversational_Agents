from NLU.nlu_module import NLU
import Gaze.Gaze as Gaze
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

# Gaze Evaluation
GazeEval = Gaze.GazeEvaluator()


@app.get("/gaze")
async def root():
    return {"currently_running": GazeEval._running, "FPS": GazeEval._FPS, "horizontal range": GazeEval._hor_Range, "vertical range": GazeEval._ver_Range}


@app.get("/gaze/start")
async def root():
    GazeEval.reset()
    GazeEval.run()
    return {"message": f"Gaze Evaluation started"}


@app.get("/gaze/stop")
async def root():
    GazeEval.stop()
    return {"message": "Finished correctly."}


@app.get("/gaze/reset")
async def root():
    GazeEval.reset()
    return {"message": f"Attention got reset successfully"}


@app.get("/gaze/getAttention")
async def root():
    temp = GazeEval.getAttention()
    return {"message": f"Attention rating is {temp}", "attention": temp}


# NLU
nlu = NLU()
nlu.load_painting_features_from_file(
    "Memory_system/listing_of_elements/human_to_machine.txt")


@app.post("/nlu/name")
async def extractName(user_response: UserResponse):
    name = nlu.extract_person_name(user_response.text)
    if name is None:
        return {"name_found": False, "name": ""}

    return {"name_found": True, "name": name}


@app.post("/nlu/purpose")
async def extractName(user_response: UserResponse):
    purposes = nlu.extract_purpose_using_candidates(user_response.text)
    return {"purpose_list": purposes}


@app.post("/nlu/feature")
async def extractName(user_response: UserResponse):
    features = nlu.extract_feature_using_candidates(user_response.text)
    return {"feature_list": features}


@app.post("/nlu/feature")
async def extractName(user_response: UserResponse):
    features = nlu.extract_feature_using_candidates(user_response.text)
    return {"feature_list": features}


@app.post("/nlu/sentiment")
async def extractName(user_response: UserResponse):
    sentiment = nlu.analyze_sentiment(user_response.text)
    return {"sentiment": sentiment}


@app.post("/nlu/yesno")
async def extractName(user_response: UserResponse):
    response = nlu.understand_yes_no(user_response.text)
    return {"response": response}


@app.post("/nlu/keywords")
async def extractName(user_response: UserResponse):
    keywords = nlu.extract_keywords(user_response.text)
    return {"keywords": keywords}
