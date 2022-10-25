from NLU.nlu_module import NLU
import Gaze.Gaze as Gaze
from typing import Union
from Memory_system.knowledge_graph_for_real import KnowledgeGraphArt
from Memory_system.knowledge_graph_stupid import KnowledgeGraphDumb
import rdflib

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

PURPOSE = "phone wallpaper"


@app.get("/")
async def root():
    return {"message": "Hello World"}


class UserResponse(BaseModel):
    text: str


# @app.post("/purpose/")
# async def create_item(user_response: UserResponse):
#     return {"message": "Purpose Processed"}

# Gaze Evaluation
GazeEval = Gaze.GazeEvaluator()


@app.get("/gaze")
async def gazeInfo():
    return {"currently_running": GazeEval._running, "FPS": GazeEval._FPS, "horizontal range": GazeEval._hor_Range, "vertical range": GazeEval._ver_Range}


@app.get("/gaze/start")
async def gazeStart():
    GazeEval.reset()
    GazeEval.run()
    return {"message": f"Gaze Evaluation started"}


@app.get("/gaze/stop")
async def gazeStop():
    GazeEval.stop()
    return {"message": "Finished correctly."}


@app.get("/gaze/reset")
async def gazeReset():
    GazeEval.reset()
    return {"message": f"Attention got reset successfully"}


@app.get("/gaze/getAttention")
async def gazeAttention():
    temp = GazeEval.getAttention()
    return {"message": f"Attention rating is {temp}", "attention": temp}


# NLU
nlu = NLU()
nlu.load_painting_features_from_file(
    "Memory_system/listing_of_elements/human_to_machine.txt")


# @app.post("/nlu/name")
# async def extractName(user_response: UserResponse):
#     name = nlu.extract_person_name(user_response.text)
#     if name is None:
#         return {"name_found": False, "name": ""}

#     return {"name_found": True, "name": name}


@app.post("/nlu/purpose")
async def extractName(user_response: UserResponse):
    purposes = nlu.extract_purpose_using_candidates(user_response.text)
    PURPOSE = purposes[0]
    return {"purpose_list": purposes}

@app.post("/nlu/feature")
async def extractName(user_response: UserResponse):
    features = nlu.extract_feature_using_candidates(user_response.text)
    print(features)
    return {"feature1": f"{features[0]}", "feature2":f"{features[1]}", "feature3":features[2]}


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
    return {"keyword": keywords[0]}

g = None
try:
    # There's an error with the format of the original file. Doing a generic AF exception is the only fix I
    # can think of quickly. It's horrible, ugly and not good at all. But it works!
    g = rdflib.Graph()
    g.parse('Memory_system/artgraph-rdf/artgraph-facts.ttl')
except Exception:
    print('This is an expected print, which is ugly but woo')

graph_art = KnowledgeGraphArt(g=g)
# graph_art = KnowledgeGraphDumb(g=g)

@app.get("/mem/set_smart")
async def set_smart():
    """Method assumes that the given text is the string version of the URI Machine name"""
    graph_art = KnowledgeGraphArt(g=g)
    return {"message": "Graph is smart"}

@app.get("/mem/set_dumb")
async def set_dumb():
    """Method assumes that the given text is the string version of the URI Machine name"""
    graph_art = KnowledgeGraphDumb(g=g)
    return {"message": "Graph is dumb"}


class KnowledgeGraphResponse(BaseModel):
    text: str
    sentiment: float


@app.post("/mem/topic")
async def giveWeightToTopic(response: UserResponse):
    """Method assumes that the given text is the string version of the URI Machine name"""
    graph_art.modify_weight_of_vertex(response.text)
    return {"message": "Topic weights modified"}


@app.post("/mem/painting_score")
async def givePaintingScore(response: KnowledgeGraphResponse):
    graph_art.update_neighboring_to_painting(response.text, response.sentiment)
    return {"message": 'Painting scores modified', 'text received': response.text}


@app.get("/mem/painting_recommend")
async def recommendPainting():
    machine_painting_name = graph_art.find_n_highest_ranked_unexplored_paintings()[0]
    filename_painting = graph_art.find_string_name_with_machine_name(machine_painting_name, False)
    piece_name, artist, medium, period = graph_art.find_artist_medium_period_for_painting(machine_painting_name)
    return {"filename": filename_painting, 'piece_name': piece_name, 'artist': artist,
            'medium': medium, 'period': period, 'machine_name': machine_painting_name}


@app.post("/mem/update_purpose")
async def addTopicToGraph(response: UserResponse):
    graph_art.add_topic_to_graph(response.text)
    return {"message": 'Topic was added'}


@app.get("/mem/wipe")
async def wipeMemory():
    graph_art.reset_memory()
    return {"message": 'Memory was removed'}
