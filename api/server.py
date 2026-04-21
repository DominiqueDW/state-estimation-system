from fastapi import FastAPI
from api.state_store import state_store

import threading
from main import main

app = FastAPI()

@app.on_event("startup")
def start_system():
    thread = threading.Thread(target=main, daemon=True)
    thread.start()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/occupancy")
def get_occupancy():
    return state_store.occupancy


@app.get("/entities")
def get_entities():
    return state_store.entities
