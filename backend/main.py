from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from elo_system import EloSystem
from data_fetcher import DataFetcher

app = FastAPI(title="Tennis Forecast AI")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

elo_manager = EloSystem(k_factor=28)
API_KEY = "ab7ee06161msh16b021a83ae7a8dp1c03dcjsn51074bf9408e"
fetcher = DataFetcher(API_KEY)

# Stats Cache
cached_matches = []

# Initial Ratings
elo_manager.ratings["Jannik Sinner"] = 2176
elo_manager.ratings["Novak Djokovic"] = 2096
elo_manager.ratings["Carlos Alcaraz"] = 2003

class MatchPrediction(BaseModel):
    player1: str
    player2: str
    prob1: float
    prob2: float
    elo1: float
    elo2: float
    recommended_winner: str
    surface: str
    tournament: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "Tennis Forecast AI"}

@app.get("/matches", response_model=List[MatchPrediction])
def get_matches():
    global cached_matches
    # Siempre intentamos sincronizar si no hay datos
    if not cached_matches:
        raw_matches = fetcher.get_upcoming_matches()
        predictions = []
        for m in raw_matches:
            r1 = elo_manager.get_rating(m["player1"], m["surface"])
            r2 = elo_manager.get_rating(m["player2"], m["surface"])
            prob1 = elo_manager.calculate_expected_score(r1, r2)
            prob2 = 1 - prob1
            
            predictions.append({
                "player1": m["player1"],
                "player2": m["player2"],
                "prob1": round(prob1 * 100, 2),
                "prob2": round(prob2 * 100, 2),
                "elo1": round(r1, 0),
                "elo2": round(r2, 0),
                "recommended_winner": m["player1"] if prob1 > prob2 else m["player2"],
                "surface": m["surface"],
                "tournament": m["tournament"]
            })
        cached_matches = predictions
    return cached_matches

@app.get("/rankings")
def get_rankings():
    sorted_rankings = sorted(elo_manager.ratings.items(), key=lambda x: x[1], reverse=True)
    return [{"name": name, "elo": round(elo, 0)} for name, elo in sorted_rankings]

@app.get("/sync")
def force_sync():
    global cached_matches
    cached_matches = []
    return get_matches()
